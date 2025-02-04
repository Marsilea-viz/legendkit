# Colorbar Class Documentation

## Table of Contents

* [1. Introduction](#1-introduction)
* [2. Class `Colorbar`](#2-class-colorbar)
    * [2.1 `__init__` Method](#21-__init__-method)
    * [2.2 `__repr__` Method](#22-__repr__-method)
    * [2.3 `set_title` Method](#23-set_title-method)
    * [2.4 `get_xrange` Method](#24-get_xrange-method)
    * [2.5 `get_yrange` Method](#25-get_yrange-method)
    * [2.6 `get_midpoint` Method](#26-get_midpoint-method)
    * [2.7 `get_corner` Method](#27-get_corner-method)


## 1. Introduction

This document provides internal code documentation for the `Colorbar` class, extending Matplotlib's colorbar functionality.  It details the class's functionality, methods, and the algorithms used within.


## 2. Class `Colorbar`

The `Colorbar` class inherits from `matplotlib.colorbar.Colorbar` and provides enhanced customization options for creating colorbars within Matplotlib plots.


### 2.1 `__init__` Method

The constructor `__init__` initializes the `Colorbar` object. It takes numerous parameters to control the colorbar's appearance and placement.

| Parameter           | Type                               | Description                                                                                                                               |
|-----------------------|------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `mappable`           | `matplotlib.cm.ScalarMappable`     | The mappable object (e.g., `pcolormesh`) whose colormap and norm will be used.                                                       |
| `norm`               | `matplotlib.colors.Normalize`       | The normalization to use.                                                                                                                 |
| `cmap`               | `matplotlib.colors.Colormap`       | The colormap to use.                                                                                                                    |
| `ax`                 | `matplotlib.axes.Axes`             | The axes to draw the colorbar in (defaults to the current axes).                                                                       |
| `style`              | `str` (`'white'`, `'normal'`)      | Colorbar style; `'white'` uses inward ticks and white color, `'normal'` uses default styling.                                           |
| `shape`              | `str` (`'rect'`, `'ellipse'`, `'triangle'`, `'trapezoid'`) | The shape of the colorbar's clipping area.                                                                                            |
| `width`, `height`    | `float`                             | Width and height of the colorbar relative to the parent axes.  Automatically determined if both are `None`.                             |
| `loc`                | `str`                               | Location of the colorbar (see Matplotlib legend placement documentation, prefixing with 'out' places it outside the axes).              |
| `deviation`          | `float`                             | Space between colorbar and axes when placed outside.                                                                                   |
| `bbox_to_anchor`, `bbox_transform`, `axes_class`, `axes_kwargs`, `borderpad` |  Various Matplotlib parameters |  Parameters passed to `inset_axes` for precise colorbar positioning and appearance. Refer to Matplotlib documentation for details. |
| `orientation`        | `str` (`'vertical'`, `'horizontal'`) | Orientation of the colorbar.                                                                                                           |
| `title`              | `str`                               | Title of the colorbar.                                                                                                                 |
| `alignment`          | `str` (`'left'`, `'right'`, `'center'`) | Alignment of the colorbar title.                                                                                                       |
| `title_fontproperties` | `dict`                              | Font properties for the colorbar title.                                                                                                |
| `colorbar_options`   | `dict`                              | Additional keyword arguments passed to `matplotlib.colorbar.Colorbar`.                                                              |


The `__init__` method performs the following steps:

1. **Handles default values:** Assigns default values for `ax` and `loc` if not provided.  It also intelligently sets default `width` and `height` based on `orientation`.
2. **Transforms location:** Uses the `Locs().transform()` method (from the `_locs` module) to determine the optimal `loc`, `bbox_to_anchor`, and `bbox_transform` for the given placement specifications.
3. **Creates inset axes:**  Uses `inset_axes` to create a set of axes within the parent axes (`ax`) to host the colorbar.
4. **Initializes parent class:** Calls the superclass constructor (`super().__init__`) to create the actual colorbar using the provided parameters.
5. **Applies styling:**  Applies the specified `style` (e.g., white ticks and outline).
6. **Sets title:** Adds a title if specified, with customizable font properties.
7. **Sets shape:** Creates a clipping path based on the specified `shape` (rectangle, ellipse, triangle, trapezoid) to clip the colorbar's elements.



### 2.2 `__repr__` Method

This method returns a string representation of the `Colorbar` object: `<Colorbar>`.


### 2.3 `set_title` Method

A simple wrapper around `self.ax.set_title`, providing a more convenient way to set the colorbar title.


### 2.4 `get_xrange` Method

Calculates the range (difference) of the x-axis limits of the colorbar axes.


### 2.5 `get_yrange` Method

Calculates the range (difference) of the y-axis limits of the colorbar axes.


### 2.6 `get_midpoint` Method

Calculates the midpoint coordinates (x, y) of the colorbar axes.


### 2.7 `get_corner` Method

Returns the coordinates of the four corners of the colorbar axes, useful for creating custom shapes.  The corner numbering is documented as follows:

```
2-----3
|     |
|     |
1-----4
```
