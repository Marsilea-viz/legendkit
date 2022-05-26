import numpy as np
import matplotlib.pyplot as plt
from legendkit import legend

plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pacoty.mplstyle')

x = np.arange(0, 10, 0.1)
_, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3), constrained_layout=True)
ax1.plot(x, np.sin(x), label="sin")
ax1.plot(x, np.cos(x), label="cos")
ax1.legend(title="Trigonometry Functions", bbox_to_anchor=(1.01, 1), bbox_transform=ax1.transAxes, loc="upper left")
ax1.set_title('Old way')


ax2.plot(x, np.sin(x), label="sin")
ax2.plot(x, np.cos(x), label="cos")
legend(title="Trigonometry Functions", title_align="left",
       bbox_to_anchor=(1.01, 1), bbox_transform=ax2.transAxes, loc="upper left")
ax2.set_title('With LegendKit')

plt.savefig("images/example1.svg", bbox_inches="tight")
plt.close()


_, ax = plt.subplots(figsize=(5, 5))
ax.plot(x, np.sin(x), label="sin")
ax.plot(x, np.cos(x), label="cos")
legend(title="Trigonometry Functions", title_pos="left", ncol=2, titlepad=1, columnspacing=0.7,
       bbox_to_anchor=(0.5, 1.01), bbox_transform=ax.transAxes, loc="lower center")

plt.savefig("images/example1-2.svg", bbox_inches="tight")
