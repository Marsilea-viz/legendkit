<p align="center">
<img src="imgs/legendkit-project.svg">
</p>

When you want to create or adjust the legend in matplotlib, things can get dirty. 
LegendKit may solve your headache.

## Features

- Easy title placement and alignment
- Layout for multiple legends
- Easy colorbar

## Installation

```shell
pip install legendkit
```

## Usage

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

You can even create legends like this
```python
legend(title="Trigonometry Functions", title_pos="left", ncols=2)
```


### Create a custom legend

```python
from legendkit import ListLegend

ListLegend(legend_items=[
    ('square', 'Item 1'),
    ('circle', 'Item 2'),
    ('rect', 'Item 3'),
    ('line', 'Item 4'),
    ('tri', 'Item 5'),
])

```

To create multiple legends with layout

```python

from legendkit.layout import VStack, HStack, Grid

VStack(ax,
       [legend1, legend2],
       spacing=2,
       align="right"
       )

```
