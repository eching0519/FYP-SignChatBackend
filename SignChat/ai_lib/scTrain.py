from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split
import os
import pandas as pd
import numpy as np
import random
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import json
from datetime import datetime
import csvHandler as csvHandler

def train(collectionId, shouldPlotGraph, averageNoOfFrame):
    X, y = load_data(collectionId, averageNoOfFrame)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
    model=build_model(y_train.shape[1], averageNoOfFrame)
    print('')
    print('              Training stage              ')
    print('==========================================')
    print('')
    history = model.fit(X_train,y_train,epochs=100,batch_size=32,validation_data=(X_test,y_test),shuffle=True)
    if shouldPlotGraph:
        plot_graphs(history, 'accuracy')
        plot_graphs(history, 'loss')
    model.save('./ai_model/'+collectionId+'.h5')

    # save model accuracy to a txt
    historyDic = history.history
    key_arr = list(historyDic.keys())

    updateTime = datetime.now().strftime("%d-%b-%Y %H:%M")
    loss = historyDic[key_arr[0]]
    accuracy = historyDic[key_arr[1]]
    val_loss = historyDic[key_arr[2]]
    val_accuracy = historyDic[key_arr[3]]
    
    print("Accuracy: " + str(accuracy[len(accuracy)-1]))
    print("loss: " + str(loss[len(loss)-1]))
    print("val_accuracy: " + str(val_accuracy[len(val_accuracy)-1]))
    print("val_loss: " + str(val_loss[len(val_loss)-1]))
    
    modelData = { 'lastUpdate': updateTime,
                  'accuracy': str(round(accuracy[len(accuracy)-1],3)), 
                  'loss': str(round(loss[len(loss)-1],3)), 
                  'val_accuracy': str(round(val_accuracy[len(val_accuracy)-1],3)), 
                  'val_loss': str(round(val_loss[len(val_loss)-1],3)) }

    filePath = './ai_model/'+collectionId+'.txt'
    with open(filePath, "w", encoding='UTF-8') as f:
        f.write(json.dumps(modelData))
    f.close()
    csvHandler.removeCsv(collectionId)
    return modelData


def load_data(collectionId, frame): #frame = average number of frame
    X = []
    Y = []

    dir_path = './ai_csv/'+collectionId
    #  listdir() returns a list containing the names of the entries in the directory given by path.
    list_file = os.listdir(dir_path)

    # for loop all Folder in dir_path
    for file in list_file:
            if "_" in file:
                continue
            file_name = file
            file_dir = dir_path + '\\' + file_name
            textlist  = os.listdir(file_dir)

            # For loop to run csv Files
            for text in textlist:
                if "DS_" in text:
                    continue
                csv_dir = file_dir + '\\' + text
                df = pd.read_csv(csv_dir)
                data_list = [list(row) for row in df.values]

                landmark_frame=[]
                data_in_a_frame = 126
                total_data_wanted = data_in_a_frame * frame

                # For loop to run rows in csv Files
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
                    if len(landmark_frame) < total_data_wanted:
                        for i in range(0,126):
                            landmark_frame.extend([row[i]])
                for i in range(len(landmark_frame),total_data_wanted):
                    landmark_frame.extend([0.000])
                landmark_frame=np.array(landmark_frame)
                landmark_frame=list(landmark_frame.reshape(-1,126))
                
                X.append(np.array(landmark_frame))
                Y.append(file_name)
        
    X=np.array(X)
    Y=np.array(Y)
        
    tmp = [[x,y] for x, y in zip(X, Y)]
    random.shuffle(tmp)
        
    X = [n[0] for n in tmp]
    Y = [n[1] for n in tmp]

    y_sets  = set(Y)
    print(y_sets)
    sorted_sets = sorted(y_sets)
    text=""
    for i in sorted_sets:
        text=text+i+"|"
    print(text)
    make_label(collectionId, text)

    s = Tokenizer()
    s.fit_on_texts([text])
    encoded = s.texts_to_sequences([Y])[0]
    one_hot = to_categorical(encoded)

    (x_train, y_train) = X, one_hot
    x_train=np.array(x_train)
    y_train=np.array(y_train)

    return x_train,y_train


def build_model(label, averageNoOfFrame):
    model = Sequential()
    model.add(layers.LSTM(64, return_sequences=True,
                   input_shape=(averageNoOfFrame, 126))) 
    model.add(layers.LSTM(32, return_sequences=True))
    model.add(layers.LSTM(32))
    model.add(layers.Dropout(0.1))
    model.add(layers.Dense(label, activation='softmax'))
    model.compile(Adam(learning_rate=0.0001),
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])
    return model


def plot_graphs(history, metric):
  plt.plot(history.history[metric])
  plt.plot(history.history['val_'+metric], '')
  plt.xlabel("Epochs")
  plt.ylabel(metric)
  plt.legend([metric, 'val_'+metric])
  plt.show()


def make_label(collectionId, text):
    filePath = "./ai_label/"+ collectionId+".txt"
    with open(filePath, "w", encoding='UTF-8') as f:
        f.write(text)
    f.close()