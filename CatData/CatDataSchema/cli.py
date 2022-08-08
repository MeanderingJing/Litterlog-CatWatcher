from os import environ
from pathlib import Path

import click

from .simple_etl import file_watcher

# click.command() decorator takes in the function test_data_watcher() and modify it so that it can be called from the command line
# Emma20220713: Path(test_data_dir) aims to join the path to get the full path (my understanding, details to be confirmed)

# CAT_DATA_DMZ = "/var/nfs/cat_watcher_output" # An NFS directory in server  # This should be added as an Environment variable at some point or defined in docker files.
@click.command()
def cat_data_watcher():
    """
    use watchdog to monitor the test data directory and fire our etl process
    """
    cat_data_dir = environ.get("CAT_DATA_DMZ", "/var/nfs/cat_watcher_output")
    file_watcher(Path(cat_data_dir))


# Entry points need to be added into setup.py in order for the command to work in terminal
@click.command()
def migrate():
    """
    run alembic migration using package alembic.ini
    """
    from pathlib import Path

    from alembic.command import upgrade
    from alembic.config import Config

    ALEMBIC_CONFIG_FILE = Path(__file__).parent / "alembic.ini"

    print("Migrating database ...")
    alembic_cfg = Config(str(ALEMBIC_CONFIG_FILE))
    alembic_cfg.set_main_option(
        "script_location", str((Path(__file__).parent / "alembic").absolute())
    )
    upgrade(alembic_cfg, "head")


#cat_data_watcher()
#migrate()
