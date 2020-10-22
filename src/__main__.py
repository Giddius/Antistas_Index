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
import logging
from src.engine.config_reader import CfgSingletonProvider
# endregion[Imports]

# region [Configs]

CFG = CfgSingletonProvider.get_config()

# endregion [Configs]

# region [Logging]

_log_file = glog.log_folderer('__main__')
log = glog.main_logger(_log_file, CFG.get('general_settings', 'logging_level'))
log.info(glog.NEWRUN())
if CFG.getboolean('general_settings', 'use_logging') is False:
    logging.disable(logging.CRITICAL)

# endregion[Logging]
