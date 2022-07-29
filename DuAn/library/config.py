from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.environ.get("KEY")
MONG_DBNAME = os.environ.get("NAME_DB")
MONGO_URI = os.environ.get("DATABASE_URL")


MAIL_SERVER='smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME= 'huuphuongtp2@gmail.com'
MAIL_PASSWORD = 'qsyikfunngmdogxn'
MAIL_USE_TLS = False
MAIL_USE_SSL = True