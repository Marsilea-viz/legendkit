from abc import ABC

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
