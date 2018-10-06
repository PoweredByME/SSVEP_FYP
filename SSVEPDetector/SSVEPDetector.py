import numpy;
from Utils import Utils;
from Globals import Globals;
from pylab import plot, show, subplot;

class SSVEPDetector(object):
    '''
        This is the module of the pipeline where the SSVEP is detected and Classified.
    '''

    def __init__(self):
        self.ssvepFreqs = [15.0]; # list of all the freqs for which the system has to detect the SSVEP.
        self.eegChannelforSOB = 3;


    

    def SOB(self, dataFrame):
        totalChannels = dataFrame.shape[1] - Globals.DATA_FRAME_APPENDAGE;
        if self.eegChannelforSOB >= totalChannels:
            raise Exception("Invalid EEG channal selected for Signal to Background (SSVEPDetector.SOB)");

        eegChannel = dataFrame[:, self.eegChannelforSOB];
        freq, Y = Utils.computeFFT(eegChannel, Globals.DATA_SAMPLING_FREQ);
        
        freq = numpy.asarray(freq);
        Y = numpy.asarray(numpy.transpose(Y))[0];
        freq = freq[0:len(Y)];

        Y = Utils.fftLowPassFilter(Y, freq, 45.0);

        highPass_5_Y = Utils.fftHighPassFilter(Y.copy(), freq, 5.0);
        highPass_11_Y = Utils.fftHighPassFilter(Y.copy(), freq, 11.0);
        bandpass_9_11_Y = Utils.fftBandStopFilter(highPass_5_Y.copy(), freq, 9.0, 11.0);

        high_11_S1 = numpy.fft.fftpack.irfft(highPass_11_Y);
        bandpass_9_11_Y_S1 = numpy.fft.fftpack.irfft(bandpass_9_11_Y);
        
        h1_lo = self.ssvepFreqs[0] - 0.5;
        h1_hi = self.ssvepFreqs[0] + 0.5;
        S2 = Utils.fftBandStopFilter(bandpass_9_11_Y, freq, h1_lo, h1_hi);

        h1_lo = 2 * self.ssvepFreqs[0] - 0.5;
        h1_hi = 2 * self.ssvepFreqs[0] + 0.5;
        S2 = Utils.fftBandStopFilter(S2, freq, h1_lo, h1_hi);
        S2 = numpy.fft.fftpack.irfft(S2);

        coeff = numpy.corrcoef(bandpass_9_11_Y_S1, S2);
        print (numpy.linalg.det(coeff));
        dot = numpy.dot(bandpass_9_11_Y_S1 ,S2);
        print ("dot = " + str(dot));
        targetFreq = dataFrame[:, dataFrame.shape[1] - Globals.DATA_FRAME_APPENDAGE + 0];
        print("ssvep = " + str(sum(targetFreq) / (13 * len(targetFreq)) * 100));

        return (dot, float(sum(targetFreq) / (self.ssvepFreqs[0] * len(targetFreq)) * 100), numpy.linalg.det(coeff))
        subplot(211);
        plot(dot);
        subplot(212);
        plot(targetFreq);
        show();