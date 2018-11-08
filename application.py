from flask import Flask, request, abort
from azure.storage.blob import AppendBlobService
from datetime import datetime
import requests, json
app = Flask(__name__)

storageService = AppendBlobService(connection_string='DefaultEndpointsProtocol=https;AccountName=thingspronotify;AccountKey=axD13Z8R9WkPSi7mcdRUtnPfx9skMYfjf3D/vA92tcs21TOSqcJMHfc4TBvribk4Ed09kNc0EIgct8lJzYRe6w==;EndpointSuffix=core.windows.net')

@app.route("/")
def hello():
    writeToAppendBlob('ThingsPro Notify')
    return "ThingsPro Notify"

@app.route("/receiver", methods=['POST'])
def receiver():
    writeToAppendBlob('Receive...')
    try:
        writeToAppendBlob('111')
        if 'x-amz-sns-message-type' in request.headers:
            writeToAppendBlob('222')
            AWS_MESSAGE_TYPE = request.headers.get('x-amz-sns-message-type')
            writeToAppendBlob('333')
            if AWS_MESSAGE_TYPE == 'SubscriptionConfirmation':
                writeToAppendBlob('444')
                postData = json.loads(request.data)
                writeToAppendBlob('555')
                subscribeURL = postData['SubscribeURL']
                writeToAppendBlob('666')
                writeToAppendBlob('SubscribeURL:' + subscribeURL)
                writeToAppendBlob('777')
                response = requests.get(subscribeURL)
                writeToAppendBlob('888')
                writeToAppendBlob(response.text)
                writeToAppendBlob('999')
                return 'OK'
            elif AWS_MESSAGE_TYPE == 'Notification':
                postData = request.get_json(silent=True)
                writeToAppendBlob('Message:' + postData['Message'])
                return 'OK'
            else:
                writeToAppendBlob('AWS Message Type Value Unmatch')
                return 'OK'
        else:
            writeToAppendBlob('AWS Message Type Not Found')
            return 'AWS Message Type Not Found'
    except Exception as ex:
        writeToAppendBlob(str(ex))
        return str(ex)

def writeToAppendBlob(logData):
    blob = 'thingsProNotify' + '/' + datetime.utcnow().strftime("%Y%m%d") + '.log'
    logData = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + '> ' + logData +'\r\n'
    if storageService.exists('logs',blob) != True:
        storageService.create_blob('logs', blob)
    try:
        storageService.append_blob_from_text('logs', blob, logData, encoding='utf-8')
        #print('Write to Azure Storage Append Blob')
    except:
        return

