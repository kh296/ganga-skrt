# File: GangaSkrt/Lib/SkrtAlg/SkrtAlg.py

"""
Define SkrtAlg application.
"""

from GangaCore.Utility.Config import config_scope
from GangaCore.Utility import logging
from GangaCore.GPIDev.Lib.File import ShareDir
from GangaCore.GPIDev.Schema import Schema, SimpleItem, Version
from GangaCore.GPIDev.Adapters.IPrepareApp import IPrepareApp

logger = logging.getLogger()


class SkrtAlg(IPrepareApp):
    """
    Represent scikit-rt algorithm as Ganga application.

    For information about Ganga applications, see documentation of
    GangaCore.GPIDev.Adapters.IApplication.IApplication.
    """

    _schema = Schema(
        Version(1, 0),
        {
            "alg_class": SimpleItem(
                defvalue="",
                doc="Name of scikit-rt algorithm class to be instantiated",
            ),
            "alg_module": SimpleItem(
                defvalue="",
                doc="Path to module containing scikit-rt algorithm class",
            ),
            "alg_name": SimpleItem(
                defvalue="",
                doc="Name to be associated with algorithm instantiation",
            ),
            "opts": SimpleItem(
                defvalue={},
                doc="Dictionary of options to be passed "
                + "to algorithm constructor",
            ),
            "patient_class": SimpleItem(
                defvalue=None,
                doc="Qualified name of class to use for loading patient datasets\n"
                + "(ignored if SkrtAlg is passed in list to SkrtApp)",
            ),
            "patient_opts": SimpleItem(
                defvalue="{}",
                doc="Dictionary of options to be passed to constructor of "
                + "patient_class\n"
                + "(ignored if SkrtAlg is passed in list to SkrtApp)",
            ),
            "log_level": SimpleItem(
                defvalue="INFO", doc=" Severity level for event logging"
            ),
            "setup_script": SimpleItem(
                defvalue="",
                doc="Bash setup script to be sourced on worker node\n"
                + "(ignored if SkrtAlg is passed in list to SkrtApp)",
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
        },
    )

    _category = "applications"
    _name = "SkrtAlg"
    # Make available methods implemented in base class
    _exportmethods = ["postprocess", "prepare", "unprepare"]

    def __init__(
        self,
        alg_class="",
        alg_module="",
        alg_name="",
        opts=None,
        log_level="",
        setup_script="",
        patient_class=None,
        patient_opts=None,
    ):
        """
        Create instance of SkrtAlg.

        Parameters in the function declaration correspond to schema items.
        Type checking is performed for parameter values.

        **Parameters:**

        alg_class : str, default=''
            Name of scikit-rt  algorithm class to be instantiated.

        alg_module : str, default=''
            Path to module containing scikit-rt algorithm class.

        alg_name : str, default=''
            Name to be associated with algorithm instantiation.

        opts : dict, default=None
            Dictionary of options to be passed to algorithm constructor.

        patient_class : str, default=None
            Qualified name of class to use for loading patient datasets;
            ignored if SkrtAlg is passed in list to SkrtApp.

        patient_opts : dict, default=None
            Dictionary to be passed to constructor of patient_class;
            ignored if SkrtAlg is passed in list to SkrtApp.

        log_level : str, default=''
            Severity level for event logging.  Allowed values are:
            'NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.

        setup_script : str, default=''
            Bash setup script to be sourced on worker node;
            ignored if SkrtAlg is passed in list to SkrtApp.
        """
        super().__init__()

        if alg_class:
            assert isinstance(alg_class, str)
            self.alg_class = alg_class

        if alg_module:
            assert isinstance(alg_module, str)
            self.alg_module = alg_module

        if alg_name:
            assert isinstance(alg_name, str)
            self.alg_name = alg_name

        if opts:
            assert isinstance(opts, dict)
            self.opts = opts

        if patient_class:
            assert isinstance(patient_class, str)
            self.patient_class = patient_class

        if patient_opts:
            assert isinstance(patient_opts, dict)
            self.patient_opts = patient_opts

        log_levels = ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if log_level:
            assert log_level in log_levels
            self.log_level = log_level

        if setup_script:
            assert isinstance(setup_script, str)
            self.setup_script = setup_script

    @classmethod
    def from_algorithm(
        cls, alg=None, setup_script="", patient_class=None, patient_opts=None
    ):
        """
        Create instance of SkrtAlg from scikit-rt algorithm

        **Parameters:**

        alg : skrt.application.Algorithm/None
            Scikit-rt algorithm from which properties are to be unpacked

        setup_script : str
            Bash setup script to be sourced on worker node;
            ignored if SkrtAlg is passed in list to SkrtApp

        patient_class : str, default=None
            Qualified name of class to use for loading patient datasets;
            ignored if SkrtAlg is passed in list to SkrtApp

        patient_opts : dict, default=None
            Dictionary to be passed to constructor of patient_class;
            ignored if SkrtAlg is passed in list to SkrtApp
        """

        if alg is None:
            skrt_alg = cls()
        else:
            alg_class = type(alg).__name__
            alg_module = alg.alg_module
            alg_name = alg.name
            opts = alg.opts
            log_level = alg.log_level
            skrt_alg = cls(
                alg_class=alg_class,
                alg_module=alg_module,
                alg_name=alg_name,
                opts=opts,
                log_level=log_level,
                setup_script=setup_script,
                patient_class=patient_class,
                patient_opts=patient_opts or {},
            )

        return skrt_alg

    def __repr__(self):
        """
        Return string representation of SkrtAlg instance.
        """
        args = [
            f"alg_class = '{self.alg_class}'",
            f"alg_module = '{self.alg_module}'",
            f"alg_name = '{self.alg_name}'",
            f"opts = {str(self.opts)}",
            f"patient_class = '{self.patient_class}'",
            f"patient_opts = {str(self.patient_opts)}",
            f"log_level = {str(self.log_level)}",
            f"setup_script = '{self.setup_script}'",
        ]
        args_string = ", ".join(args)

        alg_repr = f"SkrtAlg({args_string})"

        return alg_repr

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
        app["opts"] = self.opts
        app["log_level"] = self.log_level

        return (False, app)

    def master_configure(self):
        """
        Perform configuration that takes place before any job splitting.

        Application configuration extracts information for use by
        runtime handlers.
        """

        app = {
            "alg_class": self.alg_class,
            "alg_module": self.alg_module,
            "alg_name": self.alg_name,
            "opts": self.opts,
            "patient_class": self.patient_class,
            "patient_opts": self.patient_opts,
            "log_level": self.log_level,
            "setup_script": self.setup_script,
        }

        return (False, app)


# Add SkrtAlg to configuration scope
# (necessary to read in SkrtAlg from XML repository)
config_scope["SkrtAlg"] = SkrtAlg
