from flask import Flask, redirect, url_for, request
import flask
import json
from keras import models
import pandas as pd
import csvHandler as csvHandler
import scTrain
import scPredict
import os
import threading

app = Flask(__name__)

averageNoOfFrame = 12

@app.route('/train',methods = ['GET','POST'])
def train():
    print("----------AI Training Process Start----------")
    response = {"success":False}
    collectionId = request.args.get('collectionId')
    
    # return if collection id is not set
    if not collectionId:
        response['message'] = "Collection Id is not set."
        print("Collection Id is not set.")
        print("----------AI Training Process Completed----------")
        return json.dumps(response)
    
    csvHandler.createCsv(collectionId, averageNoOfFrame)
    dir_path = './ai_csv/'+collectionId
    if not(os.path.exists(dir_path)):
        response['message'] = "Collection has no data"
        print("Collection has no data.")
        print("----------AI Training Process Completed----------")
        model_path = './ai_model/'+collectionId+'.h5'
        modelInfo_path = './ai_model/'+collectionId+'.txt'
        if os.path.exists(dir_path):
            os.remove(dir_path)
        if os.path.exists(modelInfo_path):
            os.remove(modelInfo_path)
        return json.dumps(response)

    modelInfo = { 'lastUpdate': '',
                  'accuracy': '',
                  'loss': '',
                  'val_accuracy': '',
                  'val_loss': ''}

    # train model in background thread
    train_thread = threading.Thread(target=scTrain.train, args=(collectionId, False, averageNoOfFrame))
    train_thread.daemon = True
    train_thread.start()
    
    response['modelInfo'] = modelInfo
    response['success'] = True
    return json.dumps(response)

@app.route('/modelInfo', methods = ['GET','POST'])
def modelInfo():
    collectionId = 'hksign'
    
    collectionId = request.args.get('collectionId')
    
    path = './ai_model/'+collectionId+'.txt'

    # return if collection id is not set
    if not collectionId or not os.path.exists(path):
        info = { 'lastUpdate': '',
                  'accuracy': '', 
                  'loss': '', 
                  'val_accuracy': '', 
                  'val_loss': '' }
        modelInfo = {'modelInfo': info}
        return json.dumps(modelInfo)

    
    info_json = open(path, 'r').read()
    info = json.loads(info_json)
    modelInfo = {'modelInfo': info}
    return json.dumps(modelInfo)


# predict data
@app.route('/predict',methods = ['GET','POST'])
def predict():
    print("----------AI Prediction Start----------")
    data = {"success": False}

    requestObj = request.form.get('sign')

    # return if no request parameters
    if not requestObj:
        data["message"] = "No request object."
        print("Error: No request object")
        print("----------AI Prediction Completed----------")
        return json.dumps(data)

    # get the request parameters
    sign = request.form['sign']
    framesData = json.loads(sign)['frames']
    collectionId = json.loads(sign)['collectionId']
    
    # convert json to csv
    framesData_json = json.dumps(framesData)
    df = pd.read_json(framesData_json)
    df.to_csv(r'temp.csv', index = None, header=True)
    print("JSON is converted to a temporary file 'temp.csv'")

    # get the predict data and get the output from AI
    predict_data = pd.read_csv('temp.csv')
    
    # print(framesData)
    # data["prediction"] = ['testing','predict']
    data["prediction"] = scPredict.predict(collectionId, predict_data, averageNoOfFrame)
    data["success"] = True

    os.remove('temp.csv')

    print(json.dumps(data, ensure_ascii=False))
    return json.dumps(data, ensure_ascii=False)


if __name__=='__main__':
    app.run('0.0.0.0')