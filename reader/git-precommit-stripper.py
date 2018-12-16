#!/usr/bin/env python

"""
@summary: 

########################## 
taken from https://gist.github.com/minrk/6176788

strip outputs from an IPython Notebook
Opens a notebook, strips its output, and writes the outputless version to the original file.
Useful mainly as a git filter or pre-commit hook for users who don't want to track output in VCS.
This does mostly the same thing as the `Clear All Output` command in the notebook UI.
LICENSE: Public Domain
########################## 

But then varied so that the execution_count and ExecuteTime is stripped (not the output).
Run this before committing a jupyter notebook to gitlab/github, for a less confusing commit diff view.

@author Dr Andreas Krueger
@organization: 
@author:  https://github.com/drandreaskrueger
@see:     https://github.com/drandreaskrueger/chainhammer for updates
@param git-precommit-stripper.py filename.ipynb
@attention: overwrites file
@warning: might not work perfectly, might be incomplete - some auto-updated cell properties might not yet be removed. Please extend.
@see: https://github.com/drandreaskrueger/DevOps/blob/master/snippets/git-precommit-stripper.py
@since last edit = 2017 August 07
@version: v04
"""

import io
import sys

try:
    # Jupyter >= 4
    from nbformat import read, write, NO_CONVERT
except ImportError:
    # IPython 3
    try:
        from IPython.nbformat import read, write, NO_CONVERT
    except ImportError:
        # IPython < 3
        from IPython.nbformat import current
    
        def read(f, as_version):
            return current.read(f, 'json')
    
        def write(nb, f):
            return current.write(nb, f, 'json')


def _cells(nb):
    """Yield all cells in an nbformat-insensitive manner"""
    if nb.nbformat < 4:
        for ws in nb.worksheets:
            for cell in ws.cells:
                yield cell
    else:
        for cell in nb.cells:
            yield cell


def strip_output(nb):
    """strip the outputs from a notebook object.    obsolete = UNUSED NOW"""
    nb.metadata.pop('signature', None)
    for cell in _cells(nb):
        if 'outputs' in cell:
            cell['outputs'] = []
        if 'prompt_number' in cell:
            cell['prompt_number'] = None
    return nb

def strip_execution_time_and_counter(nb):
    """strip the execution count and time from a notebook object, good for git committing. NEW."""
    # nb.metadata.pop('signature', None)
    for cell in _cells(nb):
        if 'metadata' in cell:
            md=cell['metadata']
            if 'ExecuteTime' in md:
                md['ExecuteTime'] = {}
        if 'execution_count' in cell:
            cell['execution_count'] = None
            if 'outputs' in cell:
                for op in cell['outputs']:
                    if 'execution_count' in op: 
                        op['execution_count'] = None
    return nb



if __name__ == '__main__':
    filename = sys.argv[1]
    with io.open(filename, 'r', encoding='utf8') as f:
        nb = read(f, as_version=NO_CONVERT)
    nb = strip_execution_time_and_counter(nb)
    with io.open(filename, 'w', encoding='utf8') as f:
        write(nb, f)
