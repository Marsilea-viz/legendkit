# ColorArt Class: Axes-Independent Colorbar Documentation

## Table of Contents

* [1. Introduction](#1-introduction)
* [2. `get_colormap` Function](#2-getcolormap-function)
* [3. `ColorArt` Class](#3-colorart-class)
    * [3.1 `__init__` Method](#31-__init__-method)
    * [3.2 `_set_height_width` Method](#32-_set_height_width-method)
    * [3.3 `_make_cbar_box` Method](#33-_make_cbar_box-method)
    * [3.4 `_get_text_size` Method](#34-_get_text_size-method)
    * [3.5 `_process_values` Method](#35-_process_values-method)
    * [3.6 `_get_locator_formatter` Method](#36-_get_locator_formatter-method)
    * [3.7 `_get_ticks` Method](#37-_get_ticks-method)
    * [3.8 `_locate` Method](#38-_locate-method)
    * [3.9 `_extend_lower` and `_extend_upper` Methods](#39-_extend_lower-and-_extend_upper-methods)
    * [3.10 Other Methods](#310-other-methods)


<a name="1-introduction"></a>
## 1. Introduction

This document details the `ColorArt` class, providing an axes-independent colorbar functionality.  It serves as a replacement for Matplotlib's `colorbar` function in many scenarios. The class leverages Matplotlib's object-oriented framework for flexible customization and placement.


<a name="2-getcolormap-function"></a>
## 2. `getcolormap` Function

This helper function takes a colormap specification (either a `Colormap` object or a string colormap name) and returns a `Colormap` object.  It handles the lookup of named colormaps using `mpl.colormaps.get()`.

```python
def get_colormap(cmap):
    if isinstance(cmap, colors.Colormap):
        return cmap
    return mpl.colormaps.get(cmap)
```


<a name="3-colorart-class"></a>
## 3. `ColorArt` Class

The `ColorArt` class is the core of the colorbar creation.  It allows for highly customizable colorbars that can be positioned relative to axes or even outside of them.

<a name="31-__init__-method"></a>
### 3.1 `__init__` Method

The constructor (`__init__`) initializes the `ColorArt` object. It takes numerous parameters for controlling appearance and positioning.  Noteworthy aspects include:

* **Mappable Handling:** It accepts a `mappable` object (e.g., from `imshow`, `pcolormesh`) to inherit colormap and normalization information. If no mappable is provided, it creates a `ScalarMappable`.
* **Normalization and Colormap:** Accepts explicit `norm` and `cmap` parameters for direct control over color mapping.
* **Orientation:**  Supports both vertical and horizontal colorbars.
* **Tick Customization:** Extensive tick parameters are available for precise control over tick marks, labels, and their positions.
* **Placement:**  Uses `Locs` class to handle sophisticated placement using location strings (e.g., "out right center").  `bbox_to_anchor` and `bbox_transform` provide further control over positioning.
* **Size and Spacing:**  `width`, `height`, and `spacing` parameters control the colorbar's dimensions and the distribution of colors.
* **Title:** Includes parameters for setting the colorbar's title and its formatting.

<a name="32-_set_height_width-method"></a>
### 3.2 `_set_height_width` Method

This method sets the `width` and `height` attributes of the colorbar based on the user-provided values or default values relative to the fontsize.  The default aspect ratio is 5:1 (height:width for vertical, width:height for horizontal).

<a name="33-_make_cbar_box-method"></a>
### 3.3 `_make_cbar_box` Method

This is a key method that constructs the visual representation of the colorbar. The steps are:

1. **Get Ticks:** Calls `_get_ticks()` to determine tick locations and labels.
2. **Calculate Size:** Determines the overall size of the drawing area, considering tick labels and padding.
3. **Create Color Patches:** Creates a `PatchCollection` representing the colored segments of the colorbar.  The logic differs based on whether a `BoundaryNorm` is used (discrete boundaries) or a continuous normalization.
4. **Add Ticks and Labels:** Adds `LineCollection` objects for tick marks and `Text` objects for tick labels.  Tick placement is controlled by the `ticklocation` parameter.
5. **Add Title (if any):** If a title is specified, it is added using `TextArea` and combined with the colorbar using `VPacker`.
6. **Anchor Offsetbox:**  Finally, wraps the entire colorbar assembly (including title) within an `AnchoredOffsetbox` to manage the overall positioning as specified in the constructor.


<a name="34-_get_text_size-method"></a>
### 3.4 `_get_text_size` Method

This helper method calculates the space needed for tick labels to correctly adjust the size of the drawing area.  It uses the renderer to get the actual bounding boxes of the text labels and returns the maximum width and height.


<a name="35-_process_values-method"></a>
### 3.5 `_process_values` Method

This method determines the values and boundaries used for creating the colorbar. It handles different normalization types (`BoundaryNorm`, `NoNorm`, `LogNorm`, `SymLogNorm`, `AsinhNorm`, etc.) and user-specified values or boundaries.  The logic adapts to ensure correct mapping between data values and colormap indices.


<a name="36-_get_locator_formatter-method"></a>
### 3.6 `_get_locator_formatter` Method

This method selects the appropriate tick locator and formatter based on the normalization used and user-specified parameters. It handles various scenarios including:

* `BoundaryNorm`: Uses `FixedLocator`.
* `NoNorm`: Uses `IndexLocator`.
* `LogNorm` and `SymLogNorm`: Uses `LogLocator` and `LogFormatterSciNotation`.
* `AsinhNorm`: Uses `AsinhLocator` and a suitable formatter.
* Other cases: Uses `MaxNLocator` as a default.



<a name="37-_get_ticks-method"></a>
### 3.7 `_get_ticks` Method

This method uses the locator and formatter determined in `_get_locator_formatter` to get the actual tick positions and labels.  It adjusts for potential edge cases (e.g., log scales).


<a name="38-_locate-method"></a>
### 3.8 `_locate` Method

This method converts the tick values into pixel locations within the colorbar, accounting for orientation and flipping.  It also generates the line segments for the tick marks.


<a name="39-_extend_lower-and-_extend_upper-methods"></a>
### 3.9 `_extend_lower` and `_extend_upper` Methods

These helper methods determine whether the colorbar should show extensions at its lower and upper limits, respectively.


<a name="310-other-methods"></a>
### 3.10 Other Methods

* `get_bbox`, `get_window_extent`, `set_offset`: Standard Matplotlib Artist methods for bounding box and positioning management.
* `set_alpha`: Sets the alpha (transparency) value of the colorbar.
* `get_children`, `remove`: Methods to manage the colorbar's children and removal from the figure.
* `set_border`: A placeholder for future border drawing functionality.

This comprehensive documentation provides a detailed understanding of the internal workings of the `ColorArt` class, aiding developers in understanding, maintaining, and extending its functionality.
