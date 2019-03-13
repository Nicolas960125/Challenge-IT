#Challenge Desarrollo Prueba Técnica Convocatoria IT - Mercado Libre Colombia-2019
#Presenta: Nicolás Ayala Rivas
# Copyright 2018 Google LLC
#

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import email
from apiclient import errors


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.metadata']

def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    #1er Llamado a la API de Gmail buscando los ids de correos con criterio específico DevOps
    response = service.users().messages().list(userId='me',q='DevOps').execute()
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])
    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId='me', q='DevOps', pageToken='nextPageToken').execute()
        messages.extend(response['messages'])
    if not messages:
        print('No se encontraron mensajes :(')
    else:
        print('Mensajes Encontrados:')
        for message in messages:
            print('Id del Email: '+ message['id'])
            new_response = service.users().messages().get(userId='me', id=message['id'], format='metadata', metadataHeaders=['from','Subject','Date']).execute()
            print (new_response)
                
if __name__ == '__main__':
    main()


# [END gmail_quickstart]
