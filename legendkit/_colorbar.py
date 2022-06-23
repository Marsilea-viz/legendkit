from typing import Optional, Union, Any, Dict

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.colorbar import Colorbar as MPLColorbar
from matplotlib.colors import Colormap, Normalize
from matplotlib.patches import Ellipse
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


class Colorbar(MPLColorbar):

    def __repr__(self):
        return "<Colorbar>"

    def __init__(
            self,
            mappable: Optional[ScalarMappable] = None,
            vmin: Optional[float] = None,
            vmax: Optional[float] = None,
            clip: bool = False,
            cmap: Union[str, Colormap, None] = None,
            ax: Optional[Axes] = None,
            style: str = "white",  # normal, white
            width: float = None,
            height: float = None,
            loc: Any = None,
            bbox_to_anchor: Any = None,
            bbox_transform: Any = None,
            axes_class: Any = None,
            axes_kwargs: Any = None,
            borderpad: Any = 0,
            orientation: str = "vertical",
            title: Optional[str] = None,
            title_align: str = "center",
            title_fontproperties: Optional[Dict] = None,
            **colorbar_options,
    ):
        """

        Parameters
        ----------
        mappable
        vmin
        vmax
        clip
        cmap
        ax
        style
        width
        height
        loc
        bbox_to_anchor
        bbox_transform
        axes_class
        axes_kwargs
        borderpad
        orientation
        title
        title_align
        title_fontproperties
        colorbar_options

        """

        if ax is None:
            ax = plt.gca()
        if mappable is None:
            mappable = ScalarMappable(norm=Normalize(vmin=vmin, vmax=vmax, clip=clip), cmap=cmap)

        # if loc is None:
        #     loc = "center left"
        # if bbox_to_anchor is None:
        #     bbox_to_anchor = (1.05, 0.5, 0, 0)
        # if bbox_transform is None:
        #     bbox_transform = ax.transAxes

        if (width is None) & (height is None):
            width, height = (0.3, 1.5)
            # Flip width and height
            if orientation == 'horizontal':
                width, height = height, width
        elif (width is not None) & (height is not None):
            pass
        else:
            if width is None:
                width = 1.5 if orientation == "horizontal" else 0.3
            else:
                height = 0.3 if orientation == "horizontal" else 1.5

        axins = inset_axes(ax, width=width, height=height, borderpad=borderpad,
                           bbox_to_anchor=bbox_to_anchor, bbox_transform=bbox_transform, loc=loc,
                           axes_class=axes_class, axes_kwargs=axes_kwargs,
                           )

        super().__init__(axins, mappable, orientation=orientation, **colorbar_options)

        if style == "white":
            # Inward ticks and white color
            self._long_axis().set_tick_params(direction="in", color="white", width=1, size=5)
            # turn off outlines
            self.outline.set_visible(0)

        if title is not None:
            if title_fontproperties is None:
                title_fontproperties = {'weight': 600, 'size': 'medium'}
            self.ax.set_title(title, loc=title_align, fontdict=title_fontproperties)

    def set_title(self, *args, **kw):
        self.ax.set_title(*args, **kw)


