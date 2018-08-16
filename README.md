**Project Gesture : Developing a gesture based device capable of controlling multiple appliances simultaneously irrespective of their relative positions**

**Apoorv Sadana**

Delhi Private School Dubai

**ABSTRACT**

Hand gestures are a powerful way for human communication with lots of potential applications. While there are a few devices in the market today which seem to make gesture based interaction a reality, they come with drawbacks which include limited control and flexibility. This paper proposes the idea of Project Gesture : a wearable device which uses machine learning and image processing to overcome the drawbacks of current gesture based devices. It is a device capable of controlling multiple appliances simultaneously irrespective of their relative positions by using gestures. It consists of a pair of glasses working only using a camera sensor. The glass is capable of detecting static and dynamic gestures as well as the objects of interest (objects user wishes to control). First, OpenCV was used for hand segmentation. OpenCV was able to give a maximum of 55% accuracy with color based segmentation technique. Machine learning initially gave a 75% accuracy with the NUS dataset[1]. This was increased to 99% with a personalized dataset. Machine learning could classify images with different lighting conditions and complex background. Dynamic gesture recognition was accurate when using a smooth camera with less or no buffer. But the accuracy significantly dropped as the buffer increased. Currently, the device can detect 12 dynamic gestures ( 10 digits and 2 hand swipes - left and right).

**Keywords: human-computer interaction; hand gesture based devices; gesture recognition; smart home assistant; wearable computers; assisted living**

**1. Problem**

The vision to interact with one&#39;s surroundings by merely using hand gestures is fascinating. There are a few devices in the market today which attempt to make this vision a reality, however, they come with one or more of the following drawbacks:

1. Limited control. The device limits the number and type of gestures which can be detected.
2. Limited Appliances. The user can only interact with devices present in a room or some physical boundary. (This happens in devices that need to be fixed at a particular location)
3. Explicit user specification. The user must explicitly specify the device he/she wants to interact with i.e. the device cannot detect changes in objects of interest (object the user wishes to control).

**2. Concept**

The solution to the above problems can be obtained by building a wearable device which not only detects hand gestures but also detects the objects of interest. This can achieved by thinking of the device as a wearable - a glass - which consists of a build in camera sensor. Assuming that the user will be facing the appliance (object of interest) before he/she makes the required gesture to interact with it, it can be said that a camera sensor on the glass will be able to view the hand gesture as well as the object of interest. This approach would solve a major part of the problem. Hence, the solution can be stated as

_Using a camera sensor to detect hand gestures and objects of interest_

**3. Using OpenCV to detect Static Hand Gestures via Hand Segmentation**

The frames recorded by the camera can be classified into two categories - those which contain the hand and those which do not. An algorithm can be made to segment some part of any image used as input. It can then trained so that the segmented part must be the hand in the images which contain the hand. But this algorithm would also segment some part of an image which does not contain the hand. Hence, there must be some property of the hand which allows the computer to distinguish between hand segmentations and the other segmentations.

**3.1 Studying various Properties of the Hand**

In order to find the above mentioned property, the hand was contoured from 10 different images using OpenCV. The following properties were observed.

1. Aspect Ratio : Ratio of width to height of the bounding rectangle of the contour
2. Extent : Ratio of the area of the contour to the area of the bounding rectangle of the contour
3. Equivalent Diameter : Diameter of the circle which has the same area as that of the contour
4. Solidity : Ratio of contour area to its convex hull area.

The results obtained were as follows

