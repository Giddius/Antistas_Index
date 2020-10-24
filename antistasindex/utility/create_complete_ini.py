# region [Imports]
# * Standard Library Imports -->
import os
import configparser

# * Gid Imports -->
import antistasindex.utility.gidlogger_vend.logger_functions as glog
from antistasindex.utility.misc_functions import pathmaker

# endregion[Imports]

# region [Logging]
log = glog.aux_logger(__name__)

# endregion[Logging]

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))
PROTOTYPE_CONFIG = r"""#*********************************
[general]
#*********************************
base_directory = cfg_dir
output_location = ${base_directory}/index_output
output_file_name = file_index
path_output_seperator = /
windows_problematic_name_regex = '[\\/:"*?<>|]+'
size_unit_files = kilobyte
size_unit_combined_size = megabyte
hash_algorithm = md5
printer_function_prefix = printer
update_time_interval = 1 day
update_after_push = yes
standard_attribute_function_prefix = std
meta_attribute_function_prefix = meta
; !NOT YET IMPLEMENTED!
; use_experimental = yes

#*********************************
[general_settings]
#*********************************
logging_level = debug
use_logging = True

#*********************************
[fixed_lists]
#*********************************
output_formats_to_use = json, csv, txt, excel
external = JeroenArsenal, UPSMON
exclude_folders = .git, __pycache__, sqfvalidator
exclude_files = file_index.json,
extra_std_attributes_list =
extra_meta_attributes_list =


#*********************************
[basic_attributes]
#*********************************
use_name = yes
use_extension = yes
use_basic_file_name = yes
use_relative_full_path = yes
use_relative_folder_path = yes
use_file_size_string = yes
use_file_size_bytes = yes
use_creation_time = yes
use_most_recent_modification_time = yes
use_space_in_filename = yes
use_problematic_filename_windows = yes
use_belongs_to = yes
use_file_hash = yes


#*********************************
[basic_meta_attributes]
#*********************************
use_number_of_files_by_extension = yes
use_index_creation_time = yes
use_number_of_files = yes
use_combined_size_str = yes
use_combined_size_bytes = yes
use_overall_hash = yes

; !NOT YET IMPLEMENTED!
; #*********************************
; [experimental_file_attributes]
; #*********************************
; use_match_to_function_name = yes

; !NOT YET IMPLEMENTED!
; #*********************************
; [experimental_file_attributes]
; #*********************************
; use_function_list = yes

##############################################################################################################################################################################
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##############################################################################################################################################################################
; !NOT YET IMPLEMENTED!
; #*********************************
; [std_attribute_identifier_example]
; #*********************************
; attribute_name = example_name
; file_name = example_file.py
; function = std_get_example


; #*********************************
; [meta_attribute_identifier_example]
; #*********************************
; attribute_name = example_name
; file_name = example_file.py
; function = meta_get_example


"""


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
    pass
