import numpy as np
import pytest
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, LogNorm

from legendkit import colorart

matplotlib.use("Agg")

np.random.seed(42)


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def make_mappable(cmap="cool", norm=None, vmin=None, vmax=None):
    fig, ax = plt.subplots()
    data = np.random.rand(5, 5)
    m = ax.pcolormesh(data, cmap=cmap, norm=norm, vmin=vmin, vmax=vmax)
    return ax, m


# ------------------------------------------------------------------
# Basic construction
# ------------------------------------------------------------------


def test_colorart_basic():
    ax, m = make_mappable()
    ca = colorart(m, ax=ax)
    assert repr(ca) == "<ColorArt>"


def test_colorart_no_ax_uses_current():
    _, m = make_mappable()
    ca = colorart(m)
    assert ca is not None


def test_colorart_title():
    ax, m = make_mappable()
    ca = colorart(m, ax=ax, title="My ColorArt")
    assert ca is not None


# ------------------------------------------------------------------
# Orientation
# ------------------------------------------------------------------


def test_colorart_vertical():
    ax, m = make_mappable()
    ca = colorart(m, ax=ax, orientation="vertical")
    assert ca is not None


def test_colorart_horizontal():
    ax, m = make_mappable()
    ca = colorart(m, ax=ax, orientation="horizontal", loc="out upper center")
    assert ca is not None


# ------------------------------------------------------------------
# flip
# ------------------------------------------------------------------


def test_colorart_flip_true():
    ax, m = make_mappable()
    ca = colorart(m, ax=ax, flip=True)
    assert ca is not None


def test_colorart_flip_false():
    ax, m = make_mappable()
    ca = colorart(m, ax=ax, flip=False)
    assert ca is not None


# ------------------------------------------------------------------
# ticks / format
# ------------------------------------------------------------------


def test_colorart_custom_ticks():
    ax, m = make_mappable()
    ca = colorart(m, ax=ax, ticks=[0.2, 0.5, 0.8])
    assert ca is not None


def test_colorart_string_format():
    ax, m = make_mappable()
    ca = colorart(m, ax=ax, format="{x:.1f}")
    assert ca is not None


# ------------------------------------------------------------------
# BoundaryNorm
# ------------------------------------------------------------------


def test_colorart_boundary_norm():
    bounds = [0, 0.25, 0.5, 0.75, 1.0]
    norm = BoundaryNorm(bounds, ncolors=4)
    ax, m = make_mappable(norm=norm)
    ca = colorart(m, ax=ax)
    assert ca is not None


# ------------------------------------------------------------------
# LogNorm
# ------------------------------------------------------------------


def test_colorart_log_norm():
    norm = LogNorm(vmin=0.01, vmax=1.0)
    ax, m = make_mappable(norm=norm)
    ca = colorart(m, ax=ax)
    assert ca is not None


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
    ],
)
def test_colorart_loc(loc):
    ax, m = make_mappable()
    ca = colorart(m, ax=ax, loc=loc)
    assert ca is not None


# ------------------------------------------------------------------
# Size
# ------------------------------------------------------------------


def test_colorart_custom_size():
    ax, m = make_mappable()
    ca = colorart(m, ax=ax, width=3, height=10)
    assert ca is not None


# ------------------------------------------------------------------
# set_border raises NotImplementedError
# ------------------------------------------------------------------


def test_colorart_set_border_not_implemented():
    ax, m = make_mappable()
    ca = colorart(m, ax=ax)
    with pytest.raises(NotImplementedError):
        ca.set_border()


# ------------------------------------------------------------------
# ticklocation
# ------------------------------------------------------------------


@pytest.mark.parametrize("ticklocation", ["both", "left", "right"])
def test_colorart_ticklocation(ticklocation):
    ax, m = make_mappable()
    ca = colorart(m, ax=ax, ticklocation=ticklocation)
    assert ca is not None


# ------------------------------------------------------------------
# remove
# ------------------------------------------------------------------


def test_colorart_remove():
    ax, m = make_mappable()
    ca = colorart(m, ax=ax)
    ca.remove()  # should not raise
