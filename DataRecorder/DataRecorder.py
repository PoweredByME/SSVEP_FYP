"""
    This module is used to get the data from an EEG stream.
    The data can be online or offline.
    This class runs on a thread different fromt the main
    thread.

    Edit this code if you want to edit the method or source of
    recording the EEG data.

    MAIN PURPOSE:
    The main purpose of this module is to read data from the given
    source and pass is to the pipe line in form of a numpy matrix
"""
from Utils import Utils;
from Globals import Globals;
import glob;
from scipy.io import loadmat;


class DataReader_Offline(object):
    """
        This class reads all the dataset files with in the
        set dataset folder.
    """
    def __init__(self):
        self._dataPath = Globals.OFFLINE_DATA_PATH;
        self._dataSetFileType = ""
        self._dataSetFilesList = glob.glob(self._dataPath+"/*"+Globals.OFFLINE_DATASET_FILE_TYPE);

    def _openFile(self, filePath):
        x = loadmat(filePath)
        print("time_stamps");
        print(len(x["time_stamps"][0]));
        print("Fs");
        print(x["Fs"]);
        print("gender");
        print(x["gender"]);
        print("trial_time_stamps");
        print(len(x["trial_time_stamps"][0]));
        print("add_info");
        print(x["add_info"]);
        print("trial");
        print(x["trial"]);
        print("Y");
        print(len(x["Y"][0]));
        print("X");
        print(len(x["X"][111328]));

    def Print(self):
        for f in self._dataSetFilesList:
            self._openFile(f);
    

class DataReader_Online(object):
    def __init__(self):
        pass;

class DataRecorder(object):
    @Utils.thread
    def _readData(self):
        self._dataReader.Print();

    def _fillDataBuffer(self):
        pass;
    
    def _isDataBufferFull(self):
        pass;

    def __init__(self):
        self._DATA_BUFFER = None;
        self._DATA_MAX_BUFFER_TIME_SEC = Globals.DATA_MAX_BUFFER_TIME_SEC;
        self._DATA_SAMPLING_FREQ_HZ = Globals.DATA_SAMPLING_FREQ
        self._DATA_MAX_SAMPLES = int(self._DATA_MAX_BUFFER_TIME_SEC * self._DATA_SAMPLING_FREQ_HZ);
        if Globals.DATA_SOURCE == "offline":
            self._dataReader = DataReader_Offline();
        elif Globals.DATA_SOURCE == "online":
            self._dataReader = DataReader_Online();

        self._readDataThreadHandle = self._readData();






    

