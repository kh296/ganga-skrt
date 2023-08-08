# File: GangaSkrt/Lib/SkrtApp/SkrtApp.py
"""
Define SkrtApp application.
"""

from GangaCore.GPIDev.Lib.File import ShareDir
from GangaCore.GPIDev.Schema import Schema, SimpleItem, Version
from GangaCore.GPIDev.Adapters.IPrepareApp import IPrepareApp

from GangaSkrt.Lib.SkrtAlg.SkrtAlg import SkrtAlg


class SkrtApp(IPrepareApp):
    """
    Represent scikit-rt application as Ganga application.

    A scikit-rt application is a sequence of scikit-rt algorithms.

    For information about Ganga applications, see documentation of
    GangaCore.GPIDev.Adapters.IApplication.IApplication.
    """

    _schema = Schema(
        Version(1, 0),
        {
            "algs": SimpleItem(
                sequence=True,
                defvalue=[],
                typelist=["GangaSkrt.Lib.SkrtAlg.SkrtAlg.SkrtAlg"],
                doc="List of SkrtAlg algorithms to be run",
            ),
            "patient_class": SimpleItem(
                defvalue=None,
                doc="Qualified name of class to use for loading patient datasets",
            ),
            "patient_opts": SimpleItem(
                defvalue="{}",
                doc="Dictionary of options to be passed to constructor of "
                + "patient_class",
            ),
            "log_level": SimpleItem(
                defvalue="INFO", doc=" Severity level for event logging"
            ),
            "setup_script": SimpleItem(
                defvalue="",
                doc="Bash setup script to be sourced on worker node",
            ),
            "is_prepared": SimpleItem(
                defvalue=None,
                strict_sequence=0,
                visitable=1,
                copyable=1,
                hidden=1,
                typelist=[None, ShareDir],
                protected=0,
                comparable=1,
                doc="Once application is prepared, "
                "location of shared resources",
            ),
            "hash": SimpleItem(
                defvalue=None,
                typelist=[None, str],
                hidden=1,
                doc="MD5 hash for application's preparable attributes",
            ),
            "app": SimpleItem(
                defvalue=None,
                optional=1,
                typelist=None,
                doc="If not None, skrt.application.Application "
                "from which properties are initialised",
            ),
        },
    )

    _category = "applications"
    _name = "SkrtApp"
    # Make available methods implemented in base class
    _exportmethods = ["postprocess", "prepare", "unprepare"]

    def __init__(
        self,
        algs=None,
        setup_script="",
        log_level="",
        patient_class=None,
        patient_opts=None,
    ):
        """
        Create instance of SkrtApp.
        """
        super().__init__()

        if algs:
            self.algs = algs

        if patient_class:
            assert isinstance(patient_class, str)
            self.patient_class = patient_class

        if patient_opts:
            assert isinstance(patient_opts, dict)
            self.patient_opts = patient_opts

        if setup_script:
            self.setup_script = setup_script

        if log_level:
            self.log_level = log_level

    @classmethod
    def from_application(
        cls, app=None, setup_script="", patient_class=None, patient_opts=None
    ):
        """
        Create instance of SkrtApp from scikit-rt application

        **Parameters:**

        alg : skrt.application.Application/None
            Scikit-rt application from which properties are to be unpacked

        setup_script : str
            Bash setup script to be sourced on worker node

        patient_class : str, default=None
            Qualified name of class to use for loading patient datasets.

        patient_opts : dict, default=None
            Dictionary to be passed to constructor of patient_class.
        """

        if app is None:
            skrt_app = cls()
        else:
            algs = []
            for alg in app.algs:
                skrt_alg = SkrtAlg.from_algorithm(
                    alg=alg, setup_script=setup_script
                )
                algs.append(skrt_alg)
            skrt_app = cls(
                algs=algs,
                setup_script=setup_script,
                log_level=app.log_level,
                patient_class=patient_class,
                patient_opts=patient_opts or {},
            )

        return skrt_app

    def configure(self, master_appconfig):
        """
        Perform configuration that takes place after any job splitting.

        Application configuration extracts information for use by
        runtime handlers.

        **Parameter:**

        master_appconfig : any
            Data structure containing application information
            from configuration before any job splitting.
        """
        app = dict(master_appconfig)
        app["algs"] = self.algs
        app["log_level"] = self.log_level
        return (False, app)

    def master_configure(self):
        """
        Perform configuration that takes place before any job splitting.

        Application configuration extracts information for use by
        runtime handlers.
        """
        app = {
            "algs": self.algs,
            "log_level": self.log_level,
            "setup_script": self.setup_script,
            "patient_class": self.patient_class,
            "patient_opts": self.patient_opts,
        }

        return (False, app)
