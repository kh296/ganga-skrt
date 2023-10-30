# analysis_algorithm.py

import glob
import os

import pandas as pd

from skrt.application import Algorithm


class AnalysisAlgorithm(Algorithm):
    """Subclass of Algorithm, for analysing patient data"""

    def __init__(self, opts={}, name=None, log_level=None):
        """
        Create instance of Algorithm class.

        Parameters
        ----------
        opts : dict, default={}
            Dictionary for setting algorithm attributes.
        name : str, default=''
            Name for identifying algorithm instance.
        log_level: str/int/None, default=None
            Severity level for event logging.  If the value is None,
            log_level is set to the value of skrt.core.Defaults().log_level.
        """

        # If no name provided for instance, use class name
        class_name = str(type(self)).split(".")[-1].split("'")[0]
        name = class_name if name is None else name

        # Configurable variables
        # Maximum number of patients to be analysed
        self.max_patient = 10000

        # Create dictionary where each key is a name to be assigned
        # to a region of interest (ROI), and the associated value
        # is the list of names that may have been used during contouring.
        self.roi_names = {}

        # Call to __init__() method of base class
        # sets values for object properties based on dictionary opts,
        # and creates event logger with speficied name and log_level.
        Algorithm.__init__(self, opts, name, log_level)

        # List for storing data records
        self.roi_records = []

        # Counter of number of patients to be analysed
        self.n_patient = 0

    # The execute() method is called once for each patient, the data for
    # which is passed via an instance of the skrt.patient.Patient class.
    def execute(self, patient=None):
        # Increase patient count
        self.n_patient += 1

        # Print patient identifier
        print(f"\n{self.n_patient:03d} {patient.id}")

        # Only consider the first study.
        # In VoxTox, patients usually have only a single study,
        # but have more studies in the few cases where treatment is replanned.
        study = patient.studies[0]

        if len(study.ct_structure_sets) >= 2:
            # Assume that earliest structure set is from clinical planning
            planning_rois = study.ct_structure_sets[0].filtered_copy(
                names=self.roi_names, keep_renamed_only=True
            )
            # Assume that latest structure set is from VoxTox study
            voxtox_rois = study.ct_structure_sets[-1].filtered_copy(
                names=self.roi_names, keep_renamed_only=True
            )

            # Calculate dice scores for planning ROIs versus VoxTox ROIs,
            # and add to the list of data records.
            # Note: the ROI class defines methods for calculating
            # a number of comparison metrics.
            for planning_roi in planning_rois:
                roi_name = planning_roi.name
                if roi_name not in voxtox_rois.get_roi_names():
                    continue
                voxtox_roi = voxtox_rois[roi_name]
                dice = planning_roi.get_dice(voxtox_roi)
                self.logger.info(f"{planning_roi.name}: dice = {dice:.4f}")
                # If dice score is 1.0, the same ROI may have been picked up
                # got planning and VoxTox - worth checking.
                if dice > 0.999:
                    self.logger.warning(
                        f"Dice score of {dice:.4f} is suspicious!"
                    )
                else:
                    self.roi_records.append(
                        {
                            "id": patient.id,
                            "roi": roi_name,
                            "dice": dice,
                        }
                    )

        # Set non-zero status code if maximum number of patients reached
        if self.n_patient >= self.max_patient:
            self.status.code = 1
            self.status.reason = f"Reached {self.n_patient} patients\n"
            self.finalise()

        return self.status

    def finalise(self):
        print(f"\nNumber of patients analysed = {self.n_patient}")

        # Create dataframe from data records
        # and save in csv format
        df = pd.DataFrame(self.roi_records)
        df.to_csv("roi_info.csv", index=False)

        return self.status
