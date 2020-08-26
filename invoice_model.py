import locale

from app import db

utf8 = "utf8_general_ci"


class Invoice(db.Model):

    invoice_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    invoice_no = db.Column(db.String(30, utf8), nullable=False, unique=False)
    amount = db.Column(db.String(150, utf8), nullable=False, unique=False)
    currency = db.Column(db.String(20, utf8), nullable=False, unique=False)
    company_title = db.Column(db.String(400, utf8), nullable=False, unique=False)
    billing_address = db.Column(db.String(2500, utf8), nullable=True, unique=False)
    shipping_address = db.Column(db.String(2500, utf8), nullable=True, unique=False)
    price_info = db.Column(db.String(2500, utf8), nullable=True, unique=False)
    payment_type = db.Column(db.String(2500, utf8), nullable=True, unique=False)
    status = db.Column(db.String(100, utf8), nullable=False, unique=False)
    email = db.Column(db.String(250, utf8), nullable=False, unique=False)
    url = db.Column(db.String(64, utf8), nullable=False, unique=True)

    payment = db.relationship("Payment")

    def get_amount(self, amount: str, currency: str):

        amount = amount[:-2] + "." + amount[-2:]

        if currency == "978":

            locale.setlocale(locale.LC_ALL, "de_DE.utf8")
            return locale.currency(float(amount), grouping=True, symbol="€")

        elif currency == "949":

            locale.setlocale(locale.LC_ALL, "tr_TR.utf8")
            return locale.currency(float(amount), grouping=True, symbol="₺")

        elif currency == "840":

            locale.setlocale(locale.LC_ALL, "en_US.utf8")
            return locale.currency(float(amount), grouping=True, symbol="$")

        else:
            return "wrong price format"
