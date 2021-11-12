# File: example_job.py
'''
Example script for defining Ganga job to run Skrt application.
'''
import glob
import os

# Determine script file path, and use this to define the path
# to the script for setting up the Skrt environment.
install_dir = os.path.realpath(__file__).split('/ganga-skrt')[0]
example_job_dir = f'{install_dir}/ganga-skrt/examples/job'
app_dir = f'{example_job_dir}'
setup_script = f'{example_job_dir}/skrt_conda.sh'

# Create a dictionary of options to be passed to the algorithm
opts = {}
# Set the maximum number of patients to be analysed
opts['max_patient'] = 1000

# Create algorithm object
alg1 = SkrtAlg\
  (
   alg_class='SimpleAlgorithm',
   alg_name='simple_algorithm',
   alg_module=f'{app_dir}/simple_application.py',
   opts=opts,
   setup_script=setup_script,
  )

# Create the list of algorithms to be run (here just the one)
algs = [alg1]

# Create application object
app = SkrtApp(algs=algs, setup_script=setup_script)
app = alg1

# Create list of paths to patients folders
data_dir = '/r02/voxtox/data/head_and_neck/consolidation/'
paths = glob.glob(f'{data_dir}/VT*')
# Define the input data
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
j = Job(application=app, backend=backend, inputdata=input_data,
        outputsandbox=outbox, splitter=splitter,
        postprocessors=postprocessors, name=name)
j.submit()
