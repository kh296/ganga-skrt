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
