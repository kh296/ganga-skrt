# ganga-skrt

This package provides scikit-rt components for the Ganga job-management
framework.

The main Ganga repository is:
- [https://github.com/ganga-devs/ganga](https://github.com/ganga-devs/ganga).

## Installation

The following have been tested using python 3.8, pip 22.2.2,
conda 22.9.0 and git 2.28.0.

Perform either the user installation or the developer installation.

1. User installation, using [pip](https://pip.pypa.io/en/stable/):
   - Install from github:
     ```
     pip install git+https://github.com/kh296/ganga-skrt#egg=ganga-skrt
     ```
     This will also install Ganga and Scikit-rt, if they aren't
     installed already.

   - Create Ganga configuration file (`~/.gangarc`):
     ```
     create_config
     ```

   - Create setup script, which defines the environment variable
     PYTHONPATH such that the Python command `import skrt` executes
     successfully.  This setup script should be specified in
     Ganga jobs.

2. Developer installation, using [git](https://git-scm.com) and
   [conda](https://docs.conda.io/):

   - Clone ganga-skrt and skrt repositories:
     ```
     git clone https://github.com/kh296/ganga-skrt
     git clone https://github.com/scikit-rt/scikit-rt
     ```

   - Create and activate **ganga-skrt** environment:
     ```
     cd ganga-skrt
     conda env create --file environment_dev.yml
     conda activate ganga-skrt
     ```

   - Create Ganga configuration file (`~/.gangarc`):
     ```
     create_config
     ```

   - Create runtime setup script (`skrt_conda.sh`), ready for running example:
     ```
     cd examples/job
     create_setup 
     ```

## Running examples

   - Edit `simple_application.py` so that the function `get_data_locations()`
     returns lists of directories and search patterns that allow identification
     of  patient datasets  available on the installation machine.

   - Start `ganga` session:
     ```
     ganga
     ```

   - From inside `ganga` session, submit example job:
     ```
     ganga simple_application.py
     ```

## Further information

- For general information on using Ganga, see [Ganga User Guide](https://ganga.readthedocs.io/en/latest/UserGuide/index.html).

- For examples of [scikit-rt](https://github.com/scikit-rt/scikit-rt)
  applications that can be run interactively or via Ganga, see
  [ganga-skrt/examples/job](examples/application).
