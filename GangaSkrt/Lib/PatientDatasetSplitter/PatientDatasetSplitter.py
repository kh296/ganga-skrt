# File: GangaSkrt/Lib/PatientDatasetSplitter/PatientDatasetSplitter.py
'''Provide for patient-level dataset splitting.'''

import copy

from GangaCore.GPIDev.Schema import Schema, SimpleItem, Version
from GangaCore.GPIDev.Adapters.ISplitter import ISplitter


class PatientDatasetSplitter(ISplitter):
    '''
    Patient-level splitter for patient datasets.
    '''

    _schema = Schema(Version(1, 0), {'patients_per_subjob': SimpleItem(
        defvalue=1,
        doc='Number of patients to be processed by each subjob')})
    _category = 'splitters'
    _name = 'PatientDatasetSplitter'

    def __init__(self):
        '''
        Create instance of PatientDatasetSplitter.
        '''
        super(PatientDatasetSplitter, self).__init__()

    def split(self, job):
        '''
        Split job into subjobs.

        Parameter
        ---------
        job : GangaCore.GPIDev.Job.Job.Job
            Ganga job object for which splitting is to be performed.
        '''

        subjobs = []

        paths = job.inputdata.paths

        for i in range(0, len(paths), self.patients_per_subjob):
            subjob = self.createSubjob(job)
            inputdata = copy.deepcopy(job.inputdata)
            inputdata.paths = paths[i: i + self.patients_per_subjob]
            subjob.inputdata = inputdata
            subjobs.append(subjob)

        return subjobs
