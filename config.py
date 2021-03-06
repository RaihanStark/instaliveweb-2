import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    VERSION = '1.6.0'

    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET_BRO'
        print('SECRET KEY ENV VAR NOT SET! SHOULD NOT SEE IN PRODUCTION')

    RETINAD_API_URL = "https://www.retinad.com/api/account/login"
    RETINAD_API_SKIP = True
class DevelopmentConfig(Config):

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite'))

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')

config = {
    'development': DevelopmentConfig,
}