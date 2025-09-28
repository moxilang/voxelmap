# Configuration file for the Sphinx documentation builder.

# -- Project information
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

project = 'voxelmap'
copyright = '2023, Andrew R. Garcia'
author = 'Andrew R. Garcia, Ph.D.'

release = '5.1'
version = '5.1.0'

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

autodoc_mock_imports = [
    "vtkmodules",
    "pyvista",
    "vtkmodules.vtkFiltersExtraction",
    "scipy",
    "skimage",
    "pandas",
    "cv2",  
]


templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'