# File: GangaSkrt/Lib/SkrtAlg/__init__.py
"""
Defines SkrtAlg application and its runtime handling.
"""

from GangaCore.GPIDev.Adapters.ApplicationRuntimeHandlers import allHandlers
from GangaSkrt.Lib.SkrtAlg.SkrtAlgLocal import SkrtAlgLocal
from GangaSkrt.Lib.SkrtAlg.SkrtAlg import SkrtAlg

allHandlers.add("SkrtAlg", "Interactive", SkrtAlgLocal)
allHandlers.add("SkrtAlg", "Local", SkrtAlgLocal)
allHandlers.add("SkrtAlg", "Condor", SkrtAlgLocal)
