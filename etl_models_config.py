import logging
from pathlib import Path
from collections import OrderedDict
from typing import List
import uuid
import csv
from datetime import datetime

# Temp here for testing to create the table in the database with
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Float, Integer, Date

# from .config import DATABASE_URL

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
# temp removal, permission issue
# file_handler = logging.FileHandler(filename="/var/log/ETL.log")
# file_handler.setLevel(logging.INFO)
# file_handler.setFormatter(formatter)
# LOGGER.addHandler(file_handler)

Base = declarative_base()

# Temperarily move here
# Create CatData class with table name cat_data. This is the table name that will show up in Postges.
class CatData(Base):
    __tablename__ = "cat_data"
    # __table__args__ = {"schema":"cat_tech_database"}  I saw this line here: https://www.youtube.com/watch?v=oNky1SUC5Ak
    Id = Column(Integer, primary_key=True)
    Datetime = Column(Date)  # May change the column name to Date in the csv later
    Entry = Column(DateTime)
    Depart = Column(DateTime)
    Duration = Column(Float)


# Temp solution here for testing
DATABASE_URL = (
    "postgresql+psycopg2://emma_dev:emma_dev@192.168.1.157:5432/cat_tech_database"
)

cat_schema_engine = create_engine(DATABASE_URL)
# Create the table defined by our mapped class
Base.metadata.create_all(cat_schema_engine)  # added


def pipeline_data(filepath: Path, cat_schema_engine):
    """
    Our extract-transform-load process(ETL)

    :param filepath: A network-file-system(nfs) path containing data created from CatWatcher
    """
    pipeline_run_id = uuid.uuid4()
    LOGGER.info(f"Starting ETL pipeline {pipeline_run_id} for file {filepath}")

    try:
        extract_test_data(filepath, pipeline_run_id)  # Place holder
        cat_data = transform_test_data(filepath, pipeline_run_id)
        load_test_data(cat_data, pipeline_run_id, cat_schema_engine)
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
    # if clean_on_success:
    #    LOGGER.info(f"ETL pipeline {pipeline_run_id} removing file {filepath}")
    #    filepath.unlink(True)
    LOGGER.info(f"ETL pipeline {pipeline_run_id} complete")


def extract_test_data(filepath: Path, pipeline_run_id: uuid.UUID) -> csv.DictReader:
    """
    Extract

    pass for now
    """
    LOGGER.info(
        f"ETL pipeline {pipeline_run_id} - Extracting contents of file {filepath}"
    )
    return filepath


def transform_test_data(filepath: Path, pipeline_run_id: uuid.UUID) -> list:
    """
    Place holder. We don't need to transform our data at the moment

    :Param data: string with cat bathroom data to transform

    Returns

    """
    LOGGER.info(f"ETL pipeline {pipeline_run_id} - Transforming csv data into CatData.")
    with open(filepath, encoding="utf-8") as csv_file:
        # DictReader returns each row as an ordered dictionary with key names from the header row.
        # https://www.andrewvillazon.com/move-data-to-db-with-sqlalchemy/
        # python3.6 make this row OrderedDict
        cat_data_csv_reader = csv.DictReader(csv_file, quotechar='"')
        cat_data = [_from_orderedDict(row) for row in cat_data_csv_reader]
    return cat_data


def _from_orderedDict(row: OrderedDict) -> CatData:
    """
    Change data type to the ones that are defined in the models.py

    """
    # Change OrderedDict to dict
    row = dict(row)
    # Entry and Depart in the raw data need to be converted to datetime type
    row["Entry"] = datetime.fromtimestamp(float(row["Entry"]))
    row["Depart"] = datetime.fromtimestamp(float(row["Depart"]))
    return CatData(**row)


def load_test_data(
    cat_data: List[CatData],
    pipeline_run_id: uuid.UUID,
    cat_schema_engine,
):
    """
    Load cat_data into database at DATABASE_URL

    Parameters
    """
    LOGGER.info(f"ETL pipeline {pipeline_run_id} - Loading CatData to database")

    LOGGER.info(f"ETL pipeline {pipeline_run_id} - Beginning database session")

    Session = sessionmaker(bind=cat_schema_engine)
    s = Session()
    s.add_all(cat_data)
    s.commit()
    s.close()
    # Close the engine
    cat_schema_engine.dispose()

    LOGGER.info(f"ETL pipeline {pipeline_run_id} - Loading cat_data complete")


filepath = "/home/emma_dev22/CatWatcher/output/Atty20220719"  # to modify
pipeline_data(filepath, cat_schema_engine)
