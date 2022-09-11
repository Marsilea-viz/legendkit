from ._colorbar import Colorbar
from ._colorart import ColorArt
from ._legend import ListLegend, CatLegend, SizeLegend


def legend(*args, **kwargs):
    return ListLegend(*args, **kwargs)


def cat_legend(*args, **kwargs):
    return CatLegend(*args, **kwargs)


def size_legend(*args, **kwargs):
    return SizeLegend(*args, **kwargs)


def colorbar(*args, **kwargs):
    return Colorbar(*args, **kwargs)


def colorart(*args, **kwargs):
    return ColorArt(*args, **kwargs)


legend.__doc__ = ListLegend.__doc__
cat_legend.__doc__ = CatLegend.__doc__
size_legend.__doc__ = SizeLegend.__doc__
colorbar.__doc__ = Colorbar.__doc__
colorart.__doc__ = ColorArt.__doc__
