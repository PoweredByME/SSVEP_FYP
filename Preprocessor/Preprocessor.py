from numpy import sin, linspace, pi
import numpy;
from pylab import plot, show, title, xlabel, ylabel, subplot
import time;
from Utils import Utils;
from Globals import Globals;
from sklearn import preprocessing as pp;

class Preprocessor(object):
    def __init__(self):
        pass;

    # normalize the data.    
    def _normalize(self, dataFrame):
        for i in range(dataFrame.shape[1] - Globals.DATA_FRAME_APPENDAGE):
            dataFrame[:,i] = pp.scale(dataFrame[:,i]);
        return dataFrame;

    def _plotFFT(self, y, Fs):
        (freq, Y) = Utils.computeFFT(y,Fs);
        freq = freq[0:len(Y)];
        plot(freq, Y);
        show();

    def Process(self, dataFrame):
        normalized_DataFrame = self._normalize(dataFrame);
        self._plotFFT(
                        normalized_DataFrame[:,1]
                        ,
                        Globals.DATA_SAMPLING_FREQ
                    );



    