# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort, request
import AzureStorageClass
import io, os

_storageConnectionString = os.environ.get("StorageConnectionString", "eventNotify")
_storageContainer = os.environ.get("StorageContainer", "myContainer")
#_storageAgent = AzureStorageClass.AzureStorage(_storageConnectionString, _storageContainer)

app = Flask(__name__)

#get /test
@app.route('/test', methods=['GET'])
def get_personGroups():  
    return '{"code":0}'  
        
#post /personGroups/{personGroupId}/persons
@app.route('/personGroups/<string:personGroupId>/persons', methods=['POST'])
def create_person_into_personGroupId(personGroupId):  
    postData = None
    try:
        postData = str(request.get_json(silent=True))
    except:
        abort(400)
    callStatus, returnData = _faceAgent.createPerson(personGroupId, postData)
    if callStatus == 200:
        return returnData
    else:
        abort(callStatus)
        
       
        
#post /personGroups/<string:personGroupId>/identifyImageObject
@app.route('/personGroups/<string:personGroupId>/identifyImageObject', methods=['POST'])
def face_identify_by_imageObject(personGroupId):    
    imageData = None
    if 'photo.jpg' in request.files:
        imageData = request.files['photo.jpg']
    else:
        imageData = io.BytesIO(request.get_data())
    callStatus, returnData = _faceAgent.identifyFaceByImageObject(_storageAgent, personGroupId, imageData)
    if callStatus == 200:
        return returnData
    else:
        abort(callStatus)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)