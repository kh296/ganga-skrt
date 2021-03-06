# ganga-skrt

This package provides scikit-rt components for the Ganga job-management
framework.

The main Ganga repository is:
- [https://github.com/ganga-devs/ganga](https://github.com/ganga-devs/ganga).


## Installation

The following have been tested using python 3.8, pip 21.2.2,
conda 4.10.3 and git 2.28.0.  Repository access via token
may not work with older versions of git.

1. User installation, using [pip](https://pip.pypa.io/en/stable/):
   - With [gitlab access via ssh keys](https://docs.gitlab.com/ee/ssh/):
     ```
     pip install git+ssh://git@codeshare.phy.cam.ac.uk:/kh296/ganga-skrt
     ```
   - With [gitlab access via token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html):
     ```
     pip install git+https://codeshare.phy.cam.ac.uk/kh296/ganga-skrt
     ```
   - Create Ganga configuration file (`~/.gangarc`):
     ```
     create_config
     ```
   - Optionally create setup script to be used by jobs at runtime:
     ```
     create_setup # output by default to skrt_conda.sh
     create_setup -h # show usage information
     ```

2. Developer installation, using [git](https://git-scm.com) and
[conda](https://docs.conda.io/):
   - Set up gitlab access [via token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) or [via ssh keys](https://docs.gitlab.com/ee/ssh/).
   - `cd` to directory where code is to be installed.
   - Clone ganga-skrt and skrt repositories:
     - With [gitlab access via token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html):
       ```
       git clone https://codeshare.phy.cam.ac.uk/kh296/ganga-skrt
       git clone https://codeshare.phy.cam.ac.uk/hp346/scikit-rt
       ```
     - With [gitlab access via ssh keys](https://docs.gitlab.com/ee/ssh/):
       ```
       git clone git@codeshare.phy.cam.ac.uk:/kh296/ganga-skrt
       git clone git@codeshare.phy.cam.ac.uk/hp346/scikit-rt
       ```
   - Create and activate **ganga-skrt** environment:
     ```
     cd ganga-skrt
     conda env create --file environment.yml
     conda activate ganga-skrt
     ```
   - Add **skrt** to the **ganga-skrt** environment:
     ```
     pip install -e ../scikit-rt
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
   - Edit `simple_application.py` so that the function `get_paths()` returns
     a list of paths to patient data available on the installation machine.
   - Start `ganga` session:
     ```
     ganga
     ```
   - From inside `ganga` session, submit example job:
     ```
     ganga simple_application.py
     ```

## Usage

- For general information on using Ganga, see [Ganga User Guide](https://ganga.readthedocs.io/en/latest/UserGuide/index.html).
- For examples of defining a Ganga job to run a
[scikit-rt](https://codeshare.phy.cam.ac.uk/hp346/scikit-rt) application,
see [ganga-skrt/examples/jobs](https://codeshare.phy.cam.ac.uk/kh296/ganga-skrt/-/tree/main/examples/job).
