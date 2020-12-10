#!/usr/bin/env python3

import threading
from threading import Thread
import cv2
import numpy as np
import base64
from Queue import ThreadyQueue
import time

# shared queue  
queueSize = 10 
extractionQueue = ThreadyQueue(queueSize)
displayingQueue = ThreadyQueue(queueSize)

# filename of clip to load
global filename
filename = 'clip.mp4' # Video

class DisplayingThread(threading.Thread):
    def __init__(self, name=None):
        Thread.__init__(self)
        self.name = name

    def run(self):
        print("Display is running!")
        
        count = 0  # initialize frame count
        
        frame = displayingQueue.get() # get first Frame
        
        while frame != 'End':
            print(f'Displaying frame {count}')        

            # display the image in a window called "video" and wait 42ms
            # before displaying the next frame
            cv2.imshow('Video', frame)
            if cv2.waitKey(42) and 0xFF == ord("q"):
                break

            count += 1
            frame = displayingQueue.get()

        print('Finished displaying all frames')
        
        cv2.destroyAllWindows()  # Cleanup the windows 
    

class ExtractorThread(threading.Thread):
    def __init__(self, name=None):
        Thread.__init__(self)
        self.name = name

    def run(self):
        print("Extract is running!")
        
        count = 0  # Initialize frame count 
               
        vidcap = cv2.VideoCapture(filename)  # open video file
        
        # read first image
        success,image = vidcap.read()  # Reading each frame 1 by 1
        print(f'Reading frame {count} {success}')
        
        while success:                 
            extractionQueue.put(image)
            
            count += 1
            
            success,image = vidcap.read()
            
            print(f'Reading frame {count} {success}')
            
        print('Frame extraction complete')
        extractionQueue.put('End')
        
class GreyscalingThread(threading.Thread):
    def __init__(self, name=None):
        Thread.__init__(self)
        self.name = name

    def run(self):
        print("Greyscale is running!")
        
        count = 0  # Initialize frame count 
        
        # read first image
        colorFrame = extractionQueue.get()
        
        while colorFrame != 'End':
            print(f'Converting frame {count}')

            # convert the image to grayscale
            grayscaleFrame = cv2.cvtColor(colorFrame, cv2.COLOR_BGR2GRAY)
                                    
            displayingQueue.put(grayscaleFrame)
            count += 1
            
            colorFrame = extractionQueue.get()
            
        print('Frame greyscaling complete')
        displayingQueue.put('End')


# Start Thread Producer
extract = ExtractorThread(name='producer')  # Calls Extractor Thread Class
extract.start()

# Start Thread greyScaling
greyscale = GreyscalingThread(name='greyscaling')  # Calls GreyScaling Thread Class
greyscale.start()

# Start Thread Consumer
display = DisplayingThread(name='consumer')  # Calls Display Thread Class
display.start()

