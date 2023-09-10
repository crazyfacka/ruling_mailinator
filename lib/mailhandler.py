import imaplib
from email.parser import BytesParser

from confs import *

class Mail:
    def __init__(self, message_id, msg):
        self.message_id = message_id
        self.msg = msg

class MailHandler:
    def __init__(self):
        self.imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        self.imap.login(USERNAME, PASSWORD)

        mailbox = '"All Mail"'
        self.imap.select(mailbox, False)
    
    def get_matches(self, search, since):
        """Search for emails in the mailbox (you can specify search criteria)"""
        search_criteria = f"{search} SINCE {since.strftime('%d-%b-%Y')}"  # IMAP Search format (https://www.rfc-editor.org/rfc/rfc3501#section-6.4.4)
        status, message_ids = self.imap.search(None, search_criteria)

        matches = []

        message_id_list = message_ids[0].split()
        for message_id in message_id_list:
            status, msg_data = self.imap.fetch(message_id, "(RFC822)")
            if status == "OK":
                email_message = BytesParser().parsebytes(msg_data[0][1])
                matches.append(Mail(message_id.decode("utf-8"), email_message))
        
        return matches

    def close(self):
        self.imap.close()
