# ganga-skrt

This package provides scikit-rt components for the Ganga job-management
framework.

The main Ganga repository is:
- [https://github.com/ganga-devs/ganga](https://github.com/ganga-devs/ganga).

For general information on using Ganga, see:
- [Ganga User Guide](https://ganga.readthedocs.io/en/latest/UserGuide/index.html).

## Installation

The following have been tested using python 3.8.13, pip 22.3.1,
conda 22.9.0 and git 2.28.0.

The recommended installation is using [git](https://git-scm.com/),
[conda](https://docs.conda.io/) and [pip](https://pypi.org/project/pip/):
- Clone ganga-skrt and scikit-rt repositories:
  ```
  git clone https://github.com/kh296/ganga-skrt
  git clone https://github.com/scikit-rt/scikit-rt
  ```
- Create and activate `ganga-skrt` environment, then add `scikit-rt`:
  ```
  cd ganga-skrt
  conda env create --file environment.yml
  conda activate ganga-skrt
  pip install -e ../scikit-rt
  ```
- Create Ganga configuration file (`~/.gangarc`):
  ```
  create_config
  ```

## Running example

- With the `ganga-skrt` environment activated, navigate to the directory
  of example applications, and create a runtime setup script (`skrt_conda.sh`):
  ```
  cd examples/application
  create_setup 
  ```

- Edit `simple_application.py` so that the function `get_data_locations()`
  returns lists of directories and search patterns that allow identification
  of  patient datasets  available on the machine(s) where the application
  will run.
- Start `ganga` session:
  ```
  ganga
  ```
- From inside `ganga` session, submit example job:
  ```
  ganga simple_application.py
  ```
