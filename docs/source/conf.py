# Configuration file for the Sphinx documentation builder.

# -- Project information

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))  # so voxelmap is importable

project = 'voxelmap'
copyright = '2025, Andrew R. Garcia'
author = 'Andrew R. Garcia, Ph.D.'
release = '5.0.0'
version = '5.0.0'


# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

autodoc_mock_imports = ["vtkmodules", "pyvista", "vtkmodules.vtkFiltersExtraction"]


templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

