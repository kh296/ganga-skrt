# File: GangaSkrt/Lib/SkrtApp/__init__.py
'''
Defines SkrtApp application and its runtime handling.
'''

from GangaCore.GPIDev.Adapters.ApplicationRuntimeHandlers import allHandlers
from GangaSkrt.Lib.SkrtApp.SkrtAppLocal import SkrtAppLocal
from GangaSkrt.Lib.SkrtApp.SkrtApp import SkrtApp

allHandlers.add('SkrtApp', 'Interactive', SkrtAppLocal)
allHandlers.add('SkrtApp', 'Local', SkrtAppLocal)
allHandlers.add('SkrtApp', 'Condor', SkrtAppLocal)
