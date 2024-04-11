import os

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


'''
This class is responsible for the credential and connect to the google drive service
'''

class GoogleDriveService:
    
    def __init__(self):
        self.__SCOPES = ['https://www.googleapis.com/auth/drive', 
                         'https://www.googleapis.com/auth/drive.appdata',
                         'https://www.googleapis.com/auth/drive.file',
                         'https://www.googleapis.com/auth/drive.metadata',
                         'https://www.googleapis.com/auth/drive.metadata.readonly',
                         'https://www.googleapis.com/auth/drive.photos.readonly',
                         'https://www.googleapis.com/auth/drive.readonly']

        _base_path = os.path.dirname(__file__)
        _credential_path = os.path.join(_base_path, 'local-storm-415112-e6c15bea688c.json')
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = _credential_path

    def build(self):

        credential = ServiceAccountCredentials.from_json_keyfile_name(
            os.getenv('GOOGLE_APPLICATION_CREDENTIALS'), 
            self.__SCOPES)
        
        service = build('drive', 'v3', credentials=credential)

    

        return service
