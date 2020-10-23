

# region [Imports]

# * Standard Library Imports -->
import os
from configparser import ExtendedInterpolation

# * Gid Imports -->
import src.utility.gidlogger_vend.logger_functions as glog
from src.utility.misc_functions import pathmaker, ConfigHandler

# endregion[Imports]


# region [Logging]

log = glog.aux_logger(__name__)


# endregion[Logging]

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


class CfgSingletonProvider:
    cfg_object = None

    @classmethod
    def get_config(cls):
        if os.getenv('AS_INDEX_CFG_FILE') is not None:
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
        else:
            raise EnvironmentError('config path is not set')

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
