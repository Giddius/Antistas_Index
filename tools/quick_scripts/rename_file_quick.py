import os
import shutil
from gidtools.gidfiles import pathmaker


PROJECT_NAME = "Antistasi_Index"


def rename_persisting_placeholders(start_dir=None):
    start_dir = pathmaker(start_dir) if start_dir is not None else "../../."
    for dirname, folderlist, filelist in os.walk(start_dir):
        for _file in filelist:
            if '$XC$' in _file:
                _old_name = pathmaker(dirname, _file)
                _new_name = _old_name.replace('$XC$', PROJECT_NAME)
                os.rename(_old_name, _new_name)
                print(f"renamed file '{_old_name}' to --> '{_new_name}'")
        for _folder in folderlist:
            if '$XC$' in _folder:
                _old_name = pathmaker(dirname, _folder)
                _new_name = _old_name.replace('$XC$', PROJECT_NAME)
                os.rename(_old_name, _new_name)
                print(f"renamed folder '{_old_name}' to --> '{_new_name}'")


if __name__ == '__main__':
    pass
