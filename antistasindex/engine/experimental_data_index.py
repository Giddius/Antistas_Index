# region [Imports]

# * Standard Library Imports -->
import os
import datetime
from functools import lru_cache

# * Third Party Imports -->
from checksumdir import dirhash
import armaclass

# * Gid Imports -->
import antistasindex.utility.gidlogger_vend.logger_functions as glog
from antistasindex.utility.misc_functions import pathmaker

# * Local Imports -->
from antistasindex.utility.misc_data import SIZE_CONV
from antistasindex.engine.config_reader import CfgSingletonProvider
from antistasindex.engine.meta_data_index import get_start_dir
# endregion[Imports]

# region [Configs]

CFG = CfgSingletonProvider.get_config()

# endregion [Configs]

# region [Logging]

log = glog.aux_logger(__name__)


# endregion[Logging]

def find_function_hpps():
    _out_dict = {}
    _start_dir = get_start_dir()
    _spec_index = 0
    for dirname, folderlist, filelist in os.walk(_start_dir):
        for _file in filelist:
            if _file == "functions.hpp":
                _out_dict[_spec_index] = pathmaker(dirname, _file)
                _spec_index += 1
    return _out_dict


def parse_functions_hpps(in_functions_hpps: dict):
    _out_dict = {}
    for key, value in in_functions_hpps.items():
        with open(value, 'r') as fun_hpp_file:
            _content = fun_hpp_file.read()

        for _prefix, _value1 in armaclass.parse(_content).items():
            _out_dict[_prefix] = []
            for not_wanted_key, _value2 in _value1.items():
                for _function_name in _value2:
                    _out_dict[_prefix].append(_function_name)