![alt text](https://github.com/ApoorvSadana/ProjectGesture/blob/master/images/image1.png?raw=true)

(a)

![alt text](https://github.com/ApoorvSadana/ProjectGesture/blob/master/images/image3.png?raw=true)

(b)

![alt text](https://github.com/ApoorvSadana/ProjectGesture/blob/master/images/image2.png?raw=true)

(c)

![alt text](https://github.com/ApoorvSadana/ProjectGesture/blob/master/images/image5.png?raw=true)

(d)

_Fig 1   (a) Graph of Aspect Ratio vs Image Number_

_(b) Graph of Equivalent Diameter vs Image Number_

_(c) Graph of Extent vs Image Number_

_(d) Graph of Solidity vs Image Number_

_All graphs were plotted using matplotlib_

As solidity had the least coefficient of variation, it could be concluded that it was a characteristic property of a hand.

**3.2 Method 1: Canny Edge Detection**

As mentioned in the beginning of  section 3, an algorithm is needed which can successfully segment the hand from images which contain it. The first method employed to achieve this was Canny Edge Detection.

The algorithm was as follows:

1. Smoothen the image using Gaussian Blur
2. Find edges using canny edge detection
3. Dilate the edges
4. Find contour of maximum area

The result was as follows

Table 1

| Image Type | Number of Images | Number of images correctly segmented | Accuracy |
| --- | --- | --- | --- |
| Plane Background | 10 | 7 | 35% |
| Background with noise | 10 | 0 |

From the result it can be concluded that this method works reasonably well with images containing plane backgrounds but it fails to segment the hand from images containing backgrounds with noises.

**3.3 Method 2: Adaptive Thresholding**

Adaptive threshold could serve as a slightly better edge detector as it would be able to understand the difference between two distinct objects on the bases of their colors Hence, the algorithm of method 1 was modified to replace canny edge detection with adaptive thresholding. But conversion of RGB to grayscale image (perquisite for adaptive thresholding) and noise created by thresholding nullified the advantage of  adaptive thresholding over canny edge detection. Hence, results obtained were similar.

**3.4 Method 3: Color Based Segmentation**

inRange() thresholding was employed for this method. A range of color values for the hand were found after converting sample of RGB hand images into HSV (works better for object segmentation). These were then passed into inRange function.

The algorithm was as follows:

1. Convert image to HSV
2. Threshold image using inRange function
3. Find contour of maximum area

Table 2

| Image Type | Number of Images | Number of images correctly segmented | Accuracy |
| --- | --- | --- | --- |
| Plane Background | 10 | 6 | 55% |
| Background with noise | 10 | 5 |

Color based segmentation showed a drastic improvement in hand segmentation. The method could segment the hand when other objects were present in the background. But it was observed that the method failed when the background had objects having color loosely related to that of the hand or when the lighting conditions were significantly changed.

**3.5 Other Methods and Techniques Used**

The following methods and techniques were also used to improve results:

1. Applying morphological operations (erosion, dilation, opening and closing) to improve contour recognition
2. Using contour hierarchy to eliminate unnecessary contours
3. Using histogram equalization to normalize lighting conditions in different images
4. Using different image smoothing functions (Gaussian blur, bilateral filtering etc.)

But the result either deteriorated or remained same.

**4. Using Machine Learning to detect Static Hand Gestures**

The results from image processing were not satisfactory and hence machine learning was used for static gesture recognition.

**4.1 Transfer Learning with NUS Hand Posture dataset**

The NUS dataset contains 275 pictures (with and without human noise) of 10 gestures[1]. Out of 10, three gestures - palm, fist and index finger - were selected to train the model. The 80%, 10% and 10% paradigm was not followed for training, testing and validation images. Instead, personal set of images were used for validation to check if model was able to generalize the classification task and segment images containing different hands.

**Hyper-parameters**

Table 3

| Parameter | Value |
| --- | --- |
| Architecture | inception\_v3 |
| Learning Rate | 0.01 |
| Number of training steps | 4000 |

The results obtained can be seen in Fig 2. which shows the graph of accuracy vs number of training steps. The blue curve represents the validation accuracy and it can be seen that the validation accuracy reaches a maximum of 80% after which the model starts overfitting.

![alt text](https://github.com/ApoorvSadana/ProjectGesture/blob/master/images/image4.png?raw=true)
_Fig 2. Plot of accuracy vs number of training steps when training with NUS hand posture dataset. The red line shows the training accuracy and the blue line shows the validation accuracy. The plot was made using TensorBoard._

**4.2 Making a Personalized Dataset**

In order to improve the performance, a personalized dataset was created containing images of the user&#39;s hands. The gestures used were - palm, index finger and fist. The images were collected by extracting frames from videos containing the user&#39;s hand. For each gesture, one video was made which produced approximately 1000 images. After several trials, it was found that the best accuracy was obtained when

1. The background in all the videos was the same. This  ensured that the model was actually learning how to classify the gesture and not the background.
2. A video with just the background (no hand) was recorded and model was trained to detect frames from this video as negatives.

**4.3 Transfer Learning with Personalized Dataset**

This time 80%, 10% and 10% paradigm was followed for training, testing and validation images.

**Hyper-parameters**

Table 4

| Parameter | Value |
| --- | --- |
| Architecture | inception\_v3 |
| Learning Rate | 0.01 |
| Number of training steps | 4000 |
| Validation Percentage | 10 |

The results obtained can be seen in Fig 3. which shows the graph of the accuracy vs number of training steps. The accuracy obtained was 99%.

![alt text](https://github.com/ApoorvSadana/ProjectGesture/blob/master/images/image6.png?raw=true)
_Fig 3. Plot of accuracy vs number of training steps when training with personalized_ dataset_. The red line shows the training accuracy and the blue line shows the validation accuracy. The plot was made using TensorBoard._

On testing the model with 28 sample images the following results were obtained

Table 5

| Image Type | Number of images | Number of images correctly classified | Accuracy |
| --- | --- | --- | --- |
| Mixed (with and without noise) | 28 | 28 | 100% |

It was observed that after training on personalized dataset, the model was able to classify the gestures from complex images taken in varying lighting conditions.

**5. Detecting Objects of Interest**

The model trained to detect static gestures was also trained to detect objects of interest. The hyper parameters used were the same and the accuracy achieved was 99% on the validation dataset.

**6. Detecting Dynamic Gestures**

**6.1 Digit Recognition**

Dynamic gesture recognition for digits was toggled when the user made the index finger gesture. OpenCV&#39;s Lucas Kanade Optical Flow function was used to track hand movements and MNIST dataset was used to detect digits

The following algorithm was used

1. Once the index finger gesture is made, the hand tracking starts and the centre of the image is taken as the starting tracking point (the user&#39;s hand would be at the centre of the screen). If the user&#39;s hand covered a distance greater than a certain value from the starting point, it is assumed that the user has started drawing the digit.
2. Once the user starts drawing the digit, the program waits for the user&#39;s hand to come to rest. When the hand comes to rest, the digit is assumed to be complete.
3. To ensure that what is detected in the first two steps is a digit and not a minor hand movement, the distance moved by the hand in the two steps is calculated. If this distance is greater than a specific value, the detection is confirmed to be a digit and the image of the digit is saved. On the other hand, if the distance is less than the specific value, the detection is thought to be a minor hand movement. In that case, the position of the hand at that moment is thought of as the new starting point and the program goes back to step 1.

_Once the user has finished drawing the digit, he/she may wish to draw another one. To do so, he will first have to move his/her hand back to the center of the screen (or some other point far from where the previous digit had ended). Step 4 is used to detect hand movement between two digits._

1. As mentioned in step 2, the digit is complete when the user&#39;s hand comes to rest. After one digit, the program waits for the user to start moving his hand again. Once the motion starts, the program then waits for the user&#39;s hand to come to rest at a point far away from where the hand started moving.. This position of rest is then considered to be the new starting point. Program now goes back to step 1.
2. If at any point the user moves his hand out of the frame, the program terminates and control goes back to the master program. The master program uses the MNIST dataset to predict the digits drawn.

The program was run on a computer webcam with a resolution of 640x480. The results obtained from the above algorithm were as follows.

Table 6

| Attempt Number | No. of digits that could be drawn before tracking failed (attempt stopped after 10 digits) |
| --- | --- |
| 1 | 4 |
| 2 | 4 |
| 3 | 8 |
| 4 | 1 |
| 5 | 2 |
| 6 | 10 |
| 7 | 2 |
| 8 | 3 |
| 9 | 4 |
| 10 | 6 |

**Average 4.4**

On an average, 4.4 digits could be drawn successfully before the tracking failed. It was also observed that dynamic gesture recognition for digits required a smooth camera. Results deteriorated as the frames recorded by the camera per second decreased.

**6.2 Hand Swipe Recognition**

Dynamic Gesture Recognition for hand swipe was toggled when the user made the palm gesture for a given period of time. Considering a hand swipe as a new digit, the algorithm used for detection of hand swipes was the same as that used for detection of digits. However, instead of creating a image to be fed into the MNIST model, the program checked the direction of motion of the hand.

**7. Conclusion**

Using a combination of image processing and machine learning, the device is capable of the following

1. It can trigger actions based on gestures made by the user. Currently, 3 static and 12 dynamic gestures (10 digits and 2 hand swipes) can be detected by the device. But the number of static gestures can be increased by training the model on a larger number of images.
2. It can detect a variety of gestures as required by the user. The user has to train the model with his hand and he/she can choose any set of gestures.
3. It can find the object the user wants to control without explicit specification by the user.
4. It is universal – one device is capable of controlling all other devices irrespective of their relative positions (they do not need to be in the same room or be bounded within a physical boundary)

**7.References**

[1] Pramod Kumar Pisharady, Prahlad Vadakkepat, Ai Poh Loh, &quot;Attention Based Detection and Recognition of Hand Postures Against Complex Backgrounds&quot;, International Journal of Computer Vision, vol.101, no.3, pp.403-419, February, 2013.
