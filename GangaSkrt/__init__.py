# File: GangaSkrt/__init__.py
'''
Skrt plugins for the Ganga job-management framework.

This package has the standard structure of a Ganga runtime package:
    - BOOT.py defines code to be executed at Ganga startup
      (do-nothing implementation here);
    - PACKAGE.py defines external dependencies and their environment setup
      (do-nothing implementation here);
    - The Lib package provides plugin classes and runtime handlers.

The plugins provided are:
    - applications:
          - SkrtAlg: scikit-rt algorithm;
          - SkrtApp: scikit-rt application (list of scikit-rt algorithms);
    - datasets:
          - PatientDataset: DICOM files, following Skrt organisation;
    - splitters:
          - PatientDatasetSplitter: split datasets at patient level;
          - PatientMvctSplitter: split datasets at scan level;
    - mergers:
          - CsvMerger: merge files of data in CSV format;
          - JsonMerger: merge files of data in JSON format.

The runtime handlers provided are:
    - SkrtAlgLocal: run SkrtAlg application on local system;
    - SkrtAppLocal: run SkrtApp application on local system.

Scikit-rt builds on software developed in the context of the VoxTox study,
for information about which see:
    A. Drew et al., 'Using computing models from particle physics
    to investigate dose-toxicity correlations in cancer radiotherapy',
    Journal of Physics: Conference Series 898 (2017) 072048

For information about Ganga, see:
    J.T. Mościcki et al., 'Ganga: A tool for computational-task management
    and easy access to Grid resources',
    Computer Physics Communications 180 (2009) 2303-2316
    https://doi.org/10.1016/j.cpc.2009.06.016

The Ganga repository is:
    https://github.com/ganga-devs/ganga
'''

def loadPlugins(config={}):
    '''
    Load GangaSkrt plugins.

    If GangaSkrt is in Ganga's runtime path, this function is called
    during bootstrap, via the loadPlugins() method of
    GangaCore.Utility.Runtime.RuntimePackage.
    '''
    import GangaSkrt.Lib.CsvMerger
    import GangaSkrt.Lib.JsonMerger
    import GangaSkrt.Lib.PatientDataset
    import GangaSkrt.Lib.PatientDatasetSplitter
    import GangaSkrt.Lib.PatientMvctSplitter
    import GangaSkrt.Lib.SkrtAlg
    import GangaSkrt.Lib.SkrtApp
    return None
