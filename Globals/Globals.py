"""
    This script contains all the globals variables
    which are used in the code.

    Most of the variables are settings upon which the
    code works.
"""

DATA_SOURCE = "offline";            # can be either "offline" or "online".
DATA_SAMPLING_FREQ = 256.0;         # the sampling rate of the recorded EEG.
DATA_MAX_BUFFER_TIME_SEC = 0.5;     # The time in seconds for which the data is stored in the buffer.

OFFLINE_DATA_PATH = "DataSets/SRC";
OFFLINE_DATASET_FILE_TYPE = ".mat";