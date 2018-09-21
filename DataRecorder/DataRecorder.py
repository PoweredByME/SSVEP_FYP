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
import numpy as np;


class DataReader_Offline(object):
    """
        This class reads all the dataset files with in the
        set dataset folder.

        Change the code in this class to cater for the different datasets.

        Note: 
            The class must have the function getSample which returns a tuple
            containing index of the sample, samples in form of array of all the channels,
            target frequency and total length of the dataset.
    """
    def __init__(self):
        self._dataPath = Globals.OFFLINE_DATA_PATH;
        self._dataSetFileType = ""
        self._dataSetFilesList = glob.glob(self._dataPath+"/*"+Globals.OFFLINE_DATASET_FILE_TYPE);

    def _openFile(self, filePath):
        x = loadmat(filePath)
        if Globals.SHOW_DATA_WHEN_FILE_OPENED:
            Utils.Print(str(x));
        return x;

    def _largest_within_delta(self,X, k, delta):
        right_idx = X.searchsorted(k,'right')-1
        if (k - X[right_idx]) <= delta:
            return right_idx
        else:
            return None

    
    '''def getSample(self):
        #    This function yields samples of the EEG data.
        for file in self._dataSetFilesList:
            data = self._openFile(file);
            for i in range(len(data["X"])):
                sample = data["X"][i];
                if i < data["trial"][0][0]:
                    targetFreq = 0.0;
                else:
                    idx = self._largest_within_delta(data["trial"][0], i, 100000000);
                    targetFreq = data["Y"][0][idx];
                yield (i,sample, targetFreq, len(data["X"]));
        yield (None,None, None, None);'''

    def getSample(self):
        #   This function yields samples of the EEG data.
        for file in self._dataSetFilesList:
            data = self._openFile(file);
            for i in range(len(data["Data"][0][0][0])):
                sample = data["Data"][0][0][0][i];
                targetFreq = 0.0;
                yield (i,sample, targetFreq, len(data["Data"][0][0][0]));
        yield (None,None, None, None);
############################################################################################


class DataReader_Online(object):
    '''
        This class read the data from an online source.
        Such as an EEG device connected to it.
    '''
    def __init__(self):
        pass;
############################################################################################


class DataRecorder(object):
    @Utils.thread
    def _readData(self):
        sampleGenerator = self._dataReader.getSample();
        while True:
            if self._isDataBufferFull():
                continue;
            (counter, sample, targetFreq, totalSamples) = next(sampleGenerator);
            if targetFreq is None and sample is None and counter is None:
                Utils.Print("The data stream has ended");
                self._dataEnded = True;
                return;
            self._fillDataBuffer((counter, sample, targetFreq, totalSamples));

    def _fillDataBuffer(self, sample):
        self._DATA_BUFFER.append(sample);
    
    def _isDataBufferFull(self):
        if len(self._DATA_BUFFER) >= self._DATA_MAX_SAMPLES - 1:
            return True;
        return False;

    def _emptyBuffer(self):
        self._DATA_BUFFER = [];

    def endOfData(self):
        return self._dataEnded;

    def getData(self):
        if self._isDataBufferFull():
            (count, sample, targetFreq, totalSamples) = self._DATA_BUFFER[0];
            buffer = np.zeros((self._DATA_MAX_SAMPLES - 1, 3 + len(sample)));
            counter = 0;
            for samples in self._DATA_BUFFER:
                (count, sample, targetFreq, totalSamples) = samples;
                for i in range(len(sample)):
                    buffer[counter][i] = sample[i-1];
                offset_index = len(sample);
                ###################################################################################
                ##   UPDATE THE Global.DATA_FRAME_APPENDAGE VARIABLE IF MORE COLUMNS ARE ADDED.  ##
                ###################################################################################
                buffer[counter][offset_index + 0] = targetFreq;
                buffer[counter][offset_index + 1] = count;
                buffer[counter][offset_index + 2] = totalSamples;
                #################################################################################
                counter += 1;
            self._emptyBuffer();
            return np.asmatrix(buffer);
        else:
            return None;

    def __init__(self):
        self._DATA_BUFFER = [];
        self._dataEnded = False;
        self._DATA_MAX_BUFFER_TIME_SEC = Globals.DATA_MAX_BUFFER_TIME_SEC;
        self._DATA_SAMPLING_FREQ_HZ = Globals.DATA_SAMPLING_FREQ
        self._DATA_MAX_SAMPLES = int(self._DATA_MAX_BUFFER_TIME_SEC * self._DATA_SAMPLING_FREQ_HZ);
        if Globals.DATA_SOURCE == "offline":
            self._dataReader = DataReader_Offline();
        elif Globals.DATA_SOURCE == "online":
            self._dataReader = DataReader_Online();

        self._readDataThreadHandle = self._readData();
############################################################################################