import imaplib
import smtplib
import email
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from confs import *

# Connect to the IMAP server over SSL
imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

# Login to your email account
imap.login(USERNAME, PASSWORD)

# Select the mailbox you want to work with (e.g., INBOX)
mailbox = '"All Mail"'
imap.select(mailbox, False)

# Search for emails in the mailbox (you can specify search criteria)
search_criteria = "FROM @continente.pt SINCE 07-Sep-2023"  # You can use other criteria like "FROM example@example.com"
status, message_ids = imap.search(None, search_criteria)

# Get a list of message IDs
message_id_list = message_ids[0].split()

# Loop through the message IDs and retrieve message information
for message_id in message_id_list:
    status, msg_data = imap.fetch(message_id, "(BODY[HEADER.FIELDS (FROM TO SUBJECT DATE)])")

    if status == "OK":
        msg_raw = msg_data[0][1]
        msg = email.message_from_bytes(msg_raw)

        # Decode email subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        # Print message information
        print("From:", msg["From"])
        print("To:", msg["To"])
        print("Subject:", subject)
        print("Date:", msg["Date"])

        '''

        # Forward the email based on the FROM address
        forward_address = "your_forwarding_address@example.com"  # Replace with the forwarding address
        if msg["From"] and forward_address:
            # Create a new email to forward the message
            forward_msg = MIMEMultipart()
            forward_msg["From"] = username
            forward_msg["To"] = forward_address
            forward_msg["Subject"] = "Fwd: " + subject

            # Add the original email content as a quoted message
            quoted_msg = email.mime.text.MIMEText(msg.as_string(), "plain")
            forward_msg.attach(quoted_msg)

            # Send the forwarded email
            try:
                smtp = smtplib.SMTP(smtp_server, smtp_port)
                smtp.starttls()
                smtp.login(smtp_username, smtp_password)
                smtp.sendmail(username, forward_address, forward_msg.as_string())
                smtp.quit()
                print("Email forwarded successfully to:", forward_address)
            except Exception as e:
                print("Error forwarding email:", str(e))

        '''

        print("=" * 40)

# Logout and close the IMAP connection
imap.logout()