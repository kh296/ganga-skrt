from setuptools import find_packages, setup

setup(
    name='ganga-skrt',
    version='0.1.0',    
    description='Scikit-rt components for Ganga job-management framework',
    url='https://codeshare.phy.cam.ac.uk/kh296/ganga-skrt',
    author='K. Harrison',
    author_email='',
    license='',
    packages=find_packages(),
    install_requires=[
                      'ganga',
                      'in_place',
                     ],
    scripts=['examples/bin/create_config', 'examples/bin/create_setup'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: To be decided :: To be decided',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
    ],
)
