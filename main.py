from DataRecorder.DataRecorder import DataRecorder;
import Preprocessor.Preprocessor as Preprocessor;
import SSVEPDetector.SSVEPDetector as SSVEPDetector;
import numpy as np;
import matplotlib.pyplot as plt;


pp = Preprocessor.Preprocessor();
sd = SSVEPDetector.SSVEPDetector();
DOT = [];
SSVEP = [];
COEFF = [];

def onReceive_DataFrame(dataFrame):
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
            COEFF = np.asarray(COEFF);
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
            
            return;


if __name__ == "__main__":
    main();