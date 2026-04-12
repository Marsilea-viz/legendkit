<p align="center">
<img src="https://raw.githubusercontent.com/Mr-Milk/legendkit/main/images/legendkit-project.svg">
</p>

[![Documentation Status](https://img.shields.io/readthedocs/legendkit?logo=readthedocs&logoColor=white&style=flat-square)](https://legendkit.readthedocs.io/en/stable)
![pypi version](https://img.shields.io/pypi/v/legendkit?color=blue&logo=python&logoColor=white&style=flat-square)

When you want to create or adjust the legend in matplotlib, things can get dirty. 
Legendkit may solve your headache.

<img src="https://legendkit.readthedocs.io/en/latest/_images/cover.png">

## Features

- Easy title placement and alignment
- Easy colorbar with shape
- Layout for multiple legends and colorbar*

## Installation

```shell
pip install legendkit
```

## Quickstart

```python
import numpy as np
import matplotlib.pyplot as plt
from legendkit import cat_legend, colorbar, vstack

fig, ax = plt.subplots()
data = np.random.rand(10, 10)
mappable = ax.pcolormesh(data, cmap="RdBu")

# Categorical legend
leg = cat_legend(ax, colors=["#e63946", "#457b9d", "#2a9d8f"],
                 labels=["Group A", "Group B", "Group C"], title="Groups")

# Colorbar placed outside axes
colorbar(mappable, ax=ax, title="Value")
plt.show()
```
