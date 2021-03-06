import numpy as np
import pylab as pl

from triflow import Model, schemes

model = Model("k * dxxU - c * dxU",
              "U", ["k", "c"])

x, dx = np.linspace(0, 1, 200, retstep=True)
U = np.cos(2 * np.pi * x * 5)
fields = model.fields_template(x=x, U=U)

pl.plot(fields.x, fields.U)

parameters = dict(c=.03, k=.001, dx=dx, periodic=True)

t = 0
dt = 1E-1

scheme = schemes.Theta(model, theta=.5)  # Crank-Nicolson scheme

new_t, new_fields = scheme(t, fields, dt, parameters)

pl.plot(new_fields.x, new_fields.U)
pl.xlim(0, 1)
pl.show()
