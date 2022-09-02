"""
Quick Start
==========================
"""

import numpy as np
import matplotlib.pyplot as plt
from legendkit import legend

plt.style.use('pacoty.mplstyle')

# %%
# This is how you usually create legend in matplotlib

x = np.arange(0, 10, 0.1)
_, ax = plt.subplots()
ax.plot(x, np.sin(x), label="sin")
ax.plot(x, np.cos(x), label="cos")
ax.legend(title="Trigonometry", loc="upper right")

# %%
# You can use legendkit just like before
# But you are allow to configure it more
_, ax = plt.subplots()
ax.plot(x, np.sin(x), label="sin")
ax.plot(x, np.cos(x), label="cos")
legend(title="Trigonometry", loc="upper right",
       alignment="left")
