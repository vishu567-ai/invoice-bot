# -*- coding: utf-8 -*-
import os
import base64
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def fetch_invoice_emails():
    service = authenticate_gmail()
    results = service.users().messages().list(
        userId='me',
        q='subject:invoice has:attachment',
        maxResults=10
    ).execute()

    messages = results.get('messages', [])
    downloaded_files = []

    if not messages:
        return []

    os.makedirs('invoices', exist_ok=True)

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        parts = msg.get('payload', {}).get('parts', [])

        for part in parts:
            if part.get('filename') and part['filename'].endswith(('.pdf', '.png', '.jpg', '.jpeg')):
                attachment_id = part['body'].get('attachmentId')
                if attachment_id:
                    attachment = service.users().messages().attachments().get(
                        userId='me',
                        messageId=message['id'],
                        id=attachment_id
                    ).execute()

                    file_data = base64.urlsafe_b64decode(attachment['data'])
                    file_path = os.path.join('invoices', part['filename'])

                    with open(file_path, 'wb') as f:
                        f.write(file_data)

                    downloaded_files.append(file_path)

    return downloaded_files