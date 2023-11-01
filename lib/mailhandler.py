"""IMAP Mail handler"""

import imaplib
from email.parser import BytesParser

from confs import *

class Mail:
    """Class to represent mail information"""
    def __init__(self, imap_message_id, message_id, sent_date, msg):
        self.imap_message_id = imap_message_id
        self.message_id = message_id
        self.sent_date = sent_date
        self.msg = msg

class MailHandler:
    """Class to handle IMAP email interaction"""
    def __init__(self):
        if SECURITY == "ssl":
            self.imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        elif SECURITY == "starttls":
            self.imap = imaplib.IMAP4(IMAP_SERVER, IMAP_PORT)
            self.imap.starttls()
        else:
            raise ValueError("Invalid security configuration: should be either 'ssl' or 'starttls'")

        self.imap.login(USERNAME, PASSWORD)

        mailbox = '"All Mail"'
        self.imap.select(mailbox, True)

    def get_matches(self, search, since):
        """Search for emails in the mailbox (you can specify search criteria)"""
        # IMAP Search format (https://www.rfc-editor.org/rfc/rfc3501#section-6.4.4)
        search_criteria = f"{search} SINCE {since.strftime('%d-%b-%Y')}"
        status, message_ids = self.imap.search(None, search_criteria)

        matches = []

        message_id_list = message_ids[0].split()
        for message_id in message_id_list:
            status, msg_data = self.imap.fetch(message_id, "(BODY.PEEK[])")
            if status == "OK":
                email_message = BytesParser().parsebytes(msg_data[0][1])
                matches.append(Mail(message_id,
                                    email_message["Message-Id"],
                                    email_message["Date"],
                                    email_message))

        return matches

    def close(self):
        """Closing the IMAP connection"""
        self.imap.close()
        self.imap.logout()
