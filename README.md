<p align="center">
<img src="https://raw.githubusercontent.com/Mr-Milk/legendkit/main/images/legendkit-project.svg">
</p>

![pypi version](https://img.shields.io/pypi/v/legendkit?color=blue&logo=python&logoColor=white&style=flat-square)

When you want to create or adjust the legend in matplotlib, things can get dirty. 
LegendKit may solve your headache.

<img src="https://raw.githubusercontent.com/Mr-Milk/legendkit/main/images/showcase.svg">

## Features

- Easy title placement and alignment
- Layout for multiple legends
- Easy colorbar

## Installation

```shell
pip install legendkit
```

## Usage

Any parameters you can use in legend or colorbar in matplotlib can 
also be used here.

### Use it as the same old day

First create a plot

Usually, this is how you create the legend, the long title looks bad when it place at the center.
But you can do nothing about it.

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 10, 0.1)
plt.plot(x, np.sin(x), color="r", label="sin")
plt.plot(x, np.sin(x), color="r", label="cos")
plt.legend(title="Trigonometry Functions")
```

With legendkit, things are easy, replace the default legend creation
```python
from legendkit import legend
# plt.legend(title="Trigonometry Functions")
legend(title="Trigonometry Functions", title_align="left")
```

<img src="https://raw.githubusercontent.com/Mr-Milk/legendkit/main/images/example1.svg">

You can even create legend like this
```python
legend(title="Trigonometry Functions", title_pos="left", ncol=2)
```

<img src="https://raw.githubusercontent.com/Mr-Milk/legendkit/main/images/example1-2.svg" width="300">


### Create Colorbar

```python
from legendkit import Colorbar, EllipseColorbar

Colorbar(vmin=0, vmax=10, title="Colorbar", title_align="left")
EllipseColorbar(vmin=0, vmax=10, title="Ellipse Colorbar", title_align="left")
```

### Using preset legend

```python
import matplotlib.pyplot as plt
from legendkit import CatLegend, SizeLegend

_, ax = plt.subplots()
CatLegend(["r", "g", "b"], ["Item 1", "Item 2", "Item 3"])
SizeLegend([i for i in range(101)])
```

### Create a custom legend

If you want to create a custom legend, it's pretty easy to do it. Simple use an array to define it.

```python
from legendkit import legend

legend(legend_items=[
    # (handle, label, config)
    ('square', 'Item 1', {'color': '#01949A'}),
    ('circle', 'Item 2', {'facecolor': '#004369', 
                          'edgecolor': '#DB1F48', 
                          'linewidth': 0.5}),
    ('rect', 'Item 3', {'color': '#E5DDC8'}),
    # Or you can have no config at all
    ('line', 'Item 4'),
])

```

<img src="https://raw.githubusercontent.com/Mr-Milk/legendkit/main/images/example2.svg">

Or you can use matplotlib legend handlers for richer definition.

LegendKit provides you with some predefined handlers to use out of the box.

```python
from legendkit import legend
from legendkit.handles import SquareItem, CircleItem, RectItem, LineItem
from matplotlib.lines import Line2D

legend(
    handles=[SquareItem(), CircleItem(), RectItem(), LineItem(), Line2D([], [])], 
    labels=['Square', 'Circle', 'Rect', 'Line', 'Matplotlib Line'
])

```

<img src="https://raw.githubusercontent.com/Mr-Milk/legendkit/main/images/example2-2.svg">

If you want to use highly customized element as entry, 
please refer to [here](https://matplotlib.org/stable/tutorials/intermediate/legend_guide.html#implementing-a-custom-legend-handler)


### Composing multiple legends

Sometimes you may want to group few legends together

- `vstack` is used to stack legends vertically
- `hstack` is used to stack legends horizontally

```python
import matplotlib.pyplot as plt
from legendkit import legend
from legendkit.layout import vstack, hstack

_, ax = plt.subplots()

legend1 = legend(legend_items=[
    ('circle', 'The Moon', {'color': '#41729F'}),
], title="Earth's Moon")

legend2 = legend(legend_items=[
    ('circle', 'Deimos', {'color': '#3D550C'}),
    ('circle', 'Phobos', {'color': '#81B622'}),
], title="Mars' Moons")

legend3 = legend(legend_items=[
    ('circle', 'Io', {'color': '#FB4570'}),
    ('circle', 'Europa', {'color': '#FB6B90'}),
    ('circle', 'Ganymede', {'color': '#FB8DA0'}),
    ('circle', 'Callisto', {'color': '#EFEBE0'}),
], title="Moons of Jupyter")

legends = hstack([legend1, legend2, legend3], title="Moons in solar systems", spacing=10, frameon=True)
ax.add_artist(legends)  # Make sure you add it to the axes, or it won't be rendered

```
<img src="https://raw.githubusercontent.com/Mr-Milk/legendkit/main/images/example3.svg">


## Understand layout in matplotlib legend

If you are familiar with css flexbox model, this is similar to how legend is layout internally in 
matplotlib. 

A matplotlib legend have at least two parts, the handle and the label.

- handle: The graphic to represent the item in the plot.
- label: The text for the item.

### Parameters to control the layout

The units used in the layout system is the same as font size.

<img src="https://raw.githubusercontent.com/Mr-Milk/legendkit/main/images/handle_label_illustration.png" width="400">


#### Control the handle

- **handleheight**: The height of the handle.
- **handlelength**: The length of the handle.

#### Control the handle and the label:

- **handletextpad**: the distance between the handle and the label.

<img src="https://raw.githubusercontent.com/Mr-Milk/legendkit/main/images/layout_padding_illustration.png" width="1400">

#### Control between different items:

- **labelspacing**: This control the distance between different legend items, 
   it also controls the distance between title and items.
- **columnspacing**: The distance between multiple columns of items.

#### Control the legend outer frame:

- **frameon**: Toggle the on/off of the outer frame.
- **borderpad**: The distance between the actual legend and the outer frame, apply for both x and y direction.
- **borderaxespad**: The distance between the axes and the legend.