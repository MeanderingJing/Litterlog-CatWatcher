import logging

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
        data = extract_test_data(filepath, pipeline_run_id)
        tpd = transform_test_data(data, pipeline_run_id)
        load_test_data(tpd, pipeline_run_id)
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


def extract_test_data(filepath: Path, pipeline_run_id: uuid.UUID) -> str:
    """
    Extract

    :Param filepath: A network-file-system(nfs) path containing data created from kernels-automated-test-system (kats)

    Returns file contents from read (str)
    """
    LOGGER.info(
        f"ETL pipeline {pipeline_run_id} - Extracting contents of test file {filepath}"
    )
    file_contents = ""
    with filepath.open("r") as f:
        file_contents = f.read()
    return file_contents


def transform_test_data(
    data: str, pipeline_run_id: uuid.UUID
) -> Tuple[TestPlanData, List[Tuple[str, str]]]:
    """
    Convert string to

    :Param data: string with cat bathroom data to transform

    Returns
    Tuple[TestPlanData, List[Tuple[str, str]]]
    """
    LOGGER.info(
        f"ETL pipeline {pipeline_run_id} - Transforming json data into TestPlanData"
    )
    return TestPlanData.from_json(data)
