import itertools

import matplotlib
import pytest
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from legendkit import legend, cat_legend, size_legend

matplotlib.use("Agg")
np.random.seed(0)


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def test_normal_legend():
    x = np.arange(0, 10, 0.1)
    _, ax = plt.subplots()
    ax.plot(x, 2 * x + 1, label="Line1")
    ax.plot(x, 5 * x + 1, label="Line2")
    leg = legend(ax)
    assert len(leg.get_texts()) == 2
    assert [t.get_text() for t in leg.get_texts()] == ["Line1", "Line2"]


def test_legend_figure_level():
    """legend() should also work when passed a Figure instead of Axes."""
    fig, axes = plt.subplots(1, 2)
    for ax, label in zip(axes, ["A", "B"]):
        ax.plot([0, 1], label=label)
    leg = legend(fig)
    assert leg is not None


items = [
    "rect",
    "square",
    "circle",
    "boxplot",
    "triangle",
    "octagon",
    "line",
    "octagon",
    "pentagon",
    "star",
    "hexagon",
    "plus",
    "cross",
    "asterisk",
    "triangle-up",
    "triangle-down",
    "triangle-left",
    "triangle-right",
] + [Line2D([0], [0], marker="*")]


@pytest.mark.parametrize("legend_handle", items)
def test_legend_items(legend_handle):
    legend(legend_items=[(legend_handle, legend_handle)])
    legend(legend_items=[(legend_handle, legend_handle, {"color": "r"})])


title_loc = ["top", "bottom", "left", "right"]
alignment = ["left", "right", "top", "bottom", "center"]


@pytest.mark.parametrize("title_loc,alignment", itertools.product(title_loc, alignment))
def test_legend_title(title_loc, alignment):
    leg = legend(alignment=alignment, title_loc=title_loc)
    assert leg.get_alignment() == alignment


locations = [
    "out upper left",
    "out upper center",
    "out upper right",
    "out lower left",
    "out lower center",
    "out lower right",
    "out left upper",
    "out left center",
    "out left lower",
    "out right upper",
    "out right center",
    "out right lower",
]


@pytest.mark.parametrize("loc", locations)
def test_legend_loc(loc):
    legend(loc=loc)


fill_options = [True, False]


@pytest.mark.parametrize("handle,fill", itertools.product(items, fill_options))
def test_cat_legend(handle, fill):
    cat_legend(
        colors=["r", "g", "b"],
        labels=["item1", "item2", "item3"],
        handle=handle,
        fill=fill,
    )


def test_size_legend():
    sizes = np.arange(0, 100, 1)
    labels = np.array([0, 1, 2, 3])
    size_legend(sizes=sizes, labels=labels)


def test_size_legend_show_at():
    sizes = np.arange(1, 101)
    leg = size_legend(sizes=sizes, show_at=[0.25, 0.5, 0.75, 1.0])
    assert len(leg.get_texts()) == 4


def test_size_legend_size_array_mismatch_raises():
    with pytest.raises(ValueError, match="does not match"):
        size_legend(sizes=np.array([1, 2, 3]), array=np.array([1, 2]))


def test_size_legend_show_at_out_of_range_raises():
    with pytest.raises(ValueError, match="show_at values must be between 0 and 1"):
        size_legend(sizes=np.arange(1, 101), show_at=[0.5, 1.5])


def test_cat_legend_label_count():
    leg = cat_legend(colors=["r", "g", "b"], labels=["x", "y", "z"])
    assert len(leg.get_texts()) == 3
    assert [t.get_text() for t in leg.get_texts()] == ["x", "y", "z"]


def test_cat_legend_mismatched_colors_labels_raises():
    with pytest.raises(ValueError, match="same length"):
        cat_legend(colors=["r", "g"], labels=["x", "y", "z"])


def test_legend_items_count():
    leg = legend(
        legend_items=[
            ("square", "A"),
            ("circle", "B"),
            ("line", "C"),
        ]
    )
    assert len(leg.get_texts()) == 3


def test_loc_invalid_raises():
    from legendkit._locs import Locs

    with pytest.raises(ValueError, match="Invalid loc"):
        Locs().transform(plt.gca(), loc="bad location")


def test_loc_inside_options():
    """Inside loc values should work without raising."""
    inside_locs = [
        "lower left",
        "lower center",
        "lower right",
        "upper left",
        "upper center",
        "upper right",
        "center left",
        "center",
        "center right",
    ]
    for loc in inside_locs:
        _, ax = plt.subplots()
        leg = legend(ax, loc=loc)
        assert leg is not None
        plt.close("all")
