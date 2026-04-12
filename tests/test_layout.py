import numpy as np
import pytest
import matplotlib
import matplotlib.pyplot as plt

from legendkit import cat_legend, colorart, vstack, hstack

matplotlib.use("Agg")

np.random.seed(42)


@pytest.fixture(autouse=True)
def close_figures():
    yield
    plt.close("all")


def make_ax():
    fig, ax = plt.subplots()
    ax.set_axis_off()
    return ax


def make_legends(n=3, ax=None):
    if ax is None:
        ax = make_ax()
    return [
        cat_legend(ax=ax,
                   colors=["#A7D2CB", "#F2D388"],
                   labels=["Item 1", "Item 2"],
                   title=f"Legend {i + 1}")
        for i in range(n)
    ]


# ------------------------------------------------------------------
# vstack
# ------------------------------------------------------------------

def test_vstack_basic():
    ax = make_ax()
    legs = make_legends(3, ax=ax)
    box = vstack(legs, ax=ax)
    assert box is not None


def test_vstack_with_title():
    ax = make_ax()
    legs = make_legends(3, ax=ax)
    box = vstack(legs, title="Vertical Stack", ax=ax)
    assert box is not None


@pytest.mark.parametrize("title_loc", ["top", "bottom", "left", "right"])
def test_vstack_title_locations(title_loc):
    ax = make_ax()
    legs = make_legends(2, ax=ax)
    box = vstack(legs, title="T", title_loc=title_loc, ax=ax)
    assert box is not None


def test_vstack_with_frameon():
    ax = make_ax()
    legs = make_legends(2, ax=ax)
    box = vstack(legs, frameon=True, ax=ax)
    assert box is not None


def test_vstack_returns_without_ax():
    ax = make_ax()
    legs = make_legends(2, ax=ax)
    box = vstack(legs)  # no ax — returns box, caller places it
    assert box is not None


# ------------------------------------------------------------------
# hstack
# ------------------------------------------------------------------

def test_hstack_basic():
    ax = make_ax()
    legs = make_legends(3, ax=ax)
    box = hstack(legs, ax=ax)
    assert box is not None


def test_hstack_with_title():
    ax = make_ax()
    legs = make_legends(3, ax=ax)
    box = hstack(legs, title="Horizontal Stack", ax=ax)
    assert box is not None


def test_hstack_with_spacing():
    ax = make_ax()
    legs = make_legends(2, ax=ax)
    box = hstack(legs, spacing=10, ax=ax)
    assert box is not None


# ------------------------------------------------------------------
# Location
# ------------------------------------------------------------------

@pytest.mark.parametrize("loc", [
    "upper left", "upper right", "lower left", "lower right", "center",
    "out right center", "out upper center",
])
def test_vstack_loc(loc):
    ax = make_ax()
    legs = make_legends(2, ax=ax)
    box = vstack(legs, loc=loc, ax=ax)
    assert box is not None


# ------------------------------------------------------------------
# Nested stacks
# ------------------------------------------------------------------

def test_nested_stack():
    ax = make_ax()
    legs = make_legends(6, ax=ax)
    vs = vstack(legs[:3], spacing=5)
    hs = hstack(legs[3:], spacing=5)
    box = hstack([vs, hs], spacing=10, loc="center", ax=ax)
    assert box is not None


# ------------------------------------------------------------------
# Mixed: legend + colorart
# ------------------------------------------------------------------

def test_vstack_legend_and_colorart():
    fig, ax = plt.subplots()
    data = np.random.rand(5, 5)
    m = ax.pcolormesh(data, cmap="cool")
    ca = colorart(m, ax=ax, title="Color")
    leg = cat_legend(ax=ax,
                     colors=["red", "blue"],
                     labels=["A", "B"],
                     title="Cat")
    box = vstack([leg, ca], spacing=10, loc="out right center", ax=ax)
    assert box is not None


# ------------------------------------------------------------------
# alignment
# ------------------------------------------------------------------

@pytest.mark.parametrize("alignment", ["left", "center", "right"])
def test_vstack_alignment(alignment):
    ax = make_ax()
    legs = make_legends(2, ax=ax)
    box = vstack(legs, title="T", alignment=alignment, ax=ax)
    assert box is not None


# ------------------------------------------------------------------
# TypeError on unsupported artist type
# ------------------------------------------------------------------

def test_stack_bad_type_raises():
    from legendkit.layout import stack
    with pytest.raises(TypeError):
        stack(["not_an_artist"], ax=make_ax())
