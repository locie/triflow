#!/usr/bin/env python
# coding=utf8

import logging
import sys
from functools import partial
from itertools import product
from pickle import dump, load
from pprint import pformat

import numpy as np
from sympy import (Derivative, Function, Symbol,
                   SympifyError, symbols, sympify, lambdify)
from theano import tensor as T
from theano.ifelse import ifelse
import theano.sparse as ths
from theano import function
from triflow.core.fields import BaseFields
from triflow.core.routines import F_Routine, J_Routine

logging.getLogger(__name__).addHandler(logging.NullHandler())
logging = logging.getLogger(__name__)

sys.setrecursionlimit(40000)


def _generate_sympify_namespace(independent_variables,
                                dependent_variables,
                                helper_functions):
    """Generate the link between the symbols of the derivatives and the
      sympy Derivative operation.

      Parameters
      ----------
      independent_variable : str
          name of the independant variable ("x")
      dependent_variables : iterable of str
          names of the dependent variables
      helper_functions : iterable of str
          names of the helper functions

      Returns
      -------
      dict
          dictionnary containing the symbol to parse as keys and the sympy expression to evaluate instead as values.
      """  # noqa

    independent_variable = independent_variables[0]  # TEMP FIX BEFORE REAL ND

    symbolic_independent_variable = Symbol(independent_variable)

    def partial_derivative(symbolic_independent_variable,
                           i, expr):
        return Derivative(expr, symbolic_independent_variable,
                          i)

    namespace = {independent_variable: symbolic_independent_variable}
    namespace.update({'d%s' % (independent_variable * i):
                      partial(partial_derivative,
                              symbolic_independent_variable, i)
                      for i in range(1, 10)})
    namespace.update({'d%s%s' % (independent_variable * order, var):
                      Derivative(Function(var)(independent_variable),
                                 independent_variable, order)
                      for order, var in product(range(1, 10),
                                                dependent_variables +
                                                helper_functions)})
    logging.debug(f"sympy namespace: {namespace}")
    return namespace


def _reduce_model(eq_diffs, dep_vars, pars,
                  help_functions, bdc_conditions, module):
    model = Model(eq_diffs, dep_vars, pars,
                  help_functions, bdc_conditions, module)

    return model


