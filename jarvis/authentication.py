import os
import sys
import httplib2
import base64

from apiclient import errors
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

def _gmail_authentication():
    client_secrets_file = 'client_secret.json'
    client_secrets_file = os.path.abspath(os.path.join(os.getcwd(), 
                                          client_secrets_file))

    youtube_scope = "https://www.googleapis.com/auth/gmail.readonly"
    missing_client_message = "You need to populate the client_secrets.json!"

    flow = flow_from_clientsecrets(client_secrets_file,
            scope=youtube_scope)

    storage = Storage("{}-oauth2.json".format(sys.argv[0]))
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, argparser.parse_args())

    return build('gmail', 
                 'v1', 
                 http=credentials.authorize(httplib2.Http()))

def get_messages():
    service = _gmail_authentication()
    try:
        response = service.users().messages().list(userId='me', labelIds='INBOX').execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId='me', pageToken=page_token).execute()

            messages.extend(response['messages'])
        for message in messages:
            message = service.users().messages().get(userId='me',
                                                     id=message['id']).execute()
        
        print(message['payload'].keys())

    except errors.HttpError as error:
        print('An error occured: {}'.format(error))

if __name__ == '__main__':
    get_messages()
