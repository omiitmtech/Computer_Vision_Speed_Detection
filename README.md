
# Speed Detection Computer Vision
An implementation of a vehicle speed detection algorithm using an Haar object detector, an object correlation tracker using openCV and python. <br />

project data: <br />
https://github.com/omiitmtech/SpeedDetection_NewSpaceResearch

output video: <br />
https://drive.google.com/file/d/1rlz7IPhRPViv4Nk0o1dMv8-J4nqq8FbF/view?usp=sharing


# Problem Statement
To implement a computer vision and/or machine learning (CNN/DNN) based detector on a video, which should be able to detect vehicles, draw a red bounding box around them, calculate speed in km/hr and save the output video to disk.

# OpenCV Haar Cascade Classifier
OpenCV Haar Cascade Classifier model trained for vehicle detection, which was released by Kartike Bansal, combined with an object correlation tracker from the dlib library.

# Dependencies
1. cmake
2. dlib
3. numpy
4. opencv-python

To install the prerequisites use the following command:<br />
$ python3 pip install -r requirements.txt

# How to Run?
$ python3 calcSpeedDetection.py 'path/input_video_file'

For example:
$ python3 calcSpeedDetection.py 'inputFile/cars.mp4'

**Note:-**
1. You can press 'q' key from your keyboard to interrupt the current process anytime.
2. The processed video will be saved in the 'outputFiles/' folder.



 
