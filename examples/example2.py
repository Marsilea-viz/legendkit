import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from legendkit import legend
from legendkit.handles import LineItem, SquareItem, CircleItem, RectItem

plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pacoty.mplstyle')

_, ax = plt.subplots(figsize=(1, 1.5))
legend(legend_items=[
    # (handle, label, config)
    ('square', 'Item 1', {'color': '#01949A'}),
    ('circle', 'Item 2', {'facecolor': '#004369', 'edgecolor': '#DB1F48', 'linewidth': 0.5}),
    ('rect', 'Item 3', {'color': '#E5DDC8'}),
    # Or you can have no config at all
    ('line', 'Item 4'),
], loc="center")
ax.set_axis_off()

plt.savefig('images/example2.svg', bbox_inches="tight")
plt.close()

_, ax = plt.subplots(figsize=(1, 1.5))
legend(
    handles=[SquareItem(), CircleItem(), RectItem(), LineItem(), Line2D([], [])],
    labels=['Square', 'Circle', 'Rect', 'Line', 'Matplotlib Line']
)
ax.set_axis_off()

plt.savefig('images/example2-2.svg', bbox_inches="tight")
plt.close()