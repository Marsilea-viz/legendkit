from matplotlib.collections import PatchCollection
from matplotlib.legend_handler import HandlerPatch
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle, Circle


def min_side(w, h):
    return min([w, h])


class SquareHandler(HandlerPatch):
    def _create_patch(self, legend, orig_handle,
                      xdescent, ydescent, width, height, fontsize):
        if width > height:
            s = height
            xoffset = (width - height) / 2.0
            yoffset = 0
        else:
            s = width
            xoffset = 0
            yoffset = (height - width) / 2.0
        p = Rectangle(xy=(-xdescent + xoffset, -ydescent + yoffset),
                      width=s, height=s)
        return p


class RectHandler(HandlerPatch):
    def _create_patch(self, legend, orig_handle,
                      xdescent, ydescent, width, height, fontsize):
        if width / height < 1.2:
            height = height * 0.6
            ydescent = ydescent - height * 0.2
        p = Rectangle(xy=(-xdescent, -ydescent),
                      width=width, height=height)
        return p


class CircleHandler(HandlerPatch):
    def _create_patch(self, legend, orig_handle,
                      xdescent, ydescent, width, height, fontsize):
        if width > height:
            s = height
            xoffset = (width - height) / 2.0
            yoffset = 0
        else:
            s = width
            xoffset = 0
            yoffset = (height - width) / 2.0
        p = Circle(xy=(-xdescent + s / 2 + xoffset, -ydescent + s / 2 + yoffset), radius=s / 2)
        return p


class BoxplotHanlder(HandlerPatch):

    box_w = 0.9
    box_h = 0.6

    def _create_patch(self, legend, orig_handle,
                      xdescent, ydescent, width, height, fontsize):
        if width / height < 1.2:
            height = height * 0.6
            ydescent = ydescent - height * 0.2
        w_offset = (1 - self.box_w) / 2
        h_offset = (1 - self.box_h) / 2
        box = Rectangle(xy=(-xdescent + w_offset * width, -ydescent + height * h_offset),
                        width=width * self.box_w, height=height * self.box_h)

        linewidth = 1
        vline = Rectangle(xy=(-xdescent + width / 2 - linewidth / 2, -ydescent),
                          width=linewidth / 2, height=height)

        hline = Rectangle(xy=(-xdescent + w_offset * width,
                              -ydescent + height * 0.5 - linewidth / 4),
                          width=width * self.box_w,
                          height=linewidth / 2)

        return PatchCollection([vline, box, hline], match_original=True)

