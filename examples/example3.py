import matplotlib.pyplot as plt

from legendkit import legend
from legendkit.layout import vstack, hstack

plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pacoty.mplstyle')

_, ax = plt.subplots(figsize=(4, 3))

legend1 = legend(legend_items=[
    ('circle', 'The Moon', {'color': '#41729F'}),
], title="Earth's Moon", handletextpad=0, title_align="left")

legend2 = legend(legend_items=[
    ('circle', 'Deimos', {'color': '#3D550C'}),
    ('circle', 'Phobos', {'color': '#81B622'}),
], title="Mars' Moons", handletextpad=0, title_align="left")

legend3 = legend(legend_items=[
    ('circle', 'Io', {'color': '#FB4570'}),
    ('circle', 'Europa', {'color': '#FB6B90'}),
    ('circle', 'Ganymede', {'color': '#FB8DA0'}),
    ('circle', 'Callisto', {'color': '#EFEBE0'}),
], title="Moons of Jupyter", handletextpad=0, title_align="left")

legends = hstack([legend1, legend2, legend3], title="Moons in solar systems", loc="center", spacing=10, frameon=True)
ax.add_artist(legends)
ax.set_axis_off()

plt.savefig("images/example3.svg", bbox_inches="tight")
