# region [Imports]

import os
import sys
from gidtools.gidfiles import pathmaker, writejson, loadjson
import datetime
import re
import statistics
import hashlib
from timeit import Timer
import configparser
from configparser import ExtendedInterpolation
from checksumdir import dirhash
import gidlogger as glog
from src.engine.config_reader import CfgSingletonProvider
from functools import lru_cache
from src.utility.misc_data import SGF, SIZE_CONV
# endregion[Imports]

# region [Configs]

CFG = CfgSingletonProvider.get_config()

# endregion [Configs]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]


def _hash_exclude_output_files():
    _out_list = []
    _name = CFG.get('general', 'output_file_name')
    for _ext in CFG.getlist('fixed_lists', 'output_formats_to_use'):
        _out_list.append(_name + '.' + _ext)
    return _out_list


@lru_cache()
def get_start_dir():
    _start_dir = CFG.get('general', 'base_directory')
    if _start_dir == 'cfg_dir':
        _start_dir = pathmaker(os.path.dirname(os.getenv('AS_INDEX_CFG_FILE')))
    else:
        _start_dir = pathmaker(_start_dir)
    return _start_dir


def meta_get_number_of_files(in_list: list):
    return len(in_list)


def meta_get_index_creation_time(in_list: list):
    return datetime.datetime.now().isoformat(timespec='seconds')


def meta_get_combined_size_bytes(in_list: list):
    return sum(item.get('file_size_bytes', 0) for item in in_list)


def meta_get_combined_size_string(in_list: list):
    _unit_from_cfg = CFG.get('general', 'size_unit_combined_size')
    _factor = SIZE_CONV.get(_unit_from_cfg, {}).get('factor', 1)
    _unit = SIZE_CONV.get(_unit_from_cfg, {}).get('short_name', 'b')
    _size = meta_get_combined_size_bytes(in_list)
    _formatted_size = round(_size / _factor, ndigits=2)
    return f"{str(_formatted_size)} {_unit}"


def meta_get_overall_hash(in_list: list):
    return dirhash(get_start_dir(), 'md5', excluded_files=[os.path.basename(os.getenv('AS_INDEX_CFG_FILE'))] + _hash_exclude_output_files())


def meta_get_number_of_files_by_extension(in_list: list):
    _out_dict = {}
    for item in in_list:
        if 'extension' in item:
            _ext = item.get('extension')
        else:
            _ext = item.get('name').rsplit('.')[-1]
        if _ext not in _out_dict:
            _out_dict[_ext] = 0
        _out_dict[_ext] += 1
    return _out_dict
