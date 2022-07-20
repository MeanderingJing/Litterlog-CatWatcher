import logging
from pathlib import Path
import uuid
import pandas as pd
from .config import DATABASE_URL

filepath = "/home/emma_dev22/CatWatcher/output/{username}"  # to modify

LOGGER = logging.getLogger("ETL")
LOGGER.setLevel(logging.INFO)

LOGGER.propagate = False
# create formatter
formatter = logging.Formatter("%(asctime)s :%(levelname)s: %(message)s")


# output on stdout
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)


# add formatter to stream_handler
stream_handler.setFormatter(formatter)
LOGGER.addHandler(stream_handler)

# also try to output to log file (may consider try and except later like kernel.test.schema)
file_handler = logging.FileHandler(filename="/var/log/ETL.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

LOGGER.addHandler(file_handler)


def pipeline_data(filepath: Path):
    """
    Our extract-transform-load process(ETL)

    :param filepath: A network-file-system(nfs) path containing data created from CatWatcher
    """
    pipeline_run_id = uuid.uuid4()
    LOGGER.info(f"Starting ETL pipeline {pipeline_run_id} for file {filepath}")

    try:
        cat_data = extract_test_data(filepath, pipeline_run_id)
        transform_test_data(cat_data, pipeline_run_id)  # Place holder
        load_test_data(cat_data, pipeline_run_id)
    except sqlalchemy.exc.IntegrityError as e:
        LOGGER.error(f"ETL pipeline {pipeline_run_id} Encountered IntegrityError {e}")
        if "duplicate key value violates unique constraint" in str(e):
            LOGGER.info(
                f"ETL pipeline {pipeline_run_id} Duplicate key detected, removing file {filepath}"
            )
            filepath.unlink(True)
    except Exception as e:
        LOGGER.error(
            f"ETL pipeline {pipeline_run_id} encountered an error, aborting - {e}"
        )
        return
    if clean_on_success:
        LOGGER.info(f"ETL pipeline {pipeline_run_id} removing file {filepath}")
        filepath.unlink(True)
    LOGGER.info(f"ETL pipeline {pipeline_run_id} complete")


def extract_test_data(filepath: Path, pipeline_run_id: uuid.UUID) -> pd.DataFrame:
    """
    Extract

    :Param filepath: A network-file-system(nfs) path containing data created from CatWatcher

    Returns file contents from read (pd.core.frame.DataFrame)
    """
    LOGGER.info(
        f"ETL pipeline {pipeline_run_id} - Extracting contents of test file {filepath}"
    )
    cat_data = pd.read_csv(filepath)
    return cat_data


def transform_test_data(cat_data: str, pipeline_run_id: uuid.UUID) -> pd.DataFrame:
    """
    Place holder. We don't need to transform our data at the moment

    :Param data: string with cat bathroom data to transform

    Returns

    """
    LOGGER.info(
        f"ETL pipeline {pipeline_run_id} - Transforming json data into TestPlanData"
    )
    pass


def load_test_data(cat_data: pd.DataFrame, pipeline_run_id: uuid.UUID):
    """
    Load cat_data into database at DATABASE_URL

    Parameters
    """
    LOGGER.info(f"ETL pipeline {pipeline_run_id} - Loading TestPlanData to database")
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import (
        create_engine,
    )

    cat_schema_engine = create_engine(DATABASE_URL)

    LOGGER.info(f"ETL pipeline {pipeline_run_id} - Beginning database session")
    try:
        cat_data.to_sql(
            "csv", cat_schema_engine, if_exists="append", index=False
        )  # to understand the detail
    except:
        print("Some error has occured")
    finally:
        # Close the engine
        cat_schema_engine.dispose()
    LOGGER.info(f"ETL pipeline {pipeline_run_id} - Loading cat_data complete")
