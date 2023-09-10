"""Configuration handler"""

from lib.common import load_confs

loaded_confs = load_confs("configuration")

IMAP_SERVER = loaded_confs["email"]["imap"]["server"]
IMAP_PORT = loaded_confs["email"]["imap"]["port"]

SMTP_SERVER = loaded_confs["email"]["smtp"]["server"]
SMTP_PORT = loaded_confs["email"]["smtp"]["port"]

USERNAME = loaded_confs["email"]["username"]
PASSWORD = loaded_confs["email"]["password"]

EMAIL_FROM = loaded_confs["email"]["from"]

DB_HOST = loaded_confs["db"]["host"]
DB_NAME = loaded_confs["db"]["database"]
DB_USER = loaded_confs["db"]["user"]
DB_PASSWORD = loaded_confs["db"]["password"]
