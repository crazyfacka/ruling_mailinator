"""Where all the magic happens"""
import argparse
from datetime import datetime
import sys

from lib.storage import Storage

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
    sys.exit()

# Check last update
last_check = state.get_last_check_date()
print(last_check.strftime('%d-%b-%Y'))

state.close()
