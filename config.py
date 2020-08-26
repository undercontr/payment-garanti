import os


class Config(object):
    SECRET_KEY = 'd73626094f1e438e8ec5b07128e71899'
    SQLALCHEMY_DATABASE_URI = 'mysql://test:test@localhost:3306/payment'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
