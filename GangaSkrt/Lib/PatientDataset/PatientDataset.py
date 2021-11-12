# File: GangaSkrt/Liib/PatientDataset.py
'''Represent patient dataset'''

import os

from GangaCore.Utility.files import fullpath
from GangaCore.GPIDev.Schema import Schema, SimpleItem, Version
from GangaCore.GPIDev.Lib.File import FileBuffer
from GangaCore.GPIDev.Lib.Dataset import Dataset


class PatientDataset(Dataset):
    '''
    Representation of patient dataset.
    '''
    _schema = Schema(Version(1, 0), {
        'paths': SimpleItem(defvalue=[],
                            doc='List of paths to patient data'),
    })
    _category = 'datasets'
    _name = 'PatientDataset'

    _exportmethods = ['write_paths_to_file', 'write_paths_to_file_buffer']

    def __init__(self):
        '''
        Create instance of PatientDataset.
        '''
        super(PatientDataset, self).__init__()

    def convert_paths(self):
        '''
        Convert dataset's list of paths to string representation.
        '''
        out_lines = ['paths = \\', '    [']

        for path in self.paths:
            out_lines.append(f'    "{path}",')
        out_lines.append('    ]')

        out_string = '\n'.join(out_lines)
        return out_string

    def write_paths_to_file_buffer(self, buffer_name='patient_data.py',
                                   buffer_subdir=os.curdir):
        '''
        Create list of data paths, and return via FileBuffer object.

        Parameters
        ----------
        buffer_name : str, default='patient_data.py'
            Name of file that may be created from FileBuffer object.
        buffer_subdir: str, default=os.curdir
            Subdirectory for creating file from FileBuffer object.
        '''
        out_buffer = FileBuffer(
            buffer_name, self.convert_paths(), buffer_subdir)

        return out_buffer

    def write_paths_to_file(self, out_path='patient_data.py'):
        '''
        Write importable list of data paths.

        Return True if output file written, or False otherwise.

        Parameter
        ---------
        out_path : str, default='patient_data.py'
            Path where output file is to be written.
        '''

        out_ok = True
        out_path_full = fullpath(out_path)
        out_dir = os.path.dirname(out_path_full)

        if os.path.isdir(out_dir):
            out_string = self.convert_paths()
            out_file = open(out_path_full, 'w')
            out_file.write(out_string)
            out_file.close()
        else:
            out_ok = False

        return out_ok
