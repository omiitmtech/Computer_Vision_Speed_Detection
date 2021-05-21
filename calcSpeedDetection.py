
#importing python libraries
import cv2
import dlib
import time
import threading
import math
import sys

# In[ ]:


#estimting the speed 
def estimateSpeed(location1, location2):
    
    #pixel distance travelled by the vehicle in one frame
    distancePixels  = math.pow(location2[0] - location1[0], 2)
    distancePixels += math.pow(location2[1] - location1[1], 2)
    d_pixels = math.sqrt(distancePixels)
    #initializing variables and constants needed to process the video
    ppm = 8.8
    #converted distance of pixels to meters travelled in one frame
    distanceMeters = d_pixels / ppm
    #average fps
    fps = 18
    speed = distanceMeters * fps * 3.6
    return speed


def detectSpeedCar(inputVideoFile):
    
    #setting up an instance of CascadeClassifier using pretrained model
    carCascade = cv2.CascadeClassifier('configFiles/myhaar.xml')
    video = cv2.VideoCapture('inputFiles/cars.mp4')
    WIDTH = int(video.get(3))*2
    HEIGHT = int(video.get(4))*2
    #color of drawn rectangle
    rectangleColor = (0, 0, 255)
    frameCounter = 0
    currentCarID = 0
    fps = 0

    carTracker = {}
    carNumbers = {}
    carLocation1 = {}
    carLocation2 = {}
    speed = [None] * 1000
    fileName = 'car'
    # Write output to video file
    out = cv2.VideoWriter('outputFiles/'+fileName+'_output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (WIDTH,HEIGHT))

    #infinite loop breaks when the frames get finished
    while True:
        start_time = time.time()
        rc, frame = video.read()
        if type(frame) == type(None):
            break
        #Resizing each video frame to the dimensions that the classifier model expects
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        #Reading and making copy of a frame, and increments the frame counter
        resultImage = frame.copy()
        frameCounter = frameCounter + 1
        carIDtoDelete = []

        #updating dlib correlation tracker with the current frame
        for carID in carTracker.keys():
            trackingQuality = carTracker[carID].update(frame)
            #calling the peak to-side lobe ratio
            if trackingQuality < 7:
                carIDtoDelete.append(carID)

        #If trackingQuality < 7, object may have disappeared,so delete it 
        for carID in carIDtoDelete:
            carTracker.pop(carID, None)
            carLocation1.pop(carID, None)
            carLocation2.pop(carID, None)

        if not (frameCounter % 10):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cars = carCascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24))
            #looping through all the previous vehicle objects we detected during the last classifier run
            #tracking now, and calculating centroids of those objects
            for (x, y, w, h) in cars:
                x_bar = int(x) + 0.5 * int(w)
                y_bar = int(y) + 0.5 * int(h)
                matchCarID = None
                
                #comparing the bounding boxes and centroids of each detected object
                for carID in carTracker.keys():
                    trackedPosition = carTracker[carID].get_position()
                    tPosX = int(trackedPosition.left())
                    tPosY = int(trackedPosition.top())
                    tPosW = int(trackedPosition.width())
                    tPosH = int(trackedPosition.height())

                    tPosX_bar = tPosX + 0.5 * tPosW
                    tPosY_bar = tPosY + 0.5 * tPosH
                    #tracked object’s position overlaps with a detected object’s position
                    #this detected object is the same as the existing tracked object
                    tPosWX = (tPosX <= x_bar <= (tPosX + tPosW))
                    tPosHY = (tPosY <= y_bar <= (tPosY + tPosH))
                    tPosWXBar = (x <= tPosX_bar <= (x + w))
                    tPosYHBar =  (y <= tPosY_bar <= (y + h))
                    if (tPosWX and tPosHY and tPosWXBar and tPosYHBar):
                        matchCarID = carID

                #If no objects overlap, probably a new object detected
                if matchCarID is None:
                    tracker = dlib.correlation_tracker()
                    tracker.start_track(frame, dlib.rectangle(x, y, x + w, y + h))
                    carTracker[currentCarID] = tracker
                    carLocation1[currentCarID] = [x, y, w, h]
                    currentCarID = currentCarID + 1
        for carID in carTracker.keys():
            trackedPosition = carTracker[carID].get_position()

            tPosX = int(trackedPosition.left())
            tPosY = int(trackedPosition.top())
            tPosW = int(trackedPosition.width())
            tPosH = int(trackedPosition.height())

            #drawing boxes for these object
            cv2.rectangle(resultImage, (tPosX, tPosY), (tPosX + tPosW, tPosY + tPosH), rectangleColor, 4)
            #updating the variable with the positions calculated for each object
            carLocation2[carID] = [tPosX, tPosY, tPosW, tPosH]

        end_time = time.time()
        if not (end_time == start_time):
            fps = 1.0/(end_time - start_time)
            
        for i in carLocation1.keys():
            if frameCounter % 1 == 0:
                [x1, y1, w1, h1] = carLocation1[i]
                [x2, y2, w2, h2] = carLocation2[i]
                #positions of vehicle objects calculated in the previous frame
                carLocation1[i] = [x2, y2, w2, h2]
                if [x1, y1, w1, h1] != [x2, y2, w2, h2]:
                    #Estimating speed for a car object as it passes through a ROI.
                    if (speed[i] == None or speed[i] == 0) and y1 >= 275 and y1 <= 285:
                        speed[i] = estimateSpeed([x1, y1, w1, h1], [x2, y2, w2, h2])
                    #displaying the speed only when the object is moving quickly enough
                    if speed[i] != None and y1 >= 180:
                        cv2.putText(resultImage, str(int(speed[i])) + " km/hr", (int(x1 + w1/2), int(y1-5)),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

        #displaying frame by frame
        cv2.imshow('Processed Video', resultImage)
        #writing the processed viedo to disk
        out.write(resultImage)

        #press s on the keyboard to interrupt the process
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    out.release()
    cv2.destroyAllWindows()


#calling function and variable initialization part
#pass video file from terminal
inputFile = sys.argv[1]
detectSpeedCar(inputFile)



