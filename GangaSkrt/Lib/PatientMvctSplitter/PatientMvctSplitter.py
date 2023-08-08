# File: GangaSkrt/Lib/PatientMvctSplitter/PatientMvctSplitter.py
"""Provide for scan-level dataset splitting."""

import os
import copy

from GangaCore.GPIDev.Schema import Schema, SimpleItem, Version
from GangaCore.GPIDev.Adapters.ISplitter import ISplitter


class PatientMvctSplitter(ISplitter):
    """
    Scan-level splitter for patient datasets.
    """

    _schema = Schema(
        Version(1, 0),
        {
            "process_kv": SimpleItem(
                defvalue=0,
                doc="Processing of kV scans: 0 - omitted;"
                "1 - as well as MV; -1 only kV",
            ),
            "scans_per_subjob": SimpleItem(
                defvalue=1,
                doc="Number of MV CT scans to be processed by each subjob",
            ),
            "separate_patients": SimpleItem(
                defvalue=True,
                doc="Flag for limiting to only one patient per subjob",
            ),
        },
    )
    _category = "splitters"
    _name = "PatientMvctSplitter"

    def is_study_time_stamp(self, test_string=""):
        """
        Return True if test string contains timestamp, or False otherwise.

        Parameter
        ---------
        test_string : str, default=''
            String to be tested for timestamp.
        """
        timestamp = True
        values = test_string.split("_")
        if len(values) != 2:
            timestamp = False
        else:
            for value in values:
                if not value.isdigit():
                    timestamp = False
                    break
        return timestamp

    def split(self, job):
        """
        Split job into subjobs.

        Parameter
        ---------
        job : GangaCore.GPIDev.Job.Job.Job
            Ganga job object for which splitting is to be performed.
        """

        subjobs = []

        paths = sorted(job.inputdata.paths)

        mvct_all = {}
        mvcts = []

        # Check whether information about MVCT data
        # has been passed to job object's application.
        try:
            mvct_dict = job.application.algs[0].opts["mvct_dict"]
        except KeyError:
            mvct_dict = {}

        if mvct_dict:
            # Create list of paths to MVCT data,
            # based on information passed to job object's application.
            for patient_id in list(mvct_dict.keys()):
                mvct_all[patient_id] = mvct_dict[patient_id]
                mvcts.extend(mvct_all[patient_id])
        else:
            # Create list of paths to MVCT data,
            # based on all scan data in patient's latest study folder.
            for path in paths:
                studies = os.listdir(path)
                studies.sort(reverse=True)
                # studies.sort()
                study_dir = None
                for study in studies:
                    if self.is_study_time_stamp(study):
                        study_dir = study
                        break

                if study_dir:
                    patient_id = os.path.basename(path)
                    mvct_all[patient_id] = []
                    mvct_times = []
                    ct_times = []
                    cthd_times = []
                    # Consider kV scans only (process_kv == -1),
                    # MV scans only (process_kv == 0),
                    # both kV and MV scans (process_kv == 1)
                    if not self.process_kv == 0:
                        ct_dir = os.path.join(path, study_dir, "CT")
                        if os.path.exists(ct_dir):
                            ct_times.extend(os.listdir(ct_dir))
                        for ct_time in ct_times:
                            ct_time_dir = os.path.join(ct_dir, ct_time)
                            mvct_all[patient_id].append(ct_time_dir)
                            mvcts.append(ct_time_dir)
                        cthd_dir = os.path.join(path, study_dir, "CT_HD")
                        if os.path.exists(cthd_dir):
                            cthd_times.extend(os.listdir(cthd_dir))
                        for cthd_time in cthd_times:
                            cthd_time_dir = os.path.join(cthd_dir, cthd_time)
                            mvct_all[patient_id].append(cthd_time_dir)
                            mvcts.append(cthd_time_dir)
                    if not self.process_kv == -1:
                        mvct_dir = os.path.join(path, study_dir, "MVCT")
                        if os.path.exists(mvct_dir):
                            mvct_times.extend(os.listdir(mvct_dir))
                        for mvct_time in mvct_times:
                            mvct_time_dir = os.path.join(mvct_dir, mvct_time)
                            mvct_all[patient_id].append(mvct_time_dir)
                            mvcts.append(mvct_time_dir)

        if self.separate_patients:
            # Include data from only one patient per subjob.
            for path in paths:
                patient_id = os.path.basename(path)
                mvct_time_dirs = sorted(mvct_all[patient_id])
                for i in range(0, len(mvct_time_dirs), self.scans_per_subjob):
                    subjob = self.createSubjob(job)
                    subjob.inputdata.paths = [path]
                    subjob_mvcts = mvct_time_dirs[i : i + self.scans_per_subjob]
                    subjob_mvct_dict = {patient_id: subjob_mvcts}
                    if "SkrtAlg" == getattr(job.application, "_name"):
                        subjob.application.opts["mvct_dict"] = subjob_mvct_dict
                    else:
                        algs = copy.deepcopy(subjob.application.algs)
                        subjob.application.algs = []
                        for alg in algs:
                            alg.opts["mvct_dict"] = subjob_mvct_dict
                            subjob.application.algs.append(alg)
                    subjobs.append(subjob)
        else:
            # Allow data from multiple patients per subjob.
            mvcts.sort()
            max_range = len(mvcts)
            for i in range(0, len(mvcts), self.scans_per_subjob):
                subjob = self.createSubjob(job)
                subjob.inputdata.paths = []
                subjob_mvct_dict = {}
                for j in range(i, min(i + self.scans_per_subjob, max_range)):
                    mvct_time_dir = mvcts[j]
                    path = os.path.dirname(
                        os.path.dirname(os.path.dirname(mvct_time_dir))
                    )
                    if path not in subjob.inputdata.paths:
                        subjob.inputdata.paths.append(path)
                    patient_id = os.path.basename(path)
                    if patient_id not in subjob_mvct_dict:
                        subjob_mvct_dict[patient_id] = []
                    subjob_mvct_dict[patient_id].append(mvct_time_dir)
                if "SkrtAlg" == getattr(job.application, "_name"):
                    subjob.application.opts["mvct_dict"] = subjob_mvct_dict
                else:
                    algs = copy.deepcopy(subjob.application.algs)
                    subjob.application.algs = []
                    for alg in algs:
                        alg.opts["mvct_dict"] = subjob_mvct_dict
                        subjob.application.algs.append(alg)
                subjobs.append(subjob)

        return subjobs
