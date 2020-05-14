import csv
import math
import numpy as np
import tensorflow as tf
import pandas as pd
import json

def predict(collectionId, frameData, frame):
    data_list = [list(row) for row in frameData.values]

    landmark_frame=[]
    set_of_data = math.ceil(frameData.shape[0]/frame)
    data_in_a_frame = 126
    total_data_wanted = data_in_a_frame * frame * set_of_data

    for row in data_list:
        # Start from 0 till 125
        if len(data_list) < frame / 3:
            if len(landmark_frame) < total_data_wanted:
                for i in range(0,126):
                    landmark_frame.extend([row[i]])
        if len(data_list) < frame / 2:
            if len(landmark_frame) < total_data_wanted:
                for i in range(0,126):
                    landmark_frame.extend([row[i]])
        for i in range(0,126):
            landmark_frame.extend([row[i]])
    for i in range(len(landmark_frame),total_data_wanted):
        landmark_frame.extend([0.000])
    landmark_frame = np.array(landmark_frame)
    landmark_frame = list(np.reshape(landmark_frame,(-1, frame, 126)))

    new_model = tf.keras.models.load_model('./ai_model/'+collectionId+'.h5')
    
    labels = load_label(collectionId)
    
    yhat = new_model.predict(np.array(landmark_frame))
    predictions = np.array([np.argmax(pred) for pred in yhat])
    rev_labels = dict(zip(list(labels.values()), list(labels.keys())))

    result = []
    for i in predictions:
        result.append(rev_labels[i])

    return result


def load_label(collectionId):
    filePath = "./ai_label/"+ collectionId+".txt"
    listfile=[]
    with open(filePath, mode='r', encoding='UTF-8') as l:
        listfile=[i for i in l.read().split('|')]
    label = {}
    count = 1
    for l in listfile:
        if "_" in l:
            continue
        label[l] = count
        count += 1
    return label