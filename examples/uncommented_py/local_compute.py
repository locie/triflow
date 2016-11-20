#!/usr/bin/env python
# coding=utf8

import logging
import itertools as it

import pylab as pl
import seaborn as sns
import numpy as np
from scipy.signal import hamming

from triflow.solver import Solver
from triflow.helpers import init_4f_per
from triflow import displays, writers, materials, signals, schemes


logger = logging.getLogger()
logger.handlers = []
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

parameters = {}

physical_parameters = materials.water()
physical_parameters['Beta'] = np.pi / 2
physical_parameters['Re'] = 15
physical_parameters['Bi'] = 2.81E-03
parameters.update(physical_parameters)

initial_parameters = {
    'hini': 1.,
    'qini': 1 / 3,
    'sini': 0,
    'thetaini': physical_parameters['theta_flat'],
    'phiini': physical_parameters['phi_flat']
}
parameters.update(initial_parameters)

numerical_parameters = {'t': 0, 'dt': 1, 'tmax': 20,
                        'tol': 1E-1}
parameters.update(numerical_parameters)

domain_parameters = {'L': 200, 'Nx': 600}
parameters.update(domain_parameters)

solver, initial_fields = init_4f_per(parameters)

simul = solver.start_simulation(initial_fields, 0, **parameters)

running_simul = simul.copy()
running_simul.add_writer(writers.datreant_step_writer)
running_simul.compute_until_finished()