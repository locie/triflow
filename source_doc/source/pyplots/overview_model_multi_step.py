import itertools as it

import numpy as np
import matplotlib
matplotlib.use('Agg')  # noqa: needed before import pylab
import pylab as pl
from triflow import Model, schemes

pl.style.use('seaborn-whitegrid')

model = Model("k * dxxU - c * dxU",
              "U", ["k", "c"])

x, dx = np.linspace(0, 1, 200, retstep=True)
U = np.cos(2 * np.pi * x * 5)
fields = model.fields_template(x=x, U=U)

parameters = dict(c=.03, k=.001, dx=dx, periodic=True)

t = 0
dt = 1E-2
tmax = 5

pl.plot(fields.x, fields.U, label=f't: {t:g}')

scheme = schemes.Theta(model, theta=.5)  # Crank-Nicolson scheme

for i in it.count():
    t, fields = scheme(t, fields, dt, parameters)
    if (i + 1) % 100 == 0:
        pl.plot(fields.x, fields.U, label=f't: {t:g}')
    if t >= tmax:
        break

pl.xlim(0, 1)
legend = pl.legend(loc='best')

pl.show()
