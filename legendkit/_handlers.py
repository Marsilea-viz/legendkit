from matplotlib.legend_handler import HandlerBase
from matplotlib.patches import Rectangle, Circle


def min_side(w, h):
    return min([w, h])


class SquareHandler(HandlerBase):
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

    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        p = self._create_patch(legend, orig_handle,
                               xdescent, ydescent, width, height, fontsize)
        self.update_prop(p, orig_handle, legend)
        p.set_transform(trans)
        return [p]


class RectHandler(HandlerBase):
    def _create_patch(self, legend, orig_handle,
                      xdescent, ydescent, width, height, fontsize):
        if width / height < 1.2:
            height = height * 0.6
            ydescent = ydescent - height * 0.2
        p = Rectangle(xy=(-xdescent, -ydescent),
                      width=width, height=height)
        return p

    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        p = self._create_patch(legend, orig_handle,
                               xdescent, ydescent, width, height, fontsize)
        self.update_prop(p, orig_handle, legend)
        p.set_transform(trans)
        return [p]


class CircleHandler(HandlerBase):
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

    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        p = self._create_patch(legend, orig_handle,
                               xdescent, ydescent, width, height, fontsize)
        self.update_prop(p, orig_handle, legend)
        p.set_transform(trans)
        return [p]
