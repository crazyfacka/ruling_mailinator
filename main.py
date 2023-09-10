"""Where all the magic happens"""

import argparse
from datetime import datetime
import sys

from lib.storage import Storage
from lib.mailhandler import MailHandler
from lib.maildispatcher import send_mail
from rules import RULES

parser = argparse.ArgumentParser(
    description='Given some rules, parses an IMAP inbox, storing state in a PSQL DB and performs some actions',
    epilog='CFK ♡ 2023')

parser.add_argument('--set-since', help='Will set a new SINCE filter date and exit (Format: DD-MM-YYYY)')
args = parser.parse_args()

# Connect to backend storage
state = Storage()

# Update with new date, and exit
if args.set_since is not None:
    try:
        since = datetime.strptime(args.set_since, "%Y-%m-%d")
    except Exception as e:
        print("Error:", e)
        sys.exit()

    state.set_last_check_date(since)
    state.close()

    print("New starting date set:", since)
    sys.exit()

# Check last update
last_check = state.get_last_check_date()

processed_messages = 0
mh = MailHandler()
for rule in RULES:
    matches = mh.get_matches(rule["search"], last_check)
    actions = rule["action"].split()

    if actions[0] == "FORWARD":
        for match in matches:
            processed = state.validate_message_id(match.message_id)
            if not processed:
                send_mail(match.msg, actions[1])
                state.set_message_validated(match.message_id)
                processed_messages += 1

print("Number of processed messages:", processed_messages)

mh.close()
state.close()
