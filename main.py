from DataRecorder.DataRecorder import DataRecorder;
import numpy as np;


def onReceive_DataFrame(dataFrame):
    '''
        This function is called when ever a data frame is received.
    '''
    pass;


def main():
    dr = DataRecorder();
    while True:
        dataFrame = dr.getData();
        '''
            dataFrame is the buffer containing the required amount of data
            which is to be processed.
            The properties of a data frame include:
            - Size is always equal to that defined in by Globals.DATA_MAX_BUFFER_TIME_SEC
        '''
        if d is not None:
            onReceive_DataFrame(dataFrame);
        if dr.endOfData();
            return;


if __name__ == "__main__":
    main();