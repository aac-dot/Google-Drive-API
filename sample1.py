# import pandas as pd
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
import io
from googleapiclient.errors import HttpError


os.system('clear')

CREDENTIAL = './key.json'

scope = ['https://www.googleapis.com/auth/drive']
service_account_key = CREDENTIAL

def getDriveConnection(serviceAccountKey):
    credentials = service_account.Credentials.from_service_account_file(
        filename=serviceAccountKey,
        scopes=scope)

    service = build('drive', 'v3', credentials=credentials)

    return service

def listAll():
    service = getDriveConnection(service_account_key)

    results = service.files().list(pageSize=1000,
                                   fields="nextPageToken, files(id, name, mimeType, fileExtension)").execute()

    if results:
        items = results.get('files', [])

    return items
#print(dir(service))
#print(dir(service.drives))
def downloadAllFiles(files):
    pass

def downloadFile(fileId, fileName=None, fileExtension=None):
    try:
        # downloadedFile = open(f'file_{fileId}.pdf', 'w')
        service = getDriveConnection(serviceAccountKey=service_account_key)
        requestFile = service.files().get_media(fileId=fileId)

        file = io.FileIO(f'{fileName}', mode='wb')

        downloader = MediaIoBaseDownload(file, requestFile)
        done = False

        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}.")

    except Exception as e:
        print(f'Error: {e}')
        file = None
        return
    
    #downloadedFile.write(file.getvalue())
    # print(file.getvalue())


def emptyTrash():
    service = getDriveConnection(service_account_key)
    service.files().emptyTrash().execute()

def deleteFiles(files):
    service = getDriveConnection(serviceAccountKey=service_account_key)

    for file in files:
        response = service.files().delete(fileId=file['id']).execute()
        if response:
            print('OK')
    
# print(listAll())
files = listAll()
for file in files:
    downloadFile(file['id'], fileName=file['name'])

##deleteFiles(files)
#emptyTrash()