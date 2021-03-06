# File: GangaSkrt/Lib/SkrtApp/SkrtAppLocal.py
'''
Define SkrtApp application's runtime handling on local system.
'''

import os

from GangaCore.GPIDev.Lib.File import File
from GangaCore.Utility.files import fullpath

from GangaSkrt.Lib.SkrtAlg.SkrtAlgLocal import SkrtAlgLocal


class SkrtAppLocal(SkrtAlgLocal):
    '''
    Runtime handler for SkrtApp application on local system.

    For information about Ganga runtime handlers, see documentation of
    GangaCore.GPIDev.Adapters.IRuntimeHandler.IRuntimeHandler
    '''

    def body(self, job=None, appsubconfig=None):
        '''
        Define operations needed to run application.

        Returns body of wrapper script for handling application,
        extended list of items to be transferred for when
        application runs, and initial list of items to be returned
        after application completes.

        Parameters
        ----------
        job          : GangaCore.Lib.Job.Job
            Job object with which application is associated.
        appsubconfig : dict
            Data structure containing information extracted
            during application configuration after
            any job splitting.
        '''

        inbox = []
        outbox = []
        lines = ['algs = []']

        algs = appsubconfig['algs']
        log_level = appsubconfig['log_level']

        alg_modules = []
        for skrt_alg in algs:
            if skrt_alg.alg_module:
                alg_module = fullpath(skrt_alg.alg_module)
                if alg_module not in alg_modules:
                    alg_modules.append(alg_module)
                    inbox.append(File(alg_module))
                    alg_module_name = \
                        os.path.splitext(os.path.basename(alg_module))[0]
                    lines.append('import %s' % (alg_module_name))

        for skrt_alg in algs:
            if skrt_alg.alg_module:
                alg_module_name = os.path.splitext(
                    os.path.basename(skrt_alg.alg_module))[0]
            else:
                alg_module_name = 'skrt_app'
            lines.extend([
                    '',
                    f'SkrtAlgClass = getattr({alg_module_name}, '
                    + f'"{skrt_alg.alg_class}")',
                    f'skrt_alg = SkrtAlgClass(name="{skrt_alg.alg_name}", '
                    + f'opts = {skrt_alg.opts})',
                    'algs.append(skrt_alg)',
            ])
        lines.extend([
                '',
                'app = skrt_app.Application'
                + f'(algs=algs, log_level="{log_level}")',
                'status = app.run(paths=paths)',
                'print()',
                'print(f"Return code: {status.code}")',
                'if not status.ok():',
                '    sys.stderr.write'
                + '(\'\\n\'.join([status.name, status.reason]))',
                'print(\'\')',
        ])

        return (lines, inbox, outbox)
