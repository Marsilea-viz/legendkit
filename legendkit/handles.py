from abc import ABC

from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.collections import Collection


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


class BoxplotItem(Collection, ABC):

    def __init__(self, *args, **kwargs):
        user_ec = kwargs.get('ec')
        user_edgecolor = kwargs.get('edgecolor')
        if (user_ec is None) & (user_edgecolor is None):
            kwargs['ec'] = "black"
        super().__init__(*args, **kwargs)
