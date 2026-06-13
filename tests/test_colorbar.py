import numpy as np
import pytest
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm

from legendkit import colorbar

matplotlib.use("Agg")

np.random.seed(42)


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def make_mappable(cmap="RdBu", norm=None):
    fig, ax = plt.subplots()
    data = np.random.rand(5, 5)
    m = ax.pcolormesh(data, cmap=cmap, norm=norm)
    return ax, m


# ------------------------------------------------------------------
# Basic construction
# ------------------------------------------------------------------


def test_colorbar_basic():
    ax, m = make_mappable()
    cb = colorbar(m, ax=ax)
    assert repr(cb) == "<Colorbar>"


def test_colorbar_no_args_uses_current_axes():
    _, m = make_mappable()
    cb = colorbar(m)
    assert cb is not None


def test_colorbar_title():
    ax, m = make_mappable()
    cb = colorbar(m, ax=ax, title="My Title")
    assert cb is not None


# ------------------------------------------------------------------
# Style
# ------------------------------------------------------------------


def test_colorbar_style_white():
    ax, m = make_mappable()
    cb = colorbar(m, ax=ax, style="white")
    assert cb is not None


def test_colorbar_style_normal():
    ax, m = make_mappable()
    cb = colorbar(m, ax=ax, style="normal")
    assert cb is not None


# ------------------------------------------------------------------
# Shape
# ------------------------------------------------------------------


@pytest.mark.parametrize("shape", ["rect", "ellipse", "triangle", "trapezoid"])
def test_colorbar_shapes(shape):
    ax, m = make_mappable()
    cb = colorbar(m, ax=ax, shape=shape)
    assert cb is not None


# ------------------------------------------------------------------
# Orientation
# ------------------------------------------------------------------


def test_colorbar_vertical():
    ax, m = make_mappable()
    cb = colorbar(m, ax=ax, orientation="vertical")
    assert cb is not None


def test_colorbar_horizontal():
    ax, m = make_mappable()
    cb = colorbar(m, ax=ax, orientation="horizontal", loc="out upper center")
    assert cb is not None


# ------------------------------------------------------------------
# Location
# ------------------------------------------------------------------


@pytest.mark.parametrize(
    "loc",
    [
        "out right upper",
        "out right center",
        "out right lower",
        "out upper left",
        "out upper center",
        "out upper right",
        "out lower left",
        "out lower center",
        "out lower right",
        "out left upper",
        "out left center",
        "out left lower",
    ],
)
def test_colorbar_loc(loc):
    ax, m = make_mappable()
    cb = colorbar(m, ax=ax, loc=loc)
    assert cb is not None


# ------------------------------------------------------------------
# Width / height
# ------------------------------------------------------------------


def test_colorbar_custom_size():
    ax, m = make_mappable()
    cb = colorbar(m, ax=ax, width=0.2, height=2.0)
    assert cb is not None


def test_colorbar_only_width():
    ax, m = make_mappable()
    cb = colorbar(m, ax=ax, width=0.2)
    assert cb is not None


def test_colorbar_only_height():
    ax, m = make_mappable()
    cb = colorbar(m, ax=ax, height=1.0)
    assert cb is not None


# ------------------------------------------------------------------
# BoundaryNorm
# ------------------------------------------------------------------


def test_colorbar_boundary_norm():
    bounds = [0, 0.2, 0.5, 0.8, 1.0]
    norm = BoundaryNorm(bounds, ncolors=4)
    ax, m = make_mappable(norm=norm)
    cb = colorbar(m, ax=ax)
    assert cb is not None


# ------------------------------------------------------------------
# title_fontproperties
# ------------------------------------------------------------------


def test_colorbar_title_fontproperties():
    ax, m = make_mappable()
    cb = colorbar(
        m, ax=ax, title="T", title_fontproperties={"weight": "normal", "size": "small"}
    )
    assert cb is not None
