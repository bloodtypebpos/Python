import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter


dbdir = r'C:\Users\Sad_Matt\Desktop\Python\Ergotronix\reports'
fname = os.path.join(dbdir, 'output.gif')

fig = plt.figure()
l, = plt.plot([], [], 'k-')

plt.xlim(-5, 5)
plt.ylim(-5, 5)

def f(x):
    return np.sin(x)*3



metadata = dict(title='Movie', artist='Sad_matt')
writer = PillowWriter(fps=15, metadata=metadata)

X = []
Y = []


with writer.saving(fig, fname, 100):
    for x in np.linspace(-5, 5, 100):
        X.append(x)
        Y.append(f(x))
        l.set_data(X, Y)
        writer.grab_frame()
