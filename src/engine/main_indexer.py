# region [Imports]
from pprint import pprint
import os
import sys
sys.argv.append(r"D:\Dropbox\hobby\Modding\Programs\Github\Foreign_Repos\A3-Antistasi\as_index.ini")
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
from src.engine.config_reader import CfgSingletonProvider, get_enabled
from functools import lru_cache
from collections import namedtuple
from src.data.standard_config_data import PRINTER_CALLBOOK, BASE_META_CALLBOOK, BASE_STD_CALLBOOK
from src.engine.general_data_index import find_filter_files
# endregion[Imports]

# region [Configs]

CFG = CfgSingletonProvider.get_config()

ASFile = namedtuple('ASFile', ['name', 'directory', 'full_path'])

# endregion [Configs]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]


def index_runner():
    _std_list = []
    _meta_dict = {}
    std_list, meta_list, printer_list = get_enabled()
    for _file_object in find_filter_files():
        _item_dict = {}
        for action in std_list:
            _index_att_tup = BASE_STD_CALLBOOK.get(action)
            _item_dict[_index_att_tup.output_name] = _index_att_tup.function(_file_object)
        _std_list.append(_item_dict)
    for meta_action in meta_list:
        _index_att_tup = BASE_META_CALLBOOK.get(meta_action)
        _meta_dict[_index_att_tup.output_name] = _index_att_tup.function(_std_list)
    _combined_dict = {'meta': _meta_dict, 'files': _std_list}
    for printer_action in printer_list:
        _printer_function = PRINTER_CALLBOOK.get(printer_action)
        _printer_function(_combined_dict)


if __name__ == '__main__':
    index_runner()
