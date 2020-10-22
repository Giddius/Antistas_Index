# region [Imports]
import gidlogger as glog
import configparser
from gidtools.gidfiles import pathmaker, writejson, loadjson, readit, writeit, writebin, readbin, appendwriteit, linereadit, QuickFile, clearit
import os
from pprint import pprint, pformat
from src.data.standard_config_data import PROTOTYPE_CONFIG
# endregion[Imports]

# region [Logging]
log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))
# endregion[Logging]

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


def provide_prototype_config(in_path):
    with open(pathmaker(in_path, 'as_index.ini'), 'w') as protocfg:
        protocfg.write(PROTOTYPE_CONFIG)


def load_cfg_file_to_dict(filename):
    _out_dict = {'DEFAULT': {}}
    cfg = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    cfg.read(filename)
    for key, value in cfg.items('DEFAULT'):
        _out_dict['DEFAULT'][key] = value
    for _section in cfg.sections():
        _out_dict[_section] = {}
        for key, value in cfg.items(_section):
            if key not in _out_dict['DEFAULT']:
                _out_dict[_section][key] = value
    return _out_dict


if __name__ == '__main__':
    clearit(r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antistas_Index\src\data\standard_config_data.py")
    FILE = 'exp.ini'
    x = load_cfg_file_to_dict(FILE)
    for key in x:
        appendwriteit(r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antistas_Index\src\data\standard_config_data.py", f"{key} = {pformat(x.get(key))}\n\n")
