import os, sys
import cv2
cap=cv2.VideoCapture(0)

import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# change this as you see fit


# Read in the image_data
image_data = tf.gfile.FastGFile('/home/apoorv/Desktop/res.jpg', 'rb').read()

# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line 
                   in tf.gfile.GFile("output_labels.txt")]

# Unpersists graph from file
with tf.gfile.FastGFile("output_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')

trigger_1 = 0

with tf.Session() as sess:
    while(True):
        ret,img=cap.read()
        res = cv2.resize(img,(320, 240), interpolation = cv2.INTER_CUBIC)
        cv2.imshow('img',res)
        cv2.imwrite('image.jpg',res)
        image_data = tf.gfile.FastGFile('image.jpg', 'rb').read()
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    
        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})
    
    # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            print('%s (score = %.5f)' % (human_string, score))
            if predictions[0][2]>0.95:
                trigger_1 = 1
                print 'trigger 1 set'
            if predictions[0][3]>0.9:
                trigger_1=  0
                print 'trigger removed'
            if trigger_1==1 and node_id==1:
                print 'toggle last seen'
            break
        print ''
        print ''
        if cv2.waitKey(1)==27:
            break
