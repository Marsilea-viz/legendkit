from cycler import cycler
import legendkit

project = 'legendkit'
copyright = '2024, Mr-Milk'
author = 'Mr-Milk'
release = legendkit.__version__

extensions = [
    'numpydoc',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.autosectionlabel',
    'matplotlib.sphinxext.plot_directive',
    'sphinx.ext.intersphinx',
]

# Make sure the target is unique
autosectionlabel_prefix_document = True

# setting autosummary
autosummary_generate = True
autoclass_content = "class"
numpydoc_show_class_members = False

# setting plot directive
plot_include_source = True
plot_html_show_source_link = False
plot_html_show_formats = False
plot_formats = [('png', 200)]
plot_rcparams = {'savefig.bbox': 'tight',
                 'font.family': 'Lato',
                 'xtick.color': '.15',
                 'ytick.color': '.15',
                 'axes.axisbelow': True,
                 'grid.linestyle': '-',
                 'lines.solid_capstyle': 'round',
                 'axes.grid': True,
                 'axes.facecolor': 'EAEAF2',
                 'axes.edgecolor': 'white',
                 'axes.linewidth': 0,
                 'grid.color': 'white',
                 'xtick.major.size': 0,
                 'ytick.major.size': 0,
                 'xtick.minor.size': 0,
                 'ytick.minor.size': 0,
                 'axes.prop_cycle': cycler('color',
                                           ['#5A5B9F', '#D94F70', '#009473',
                                            '#F0C05A', '#7BC4C4', '#FF6F61']),
                 'legend.borderpad': 0.,
                 'legend.labelspacing': 0.5,
                 'legend.handlelength': 1.0,
                 'legend.handleheight': 1.0,
                 'legend.handletextpad': 0.5,
                 'legend.borderaxespad': 0.5,
                 'legend.columnspacing': 1.0
                 }
plot_apply_rcparams = True
plot_pre_code = """
import numpy as np
from matplotlib import pyplot as plt
import mpl_fontkit as fk

fk.install("Lato")
np.random.seed(0)

"""

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'furo'
html_static_path = ['_static']
html_favicon = "../../images/legendkit-logo.svg"

intersphinx_mapping = {
    'matplotlib': ('https://matplotlib.org/stable', None),
}


def setup(app):
    import legendkit as lk
    # Trick sphinx that these APIs are not alias
    lk.legend.__name__ = "legend"
    lk.cat_legend.__name__ = "cat_legend"
    lk.size_legend.__name__ = "size_legend"
    lk.colorbar.__name__ = "colorbar"
    lk.colorart.__name__ = "colorart"
