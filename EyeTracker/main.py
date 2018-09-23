import os;
os.system("python cythonizer.py build_ext --inplace");

import camera, display, utils;
import faceLandmarkDetector, eyeTracker;
import cv2;
import numpy as np;
#from Utils import Utils;


def myFrameFunction(cam, disp, fld, et, eb):
    ''' 
        This function capture a frame from the video stream and
        do required processing on it and then display it.
    '''
    ret, frame = cam.getVideoFrame();
    if not ret:
        pass;
        #Utils.Print("No frame available. Ending video stream");

    fld.setFrame(frame);
    fldList = fld.detect();
    for (face, landmarks) in fldList:
        x,y,w,h = face;
        et.setParameters(frame, face, landmarks);
        ((lx,ly),(rx,ry)) = et.Process();
        eb.detect(landmarks);
        cv2.circle(frame, (lx, ly), 4, (0,0,255), -1);
        cv2.circle(frame, (rx, ry), 4, (0,0,255), -1);

        #for (x1,y1) in landmarks:
        #    cv2.circle(frame, (x1,y1), 5, (255,0,0), -1);

    disp.showFrame(frame);
            


def onEyeBlink():
    pass;
    #Utils.Print("Eye blinked");



def main():

    cam = camera.Camera();
    cam.setVideoSource(0);
    disp = display.Display();
    fld = faceLandmarkDetector.faceLandmarkDetector();
    et = eyeTracker.eyeTracker();
    eb = eyeTracker.eyeBlinkDetector(onEyeBlinkFunction=onEyeBlink);

    while cam.isVideoSourceAvaiable():
        myFrameFunction(cam, disp, fld, et, eb);
        if utils.CV_isButtonPressed("q"):
            break;

    cam.end();
    disp.end();




if __name__  == "__main__":
    main();
