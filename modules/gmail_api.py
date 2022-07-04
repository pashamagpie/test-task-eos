import base64
import pickle
import re
import time

from googleapiclient.discovery import build

SCOPES = ['https://mail.google.com/']


class GmailAPI:

    def __init__(self):
        with open('modules/token.pickle', 'rb') as token:
            self.credentials = pickle.load(token)

        self.service = build('gmail', 'v1', credentials=self.credentials)

    def get_confirmation_code(self, wait_time: int = 10):
        start = time.time()
        while int(time.time() - start) < wait_time:
            result = self.service.users().messages().list(userId='me').execute()
            messages = result.get('messages')

            if messages is not None:
                msg = self.service.users().messages().get(userId='me', id=messages[0]['id']).execute()
                payload = msg['payload']
                headers = payload['headers']
                title = [i['value'] for i in headers if 'Subject' in i['name']][0]
                if 'EOS Crop Monitoring - Verify your email' in title:
                    code = self._parse_message(payload)
                    return code[0]
        return None

    def remove_all_emails(self):
        result = self.service.users().messages().list(userId='me').execute()

        if result['resultSizeEstimate'] > 0:
            for i in range(len(result['messages'])):
                email_id = result['messages'][i]['id']
                self.service.users().messages().delete(userId='me', id=email_id).execute()

    @staticmethod
    def _parse_message(payload):
        parts = payload.get('parts')
        message_data = parts[0]['body']['data']
        decoded_data = base64.urlsafe_b64decode(message_data)
        return re.findall('[0-9]{2}-[0-9]{2}', str(decoded_data))
