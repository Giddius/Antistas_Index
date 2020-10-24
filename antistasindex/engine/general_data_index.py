# region [Imports]

# * Standard Library Imports -->
import os
import re
import hashlib
import datetime
from functools import lru_cache
from collections import namedtuple

# * Gid Imports -->
import antistasindex.utility.gidlogger_vend.logger_functions as glog
from antistasindex.utility.misc_functions import pathmaker

# * Local Imports -->
from antistasindex.utility.misc_data import SIZE_CONV
from antistasindex.engine.config_reader import CfgSingletonProvider

# endregion[Imports]

# region [Configs]

CFG = CfgSingletonProvider.get_config()

ASFile = namedtuple('ASFile', ['name', 'directory', 'full_path'])

# endregion [Configs]

# region [Logging]

log = glog.aux_logger(__name__)


# endregion[Logging]


def _exclude_output_files():
    _out_list = []
    _name = CFG.get('general', 'output_file_name')
    for _ext in CFG.getlist('fixed_lists', 'output_formats_to_use'):
        _out_list.append(_name + '.' + _ext)
    return _out_list


def std_get_file_hash(in_file: ASFile):
    _algorithm = CFG.get('general', 'hash_algorithm')
    with open(in_file.full_path, 'rb') as binfile:
        _content = binfile.read()
    return getattr(hashlib, _algorithm)(_content).hexdigest()


@lru_cache()
def get_start_dir():
    _start_dir = CFG.get('general', 'base_directory')
    if _start_dir == 'cfg_dir':
        _start_dir = pathmaker(os.path.dirname(os.getenv('AS_INDEX_CFG_FILE')))
    else:
        _start_dir = pathmaker(_start_dir)
    return _start_dir


def std_get_filename(in_file: ASFile):
    return in_file.name


def std_get_relative_full_path(in_file: ASFile):
    return in_file.full_path.replace(get_start_dir() + '/', '')


def std_get_relative_folder_path(in_file: ASFile):
    _out = pathmaker(in_file.directory).replace(get_start_dir(), '').strip()
    if _out == '':
        _out = 'ROOT'
    else:
        _out = _out.lstrip('/')
    return _out


def std_get_file_size_bytes(in_file: ASFile):
    return os.stat(in_file.full_path).st_size


def std_get_extension(in_file: ASFile):
    return in_file.name.split('.')[-1]


def std_get_basic_file_name(in_file: ASFile):
    _out = in_file.name.rsplit('.', 1)[0]
    if _out == '':
        _out = in_file.name.rsplit('.')[-1]
    return _out.replace('.', '')


def std_get_space_in_filename(in_file: ASFile):
    return ' ' in in_file.name


def std_get_creation_time(in_file: ASFile):
    try:
        _out = datetime.datetime.fromtimestamp(os.stat(in_file.full_path).st_birthtime).isoformat(timespec='seconds')
    except AttributeError:
        _out = datetime.datetime.fromtimestamp(os.stat(in_file.full_path).st_ctime).isoformat(timespec='seconds')
    return _out


def std_get_modification_time(in_file: ASFile):
    return datetime.datetime.fromtimestamp(os.path.getmtime(in_file.full_path)).isoformat(timespec='seconds')


def std_get_problematic_name_windows(in_file: ASFile):
    _pattern = CFG.get('general', 'windows_problematic_name_regex').replace("'", "")
    _match = re.search(_pattern, in_file.name)
    return bool(_match)


def std_get_belongs_to(in_file: ASFile):
    _out = 'Antistasi'
    _external_list = CFG.getlist('fixed_lists', 'external')
    for _extern in _external_list:
        if _extern.casefold() in in_file.directory.casefold() or _extern.casefold() in in_file.name.casefold():
            _out = _extern
    return _out


def std_get_file_size_string(in_file: ASFile):
    _unit_from_cfg = CFG.get('general', 'size_unit_files')
    _factor = SIZE_CONV.get(_unit_from_cfg, {}).get('factor', 1)
    _unit = SIZE_CONV.get(_unit_from_cfg, {}).get('short_name', 'b')
    _size = os.stat(in_file.full_path).st_size
    _formatted_size = round(_size / _factor, ndigits=2)
    return f"{str(_formatted_size)} {_unit}"


def find_filter_files():
    _start_dir = get_start_dir()
    log.info('starting file search in %s', _start_dir)
    _exclude_folder = CFG.getlist('fixed_lists', 'exclude_folders')
    _exclude_files = CFG.getlist('fixed_lists', 'exclude_files')
    for dirname, folderlist, filelist in os.walk(_start_dir):
        if all(_ex_folder not in pathmaker(dirname).split('/') for _ex_folder in _exclude_folder):
            for _file in filelist:
                if _file not in _exclude_files and _file.casefold() != os.path.basename(os.getenv('AS_INDEX_CFG_FILE')).casefold() and _file not in _exclude_output_files():
                    log.info('examining file "%s"', _file)
                    yield ASFile(_file, pathmaker(dirname), pathmaker(dirname, _file))


if __name__ == '__main__':
    pass
