# File: GangaSkrt/Lib/JsonMerger.py
'''Provide for merging files of data in JSON format.'''

import json

from GangaCore.GPIDev.Schema import SimpleItem
from GangaCore.GPIDev.Adapters.IMerger import IMerger
from GangaCore.Utility.logging import getLogger

logger = getLogger()


class JsonMerger(IMerger):
    '''Merger for files of data in JSON format.'''
    _category = 'postprocessor'
    _name = 'JsonMerger'
    _schema = IMerger._schema.inherit_copy()
    _schema.datadict['indent'] = SimpleItem(defvalue=1, doc='Indent level.')
    _schema.datadict['separators'] = SimpleItem(
            defvalue=(",", ":"), doc='Tuple defining '
            'separators between items, and between keys and items.')
    _schema.datadict['sort_keys'] = SimpleItem(
            defvalue=True,
            doc='Specify whether to sort keys of output dictionaries.')

    def mergefiles(self, in_paths=[], out_path=''):
        '''
        Merge files of data in JSON format.

        Parameters
        ----------
        in_paths : list, default=[]
            List of paths to input files.
        out_path : str, default = ''
            Path where output file is to be created.
        '''

        if out_path:
            json_data = []
            for in_path in in_paths:
                with open(in_path) as in_file:
                    json_data.append(json.load(in_file))

            with open(out_path, "w") as out_file:
                json.dump(json_data, out_file, indent=self.indent,
                          separators=self.separators,
                          sort_keys=self.sort_keys)
        else:
            logger.warning('Path to output file not defined')

        return None
