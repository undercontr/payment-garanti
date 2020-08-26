import os


class Config(object):
    SECRET_KEY = 'd73626094f1e438e8ec5b07128e71899'
    SQLALCHEMY_DATABASE_URI = 'mysql://test:test@localhost:3306/payment'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "webmaster@analitikkimya.com.tr"
    MAIL_PASSWORD = "Anw6318A."
    MAIL_DEBUG = False
    ADMINS = ['webmaster@analitikkimya.com.tr']
    LANGUAGES = ['en', 'tr']
    DATA_PER_PAGE = 25
    RECAPTCHA_PUBLIC_KEY = "6Lf7OVcUAAAAAGiFguM0f62nkEiBGT_trydb5DM2"
    RECAPTCHA_PRIVATE_KEY = "6Lf7OVcUAAAAAIw-7pk5A5F3VdeGoGzU45KnM56E"