class EllipseColorbar:

    def __init__(
            self,
            vmin: Optional[float] = None,
            vmax: Optional[float] = None,
            cmap: Union[str, Colormap, None] = None,
            ax: Optional[Axes] = None,
            width: float = None,
            height: float = None,
            loc: Any = None,
            bbox_to_anchor: Any = None,
            bbox_transform: Any = None,
            axes_class: Any = None,
            axes_kwargs: Any = None,
            borderpad: Any = 0,
            ticklocation: str = "auto",
            orientation: str = "vertical",
            title: Optional[str] = None,
            title_align: str = "center",
            title_fontproperties: Optional[Dict] = None,
            alpha: Optional[float] = None,
            **colorbar_options,
    ):
        """

        Parameters
        ----------
        vmin
        vmax
        cmap
        ax
        width
        height
        loc
        bbox_to_anchor
        bbox_transform
        axes_class
        axes_kwargs
        borderpad
        orientation
        title
        title_align
        title_fontproperties
        alpha
        colorbar_options

        """

        if ax is None:
            ax = plt.gca()

        # We don't need to do this for user
        # if loc is None:
        #     loc = "center left"
        # if bbox_to_anchor is None:
        #     bbox_to_anchor = (1.05, 0.5, 0, 0)
        # if bbox_transform is None:
        #     bbox_transform = ax.transAxes
        self.vmin = vmin
        self.vmax = vmax
        self.orientation = orientation
        self.ticklocation = ticklocation

        if (width is None) & (height is None):
            width = 0.4
            height = width * 1.5
            # Flip width and height
            if orientation == 'horizontal':
                width, height = height, width
        elif (width is not None) & (height is not None):
            pass
        else:
            if width is None:
                width = 1
            else:
                height = 1

        self.axins = inset_axes(ax, width=width, height=height, borderpad=borderpad,
                                bbox_to_anchor=bbox_to_anchor, bbox_transform=bbox_transform, loc=loc,
                                axes_class=axes_class, axes_kwargs=axes_kwargs,
                                )
        self.axins.set_ylim(0, height)
        self.axins.set_xlim(0, width)
        patch = Ellipse((width / 2, height / 2), width, height, facecolor='none')
        self.axins.add_patch(patch)

        self._set_axis()

        sample_range = height if orientation == "horizontal" else width
        draw_content = np.repeat(np.linspace(0, sample_range, num=100), 100).reshape(100, 100)
        if orientation == "horizontal":
            draw_content = draw_content.T

        self.axins.imshow(draw_content,
                          alpha=alpha,
                          interpolation='spline16',
                          cmap=cmap,
                          origin='lower',
                          extent=[0, width, 0, height],
                          clip_path=patch,
                          clip_on=True)
        # Turn off the frame
        for spine in self.axins.spines.values():
            spine.set_visible(0)
        # Tick control
        #
        #     self._long_axis.set_ticklabel
        #     axins.set_yticks(list(axins.get_ylim()))
        #     # Set label
        #     axins.yaxis.set_label_position("right")
        #     axins.set_yticklabels([vmin, vmax])
        # else:
        #     # Turn off yaxis
        #     axins.yaxis.set_visible(0)
        #     # Set Ticks
        #     # axins.yaxis.tick_right()
        #     axins.yaxis.set_tick_params(direction="in")
        #     axins.set_xticks(list(axins.get_xlim()))
        #     # Set label
        #     # axins.xaxis.set_label_position("bottom")
        #     axins.set_xticklabels([vmin, vmax])

        if title is not None:
            if title_fontproperties is None:
                title_fontproperties = {'weight': 600, 'size': 'medium'}
            self.axins.set_title(title, loc=title_align, fontdict=title_fontproperties)

    def set_title(self, *args, **kw):
        self.axins.set_title(*args, **kw)

    def _set_axis(self):
        raise_error = False
        if self.orientation == "vertical":
            self._long_axis = self.axins.yaxis
            self._short_axis = self.axins.xaxis
            self._ticks = list(self.axins.get_ylim())
            if self.ticklocation in ["auto", "right"]:
                self._long_axis.tick_right()
                self._long_axis.set_label_position("right")
            elif self.ticklocation == "left":
                self._long_axis.tick_left()
                self._long_axis.set_label_position("left")
            else:
                raise_error = True
        else:
            self._long_axis = self.axins.xaxis
            self._short_axis = self.axins.yaxis
            self._ticks = list(self.axins.get_xlim())
            if self.ticklocation in ["auto", "bottom"]:
                self._long_axis.tick_bottom()
                self._long_axis.set_label_position("bottom")
            elif self.ticklocation == "top":
                self._long_axis.tick_top()
                self._long_axis.set_label_position("top")
            else:
                raise_error = True

        # Turn off xaxis
        self._short_axis.set_visible(0)
        # Set Ticks
        self._long_axis.set_tick_params(direction="in")
        self._long_axis.set_ticks(self._ticks, labels=[self.vmin, self.vmax])

        if raise_error:
            raise ValueError(f"Cannot set ticklocation=`{self.ticklocation}`"
                             f"when orientation=`{self.orientation}`")
