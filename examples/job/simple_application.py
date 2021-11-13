# File: simple_application.py
'''
Example scikit-rt algorithm.
'''

import glob
import os
import sys

from skrt.application import Algorithm, Application
from skrt.core import fullpath

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

    def __init__(self, opts={}, name=None, log_level='INFO',
                 alg_module=''):
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
        alg_module: str, default=''
            Path to module where algorithm is defined.
        '''

        # Configurable variables
        # Maximum number of patients to be analysed
        self.max_patient = 10

        # Call to __init__() method of base class
        # sets values for object properties based on dictionary opts
        Algorithm.__init__(self, opts, name, log_level, alg_module)

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

    # Set the severity level for event logging
    log_level = 'INFO'

    # Create algorithm object
    alg_module = fullpath(sys.argv[0])
    alg = SimpleAlgorithm(opts=opts, name=None, log_level=log_level,
                          alg_module=alg_module)

    # Create the list of algorithms to be run (here just the one)
    algs = [alg]

    # Create the application
    app = Application(algs=algs, log_level=log_level)

    return app

def get_paths():
    # Define the patient data to be analysed
    data_dir = '/Users/karl/data/head_and_neck/vspecial/' \
               '3_patients__multiple_structures__all_mv/'
    data_dir = '/r02/voxtox/data/head_and_neck/consolidation/'
    paths = glob.glob(f'{data_dir}/VT*')

    return paths

if '__main__' == __name__:
    # Define and configure the application to be run.
    app = get_app()

    # Define the patient data to be analysed
    paths = get_paths()

    # Run application for the selected data
    app.run(paths)

if 'Ganga' in __name__:
    # Define script for setting analysis environment
    setup_script = fullpath('skrt_conda.sh')

    # Define and configure the application to be run.
    ganga_app = SkrtApp._impl.from_application(get_app(), setup_script)

    # Define the patient data to be analysed
    paths = get_paths()
    input_data = PatientDataset(paths=paths[0:3])

    # Define processing system
    backend = Local()
    # backend = Condor()

    # Define how job should be split into subjobs
    splitter = PatientDatasetSplitter(patients_per_subjob=1)

    # Define merging of subjob outputs
    merger = SmartMerger()
    merger.files = ['stderr', 'stdout']
    merger.ignorefailed = True
    postprocessors = [merger]

    # Define job name
    name = 'example_job'

    # Define list of outputs to be saved
    outbox = []

    # Create the job, and submit to processing system
    j = Job(application=ganga_app, backend=backend, inputdata=input_data,
            outputsandbox=outbox, splitter=splitter,
            postprocessors=postprocessors, name=name)
    j.submit()
