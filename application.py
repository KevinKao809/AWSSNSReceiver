from flask import Flask, request, abort
from azure.storage.blob import AppendBlobService
from datetime import datetime
import requests
app = Flask(__name__)

storageService = AppendBlobService(connection_string='DefaultEndpointsProtocol=https;AccountName=thingspronotify;AccountKey=axD13Z8R9WkPSi7mcdRUtnPfx9skMYfjf3D/vA92tcs21TOSqcJMHfc4TBvribk4Ed09kNc0EIgct8lJzYRe6w==;EndpointSuffix=core.windows.net')

@app.route("/")
def hello():
    writeToAppendBlob('ThingsPro Notify')
    return "ThingsPro Notify"

@app.route("/receiver")
def receiver():
    if 'x-amz-sns-message-type' in request.headers:
        AWS_MESSAGE_TYPE = request.headers.get('x-amz-sns-message-type')
        if AWS_MESSAGE_TYPE == 'SubscriptionConfirmation':
            postData = request.get_json(silent=True)
            subscribeURL = postData['SubscribeURL']
            writeToAppendBlob('SubscribeURL:' + subscribeURL)
            response = requests.get(subscribeURL)
            writeToAppendBlob(response)
            return
        elif AWS_MESSAGE_TYPE == 'Notification':
            postData = request.get_json(silent=True)
            writeToAppendBlob('Message:' + postData['Message'])
            return
        else:
            writeToAppendBlob('AWS Message Type Value Unmatch')
    else:
        writeToAppendBlob('AWS Message Type Not Found')
        abort()

def writeToAppendBlob(logData):
    blob = 'thingsProNotify' + '/' + datetime.utcnow().strftime("%Y%m%d") + '.log'
    logData = logData +'\r\n'
    if storageService.exists('logs',blob) != True:
        storageService.create_blob('logs', blob)
    try:
        storageService.append_blob_from_text('logs', blob, logData, encoding='utf-8')
        #print('Write to Azure Storage Append Blob')
    except:
        return

