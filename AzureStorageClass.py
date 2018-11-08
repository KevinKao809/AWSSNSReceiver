# -*- coding: utf-8 -*-
from azure.storage.blob import BlockBlobService
import UtilityHelper

class AzureStorage:
    
    def __init__(self, connectionString, container):
        self.BlobService = BlockBlobService(connection_string=connectionString)
        nameValue = UtilityHelper.connectStringToDictionary(connectionString)
        self.AccountName = nameValue['AccountName']
        self.container = container
        
    def getBaseURL(self):
        return 'https://' + self.AccountName + '.blob.core.windows.net/'
    
    def uploadByLocalFile(self, localFullFileName, remoteBlobName):  
        self.BlobService.create_blob_from_path(self.container, remoteBlobName, localFullFileName)
        blobURL = 'https://' + self.AccountName + '.blob.core.windows.net/' + self.container + '/' + remoteBlobName
        return blobURL
    
    def uploadByStream(self, streamData, remoteBlobName):
        self.BlobService.create_blob_from_stream(self.container, remoteBlobName, streamData)
        blobURL = 'https://' + self.AccountName + '.blob.core.windows.net/' + self.container + '/' + remoteBlobName
        return blobURL
        
    def uploadByBytes(self,bytesData, remoteBlobName):
        self.BlobService.create_blob_from_bytes(self.container, remoteBlobName, bytesData)
        blobURL = 'https://' + self.AccountName + '.blob.core.windows.net/' + self.container + '/' + remoteBlobName
        return blobURL
    
    def delete(self, blobName):
        self.BlobService.delete_blob(self.container, blobName)
        
    def copy(self, sourceBlobURL, targetBlobName):
        self.BlobService.copy_blob(self.container, targetBlobName, sourceBlobURL)