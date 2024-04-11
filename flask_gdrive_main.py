import io
from gdrive_service import GoogleDriveService
from googleapiclient.http import MediaIoBaseDownload

from flask import Flask

app = Flask(__name__)
print(__name__)

# @app.get('/gdrive-files')
def getFileListFromGDrive():

    selected_fields = "files(id,name,webViewLink,fileExtension,mimeType)"
    g_drive_service = GoogleDriveService().build()
    list_file = g_drive_service.files().list(fields=selected_fields).execute()

    # print(list_file, end='\n\n')
    '''
    for file in list_file.get('files'):
        if 'fileExtension' in file and file['fileExtension'] == 'txt':
            print(f'O arquivo {file['name']} tem uma extensão {file['fileExtension']}')
    '''
    return {"files": list_file.get('files')}

def downloadFilesFromDrive():
    
    files = getFileListFromGDrive()
    g_drive_service = GoogleDriveService().build()

    for file in files['files']:
        # f = g_drive_service.files().get_media(fileId=file['id'])
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            continue

        if file['mimeType'] == 'text/x-python':
            file['mimeType'] = 'text/plain'

        f = g_drive_service.files().export_media(fileId=file['id'], mimeType=file['mimeType'])
        
        fh = io.BytesIO()
        # fh = io.FileIO(file['webViewLink'], mode='r')
        
        downloader = MediaIoBaseDownload(fd=fh, request=f)

        done = False

        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}.")
    
        return file.getvalue()

if __name__ == '__main__':
    downloadFilesFromDrive()