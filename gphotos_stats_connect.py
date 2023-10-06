import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

google_photos = build('photoslibrary', 'v1', credentials=creds,static_discovery=False)

items = []
nextpagetoken = None
# The default number of media items to return at a time is 25. The maximum pageSize is 100.
while nextpagetoken != '':
    print(f"Number of items processed:{len(items)}", end='\r')
    results = google_photos.mediaItems().list(pageSize=100, pageToken=nextpagetoken).execute()
    items += results.get('mediaItems', [])
    nextpagetoken = results.get('nextPageToken', '')

for item in items:
    if('video' in item['mediaMetadata']):
        continue
    photo = item['mediaMetadata']['photo']
    if(photo):
        if(photo['focalLength'] == 1.74):
           with open ('0.5\\' + item['filename'],'wb') as f:
               f.write((requests.get(item['baseUrl'])).content)
               f.close