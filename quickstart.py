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
        # Recorrer la lista de mensajes obtenidos mediante el Método list()
        for message in messages:
            #Solicitud de una nueva respuesta, esta vez por un método get() a partir de los id obtenidos con la lista, 
            #al parecer este método no funciona sin el message id, y el mismo se obtiene sólo con un list() 
            # el new_response es un diccionario.
            new_response = service.users().messages().get(userId='me', id=message['id'], format='metadata', metadataHeaders=['Date','From','Subject']).execute()
            #Se inicia la navegación en los índices para llegar a los headers que es lo que nos interes almacenar 
            for payload in new_response:
                payload = new_response.get('payload')
            for headers in payload: 
                headers = payload.get('headers')
            for array in headers:
                date = array
                from_ = array
                subject = array
                if array.get('name')=='Date':
                    delete = date.pop('name')
                    date_value = date.get('value')
                if array.get('name')=='From':
                    delete = from_.pop('name')
                    from_value = from_.get('value')
                if array.get('name')=='Subject':
                    delete = subject.pop('name')
                    subject_value = subject.get('value') 
            print ('Id del Email: '+ message['id'])
            print ("Fecha del correo: "+date_value)
            print ("Asunto del correo : "+subject_value)
            print ("Remitente del correo :" +from_value)

           
                
                         
                         
                
if __name__ == '__main__':
    main()


# [END gmail_quickstart]
