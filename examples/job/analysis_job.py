import glob
from inspect import getfile

from skrt.application import Application
from skrt.core import fullpath

from analysis_application import AnalysisAlgorithm


def get_app(setup_script=''):
    '''
    Define and configure application to be run.
    '''

    # Create a dictionary of options to be passed to the algorithm
    opts = {}
    # Set the maximum number of patients to be analysed
    opts['max_patient'] = 3

    # Set options differently for batch processing via Ganga
    if 'Ganga' in __name__:
        # The number of datasets for processing is set via PatientDataset
        opts['max_patient'] = 10000
        # Ganga needs to know the module from which to import the algorithm
        opts['alg_module'] = getfile(AnalysisAlgorithm)

    # Create dictionary where each key is a name to be assigned
    # to a region of interest (ROI), and the associated value
    # is the list of names that may have been used during contouring.
    opts['roi_map'] = {}
    opts['roi_map']['parotid_left'] = [
        'left parotid (dn)', 'left parotid - dn',
        'l parotid', 'left parotid', 'lt parotid', 'parotid lt', 'parotid_l',
        'parotid l', 'parotid_l_', 'parotid_l1', 'parotid left',
        'parotid_l_sp', 'left  parotid', 'l  parotid', 'l parotid_old',
        'l parotid b', 'leftparotid']
    opts['roi_map']['parotid_right'] = [
        'right parotid (dn)', 'right parotid - dn',
        'r parotid', 'right parotid', 'rt parotid', 'parotid rt', 'parotid_r',
        'parotid r', 'parotid_r_', 'parotid_r1', 'parotid right',
        'parotid_r_sp', 'right  parotid', 'r  parotid', 'r parotid_old',
        'r parotid b', 'rightparotid']
    opts['roi_map']['smg_left'] = [
        'l submandibular gland', 'left submandibular', 'lt submandibular',
        'left submandibular gland', 'l submandibular', 'l submandib',
        'left submandibular glan', 'l submand', 'l submand gland',
        'lt submand', 'submandibular lt', 'submandibular gland lt',
        'lt submandibular gland', 'submand left', 'submandibular l',
        'lt submang', 'submandibular left', 'subman lt', 'l sub mandibular',
        'l submandibular galnd', 'l sub mand gland', 'left smg', 'l smg',
        'lt smg', 'l  submandibular', 'left subm gland', 'lt submandib',
        'left sm gland', 'left submandibular aj', 'lt submandibular galnd',
        'submnd_salv_l1', 'lt sm Gland', 'lt submand gland',
        'left submandibular gl', 'l sm gland', 'left submand  gland',
        'left submandibular g', 'l submandidular', 'left submand gl',
        'left submand gland', 'lt submandblr', 'submand left (in ptv)',
        'l smgland', 'l submadibular', 'left sumandibular gland',
        'l submandibular_old', 'l sum mandib']
    opts['roi_map']['smg_right'] = [
        'r submandibular gland', 'right submandibular', 'rt submandibular',
        'right submandibular gland', 'r submandibular', 'r submandib',
        'right submandibular glan', 'r submand', 'r submand gland',
        'rt submand', 'submandibular rt', 'submandibular gland rt',
        'rt submandibular gland', 'submand right', 'submandibular r',
        'rt submang', 'submandibular right', 'subman rt', 'r sub mandibular',
        'r submandibular galnd', 'r sub mand gland', 'right smg', 'r smg',
        'rt smg', 'r  submandibular', 'right subm gland', 'rt submandib',
        'right sm gland', 'right submandibular aj', 'rt submandibular galnd',
        'submnd_salv_r1', 'rt sm Gland', 'rt submand gland',
        'right submandibular gl', 'r sm gland', 'right submand  gland',
        'right submandibular g', 'r submandidular', 'right submand gl',
        'right submand gland', 'rt submandblr', 'submand right (in ptv)',
        'r smgland', 'r submadibular', 'right sumandibular gland',
        'r submandibular_old', 'r sum mandib']
    opts['roi_map']['spinal_cord'] = [
        'spinal cord - dn', 'cord', 'spinal cord', 'spinal_cord',
        'spinal cord sjj', 'spinal cord - sjj', 'spinal_cord_sp'
        'spine', 'spinal_canal_sp', 'spinal_cord_', 'spinal canal',
        'spinal_canal', 'spinal cord sld', 'cord b', 'SC', 'spinalcord']

    # Severity level for event logging.
    # Defined values are: 'NOTSET' (0), 'DEBUG' (10), 'INFO' (20),
    # 'WARNING' (30), 'ERROR' (40), 'CRITICAL' (50)
    log_level = 'INFO'

    # Create algorithm object
    alg = AnalysisAlgorithm(opts=opts, name=None, log_level=log_level)

    # Create the list of algorithms to be run (here just the one)
    algs = [alg]

    # Create the application
    app = Application(algs=algs, log_level=log_level)

    return app


def get_paths():
    # Define the patient data to be analysed
    data_dir = '/Users/karl/data/head_and_neck/vspecial/' \
               '3_patients__multiple_structures__all_mv/'
    # data_dir = '/r02/voxtox/data/head_and_neck/consolidation/'
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
    name = 'analysis_job'

    # Define list of outputs to be saved
    outbox = []

    # Create the job, and submit to processing system
    j = Job(application=ganga_app, backend=backend, inputdata=input_data,
            outputsandbox=outbox, splitter=splitter,
            postprocessors=postprocessors, name=name)
    j.submit()
