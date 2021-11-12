# File: GangaSkrt/Lib/CsvMerger.py
'''Provide for merging files of data in CSV format.'''

from GangaCore.GPIDev.Adapters.IMerger import IMerger
from GangaCore.Utility.logging import getLogger

logger = getLogger()

class CsvMerger(IMerger):
    '''Merger for files of data in CSV format.'''
    _category = 'postprocessor'
    _name = 'CsvMerger'
    _schema = IMerger._schema.inherit_copy()
    _schema.datadict['strip_headers'] = SimpleItem(defvalue=True,
            doc='Strip first row (header) from all files except the first.')

    def mergefiles(self, in_paths=[], out_path=''):
        '''
        Merge files of data in CSV format.

        Parameters
        ----------
        in_paths : list, default=[]
            List of paths to input files.
        out_path : str, default = ''
            Path where output file is to be created.
        '''

        if out_path:
            lines = []
            append_line = True
            for in_path in in_paths:
                with open(in_path) as in_file:
                    for line in in_file:
                        if append_line:
                            lines.append(line.rstrip())
                        append_line = True
                if self.strip_headers:
                    append_line = False

            out_string = '\n'.join(lines)
            with open(out_path, 'w') as out_file:
                out_file.write(out_string)
        else:
            logger.warning('Path to output file not defined')

        return None
