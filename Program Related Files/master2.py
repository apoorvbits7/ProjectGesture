import os, sys
import cv2
import tensorflow as tf
import numpy as np
import OpticalFlow3 as flow
import OpticalFlowSwipe as swipe
import time
import multiprocessing
import webbrowser
from playsound import playsound
import HomeAutomation as auto
import subprocess

label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("output_labels.txt")]

with tf.gfile.FastGFile("output_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')

photo_list = []
for filename in os.listdir('Photos'):
    photo_list.append(filename)

counter = 1
def control_music(parameter):
    num_music=3
    global counter
    if parameter == 'left':
        if counter==1:
            counter=num_music
        else:
            counter = counter - 1
    elif parameter == 'right':
        if counter==num_music:
            counter=1
        else:
            counter = counter + 1
    elif parameter == 'open':
        pass
    elif parameter == 'close':
        os.system("vlc-ctrl quit")
        return None
    os.system("vlc-ctrl play -p /home/apoorv/Music/" + str(counter) + ".mp3")

object_list = ['negative','negative']
def object_list_editor(detected_object):
    global object_list
    object_list[0] = object_list[1]
    object_list[1] = detected_object

start_palm_time = 0
elapsed_palm_time = 0
previous_detected_object = 0
is_photos_open = False
counter_palm = 0
counter_index = 0
gesture_detection_going_on = False  #this variable holds true if gesture detection is in progress 
def object_control(detected_object, last_seen_interactive_object,sess):
    global is_gesture_palm
    global start_palm_time
    global elapsed_palm_time
    global is_photos_open
    global gesture_detection_going_on
    global previous_detected_object
    global object_list
    global counter_palm
    global counter_index
    object_list_editor(detected_object)
    if object_list[0] == 'palm' and object_list[1] == 'fist':
        if last_seen_interactive_object == 'laptop':
            if is_photos_open == False:
                control_music('open')
                is_photos_open = True
            else:
                control_music('close')
                is_photos_open = False
        if last_seen_interactive_object == 'tv':
            auto.tv('toggle')
        if last_seen_interactive_object == 'ac':
            print "toggling ac"
            time.sleep(5)
            auto.ac('toggle')
    print object_list
    if object_list[0] == 'palm' and object_list[1] == 'palm':
        counter_palm = counter_palm + 1
    else:
        counter_palm = 0
    if object_list[0] == 'index' and object_list[1] == 'index':
        counter_index = counter_index + 1
    else:
        counter_index = 0
    if counter_palm == 3:
        swipe_direction = swipe.main(320,240)
        if last_seen_interactive_object == 'laptop' and is_photos_open == True:
            control_music(swipe_direction)
            print swipe_direction
        if last_seen_interactive_object == 'tv':
            if swipe_direction=='right':
                auto.tv('volume_up')
            elif swipe_direction=='left':
                auto.tv('volume_down')
        counter_palm = 0
    if counter_index == 3:
        digits = []
        flow.main(320,240)
        result = subprocess.check_output('python Predicting_Digit.py', shell=True)
        for t in result:
            if t.isdigit() == True:
                digits.append(int(t))
        print digits
        if last_seen_interactive_object == 'tv':
            auto.tv('channel', digits)
        if last_seen_interactive_object == 'ac':
            auto.ac('temp_manual',digits)
def start_video_capture(): 
    cap=cv2.VideoCapture(1)
    return cap

cv2.namedWindow('test')
interactive_objects = ['tv','laptop','ac']
last_seen_interactive_object = None
start_object_time = 0
cap = start_video_capture()
counter_s = 0;
with tf.Session() as sess:
    while(True):
        global start_object_time
        global start_palm_time
        global elapsed_palm_time
        ret,frame = cap.read()
        #
        #frame = cv2.resize(frame, (640, 480))
        #
        #cv2.imshow('img',frame)
        cv2.imwrite('temp_img_to_load_in_graph.jpg',frame)
        image = tf.gfile.FastGFile('temp_img_to_load_in_graph.jpg', 'rb').read()
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image})
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]   #returns the objects seen in image in decreasing order of probabiltiy
        top_prediction = top_k[0]   #gets the object with highest probabiltiy in terms of number which represents that object
        detected_object = label_lines[top_prediction]  #converts the number to human string
        score = predictions[0][top_prediction]
        if detected_object == last_seen_interactive_object:
            for t in top_k:
                human_string = label_lines[t]
                if human_string == 'palm':
                    palm_score = predictions[0][t]
                elif human_string == 'fist':
                    fist_score = predictions[0][t]
                elif human_string == 'index':
                    index_score = predictions[0][t]
                elif human_string == 'negatives':
                    negatives_score = predictions[0][t]
            total = palm_score + fist_score + index_score + negatives_score
            palm_prob = palm_score/total
            fist_prob = fist_score/total
            index_prob = index_score/total
            negatives_prob = negatives_score/total
            if palm_prob>0.8:
                detected_object = 'palm'
            elif fist_prob>0.8:
                detected_object = 'fist'
            elif index_prob>0.8:
                detected_object = 'index'
            elif negatives_prob>0.8:
                detected_object = 'negatives'
        print detected_object
        print score
        print ''
        if detected_object in interactive_objects:
            last_seen_interactive_object = detected_object
            start_object_time = time.time()
        if start_object_time != 0:
            elapsed_object_time = time.time() - start_object_time
            if elapsed_object_time<10:
                object_control(detected_object, last_seen_interactive_object,sess)
        #cv2.imshow('img',frame)
        #cv2.imwrite('Video/' + str(counter_s) + '.jpg',frame);
        counter_s = counter_s+1
        if cv2.waitKey(1) == 27:
            cap.release()
            break



        
