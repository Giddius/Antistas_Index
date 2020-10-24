# region [Imports]
# * Standard Library Imports -->
from collections import namedtuple

# * Gid Imports -->
import antistasindex.utility.gidlogger_vend.logger_functions as glog

# * Local Imports -->
from antistasindex.engine.config_reader import CfgSingletonProvider, get_enabled
from antistasindex.data.standard_config_data import PRINTER_CALLBOOK, BASE_STD_CALLBOOK, BASE_META_CALLBOOK
from antistasindex.engine.general_data_index import find_filter_files

# endregion[Imports]

# region [Configs]

CFG = CfgSingletonProvider.get_config()

ASFile = namedtuple('ASFile', ['name', 'directory', 'full_path'])

# endregion [Configs]

# region [Logging]

log = glog.aux_logger(__name__)


# endregion[Logging]


def index_runner():
    log.info('starting...')
    _std_list = []
    _meta_dict = {}
    std_list, meta_list, printer_list = get_enabled()
    for _file_object in find_filter_files():
        _item_dict = {}
        for action in std_list:
            _index_att_tup = BASE_STD_CALLBOOK.get(action)
            _item_dict[_index_att_tup.output_name] = _index_att_tup.function(_file_object)
        _std_list.append(_item_dict)
    log.info('finished collecting file info')
    log.info('starting collecting meta info')
    for meta_action in meta_list:
        _index_att_tup = BASE_META_CALLBOOK.get(meta_action)
        _meta_dict[_index_att_tup.output_name] = _index_att_tup.function(_std_list)
    _combined_dict = {'meta': _meta_dict, 'files': _std_list}
    log.info('finished collecting meta info')
    log.info('starting output operations')
    for printer_action in printer_list:
        _printer_function = PRINTER_CALLBOOK.get(printer_action)
        _printer_function(_combined_dict)
    log.info('...finished')
