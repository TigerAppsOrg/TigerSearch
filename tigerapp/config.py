# ----------------------------------------------------------------------
# config.py
# Authors: Anagha Rajagopalan, Mandy Lin, Moin Mir, and Omar El-Kishky
# ----------------------------------------------------------------------
import os

class Config:
    SECRET_KEY = 'tiger_search_cos_333'
    # SQLALCHEMY_DATABASE_URI ='sqlite:///site.db'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/tigersearch'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # ENV = 'development'
    # DEBUG = True
    # TESTING = True

CLOUD_NAME= os.environ.get('CLOUD_NAME')
API_KEY= os.environ.get('API_KEY')
API_SECRET= os.environ.get('API_SECRET')
SENDGRID_API_KEY= os.environ.get('SENDGRID_API_KEY')
DEFAULT_SENDER= os.environ.get('DEFAULT_SENDER')

# NUM_TAGS = 21 (this is hard-coded in scripts.js)
DAYS_UNTIL_EXPIRE = 30
RENEWAL_THRESHOLD = 7
SCHEDULER_FREQ = 24  # in hours
# max chars
MAX_DESCRIPTION = 1000
MAX_TITLE = 50
MAX_LOCATION = 50

ADMIN_NETID = ['tigersearch']

DEFAULT_IMAGE = "https://res.cloudinary.com/drcv8tnqh/image/upload/v1635815196/rywyprm1prwnwcp13vgo.jpg"
