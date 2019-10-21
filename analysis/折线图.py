import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2, 100)

plt.plot(x, x, label="x")
plt.plot(x, x**2, label="x2")
plt.plot(x, x**3, label="x3")

plt.xlabel("x轴")
plt.ylabel("y轴")

plt.legend()
plt.show()
