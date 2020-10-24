
# region [Imports]

# * Standard Library Imports -->
from collections import namedtuple

# * Local Imports -->
from antistasindex.engine.printers import printer_csv_file, printer_pkl_file, printer_txt_file, printer_json_file, printer_excel_file
from antistasindex.engine.meta_data_index import (meta_get_overall_hash, meta_get_number_of_files, meta_get_combined_size_bytes,
                                                  meta_get_index_creation_time, meta_get_combined_size_string, meta_get_number_of_files_by_extension)
from antistasindex.engine.general_data_index import (std_get_filename, std_get_extension, std_get_file_hash, std_get_belongs_to, std_get_creation_time,
                                                     std_get_basic_file_name, std_get_file_size_bytes, std_get_file_size_string,
                                                     std_get_modification_time, std_get_space_in_filename, std_get_relative_full_path,
                                                     std_get_relative_folder_path, std_get_problematic_name_windows)

# endregion[Imports]


IndexAttribute = namedtuple('IndexAttribute', ['output_name', 'function'])

BASE_STD_CALLBOOK = {
    'use_name': IndexAttribute('name', std_get_filename),
    'use_extension': IndexAttribute('extension', std_get_extension),
    'use_basic_file_name': IndexAttribute('basic_file_name', std_get_basic_file_name),
    'use_relative_full_path': IndexAttribute('relative_full_path', std_get_relative_full_path),
    'use_relative_folder_path': IndexAttribute('relative_folder_path', std_get_relative_folder_path),
    'use_file_size_string': IndexAttribute('file_size_formatted', std_get_file_size_string),
    'use_file_size_bytes': IndexAttribute('file_size_bytes', std_get_file_size_bytes),
    'use_creation_time': IndexAttribute('creation_time', std_get_creation_time),
    'use_most_recent_modification_time': IndexAttribute('most_recent_modification_time', std_get_modification_time),
    'use_space_in_filename': IndexAttribute('has_space_in_filename', std_get_space_in_filename),
    'use_problematic_filename_windows': IndexAttribute('has_problematic_filename_for_windows', std_get_problematic_name_windows),
    'use_belongs_to': IndexAttribute('belongs_to', std_get_belongs_to),
    'use_file_hash': IndexAttribute('file_hash', std_get_file_hash),
}

BASE_META_CALLBOOK = {
    'use_number_of_files_by_extension': IndexAttribute('amount_of_files_per_extension', meta_get_number_of_files_by_extension),
    'use_index_creation_time': IndexAttribute('index_creation_time', meta_get_index_creation_time),
    'use_number_of_files': IndexAttribute('general_amount_of_files', meta_get_number_of_files),
    'use_combined_size_str': IndexAttribute('combined_size_formated', meta_get_combined_size_string),
    'use_combined_size_bytes': IndexAttribute('combined_size_bytes', meta_get_combined_size_bytes),
    'use_overall_hash': IndexAttribute('overall_hash', meta_get_overall_hash),
}

PRINTER_CALLBOOK = {'json': printer_json_file,
                    'csv': printer_csv_file,
                    'excel': printer_excel_file,
                    'txt': printer_txt_file,
                    'pkl': printer_pkl_file}


if __name__ == '__main__':
    pass
