from ._colorbar import Colorbar, EllipseColorbar
from ._list_legend import ListLegend
from ._preset import CatLegend, SizeLegend
# To register default setting and legend handlers
from ._register import register
from .api import legend
from .handles import SquareItem, RectItem, CircleItem
from .layout import stack, vstack, hstack

register()
