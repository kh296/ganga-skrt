# File: simple_application.py
'''
Example scikit-rt algorithm.
'''

import glob

from skrt.application import Algorithm, Application

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
        # sets values for object properties based on dictionary optDict
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

if '__main__' == __name__:
    # The following code provides for configuring
    # and running the algorithm

    # Create a dictionary of options to be passed to the algorithm
    opts = {}
    # Set the maximum number of patients to be analysed
    opts['max_patient'] = 2

    # Set the severity level for event logging
    log_level = 'INFO'

    # Create algorithm object
    alg = SimpleAlgorithm(opts=opts, name=None, log_level=log_level)

    # Create the list of algorithms to be run (here just the one)
    algs = [alg]

    # Create the application
    app = Application(algs)

    # Define the patient data to be analysed
    data_dir = '/Users/karl/data/head_and_neck/vspecial/' \
               '3_patients__multiple_structures__all_mv/'
    paths = glob.glob(f'{data_dir}/VT*')

    # Run application for the selected data
    app.run(paths)
