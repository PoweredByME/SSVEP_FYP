from DataRecorder.DataRecorder import DataRecorder;
import numpy as np;

dr = DataRecorder();
while True:
    d = dr.getData();
    if d is not None:
        print(d)
    if dr.endOfData():
        break;
    
print("main thread end")