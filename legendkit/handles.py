from abc import ABC

from matplotlib.lines import Line2D
from matplotlib.patches import Patch


class SquareItem(Patch, ABC):
    """Create square for legend handles"""
    pass


class RectItem(Patch, ABC):
    """Create rectangle for legend handles"""
    pass


class CircleItem(Patch, ABC):
    """Create circle for legend handles"""
    pass


class LineItem(Line2D, ABC):
    """Create line for legend handles"""

    def __init__(self, *args, **kwargs):
        super().__init__([], [], *args, **kwargs)
