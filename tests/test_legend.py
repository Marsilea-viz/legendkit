import itertools

import pytest
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from legendkit import legend, cat_legend, size_legend

np.random.seed(0)


def test_normal_legend():
    x = np.arange(0, 10, 0.1)
    _, ax = plt.subplots()
    ax.plot(x, 2 * x + 1, label="Line1")
    ax.plot(x, 5 * x + 1, label="Line2")
    legend(ax)


items = ["rect", "square", "circle", "boxplot", "triangle", "octagon", "line",
         "octagon", "pentagon", "star", "hexagon", "plus", "cross", "asterisk",
         "triangle-up", "triangle-down", "triangle-left", "triangle-right"] \
    + [Line2D([0], [0], marker="*")]


@pytest.mark.parametrize("legend_handle", items)
def test_legend_items(legend_handle):
    legend(legend_items=[(legend_handle, legend_handle)])
    legend(legend_items=[(legend_handle, legend_handle, {'color': 'r'})])


title_loc = ["top", "bottom", "left", "right"]
alignment = ["left", "right", "top", "bottom", "center"]


@pytest.mark.parametrize("title_loc,alignment",
                         itertools.product(title_loc, alignment))
def test_legend_title(title_loc, alignment):
    leg = legend(alignment=alignment, title_loc=title_loc)
    assert leg.get_alignment() == alignment


locations = [
    "out upper left", "out upper center", "out upper right",
    "out lower left", "out lower center", "out lower right",
    "out left upper", "out left center", "out left lower",
    "out right upper", "out right center", "out right lower",
]


@pytest.mark.parametrize("loc", locations)
def test_legend_loc(loc):
    legend(loc=loc)


fill_options = [True, False]


@pytest.mark.parametrize("handle,fill",
                         itertools.product(items, fill_options))
def test_cat_legend(handle, fill):
    cat_legend(colors=["r", "g", "b"],
               labels=["item1", "item2", "item3"],
               handle=handle,
               fill=fill)


def test_size_legend():
    sizes = np.arange(0, 100, 1)
    labels = np.array([0, 1, 2, 3])
    size_legend(sizes=sizes, labels=labels)
