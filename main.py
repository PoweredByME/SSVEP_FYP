from DataRecorder.DataRecorder import DataRecorder;
import Preprocessor.Preprocessor as Preprocessor;
import SSVEPDetector.SSVEPDetector as SSVEPDetector;
import SSVEPParadigm.SSVEPParadigm as SSVEPParadigm;
import numpy as np;
import matplotlib.pyplot as plt;
from Globals import Globals;
from Utils import Utils;


pp = Preprocessor.Preprocessor();
sd = SSVEPDetector.SSVEPDetector();
DOT = [];
SSVEP = [];
COEFF = [];
counter = 1;

def onReceive_DataFrame(dataFrame):
    #print ("Hello dataframe");
    global counter;
    d = dataFrame[:,2];
    targetFreq = dataFrame[:, dataFrame.shape[1] - Globals.DATA_FRAME_APPENDAGE + 0];
    print(str(counter) + ". ssvep = " + str(sum(targetFreq) / (13 * len(targetFreq)) * 100));
    if sum(targetFreq) / (13 * len(targetFreq)) * 100 > -1.0:
        plt.subplot(211);
        re = plt.psd(d, Fs=Globals.DATA_SAMPLING_FREQ);
        (Pxx, Fxx) = re;
        f = 13;
        print("-> " + str(Pxx[f]) + ", " + str(Pxx[f * 2]) + ", "+ str(Pxx[f * 3]));
        f = 15;
        print("-> " + str(Pxx[f]) + ", " + str(Pxx[f * 2]) + ", "+ str(Pxx[f * 3]));
        f = 17;
        print("-> " + str(Pxx[f]) + ", " + str(Pxx[f * 2]) + ", "+ str(Pxx[f * 3]));
        f = 19;
        print("-> " + str(Pxx[f]) + ", " + str(Pxx[f * 2]) + ", "+ str(Pxx[f * 3]));
        plt.subplot(212);
        (freq, Y) = Utils.computeFFT(d, Globals.DATA_SAMPLING_FREQ);
        freq = freq[6:len(Y)];
        Y = Y[6:len(Y)];
        plt.plot(freq, Y);
        plt.show();
    counter += 1;
    return;


    global pp,sd, DOT, SSVEP, COEFF;
    '''
        This function is called when ever a data frame is received.
    '''
    preprocessed_dataFrame = pp.Process(dataFrame);
    (dot, ssvep, coeff) = sd.SOB(preprocessed_dataFrame);
    DOT.append(dot);
    SSVEP.append(ssvep);
    COEFF.append(coeff);


def main():
    global COEFF, SSVEP, DOT;
    dr = DataRecorder();
    #paradigm = SSVEPParadigm.SSVEPParadigm(500,500);
   

    while True:
        dataFrame = dr.getData();
        '''
            dataFrame is the buffer containing the required amount of data
            which is to be processed.
            The properties of a data frame include:
            - Size is always equal to that defined in by Globals.DATA_MAX_BUFFER_TIME_SEC
        '''
        if dataFrame is not None:
            onReceive_DataFrame(dataFrame);
        if dr.endOfData():
            '''COEFF = np.asarray(COEFF);
            SSVEP = np.asarray(SSVEP);

            plt.subplot(311);
            plt.plot(SSVEP);
            plt.subplot(312);
            c = COEFF.copy();
            c[(SSVEP < 1)] = 0
            plt.plot(c);
            plt.subplot(313);
            COEFF[(SSVEP > 1)] = 0;
            plt.plot(COEFF);
            plt.show();
            
            return;'''
            pass;


if __name__ == "__main__":
    main();