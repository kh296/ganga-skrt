# File: GangaSkrt/Lib/SkrtApp/SkrtApp.py
'''
Define SkrtApp application.
'''

from GangaCore.GPIDev.Lib.File import ShareDir
from GangaCore.GPIDev.Schema import Schema, SimpleItem, Version
from GangaCore.GPIDev.Adapters.IPrepareApp import IPrepareApp


class SkrtApp(IPrepareApp):
    '''
    Represent scikit-rt application as Ganga application.

    A scikit-rt application is a sequence of scikit-rt algorithms.

    For information about Ganga applications, see documentation of
    GangaCore.GPIDev.Adapters.IApplication.IApplication.
    '''

    _schema = Schema(Version(1, 0), {
        'algs': SimpleItem(
            sequence=True, defvalue=[],
            typelist=['GangaSkrt.Lib.SkrtAlg.SkrtAlg.SkrtAlg'],
            doc='List of SkrtAlg algorithms to be run'),
        'log_level': SimpleItem(
            defvalue='INFO',
            doc=' Severity level for event logging'),
        'setup_script': SimpleItem(
            defvalue='',
            doc='Bash setup script to be sourced on worker node'),
        'is_prepared': SimpleItem(
            defvalue=None, strict_sequence=0, visitable=1, copyable=1,
            hidden=1, typelist=[None, ShareDir], protected=0, comparable=1,
            doc='Once application is prepared, '
                'location of shared resources'),
        'hash': SimpleItem(
            defvalue=None, typelist=[None, str], hidden=1,
            doc='MD5 hash for application\'s preparable attributes'),
    })

    _category = 'applications'
    _name = 'SkrtApp'
    # Make available methods implemented in base class
    _exportmethods = ['postprocess', 'prepare', 'unprepare']

    def __init__(self):
        '''
        Create instance of SkrtApp.
        '''
        super(SkrtApp, self).__init__()

    def configure(self, master_appconfig):
        '''
        Perform configuration that takes place after any job splitting.

        Application configuration extracts information for use by
        runtime handlers.

        Parameter
        master_appconfig : any
            Data structure containing application information
            from configuration before any job splitting.
            During job submission, this 
        '''
        app = dict(master_appconfig)
        app['algs'] = self.algs
        app['log_level'] = self.log_level
        return (False, app)

    def master_configure(self):
        '''
        Perform configuration that takes place before any job splitting.

        Application configuration extracts information for use by
        runtime handlers.
        '''
        app = {
              'algs': self.algs,
              'log_level': self.log_level,
              'setup_script': self.setup_script,
              }
        return(False, app)
