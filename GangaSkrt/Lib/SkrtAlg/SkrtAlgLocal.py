# File: GangaSkrt/Lib/SkrtAlg/SkrtAlgLocal.py
'''
Define SkrtAlg application's runtime handling on local system.
'''

import os
import time

from GangaCore.GPIDev.Adapters.IRuntimeHandler import IRuntimeHandler
from GangaCore.GPIDev.Adapters.StandardJobConfig import StandardJobConfig
from GangaCore.GPIDev.Lib.File import File
from GangaCore.GPIDev.Lib.File import FileBuffer
from GangaCore.Utility.files import fullpath


class SkrtAlgLocal(IRuntimeHandler):
    '''
    Runtime handler for SkrtAlg application on local system.

    For information about Ganga runtime handlers, see documentation of
    GangaCore.GPIDev.Adapters.IRuntimeHandler.IRuntimeHandler
    '''

    def prepare(self, app, appsubconfig, appmasterconfig, jobmasterconfig):
        '''
        Prepare for running SkrtAlg application on local system.

        The preparation stage involves:
            - create wrapper script for running application;
            - define items to be transferred for when application runs;
            - define items to be returned after application completes.

        **Parameters:**

        app : GangaSkrt.Lib.SkrtAlg.SkrtAlg
            Object representing application to be run.

        appsubconfig : dict
            Data structure containing information extracted
            during application configuration after
            any job splitting.

        appmasterconfig: any
            In principle a data structure containing information
            extracted during application configuration before
            any job splitting, but here ignored.

        jobmasterconfig: any
            In principle a data structure containing information
            extracted during job configuration before
            any job splitting, but here ignored.
        '''

        job = app.getJobObject()

        lines = []
        inbox = []
        outbox = []

        head_lines, head_box = self.head(job=job, appsubconfig=appsubconfig)
        lines.extend(head_lines)
        inbox.extend(head_box)

        body_lines, body_inbox, body_outbox = \
            self.body(job=job, appsubconfig=appsubconfig)
        lines.extend(body_lines)
        inbox.extend(body_inbox)
        outbox.extend(body_outbox)

        tail_lines, tail_box = self.tail(job=job)
        lines.extend(tail_lines)
        outbox.extend(tail_box)

        job_script = '\n'.join(lines)
        job_wrapper = FileBuffer(
                f'skrt_{app._name[6:].lower()}.sh',
                job_script, executable=1)

        for outputfile in job.outputfiles:
            outbox.append(outputfile.namePattern)

        return StandardJobConfig(
                exe=job_wrapper, inputbox=inbox, outputbox=outbox)

    def head(self, job=None, appsubconfig=None,
             patient_data='patient_data'):

        '''
        Define operations needed before application is run.

        Returns head of wrapper script for handling application,
        and initial list of items to be transferred for when
        application runs.

        **Parameters:**

        job          : GangaCore.Lib.Job.Job
            Job object with which application is associated.

        appsubconfig : dict
            Data structure containing information extracted
            during application configuration after
            any job splitting.

        patient_data : str, default='patient_data'
            Name to be used for file containing paths to input data.
        '''

        paths_file = f'{patient_data}.py'
        inbox = [job.inputdata.write_paths_to_file_buffer(paths_file)]

        setup_script = appsubconfig['setup_script']

        time_now = time.strftime('%c')
        lines = [
                '#!/bin/bash',
                '',
                f'# Run script for application {job.application._name}',
                f'# Created by Ganga - {time_now}',
                '',]
        if setup_script:
            lines.extend([
                    f'source {setup_script}',
                    'env',
                    '',])
        lines.extend([
            'python << PYTHON_END',
            'import importlib',
            'import multiprocessing',
            'import platform',
            'import socket',
            'import sys',
            'import time',
            '',
            '# from cpuinfo import cpuinfo',
            f'from {patient_data} import paths',
            'from skrt import application as skrt_app',
            '',
            'job_start_time = f\'{time.time(): .6f}\'',
            'time_format = \'%a %d %b %Y %T %Z\'',
            '',
            'hostname = socket.getfqdn()',
            '# brand = cpuinfo.get_cpu_info()[\'brand_raw\']',
            'print()',
            'print()',
            'print(f\'Job running on {hostname}\')',
            'print(f\'Processor architecture: {platform.machine()}\')',
            '# print(f\'Processor type: {brand}\')',
            'print(\'CPU cores: {multiprocessing.cpu_count()}\')',
            'print()',
            'print(\'Start time: {time.strftime(time_format)}\')',
            'print()',
            'work_dir = platform.os.getcwd()',
            '',
        ])

        return (lines, inbox)

    def body(self, job=None, appsubconfig=None):
        '''
        Define operations needed to run application.

        Returns body of wrapper script for handling application,
        extended list of items to be transferred for when
        application runs, and initial list of items to be returned
        after application completes.

        **Parameters:**

        job          : GangaCore.Lib.Job.Job
            Job object with which application is associated.

        appsubconfig : dict
            Data structure containing information extracted
            during application configuration after
            any job splitting.
        '''

        alg_class = appsubconfig['alg_class']
        if appsubconfig['alg_module']:
            alg_module = fullpath(appsubconfig['alg_module'])
        else:
            alg_module = ''
        alg_name = appsubconfig['alg_name']
        opts = appsubconfig['opts']
        log_level = appsubconfig['log_level']

        inbox = []
        outbox = []

        lines = []
        if alg_module:
            alg_module_name = os.path.splitext(
                    os.path.basename(alg_module))[0]
            inbox.append(File(alg_module))
            lines.append('import %s' % (alg_module_name))
        else:
            alg_module_name = 'skrt_app'

        if appsubconfig['patient_class']:
            p_module, p_class = appsubconfig['patient_class'].rsplit('.', 1)
            lines.extend([
                'PatientClass = getattr(importlib.import_module(',
               f'    "{p_module}"), "{p_class}")',
                ])
        else:
            lines.append('PatientClass = None')

        lines.extend([
            f'kwargs = {appsubconfig["patient_opts"]}',
            '',
            ])

        lines.extend([
            f'SkrtAlgClass = getattr({alg_module_name}, "{alg_class}")',
            f'skrt_alg = SkrtAlgClass(name="{alg_name}", opts={opts}, '
            f'log_level="{log_level}")',
            'algs = [skrt_alg]',
            'app = skrt_app.Application(algs=algs)',
            f'status = app.run(paths, PatientClass, **kwargs)',
            'print()',
            'print(f"Return code: {status.code}")',
            'if not status.ok():',
            '    print(f\'Status name: {status.name}\')',
            '    print(f\'Status reason: {status.reason}\')',
            'print()',
        ])

        return (lines, inbox, outbox)

    def tail(self, job=None):
        '''
        Define operations needed after application has run.

        Returns tail of wrapper script for handling application, and
        extended list of items to be returned after application completes.

        **Parameter:**

        job : GangaCore.Lib.Job.Job
            Job object with which application is associated.
        '''
        lines = \
            [
                '',
                'run_data_path = \'%s/execute.dat\' % work_dir',
                'run_data = open( run_data_path, \'w\' )',
                'run_data.write( \'Hostname: %s\\n\' % hostname )',
                'run_data.write( \'Job_start: %s\\n\' % job_start_time )',
                'run_data.write( \'Job_end: %.6f\\n\' % time.time() )',
                'run_data.close()',
                'print(\'End time: %s\\n\' % time.strftime( time_format ))',
                'sys.exit( status.code )',
                'PYTHON_END',
            ]

        outbox = ['execute.dat']

        return (lines, outbox)
