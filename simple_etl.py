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

