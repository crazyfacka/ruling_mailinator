"""Configuration handler"""
import json
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(f'{__location__}/confs.json') as f:
    loaded_confs = json.load(f)

IMAP_SERVER = loaded_confs["email"]["imap"]["server"]
IMAP_PORT = loaded_confs["email"]["imap"]["port"]

SMTP_SERVER = loaded_confs["email"]["smtp"]["server"]
SMTP_PORT = loaded_confs["email"]["smtp"]["port"]

USERNAME = loaded_confs["email"]["username"]
PASSWORD = loaded_confs["email"]["password"]

DB_HOST = loaded_confs["db"]["host"]
DB_NAME = loaded_confs["db"]["database"]
DB_USER = loaded_confs["db"]["user"]
DB_PASSWORD = loaded_confs["db"]["password"]
