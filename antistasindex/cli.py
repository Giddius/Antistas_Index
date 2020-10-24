# region [Imports]
import antistasindex.utility.gidlogger_vend.logger_functions as glog
from antistasindex.utility.misc_functions import pathmaker
import os
import click
# endregion[Imports]

__updated__ = '2020-10-24 20:11:50'

# region [Logging]
log = glog.main_logger_stdout('debug')
# endregion[Logging]

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


@click.command(name='Get Full Config Example',)
@click.argument('output_location')
def create_configuration(output_location):
    from antistasindex.utility.create_complete_ini import provide_prototype_config
    if os.path.exists(pathmaker(output_location)):
        provide_prototype_config(pathmaker(output_location))
    else:
        raise FileNotFoundError(f'output_location "{pathmaker(output_location)}", does not exist')


@click.command(name='Start indexing')
@click.argument('config_file')
def index_files(config_file):
    os.environ["AS_INDEX_CFG_FILE"] = pathmaker(config_file)
    from antistasindex.engine.main_indexer import index_runner
    index_runner()
