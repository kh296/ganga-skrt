# File: GangaSkrt/Lib/PatientImageSplitter/PatientImageSplitter.py
"""Provide for image-level dataset splitting."""

import copy
from pathlib import Path

from GangaCore.GPIDev.Schema import Schema, SimpleItem, Version
from GangaCore.GPIDev.Adapters.ISplitter import ISplitter


class PatientImageSplitter(ISplitter):
    """
    Image-level splitter for patient datasets.
    """

    _schema = Schema(
        Version(1, 0),
        {
            "image_types": SimpleItem(
                defvalue=[], doc="Type(s) of image to be processed"
            ),
            "images_per_subjob": SimpleItem(
                defvalue=1,
                doc="Number of images to be processed by each subjob",
            ),
            "separate_patients": SimpleItem(
                defvalue=True,
                doc="Flag for limiting to only one patient per subjob",
            ),
        },
    )
    _category = "splitters"
    _name = "PatientImageSplitter"

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

        job_images = self.get_job_images(job, paths)

        if self.separate_patients:
            # Include data from only one patient per subjob.
            for path, images in job_images.items():
                for idx in range(0, len(images), self.images_per_subjob):
                    subjobs.append(
                        self.new_sub_job(
                            job,
                            {path: images[idx : idx + self.images_per_subjob]},
                        )
                    )

        else:
            # Allow data from multiple patients per subjob.
            subjob_images = {}
            n_image = 0
            for path, images in job_images.items():
                idx1 = 0
                while idx1 < len(images):
                    idx2 = min(
                        idx1 + self.images_per_subjob - n_image, len(images)
                    )
                    subjob_images.update({path: images[idx1:idx2]})
                    n_image += idx2 - idx1
                    if n_image == self.images_per_subjob:
                        subjobs.append(self.new_sub_job(job, subjob_images))
                        subjob_images = {}
                        n_image = 0
                    idx1 = idx2

            if subjob_images:
                subjobs.append(self.new_sub_job(job, subjob_images))

        return subjobs

    def new_sub_job(self, job, subjob_images):
        """
        Create new subjob.

        Parameter
        ---------
        job : GangaCore.GPIDev.Job.Job.Job
            Ganga job object for which new subjob is to be created.

        subjob_images : dict
            Dictionary where each key is the paths to a patient folder,
            and the associated value is a list of paths to image data
            within the folder.
        """
        subjob = self.createSubjob(job)
        inputdata = copy.deepcopy(job.inputdata)
        inputdata.paths = list(subjob_images.keys())
        subjob.inputdata = inputdata
        subjob_images_by_id = {
            Path(path).name: images for path, images in subjob_images.items()
        }

        if "SkrtAlg" == getattr(job.application, "_name"):
            subjob.application.opts["images"] = subjob_images_by_id
        else:
            algs = copy.deepcopy(subjob.application.algs)
            subjob.application.algs = []
            for alg in algs:
                alg.opts["images"] = subjob_images_by_id
                subjob.application.algs.append(alg)

        return subjob

    def get_job_images(self, job, paths):
        """
        Obtain dictionary associating patient folders to lists of image paths.

        Parameters
        ----------
        job : GangaCore.GPIDev.Job.Job.Job
            Ganga job object for which dictionary is to be created.

        paths : list
            List of paths to patient folders.
        """
        # If dictionary associating patient ids to image paths
        # has been passed to job object's application,
        # use this to create associations between
        # patient folders and image paths.
        job_images_by_id = job.application.algs[0].opts.get("images", {})
        if job_images_by_id:
            return {path: job_images_by_id[Path(path).name] for path in paths}

        # Create list of paths to image data of required type(s),
        # taking into account all study folders.
        job_images = {}
        for path in paths:
            job_images[path] = []
            patient_path = Path(path)
            studies = patient_path.glob("2*")
            for study in sorted(studies):
                if not self.is_study_time_stamp(study.name):
                    continue

                image_types = set(path.name.upper() for path in study.iterdir())
                if self.image_types:
                    image_types = set(
                        image_type.upper() for image_type in self.image_types
                    ).intersection(image_types)

                for image_type in image_types:
                    if str(image_type).startswith("."):
                        continue

                    job_images[path].extend(
                        [
                            str(image_path)
                            for image_path in sorted(
                                (study / image_type).glob("2*")
                            )
                        ]
                    )

        return job_images
