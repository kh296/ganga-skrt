# File: GangaSkrt/Lib/SkrtApp/SkrtAppLocal.py
"""
Define SkrtApp application's runtime handling on local system.
"""

import os

from GangaCore.GPIDev.Lib.File import File
from GangaCore.Utility.files import fullpath

from GangaSkrt.Lib.SkrtAlg.SkrtAlgLocal import SkrtAlgLocal


class SkrtAppLocal(SkrtAlgLocal):
    """
    Runtime handler for SkrtApp application on local system.

    For information about Ganga runtime handlers, see documentation of
    GangaCore.GPIDev.Adapters.IRuntimeHandler.IRuntimeHandler
    """

    def body(self, appsubconfig=None):
        """
        Define operations needed to run application.

        Returns body of wrapper script for handling application,
        extended list of items to be transferred for when
        application runs, and initial list of items to be returned
        after application completes.

        Parameter
        ---------
        appsubconfig : dict
            Data structure containing information extracted
            during application configuration after
            any job splitting.
        """

        inbox = []
        outbox = []
        lines = ["algs = []"]

        algs = appsubconfig["algs"]
        log_level = appsubconfig["log_level"]

        alg_modules = []
        for skrt_alg in algs:
            if skrt_alg.alg_module:
                alg_module = fullpath(skrt_alg.alg_module)
                if alg_module not in alg_modules:
                    alg_modules.append(alg_module)
                    inbox.append(File(alg_module))
                    alg_module_name = os.path.splitext(
                        os.path.basename(alg_module)
                    )[0]
                    lines.append(f"import {alg_module_name}")

        if appsubconfig["patient_class"]:
            p_module, p_class = appsubconfig["patient_class"].rsplit(".", 1)
            lines.extend(
                [
                    "PatientClass = getattr(importlib.import_module(",
                    f'    "{p_module}"), "{p_class}")',
                ]
            )
        else:
            lines.append("PatientClass = None")

        lines.extend(
            [
                f'kwargs = {appsubconfig["patient_opts"]}',
                "",
            ]
        )

        for skrt_alg in algs:
            if skrt_alg.alg_module:
                alg_module_name = os.path.splitext(
                    os.path.basename(skrt_alg.alg_module)
                )[0]
            else:
                alg_module_name = "skrt_app"
            lines.extend(
                [
                    "",
                    f"SkrtAlgClass = getattr({alg_module_name}, "
                    + f'"{skrt_alg.alg_class}")',
                    f'skrt_alg = SkrtAlgClass(name="{skrt_alg.alg_name}", '
                    + f"opts = {skrt_alg.opts}, "
                    + f'log_level="{skrt_alg.log_level}")',
                    "algs.append(skrt_alg)",
                ]
            )
        lines.extend(
            [
                "",
                "app = skrt_app.Application"
                + f'(algs=algs, log_level="{log_level}")',
                "status = app.run(paths, PatientClass, **kwargs)",
                "print()",
                'print(f"Return code: {status.code}")',
                "if not status.is_ok():",
                "    sys.stderr.write"
                + "('\\n'.join([status.name, status.reason]))",
                "print('')",
            ]
        )

        return (lines, inbox, outbox)
