#!/usr/bin/env python
# coding=utf8

import itertools as it
import logging
from logging import debug, error, info
from uuid import uuid1

import numpy as np

from triflow import displays, schemes


class Simulation(object):
    """ """

    def __init__(self, solver, U0, t0, **pars):
        self.id = str(uuid1())
        self.solver = solver
        self.pars = pars
        self.nvar = self.solver.nvar
        self.U = U0
        self.t = t0
        self.i = 0
        self.x, self.pars['dx'] = np.linspace(0, pars['L'], pars['Nx'],
                                              retstep=True)
        self.iterator = self.compute()
        self.internal_iter = None
        self.err = None
        self.drivers = []
        self.writers = []
        self.display = displays.simple_display
        self.scheme = schemes.ROS_vart_scheme
        self.signals = {}
        self.conf = {}

    def compute(self):
        """ """

        nvar = self.nvar
        self.pars['Nx'] = int(self.U.size / nvar)
        self.U = self.hook(self.U)

        display = self._init_display_()
        writers = self._init_writers_()
        numerical_scheme = self._init_scheme_()

        for self.i, self.U in enumerate(filter(
                self.filter,
                it.takewhile(self.takewhile,
                             numerical_scheme))):
            self.t += self.pars['dt']
            self.driver(self.t)
            self.write(writers)
            yield display.send(self)

    def add_signal(self, field, signal):
        self.signals[field] = signal

    def add_writer(self, writer):
        try:
            assert not(writer.writer_type in [writer.writer_type
                                              for writer
                                              in self.writers]), \
                'Already %s writer attached' % writer.writer_type
        except AttributeError:
            logging.warning('writer_type not found')
        self.writers.append(writer)

    def _init_writers_(self):
        return [writer(self) for writer in self.writers]

    def set_display(self, display):
        self.display = display

    def _init_display_(self):
        return self.display(self)

    def set_scheme(self, scheme):
        if scheme == 'theta':
            if self.pars['theta'] != 0:
                self.scheme = schemes.BE_scheme
                return
            self.scheme = schemes.FE_scheme
            return
        if scheme == 'BDF':
            self.scheme = schemes.BDF2_scheme
            return
        if scheme == 'BDF-alpha':
            self.scheme = schemes.BDFalpha_scheme
            return
        if scheme == 'SDIRK':
            self.scheme = schemes.SDIRK_scheme
            return
        if scheme == 'ROS':
            self.scheme = schemes.ROS_scheme
            return
        if scheme == 'ROS_vart':
            self.scheme = schemes.ROS_vart_scheme
            return
        if callable(scheme):
            self.scheme = scheme
            return
        raise NotImplementedError('method not implemented')

    def _init_scheme_(self):
        return self.scheme(self)

    def write(self, writers):
        for writer in writers:
            writer.send(self)

    def driver(self, t):
        """
        Modify the parameters at each internal time steps. The driver have
        to be appened to the attribute drivers.
        Parameters
        ----------
        t : actual time


        Returns
        -------
        None

        """

        for driver in self.drivers:
            driver(self, t)

        for field, signal in self.signals.items():
            self.pars['%sini' % field] = signal(t)

    def takewhile(self, U):
        """

        Parameters
        ----------
        U :


        Returns
        -------
        Stopping condition for the simulation: without overide
        this will raise an error if the film thickness go less than 0 and
        exit when tmax is reached if in the parameters.
        """

        if any(U[::self.nvar] < 0):
            error('h above 0, solver stopping')
            raise RuntimeError('h above 0')
        if self.pars.get('tmax', None) is None:
            return True
        if self.t >= self.pars.get('tmax', None):
            return False
        return True

    def filter(self, U):
        """

        Parameters
        ----------
        U :


        Returns
        -------
        Tell when return the solution to the user.
        Default return all solutions reaching dt.
        """

        return True

    def hook(self, U):
        """

        Parameters
        ----------
        U :


        Returns
        -------

        """

        return U

    def __iter__(self):
        return self.iterator

    def __next__(self):
        return next(self.iterator)