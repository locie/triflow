import itertools as it

import numpy as np
import pylab as pl

from triflow import Model, schemes

model = Model("k * dxxU - c * dxU",
              "U", ["k", "c"])

x, dx = np.linspace(0, 1, 200, retstep=True)
U = np.cos(2 * np.pi * x * 5)
fields = model.fields_template(x=x, U=U)

parameters = dict(c=.03, k=.001, dx=dx, periodic=True)

t = 0
dt = 1E-2
tmax = 5

pl.plot(fields.x, fields.U, label='t: %g' % t)

scheme = schemes.Theta(model, theta=.5)  # Crank-Nicolson scheme

for i in it.count():
    t, fields = scheme(t, fields, dt, parameters)
    if (i + 1) % 100 == 0:
        pl.plot(fields.x, fields.U, label='t: %g' % t)
    if t >= tmax:
        break

pl.xlim(0, 1)
legend = pl.legend(loc='best')

pl.show()
