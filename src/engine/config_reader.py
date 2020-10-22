

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
from gidtools.gidconfig import ConfigHandler, Get
import gidlogger as glog

# endregion[Imports]


# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

if len(sys.argv) > 1:
    os.environ["AS_INDEX_CFG_FILE"] = sys.argv[1].replace('\\\\', '/').replace('\\', '/')
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


class CfgSingletonProvider:
    cfg_object = None

    @classmethod
    def get_config(cls):
        if cls.cfg_object is None:
            try:
                _cfg = ConfigHandler(config_file=pathmaker(os.getenv('AS_INDEX_CFG_FILE')), interpolation=ExtendedInterpolation())
            except Exception as error:
                log.error("Error while trying to create configreader from provided stdin filepath, error: %s", error)
                log.error('Trying again with standard config')
                _old_cwd = os.getcwd()
                os.chdir(THIS_FILE_DIR)
                _cfg = ConfigHandler(config_file=pathmaker(r"..\src\data\exp.ini"), interpolation=ExtendedInterpolation())
                os.chdir(_old_cwd)
            cls.cfg_object = _cfg

        return cls.cfg_object


def get_enabled():
    _std_enabled_list = []
    _meta_enabled_list = []
    CFG = CfgSingletonProvider.get_config()
    for key in CFG.options('basic_attributes'):
        if CFG.getboolean('basic_attributes', key) is True:
            _std_enabled_list.append(key)
    for key in CFG.options('basic_meta_attributes'):
        if CFG.getboolean('basic_meta_attributes', key) is True:
            _meta_enabled_list.append(key)
    _enabled_printer_list = CFG.getlist('fixed_lists', 'output_formats_to_use')
    return _std_enabled_list, _meta_enabled_list, _enabled_printer_list


if __name__ == '__main__':
    pass
