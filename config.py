import os

class Config(object):
    SECRET_KEY=os.environ.get('SECRET_KEY') or b'}\xecUG\x9f\xf9\x18\xfaVQ$k\xf3RJ\xe4'

    MONGODB_SETTINGS = {
        'db': 'OCRSdb',
        'host': 'mongodb+srv://kira:Ilovesh221b.@ocrsflask.o9arh10.mongodb.net/OCRSdb?retryWrites=true&w=majority'
    }