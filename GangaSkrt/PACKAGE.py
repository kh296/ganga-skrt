# File: GangaSkrt/PACKAGE.py
"""
External dependencies and environment setup (do-nothing implementation).

This module is imported at Ganga startup,
via __init__() method of GangaCore.Utility.Runtime.RuntimePackage.

PACKAGE.setup defines external dependencies.

For more details of module purpose, see PACKAGE.py in GangaCore package.
"""

from GangaCore.Utility.Setup import PackageSetup

# External dependencies
setup = PackageSetup({})


def standardSetup(setup=setup):
    """
    Perform environment setup for external dependencies.
    """
