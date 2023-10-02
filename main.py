"""Where all the magic happens"""

import argparse
from datetime import datetime, timedelta
import time
from threading import Thread, Lock
import signal
import sys

from lib.storage import Storage
from lib.mailhandler import MailHandler
from lib.maildispatcher import send_mail
from rules import RULES

lock = Lock()

def signal_handler(signo, _frame):
    """Func to handle signal"""
    print("Signal caught. Terminating application...")
    if lock.acquire(timeout=15) is False:
        print("Timeout. Forcing termination.")

    state.close()
    sys.exit(0)

def run_logic(lock = None):
    """Main application logic"""

    if lock is not None:
        lock.acquire()

    print(f"[{datetime.today()}] Fetching messages...")
    last_check = state.get_last_check_date()

    processed_messages = 0
    mh = MailHandler()
    for rule in RULES:
        matches = mh.get_matches(rule["search"], last_check)
        actions = rule["action"].split()

        if actions[0] == "FORWARD":
            for match in matches:
                processed = state.validate_message_id(match.message_id, match.sent_date)
                if not processed:
                    send_mail(match.msg, actions[1])
                    state.set_message_validated(match.message_id, match.sent_date)
                    processed_messages += 1

    new_last_check = datetime.today() - timedelta(days=1)
    state.set_last_check_date(new_last_check)
    mh.close()

    if processed_messages > 0:
        print(f"[{datetime.today()}] Number of processed messages: {processed_messages}")

    if lock is not None:
        lock.release()

parser = argparse.ArgumentParser(
    description='Given some rules, parses an IMAP inbox, storing state in a PSQL DB and performs some actions',
    epilog='CFK ♡ 2023')

parser.add_argument('-c', '--cron',
                    type=int,
                    dest='minutes',
                    help='Leave the application in the backgroud, and do a check every [1-20] minutes')
parser.add_argument('--set-since',
                    help='Will set a new SINCE filter date and exit (Format: YYYY-MM-DD)')

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

if args.minutes is None:
    run_logic()
    state.close()
else:
    if args.minutes < 1 or args.minutes > 20:
        print("Invalid value for minutes. Defaulting to every 5 minutes.")
        args.minutes = 5

    print(f"Ruling Mailinator: Executing every {args.minutes} minutes...")
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    thread_alive_count = 0

    t = Thread(target=run_logic, args=(lock,))
    t.start()
    while True:
        time.sleep(60 * args.minutes)
        if t.is_alive():
            thread_alive_count += 1
            if thread_alive_count >= 5:
                print("Thread probably has zombied out. Killing application...")
                state.close()
                sys.exit(-1)

            print("Thread is still alive, sleeping again...")
            continue

        thread_alive_count = 0
        t = Thread(target=run_logic, args=(lock,))
        t.start()
