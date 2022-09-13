Colorbar Creation
=================

The colorbar in legendkit is similar to matplotlib's colorbar,
you can change the shape of the colorbar.

.. plot::
    :context: close-figs

    >>> from legendkit import colorbar
    >>> _, ax = plt.subplots()
    >>> m = np.random.randn(10, 10)
    >>> mappable = ax.pcolormesh(m, cmap="Wistia")
    >>> colorbar(mappable, loc="out right upper", shape="ellipse")
    >>> colorbar(mappable, ax=ax, orientation="horizontal", loc="out upper center")
    >>> colorbar(mappable, ax=ax, loc="out right lower", shape="triangle")


Legendkit also provide you with an `Artist` based implementation of colorbar,
it's useful in layout multiple legends and colorbars.

.. plot::
    :context: close-figs

    >>> from legendkit import colorart
    >>> _, ax = plt.subplots()
    >>> m = np.random.randn(10, 10)
    >>> mappable = ax.pcolormesh(m, cmap="cool")
    >>> colorart(mappable, ax=ax, loc="out right center")