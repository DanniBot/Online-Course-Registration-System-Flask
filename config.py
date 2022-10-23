import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    SECRET_KEY=os.environ.get('SECRET_KEY') or b'}\xecUG\x9f\xf9\x18\xfaVQ$k\xf3RJ\xe4'

    MONGODB_SETTINGS = {
        'db': 'OCRSdb',
        'host': os.environ.get('MONGODB_URI')
    }