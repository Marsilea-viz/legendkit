# Legend Creation and Manipulation Library: Internal Documentation

[TOC]

## 1. Introduction

This document provides internal documentation for the legend creation and manipulation library.  The library simplifies the process of generating and customizing legends within matplotlib plots.  It leverages several key classes to handle different legend types and offers convenient functions for layout management.  The current version is 0.3.4.

## 2. Module Structure and Key Classes

The library is structured around several core classes, each responsible for a specific type of legend:

| Class Name       | Description                                                                  |
|-------------------|------------------------------------------------------------------------------|
| `ColorArt`        | (Located in `_colorart.py`)  Handles color-related aspects of legend creation.  Details omitted for brevity. |
| `Colorbar`        | (Located in `_colorbar.py`)  Manages colorbar creation and integration with legends. Details omitted for brevity. |
| `ListLegend`      | (Located in `_legend.py`) Creates legends for lists of items.  Details omitted for brevity. |
| `CatLegend`       | (Located in `_legend.py`) Creates legends for categorical data. Details omitted for brevity. |
| `SizeLegend`      | (Located in `_legend.py`) Creates legends representing size variations. Details omitted for brevity. |


The module also includes:

* **`_register.py`**: This module contains the `register()` function.  Its purpose is to register default settings and legend handlers with matplotlib, ensuring consistent and predictable behavior across different uses of the library.  The `register()` function is called at the end of the main module's initialization.

* **`layout.py`**: This module provides functions `vstack` and `hstack` for arranging legend elements vertically and horizontally, respectively.  Details are omitted for brevity.


## 3. Public API

The module exposes the following functions and classes for public use:

* **`colorbar`**: An alias for the `Colorbar` class, providing a more concise way to access its functionality.

* **`colorart`**: An alias for the `ColorArt` class.

* **`legend`**: An alias for the `ListLegend` class, setting it as the default legend type.

* **`cat_legend`**: An alias for the `CatLegend` class.

* **`size_legend`**: An alias for the `SizeLegend` class.

These aliases simplify common use cases by providing readily accessible names for the primary legend classes.


## 4. Initialization

The `register()` function from `_register.py` is called upon module import. This ensures that necessary default settings and legend handlers are registered with matplotlib. This setup happens automatically when the module is imported, requiring no explicit user action.
