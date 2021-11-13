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
   - Clone repository:
     - With [gitlab access via ssh keys](https://docs.gitlab.com/ee/ssh/):
       ```
       git clone git@codeshare.phy.cam.ac.uk:/kh296/ganga-skrt
       ```
     - With [gitlab access via token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html):
       ```
       git clone https://codeshare.phy.cam.ac.uk/kh296/ganga-skrt
       ```
   - From top-level directory of cloned repository, create **ganga-skrt**
     environment:
     ```
     conda env create --file environment.yml
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

## Usage

- For general information on using Ganga, see [Ganga User Guide](https://ganga.readthedocs.io/en/latest/UserGuide/index.html).

- For examples of defining a Ganga job to run a
[scikit-rt](https://codeshare.phy.cam.ac.uk/hp346/scikit-rt) application,
see [ganga-skrt/examples/jobs](https://codeshare.phy.cam.ac.uk/kh296/ganga-skrt/-/tree/main/examples/job).  Once data paths and setup script are defined
correctly, example scripts can be used for job submission from within
a Ganga session with:
```
ganga <example.py>
```

- The [scikit-rt](https://codeshare.phy.cam.ac.uk/hp346/scikit-rt) package
doesn't need to be available when submitting a Ganga job to run a
[scikit-rt](https://codeshare.phy.cam.ac.uk/hp346/scikit-rt) application,
but must be available when the job runs.
