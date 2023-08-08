# File: GangaSkrt/Lib/CsvMerger.py
"""Provide for merging files of data in CSV format."""

from GangaCore.GPIDev.Adapters.IMerger import IMerger
from GangaCore.Utility.logging import getLogger

logger = getLogger()


class CsvMerger(IMerger):
    """Merger for files of data in CSV format."""

    _category = "postprocessor"
    _name = "CsvMerger"
    _schema = IMerger._schema.inherit_copy()

    def mergefiles(self, in_paths=None, out_path=""):
        """
        Merge files of data in CSV format.

        Parameters
        ----------
        in_paths : list, default=None
            List of paths to input files.
        out_path : str, default = ''
            Path where output file is to be created.
        """

        in_paths = in_paths or []
        if out_path:
            # Obtain sorted list of all column labels.
            all_labels = set()
            for in_path in in_paths:
                with open(in_path, encoding="utf-8") as in_file:
                    labels = in_file.readline().rstrip().split(",")
                    all_labels = all_labels.union(labels)
            all_labels = sorted(list(all_labels))
            lines = [",".join(all_labels)]

            # Obtain ordered list of values for each input line of each file,
            # taking into account that all labels may not be present.
            for in_path in in_paths:
                with open(in_path, encoding="utf-8") as in_file:
                    labels = in_file.readline().rstrip().split(",")
                    for line in in_file:
                        in_values = line.rstrip().split(",")
                        out_values = []
                        for label in all_labels:
                            if label in labels:
                                idx = labels.index(label)
                                out_values.append(in_values[idx])
                            else:
                                out_values.append("")

                        lines.append(",".join(out_values))

            # Write the merged file.
            with open(out_path, "w", encoding="utf-8") as out_file:
                out_file.write("\n".join(lines))

        else:
            logger.warning("Path to output file not defined")