class Model:
    """Contain finite difference approximation and routine of the dynamical system

      Take a mathematical form as input, use Sympy to transform it as a symbolic
      expression, perform the finite difference approximation and expose theano
      optimized routine for both the right hand side of the dynamical system and
      Jacobian matrix approximation.

      Parameters
      ----------
      differential_equations : iterable of str or str
          the right hand sides of the partial differential equations written as :math:`\\frac{\partial U}{\partial t} = F(U)`, where the spatial derivative can be written as `dxxU` or `dx(U, 2)` or with the sympy notation `Derivative(U, x, x)`
      dependent_variables : iterable of str or str
          the dependent variables with the same order as the temporal derivative of the previous arg.
      parameters : iterable of str or str, optional, default None
          list of the parameters. Can be feed with a scalar of an array with the same size
      help_functions : None, optional
          All fields which have not to be solved with the time derivative but will be derived in space.
      double: bool, optional
          Choose if the dtypes are float64 (the default) or float32

      Attributes
      ----------
      F : triflow.F_Routine
          Callable used to compute the right hand side of the dynamical system
      F_array : numpy.ndarray of sympy.Expr
          Symbolic expressions of the right hand side of the dynamical system
      J : triflow.J_Routine
          Callable used to compute the Jacobian of the dynamical system
      J_array : numpy.ndarray of sympy.Expr
          Symbolic expressions of the Jacobian side of the dynamical system

      Properties
      ----------
      fields_template: Model specific Fields container used to store and access to the model variables in an efficient way.

      Methods
      -------
      save: Save a binary of the Model with pre-optimized F and J routines

      Examples
      --------
      A simple diffusion equation:

      >>> from triflow import Model
      >>> model = Model("k * dxxU", "U", "k")

      A coupled system of convection-diffusion equation:

      >>> from triflow import Model
      >>> model = Model(["k1 * dxxU - c1 * dxV",
      ...                "k2 * dxxV - c2 * dxU",],
      ...                ["U", "V"], ["k1", "k2", "c1", "c2"])
      """  # noqa

    def __init__(self,
                 differential_equations,
                 dependent_variables,
                 parameters=None,
                 help_functions=None,
                 bdc_conditions=None,
                 double=True):
        logging.debug('enter __init__ Model')
        self._double = double
        self._symb_t = Symbol("t")
        indep_vars = ["x"]

        # coerce the inputs the way to have coherent types
        def coerce(arg):
            if arg is None:
                return tuple()
            else:
                if isinstance(arg, (str, )):
                    return tuple([arg])
            return tuple(arg)

        (self._diff_eqs,
         self._indep_vars,
         self._dep_vars,
         self._pars,
         self._help_funcs,
         self._bdcs) = map(coerce, (differential_equations,
                                    indep_vars,
                                    dependent_variables,
                                    parameters,
                                    help_functions,
                                    bdc_conditions))

        self._nvar = len(self._dep_vars)
        # generate the sympy namespace which will connect the math input into
        # sympy operation.
        sympify_namespace = {}
        sympify_namespace.update(_generate_sympify_namespace(
            self._indep_vars,
            self._dep_vars,
            self._help_funcs))

        # parse the inputs in order to have Sympy symbols and expressions
        (self._symb_diff_eqs,
         self._symb_indep_vars,
         self._symb_dep_vars,
         self._symb_pars,
         self._symb_help_funcs,
         self._symb_bdcs) = self._sympify_model(self._diff_eqs,
                                                self._indep_vars,
                                                self._dep_vars,
                                                self._pars,
                                                self._help_funcs,
                                                self._bdcs,
                                                sympify_namespace)

        # we will need to extract the order of the != spatial derivative
        # in order to know the size of the ghost area at the limit of
        self._symb_vars_with_spatial_diff_order = {str(svar.func):
                                                   {(svar.func, 0)}
                                                   for svar
                                                   in (self._symb_dep_vars +
                                                       self._symb_help_funcs)}

        # Use finite difference scheme to generate a spatial approximation and
        # have a rhs which will only be a function of the discretized dependent
        # variables and help functions.
        approximated_diff_eqs = self._approximate_derivative(
            self._symb_diff_eqs,
            self._symb_indep_vars,
            self._symb_dep_vars,
            self._symb_help_funcs)
        self._dbdcs = self._approximate_derivative(
            self._symb_bdcs,
            self._symb_indep_vars,
            self._symb_dep_vars,
            self._symb_help_funcs)
        logging.debug(f"approximated equations: {approximated_diff_eqs}")

        # We compute the size of the the ghost area at the limit of
        # the spatial domain
        self._bounds = self._extract_bounds(
            self._dep_vars,
            self._symb_vars_with_spatial_diff_order)
        self._window_range = self._bounds[-1] - self._bounds[0] + 1

        # We obtain a Fortran like flattened vector containing all the discrete
        # dependent variable needed for the spatial approximation around the
        # local node i
        U = self._extract_unknowns(
            self._dep_vars,
            self._bounds,
            self._symb_vars_with_spatial_diff_order).flatten('F')

        # We do the same as for the U variable but with all the discrete
        # variables, dependent variables and help functions.
        self._discrete_variables = self._extract_unknowns(
            self._dep_vars + self._help_funcs,
            self._bounds,
            self._symb_vars_with_spatial_diff_order).flatten('F')

        # We expose a numpy.ndarray filled with the rhs of our approximated
        # dynamical system
        self.F_array = np.array(approximated_diff_eqs)

        # We compute the jacobian as the partial derivative of all equation of
        # our system according to all the discrete variable in U.
        self.J_array = np.array([
            [diff_eq.diff(u).expand()
             for u in U]
            for diff_eq in approximated_diff_eqs]).flatten('F')

        # We flag and store the null entry of the Jacobian matrix
        self._sparse_indices = np.where(self.J_array != 0)
        # We drop all the null term of the Jacobian matrix, because we target
        # a sparse matrix storage for memory saving and efficient linalg ops.
        self._J_sparse_array = self.J_array[self._sparse_indices]

        # We convert the sympy description of the system into a theano
        # graph compilation
        F, J, args, self._map_extended = self._theano_convert(
            self.F_array,
            self._J_sparse_array,
            self._dbdcs)
        self._th_args = args
        self._th_vectors = [F, J]
        # We compile the previous graphs and obtain optimized C based
        # routines
        logging.debug(args)
        logging.debug(list(map(type, args)))
        F_theano_function = function(inputs=args,
                                     outputs=F,
                                     on_unused_input='ignore',
                                     allow_input_downcast=True)
        J_theano_function = function(inputs=args,
                                     outputs=J,
                                     on_unused_input='ignore',
                                     allow_input_downcast=True)
        self._theano_routines = [F_theano_function, J_theano_function]
        self._compile(self.F_array, self._J_sparse_array,
                      F_theano_function, J_theano_function)

    def _theano_convert(self, F_array, J_array, bdc):

        mapargs = {arg: T.vector(arg)
                   for arg, sarg
                   in zip(self._args, self._symbolic_args)}

        to_feed = mapargs.copy()

        x_th = mapargs['x']
        N = x_th.size
        L = x_th[-1] - x_th[0]
        dx = L / (N - 1)
        to_feed['dx'] = dx

        periodic = T.scalar("periodic", dtype="int32")

        middle_point = int((self._window_range - 1) / 2)

        th_args = [mapargs[key]
                   for key
                   in [*self._indep_vars,
                       *self._dep_vars,
                       *self._help_funcs,
                       *self._pars]] + [periodic]

        map_extended = {}

        for (varname, discretisation_tree) in \
                self._symb_vars_with_spatial_diff_order.items():
            pad_left, pad_right = self._bounds

            per_extended_var = T.concatenate([mapargs[varname][pad_left:],
                                              mapargs[varname],
                                              mapargs[varname][:pad_right]],
                                             axis=0)

            edge_extended_var = T.concatenate([T.repeat(mapargs[varname][:1],
                                                        middle_point),
                                               mapargs[varname],
                                               T.repeat(mapargs[varname][-1:],
                                                        middle_point)],
                                              axis=0)

            extended_var = ifelse(periodic,
                                  per_extended_var,
                                  edge_extended_var)

            map_extended[varname] = extended_var
            for order in range(pad_left, pad_right + 1):
                if order != 0:
                    var = (f"{varname}_{'m' if order < 0 else 'p'}"
                           f"{np.abs(order)}")
                else:
                    var = varname
                new_var = extended_var[order - pad_left:
                                       extended_var.size +
                                       order - pad_right]
                to_feed[var] = new_var

        F = lambdify((self._symbolic_args),
                     expr=self.F_array.tolist(),
                     modules=T)(*[to_feed[key]
                                  for key
                                  in self._args])
        F = T.concatenate(F, axis=0).reshape((self._nvar, N)).T
        F = T.stack(F).flatten()

        J = lambdify((self._symbolic_args),
                     expr=self.J_array.tolist(),
                     modules=T)(*[to_feed[key]
                                  for key
                                  in self._args])

        J = [j if j != 0 else T.constant(0.) for j in J]
        J = T.stack([T.repeat(j, N) if j.ndim == 0 else j for j in J])
        J = J[self._sparse_indices[0]].T.squeeze()

        i = T.arange(N).dimshuffle([0, 'x'])
        idx = T.arange(N * self._nvar).reshape((N, self._nvar)).T
        edge_extended_idx = T.concatenate([T.repeat(idx[:, :1],
                                                    middle_point,
                                                    axis=1),
                                           idx,
                                           T.repeat(idx[:, -1:],
                                                    middle_point,
                                                    axis=1)],
                                          axis=1).T.flatten()
        per_extended_idx = T.concatenate([idx[:, -middle_point:],
                                          idx,
                                          idx[:, :middle_point]],
                                         axis=1).T.flatten()
        extended_idx = ifelse(periodic,
                              per_extended_idx,
                              edge_extended_idx)

        rows = T.tile(T.arange(self._nvar),
                      self._window_range * self._nvar) + i * self._nvar
        cols = T.repeat(T.arange(self._window_range * self._nvar),
                        self._nvar) + i * self._nvar
        rows = rows[:, self._sparse_indices].reshape(J.shape).flatten()
        cols = extended_idx[cols][:, self._sparse_indices] \
            .reshape(J.shape).flatten()

        permutation = T.argsort(cols)

        J = J.flatten()[permutation]
        rows = rows[permutation]
        cols = cols[permutation]
        count = T.zeros((N * self._nvar + 1,), dtype=int)
        uq, cnt = T.extra_ops.Unique(False, False, True)(cols)
        count = T.set_subtensor(count[uq + 1], cnt)

        indptr = T.cumsum(count)
        shape = T.stack([N * self._nvar, N * self._nvar])
        sparse_J = ths.CSC(J, rows, indptr, shape)

        return F, sparse_J, th_args, map_extended

    def _compile(self, F_array, J_array,
                 F_function, J_function):
        logging.debug('compile F')
        self.F = F_Routine(F_array,
                           (self._dep_vars +
                            self._help_funcs),
                           self._pars, F_function)
        logging.debug('compile J')
        self.J = J_Routine(J_array,
                           (self._dep_vars +
                            self._help_funcs),
                           self._pars, J_function)

    @property
    def fields_template(self):
        return BaseFields.factory(self._dep_vars,
                                  self._help_funcs)

    @property
    def _args(self):
        return list(map(str, self._symbolic_args))

    @property
    def _symbolic_args(self):
        return ([*list(self._symb_indep_vars),
                 *list(self._discrete_variables),
                 *list(self._symb_pars),
                 Symbol('dx')])

    def save(self, filename):
        """Save the model as a binary pickle file.

        Parameters
        ----------
        filename : str
            name of the file where the model is saved.

        Returns
        -------
        None
        """
        with open(filename, 'wb') as f:
            dump(self, f)

    @staticmethod
    def load(filename):
        """load a pre-compiled triflow model. The internal of theano allow a
        caching of the model. Will be slow if it is the first time the model is
        loaded on the system.

        Parameters
        ----------
        filename : str
            path of the pre-compiled model

        Returns
        -------
        triflow.core.Model
            triflow pre-compiled model
        """
        with open(filename, 'rb') as f:
            return load(f)

    def _extract_bounds(self, variables, dict_symbol):
        bounds = (0, 0)
        for var in variables:
            dvars, orders = zip(*dict_symbol[var])

            bounds = (min(bounds[0],
                          min(orders)),
                      max(bounds[1],
                          max(orders))
                      )
        return bounds

    def _extract_unknowns(self, vars, bounds, dict_symbol):
        unknowns = np.zeros((len(vars), bounds[-1] - bounds[0] + 1),
                            dtype=object)
        for i, var in enumerate(vars):
            dvars, orders = zip(*dict_symbol[var])
            for j, order in enumerate(range(bounds[0], bounds[1] + 1)):
                if order == 0:
                    unknowns[i, j] = Symbol(var)
                if order < 0:
                    unknowns[i, j] = Symbol(f'{var}_m{np.abs(order)}')
                if order > 0:
                    unknowns[i, j] = Symbol(f'{var}_p{np.abs(order)}')
        return unknowns

    def _finite_diff_scheme(self, U, order):
        logging.debug("finite diff approximation %i, %s" % (order, U))
        dx = Symbol('dx')
        var_label = str(U)
        if order == 1:
            Um1 = Symbol('%s_m1' % var_label)
            Up1 = Symbol('%s_p1' % var_label)
            self._symb_vars_with_spatial_diff_order[var_label].add((Um1, -1))
            self._symb_vars_with_spatial_diff_order[var_label].add((Up1, 1))
            return (1 / 2 * Up1 - 1 / 2 * Um1) / dx
        if order == 2:
            Um1 = Symbol('%s_m1' % var_label)
            Up1 = Symbol('%s_p1' % var_label)
            self._symb_vars_with_spatial_diff_order[var_label].add((Um1, -1))
            self._symb_vars_with_spatial_diff_order[var_label].add((Up1, 1))
            return (Up1 - 2 * U + Um1) / dx ** 2
        if order == 3:
            Um1 = Symbol('%s_m1' % var_label)
            Um2 = Symbol('%s_m2' % var_label)
            Up1 = Symbol('%s_p1' % var_label)
            Up2 = Symbol('%s_p2' % var_label)
            self._symb_vars_with_spatial_diff_order[var_label].add((Um1, -1))
            self._symb_vars_with_spatial_diff_order[var_label].add((Up1, 1))
            self._symb_vars_with_spatial_diff_order[var_label].add((Um2, -2))
            self._symb_vars_with_spatial_diff_order[var_label].add((Up2, 2))
            return (-1 / 2 * Um2 + Um1 - Up1 + 1 / 2 * Up2) / dx ** 3
        if order == 4:
            Um1 = Symbol('%s_m1' % var_label)
            Um2 = Symbol('%s_m2' % var_label)
            Up1 = Symbol('%s_p1' % var_label)
            Up2 = Symbol('%s_p2' % var_label)
            self._symb_vars_with_spatial_diff_order[var_label].add((Um1, -1))
            self._symb_vars_with_spatial_diff_order[var_label].add((Up1, 1))
            self._symb_vars_with_spatial_diff_order[var_label].add((Um2, -2))
            self._symb_vars_with_spatial_diff_order[var_label].add((Up2, 2))
            return (Um2 - 4 * Um1 + 6 * U - 4 * Up1 + Up2) / dx ** 4
        raise NotImplementedError('Finite difference up '
                                  'to 5th order not implemented yet')

    def _sympify_model(self,
                       diff_eqs,
                       indep_vars,
                       dep_vars,
                       pars,
                       help_functions,
                       bdc_conditions,
                       sympify_namespace):
        logging.debug('enter _sympify_model')
        logging.debug(pformat(diff_eqs))
        logging.debug(pformat(dep_vars))
        logging.debug(pformat(pars))
        logging.debug(pformat(help_functions))

        symbolic_indep_vars = tuple([(Symbol(indep_var))
                                     for indep_var in indep_vars])

        symbolic_dep_vars = tuple([Function(dep_var)(*symbolic_indep_vars)
                                   for dep_var in dep_vars])

        symbolic_help_functions = tuple([Function(help_function)
                                         (*symbolic_indep_vars)
                                         for help_function in help_functions])
        symbolic_pars = symbols(pars)

        def sympify_equations(equations):
            try:
                return tuple(
                    [sympify(func,
                             locals=sympify_namespace)
                     .subs(zip(map(Symbol,
                                   dep_vars),
                               (symbolic_dep_vars +
                                symbolic_help_functions)))
                     .doit()
                     for func
                     in equations])
            except (TypeError, SympifyError):
                raise ValueError("badly formated differential equations")

        symbolic_diff_eqs, symbolic_bdcs = map(sympify_equations,
                                               (diff_eqs,
                                                bdc_conditions))

        return (symbolic_diff_eqs, symbolic_indep_vars, symbolic_dep_vars,
                symbolic_pars, symbolic_help_functions, symbolic_bdcs)

    def _approximate_derivative(self,
                                symbolic_diff_eqs: tuple,
                                symbolic_indep_vars: tuple,
                                symbolic_dep_vars: tuple,
                                symbolic_fields: tuple) -> tuple:

        logging.debug('enter _approximate_derivative')
        approximated_diff_eqs = []
        for func in symbolic_diff_eqs:
            afunc = func
            for derivative in func.find(Derivative):
                var = Symbol(str(derivative.args[0].func))
                logging.debug(f"{derivative}, {var}")
                order = len(derivative.args) - 1
                afunc = afunc.replace(
                    derivative,
                    self._finite_diff_scheme(var,
                                             order))
            afunc = afunc.subs([(var, Symbol(str(var.func)))
                                for var in symbolic_dep_vars +
                                symbolic_fields])
            approximated_diff_eqs.append(afunc.expand())
        return tuple(approximated_diff_eqs)

    def __reduce__(self):
        return (_reduce_model, (self._diff_eqs, self._dep_vars,
                                self._pars, self._help_funcs,
                                self._bdcs, self._module))
