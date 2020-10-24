

# * Standard Library Imports -->
import json
import pickle
import os
import enum
import configparser
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
# * Gid Imports -->
import antistasindex.utility.gidlogger_vend.logger_functions as glog
from typing import Union

# region [Logging]

log = glog.aux_logger(__name__)


# endregion[Logging]


class Get(enum.Enum):
    basic = enum.auto()
    boolean = enum.auto()
    int = enum.auto()
    list = enum.auto()
    path = enum.auto()
    datetime = enum.auto()


def pathmaker(first_segment, *in_path_segments, rev=False):
    """
    Normalizes input path or path fragments, replaces '\\\\' with '/' and combines fragments.

    Parameters
    ----------
    first_segment : str
        first path segment, if it is 'cwd' gets replaced by 'os.getcwd()'
    rev : bool, optional
        If 'True' reverts path back to Windows default, by default None

    Returns
    -------
    str
        New path from segments and normalized.
    """
    _first = os.getcwd() if first_segment == 'cwd' else first_segment
    _path = os.path.join(_first, *in_path_segments)
    _path = _path.replace('\\\\', '/')
    _path = _path.replace('\\', '/')
    if rev is True:
        _path = _path.replace('/', '\\')

    return _path.strip()


def writeit(in_file, in_data, append=False, in_encoding='utf-8'):
    """
    Writes to a file.

    Parameters
    ----------
    in_file : str
        The target file path
    in_data : str
        The data to write
    append : bool, optional
        If True appends the data to the file, by default False
    in_encoding : str, optional
        Sets the encoding, by default 'utf-8'
    """
    if isinstance(in_file, (tuple, list)):
        _file = pathmaker(*in_file)
    elif isinstance(in_file, str):
        _file = pathmaker(in_file)
    _write_type = 'w' if append is False else 'a'
    _in_data = in_data
    with open(_file, _write_type, encoding=in_encoding) as _wfile:
        _wfile.write(_in_data)


def writejson(in_object, in_file, sort_keys=True, indent=0):
    writeit(in_file, json.dumps(in_object, sort_keys=sort_keys, indent=indent))


def pickleit(obj, in_path):
    """
    saves an object as pickle file.

    Parameters
    ----------
    obj : object
        the object to save
    in_name : str
        the name to use for the pickled file
    in_dir : str
        the path to the directory to use
    """
    with open(pathmaker(in_path), 'wb') as filetopickle:
        log.debug(f"saved object [{str(obj)}] as pickle file [{in_path}]")
        pickle.dump(obj, filetopickle, pickle.HIGHEST_PROTOCOL)


class ConfigHandler(configparser.ConfigParser):
    def __init__(self, config_file=None, auto_read=True, auto_save=True, **kwargs):
        super().__init__(**kwargs)
        self.config_file = '' if config_file is None else config_file
        self.auto_read = auto_read
        self.auto_save = auto_save
        self._method_select = {Get.basic: self.get, Get.boolean: self.getboolean, Get.int: self.getint, Get.list: self.getlist, Get.path: self.get_path, Get.datetime: self.get_datetime}

        if self.auto_read is True:
            self.read(self.config_file)

    def getlist(self, section, key, delimiter=',', as_set=False):
        _raw = self.get(section, key).strip()
        if _raw.endswith(delimiter):
            _raw = _raw.rstrip(delimiter)
        if _raw.startswith(delimiter):
            _raw = _raw.lstrip(delimiter).strip()
        _out = _raw.replace(delimiter + ' ', delimiter).split(delimiter)
        if as_set is True:
            _out = set(_out)
        return _out

    def list_from_keys_only(self, section, as_set=True):
        _result = self.options(section)
        _out = []
        for line in _result:
            if line != '':
                _out.append(line)
        if as_set is True:
            _out = set(_out)
        return _out

    def get_path(self, section, key, cwd_symbol='+cwd+'):
        _raw_path = self.get(section, key)
        if cwd_symbol in _raw_path:
            _out = _raw_path.replace(cwd_symbol, os.getcwd()).replace('\\', '/')
        elif '+userdata+' in _raw_path:
            _out = _raw_path.replace('+userdata+', os.getenv('APPDATA')).replace('\\', '/')
        elif _raw_path == 'notset':
            _out = None
        else:
            _out = os.path.join(_raw_path).replace('\\', '/')
        return _out

    def _best_fuzzymatch(self, in_term, in_targets: Union[list, set, frozenset, tuple, dict]):
        # Todo: replace with process.extractOne() from fuzzywuzzy!
        _rating_list = []
        for _target in in_targets:
            _rating_list.append((_target, fuzz.ratio(in_term, _target)))
        _rating_list.sort(key=lambda x: x[1], reverse=True)
        log.debug("with a fuzzymatch, the term '%s' was best matched to '%s' with and Levenstein-distance of %s", in_term, _rating_list[0][0], _rating_list[0][1])
        return _rating_list[0][0]

    def get_timedelta(self, section, key, amount_seperator=' ', delta_seperator=','):
        _raw_timedelta = self.get(section, key)
        if _raw_timedelta != 'notset':
            _raw_timedelta_list = _raw_timedelta.split(delta_seperator)
            _arg_dict = {'days': 0,
                         'seconds': 0,
                         'microseconds': 0,
                         'milliseconds': 0,
                         'minutes': 0,
                         'hours': 0,
                         'weeks': 0}
            for raw_delta_data in _raw_timedelta_list:
                _amount, _typus = raw_delta_data.strip().split(amount_seperator)
                _key = self._best_fuzzymatch(_typus, _arg_dict)
                _arg_dict[_key] = float(_amount) if '.' in _amount else int(_amount)
            return timedelta(**_arg_dict)

    def get_datetime(self, section, key, dtformat=None):
        _dtformat = '%Y-%m-%d %H:%M:%S' if dtformat is None else format
        _date_time_string = self.get(section, key)
        if _date_time_string == "notset":
            return None
        else:
            return datetime.strptime(_date_time_string, _dtformat).astimezone()

    def set_datetime(self, section, key, datetime_object, dtformat=None):
        _dtformat = '%Y-%m-%d %H:%M:%S' if dtformat is None else format
        self.set(section, key, datetime_object.strftime(_dtformat))
        if self.auto_save is True:
            self.save()

    def enum_get(self, section: str, option: str, typus: Get = Get.basic):
        return self._method_select.get(typus, self.get)(section, option)

    def save(self):
        with open(self.config_file, 'w') as confile:
            self.write(confile)
        self.read()

    def read(self, filenames=None):
        _configfile = self.config_file if filenames is None else filenames

        super().read(_configfile)
