# Building Documentation with Sphinx

This document will outline the steps required to automatically document the Toolbox using Sphinx.

## Prerequisites

1. Sphinx: `pip install sphinx`
2. Read the Docs theme: `pip install sphinx-rtd-theme`
3. All modules must have __init__.py (duh) to be considered a module by Sphinx.
4. Well commented code with docstrings

## How to run sphinx

The initial setup has already been completed, with the file structure inside the docs folder.

1. To update the name, version, etc. update `conf.py`

2. From the src folder, run:

    `sphinx-apidoc -o docs src`

    This will generate / update the .rst files inside docs/source.

3. From the docs folder, run:

    `./make.bat html`

    This will execute the make.bat file in docs and create the html files for the final documentation.

    The html files will be stored in doc/build/html, along with all the css, javascript, images etc.

## Notes

If the structure of the toolbox changes, the toctrees (table of contents trees) inside modules.rst and index.rst may have to change.
These files dictate the tree structure for sphinx as it traverses the toolbox.

Sphinx will sometimes throw errors during the build, this will not stop the execution, but modules which throw errors may not be filled out completely.
Read the stacktrace to understand where the errors are, and fix them where possible. They can usually be subdued with creative error handling inside the
error-prone files.

The build process should be re-exectued for every new release, updating the documentation to reflect the new code structure / new tools.

Additional information can be found at: <https://www.sphinx-doc.org/en/master/>

A good video explaining the process: <https://www.youtube.com/watch?v=BWIrhgCAae0>
