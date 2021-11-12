from setuptools import find_packages, setup

setup(
    name='ganga-skrt',
    version='0.1.0',    
    description='Scikit-rt components for Ganga job-management framework',
    url='https://codeshare.phy.cam.ac.uk/kh296/ganga-skrt',
    author='',
    author_email='',
    license='',
    packages=find_packages(),
    install_requires=[
                      'ganga==8.5.0',
                      'in_place',
                     ],
    scripts=['examples/bin/create_config'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: To be decided :: To be decided',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
