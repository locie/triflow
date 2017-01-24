#!/usr/bin/env python3
# coding=utf8

import logging
from logging import info
import sympy as sp

import numpy as np


def model():
    """ """
    Re, We, Ct = sp.symbols('Re, We, Ct')
    Pe, Bi, M = sp.symbols('Pe, Bi, M')

    info('mise en place des variables')

    dx = sp.symbols('dx')

    fields = h, q, theta, phi, s = sp.symbols('h_i, q_i, theta_i, phi_i, s_i')
    hm1, hm2, hm3 = sp.symbols('h_im1:4')
    hp1, hp2, hp3 = sp.symbols('h_ip1:4')
    qm1, qm2, qm3 = sp.symbols('q_im1:4')
    qp1, qp2, qp3 = sp.symbols('q_ip1:4')
    thetam1, thetam2, thetam3 = sp.symbols('theta_im1:4')
    thetap1, thetap2, thetap3 = sp.symbols('theta_ip1:4')
    phim1, phim2, phim3 = sp.symbols('phi_im1:4')
    phip1, phip2, phip3 = sp.symbols('phi_ip1:4')
    sm1, sm2, sm3 = sp.symbols('s_im1:4')
    sp1, sp2, sp3 = sp.symbols('s_ip1:4')

    info('Calcul des dérivés en x')
    dxh = (-.5 * hm1 + .5 * hp1) / dx
    dxs = (-.5 * sm1 + .5 * sp1) / dx
    dxtheta = (-.5 * thetam1 + .5 * thetap1) / dx
    dxphi = (-.5 * phim1 + .5 * phip1) / dx
    dxq = (-.5 * qm1 + .5 * qp1) / dx

    dxxh = (1 * hm1 - 2 * h + 1 * hp1) / dx**2
    dxxq = (1 * qm1 - 2 * q + 1 * qp1) / dx**2
    dxxs = (1 * sm1 - 2 * s + 1 * sp1) / dx**2
    dxxphi = (1 * phim1 - 2 * phi + 1 * phip1) / dx**2
    dxxtheta = (1 * thetam1 - 2 * theta + 1 * thetap1) / dx**2

    dxxxh = (-.5 * hm2 + hm1 - hp1 + .5 * hp2) / dx**3
    dxxxs = (-.5 * sm2 + sm1 - sp1 + .5 * sp2) / dx**3

    info('Calcul du membre de droite')
    Fs = 0
    Fh = -dxq
    Fq = ((378 * dxxq * h**2 - 105 * dxtheta * h**2 * M +
           336 * dxh**2 * q - 210 * (q + 2 * dxs**2 * q) -
           9 * h * q * (56 * dxxh + 35 * dxxs + 68 * dxq * Re) -
           2 * dxh * (189 * dxq * h + 35 * Ct * h**3 +
                      3 * q * (35 * dxs - 54 * q * Re)) +
           70 * h**3 * (1 - Ct * dxs +
                        (dxxxh + dxxxs) * We)) / (252. * h**2 * Re))

    Ftheta = (180 / (17 * h**2) -
              96 * Bi * h / (17 * h**2) * theta +
              7 / (17 * h**2) * phi +
              dxxtheta) / (3 * Pe) - 3 / (2 * h) * dxtheta

    Fphi = ((-460 / (17 * h**2) -
             120 * Bi * h / (17 * h**2) * theta +
             3 / (17 * h**2) * phi +
             dxxphi) / (3 * Pe) - phi * dxq / h ** 2) * h

    F_therm = sp.Matrix([Fh, Fq, Ftheta, Fphi, Fs])

    U_therm = np.array([hm2, qm2, thetam2, phim2, sm2,
                        hm1, qm1, thetam1, phim1, sm1,
                        h, q, theta, phi, s,
                        hp1, qp1, thetap1, phip1, sp1,
                        hp2, qp2, thetap2, phip2, sp2]).reshape((5, 5))

    info('Calcul du jacobien')

    J_therm = sp.Matrix(np.array([F_therm.diff(u).tolist()
                                  for u
                                  in U_therm.flatten()]).squeeze().tolist()).T
    return U_therm, F_therm, J_therm, (Re, We, Ct, Pe, B, M), {}


if __name__ == '__main__':
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    model()