from numpy import sin, linspace, pi
import numpy;
from pylab import plot, show, title, xlabel, ylabel, subplot
import time;
from Utils import Utils;
from Globals import Globals;
from sklearn import preprocessing as pp;
from scipy import signal;
import mne.filter as mne_filt;
import Utils.gumpy.gumpy.signal as gumpy_signal;


class Preprocessor(object):
    '''
        This is the Preprocessor which preprocesses the data.
        
        -   All of the preprocess steps must be called in the Process function;
        -   Call the Process() function to do all the preprocessing
        -   The Process() method must not damage the data protocol of the data frame which is
            defined in README file on the DataRecorder

    '''
    def __init__(self):
        pass;

    # normalize the data.    
    def _normalize(self, dataFrame):
        for i in range(dataFrame.shape[1] - Globals.DATA_FRAME_APPENDAGE):
            dataFrame[:,i] = gumpy_signal.normalize(dataFrame[:,i], "mean_std"); #pp.scale(dataFrame[:,i]);
        return dataFrame;

    def _bandPassFilter(self, data, lo, hi):
        return gumpy_signal.butter_bandpass(data, lo = lo, hi = hi);
        
    def _bandPassDataFrame(self, dataFrame, lo, hi):
        # This function implements a notch filter and removes specifically a signal frequency
        for i in range(dataFrame.shape[1] - Globals.DATA_FRAME_APPENDAGE):
            dataFrame[:,i] = self._bandPassFilter(dataFrame[:,i], lo, hi);
        return dataFrame;

    def Process(self, dataFrame):
        '''
            The steps followed by this function are:
            -> data frame normalization (using gumpy normalize via mean_std)
            -> data frame filter by a bandpass filter of 5 to 40 Hz
        '''

        # normalize the DataFrame
        normalized_DataFrame = self._normalize(dataFrame);

        # remove artificats from the dataframe.
        freq_cut_lo_Hz = 5;
        freq_cut_hi_Hz = 40;
        filtered_DataFrame = self._bandPassDataFrame(normalized_DataFrame, freq_cut_lo_Hz, freq_cut_hi_Hz);

        return normalized_DataFrame;

    def _util_plotFFT(self, y, Fs):
        (freq, Y) = Utils.computeFFT(y,Fs);
        freq = freq[0:len(Y)];
        plot(freq, Y);
        show();

    