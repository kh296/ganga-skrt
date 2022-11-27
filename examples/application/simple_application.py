# File: simple_application.py
'''
Example algorithm and application.

The application is defined and configured via three user-provided functions:

- **get_app()**: this defines the algorithm(s) to run,
  and run-time parameter values.
- **get_data_loader()**: this defines the class to be used for
  loading patient datasets, and options to be passed to the class constructor.
- **get_data_locations()**: this defines directories and search patterns
  for identifying datasets to be analysed.

With these functions, algorithm(s) to run, options, and datasets to be analysed
are defined once, then can be used for running both interactively and
using Ganga.
'''

import platform
import sys

from pathlib import Path

from skrt.application import Algorithm, Application, get_paths
from skrt.core import fullpath, qualified_name

class SimpleAlgorithm(Algorithm):

    '''
    Example scikit-rt algorithm.

    A Skrt algorithm inherites from skrt.application.Algorithm,
    which includes code for setting object properties.

    When processing of patient datasets is carried out via
    a call to the run() method of skrt.application.Application,
    algorithm methods are called as follows:
    - initialise() : called before processing any datasets;
    - execute()    : called once for each dataset;
    - finalise()   : called after processing all datasets.
    '''

    def __init__(self, opts={}, name=None, log_level='INFO'):
        '''
        Create instance of SimpleAlgorithm.

        Parameters
        ----------
        opts : dict, default={}
            Dictionary of options, the keys of which are mapped
            to instance attributes.
        name : str/None, default=None
            Name to be associated with algorithm instance; if None,
            the instance name is set to the class name.
        log_level : str, default='INFO'
            Severity level for event logging.  Defined values are:
            'NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
        '''

        # Configurable variables
        # Maximum number of patients to be analysed
        self.max_patient = 10

        # Call to __init__() method of base class
        # sets values for object properties based on dictionary opts
        Algorithm.__init__(self, opts, name, log_level)

        # Counter of number of patients to be analysed
        self.n_patient = 0

    def execute(self, patient=None):
        '''
        Perform processing for an individual patient dataset.

        Parameter:
        patient : voxtox.utility.Patient
            Patient object for which processing is to be performed.
        '''
    # The execute() method is called once for each patient, the
    # data for which is passed via an instance of the Patient class.

        # Increase patient count
        self.n_patient += 1

        # Print patient identifier and path
        print(f'{patient.id}: {patient.path}')

        # Set non-zero status code if maximum number of patients reached
        if self.n_patient >= self.max_patient:
            self.status.code = 1
            self.status.reason = f'Reached {self.n_patient} patients'
            self.finalise()

        return self.status

    def finalise(self):
        '''
        Perform tasks required after processing all patients datasets.
        '''

        print (f'Number of patients analysed = {self.n_patient}')

        return self.status

def get_app(setup_script=''):
    '''
    Define and configure application to be run.
    '''

    # Create a dictionary of options to be passed to the algorithm
    opts = {}
    # Set the maximum number of patients to be analysed
    opts['max_patient'] = 2

    # Set options differently for batch processing
    if 'Ganga' in __name__:
        opts['max_patient'] = 4

    # Set options differently for batch processing via Ganga
    if 'Ganga' in __name__:
        # The number of datasets for processing is set via PatientDataset
        opts['max_patient'] = 10000
        # Ganga needs to know the module from which to import the algorithm
        opts['alg_module'] = fullpath(sys.argv[0])

    # Set the severity level for event logging
    log_level = 'INFO'

    # Create algorithm object
    alg = SimpleAlgorithm(opts=opts, name=None, log_level=log_level)

    # Create the list of algorithms to be run (here just the one)
    algs = [alg]

    # Create the application
    app = Application(algs=algs, log_level=log_level)

    return app

def get_data_loader():
    """
    Define class and options to be used for loading patient data.
    """
    # With PatientClass set to None,
    # the class for data loading defaults to skrt.patient.Patient.
    PatientClass = None
    patient_opts = {}

    return (PatientClass, qualified_name(PatientClass), patient_opts)

def get_data_locations():
    """
    Specify locations of patient datasets.
    """
    # Define the patient data to be analysed
    if "Linux" == platform.system():
        data_dirs = [Path(f"/r02/voxtox/data/{site}")
                for site in ["cns", "head_and_neck", "prostate"]]
        patterns = [f"{subdir}{cohort}/VT*"
                for cohort in ["consolidation", "discovery"]
                for subdir in ["", "*/"]]
    else:
        data_dirs = [Path("~/data/voxtox_check").expanduser()]
        patterns = ["VT*"]

    return {data_dir: patterns for data_dir in data_dirs}

if '__main__' == __name__:
    # Define and configure the application to be run.
    app = get_app()

    # Define class and options for loading patient datasets.
    PatientClass, patient_class, patient_opts = get_data_loader()

    # Define the patient data to be analysed
    paths = get_paths(get_data_locations(), 2)

    # Run application for the selected data
    app.run(paths)

if 'Ganga' in __name__:
    # Define script for setting analysis environment
    setup_script = fullpath('skrt_conda.sh')

    # Define class and options for loading patient datasets.
    PatientClass, patient_class, patient_opts = get_data_loader()

    # Define and configure the application to be run.
    ganga_app = SkrtApp._impl.from_application(get_app(), setup_script,
            patient_class, patient_opts)

    # Define the patient data to be analysed
    if "Linux" == platform.system():
        paths = get_paths(get_data_locations())
    else:
        paths = get_paths(get_data_locations(), 2)

    input_data = PatientDataset(paths=paths)

    # Define processing system.
    if "Linux" == platform.system():
        backend = Condor()
        backend.cdf_options["request_memory"]="12G"
    else:
        backend = Local()

    # Define how job should be split into subjobs
    splitter = PatientDatasetSplitter(patients_per_subjob=1)

    # Define merging of subjob outputs
    merger = SmartMerger()
    merger.files = ['stderr', 'stdout']
    merger.ignorefailed = True
    postprocessors = [merger]

    # Define job name
    name = 'simple_application'

    # Define list of outputs to be saved
    outbox = []

    # Create the job, and submit to processing system
    j = Job(application=ganga_app, backend=backend, inputdata=input_data,
            outputsandbox=outbox, splitter=splitter,
            postprocessors=postprocessors, name=name)
    j.submit()
