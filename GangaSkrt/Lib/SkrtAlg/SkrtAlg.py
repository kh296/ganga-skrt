# File: GangaSkrt/Lib/SkrtAlg/SkrtAlg.py

'''
Define SkrtAlg application.
'''

from GangaCore.Utility.Config import config_scope
from GangaCore.Utility import logging
from GangaCore.GPIDev.Base.Proxy import getName
from GangaCore.GPIDev.Lib.File import ShareDir
from GangaCore.GPIDev.Schema import Schema, SimpleItem, Version
from GangaCore.GPIDev.Adapters.IPrepareApp import IPrepareApp

logger = logging.getLogger()


class SkrtAlg(IPrepareApp):
    '''
    Represent scikit-rt algorithm as Ganga application.

    For information about Ganga applications, see documentation of
    GangaCore.GPIDev.Adapters.IApplication.IApplication.
    '''

    _schema = Schema(Version(1, 0), {
        'alg_class': SimpleItem(
            defvalue='',
            doc='Name of scikit-rt algorithm class to be instantiated'),
        'alg_module': SimpleItem(
            defvalue='',
            doc='Path to module containing scikit-rt algorithm class'),
        'alg_name': SimpleItem(
            defvalue='',
            doc='Name to be associated with algorithm instantiation'),
        'opts': SimpleItem(
            defvalue={},
            doc='Dictionary of options to be passed '
                + 'to algorithm constructor'),
        'log_level': SimpleItem(
            defvalue='INFO',
            doc=' Severity level for event logging'),
        'setup_script': SimpleItem(
            defvalue='',
            doc='Bash setup script to be sourced on worker node\n'
            + '(ignored if SkrtAlg is passed in list to SkrtApp)'),
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
    _name = 'SkrtAlg'
    # Make available methods implemented in base class
    _exportmethods = ['postprocess', 'prepare', 'unprepare']

    def __init__(self, alg_class='', alg_module='', alg_name='',
                 opts={}, setup_script='', root_file=''):
        '''
        Create instance of SkrtAlg.

        Parameters in the function declaration correspond to schema items.
        Type checking is performed for parameter values.

        Parameters
        ----------
        alg_class    : str, default=''
            Name of Skrt algorithm class to be instantiated
        alg_module   : str, default=''
            Path to module containing Skrt algorithm class
        alg_name     : str, default=''
            Name to be associated with algorithm instantiation
        opts         : dict, default={}
            Dictionary of options to be passed to algorithm constructor
        log_level    : str, default='INFO'
            Severity level for event logging.  Allowed values are:
            'NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
        setup_script : str, default=''
            Bash setup script to be sourced on worker node
            ignored if SkrtAlg is passed in list to SkrtApp
        '''
        super(SkrtAlg, self).__init__()

        if alg_class:
            assert(isinstance(alg_class, str))
            self.alg_class = alg_class

        if alg_module:
            assert(isinstance(alg_module, str))
            self.alg_module = alg_module

        if alg_name:
            assert(isinstance(alg_name, str))
            self.alg_name = alg_name

        if opts:
            assert(isinstance(opts, dict))
            self.opts = opts

        log_levels = ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if log_level:
            assert(log_level in log_levels)

        if setup_script:
            assert(isinstance(setup_script, str))
            self.setup_script = setup_script

    def __repr__(self):
        '''
        Return string representation of SkrtAlg instance.
        '''
        args = \
            [
                'alg_class = \'%s\'' % self.alg_class,
                'alg_module = \'%s\'' % self.alg_module,
                'alg_name = \'%s\'' % self.alg_name,
                'opts = %s' % str(self.opts),
                'log_level = %s' % str(self.log_level),
                'setup_script = \'%s\'' % self.setup_script,
            ]
        args_string = ', '.join(args)

        alg_repr = f'SkrtAlg({args_string})'

        return alg_repr

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
        app['opts'] = self.opts
        app['log_level'] = self.log_level

        return (False, app)

    def master_configure(self):
        '''
        Perform configuration that takes place before any job splitting.

        Application configuration extracts information for use by
        runtime handlers.
        '''

        app = \
            {
                'alg_class': self.alg_class,
                'alg_module': self.alg_module,
                'alg_name': self.alg_name,
                'opts': self.opts,
                'log_level': self.log_level,
                'setup_script': self.setup_script,
            }

        return(False, app)


# Add SkrtAlg to configuration scope
# (necessary to read in SkrtAlg from XML repository)
config_scope['SkrtAlg'] = SkrtAlg
