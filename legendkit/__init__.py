"""Legend creation and manipulation with ease for matplotlib"""
from ._version import version

__version__ = version

from ._colorart import ColorArt
from ._colorbar import Colorbar
from ._legend import ListLegend, CatLegend, SizeLegend
# To register default setting and legend handlers
from ._register import register
from .layout import vstack, hstack, stack

register()

colorbar = Colorbar
colorart = ColorArt
legend = ListLegend
cat_legend = CatLegend
size_legend = SizeLegend


__all__ = [
    "colorbar",
    "colorart",
    "legend",
    "cat_legend",
    "size_legend",
    "vstack",
    "hstack",
    "stack",
]