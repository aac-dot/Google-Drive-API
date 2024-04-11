import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
import io
from googleapiclient.errors import HttpError

CREDENTIAL = 'credentials.json'

scope = ['https://www.googleapis.com/auth/drive']
service_account_key = CREDENTIAL

credentials = service_account.Credentials.from_service_account_file(
    filename=CREDENTIAL,
    scopes=scope)

service = build('drive', 'v3', credentials=credentials)

results = service.files().list(pageSize=1000, fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)", q='name contains "de"').execute()

items = results.get('files', [])

#print(dir(service))
#print(dir(service.drives))
print(results)
print(items)
