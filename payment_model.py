from app import db

utf8 = "utf8_general_ci"


class Payment(db.Model):

    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    ip_address = db.Column(db.String(15, utf8), nullable=False, unique=False)
    email_address = db.Column(db.String(150, utf8), nullable=True, unique=False)
    order_id = db.Column(db.String(15), nullable=False, unique=True)
    invoice_amount = db.Column(db.String(150, utf8), nullable=False, unique=False)
    status = db.Column(db.String(30, utf8), nullable=True, unique=False)
    currency = db.Column(db.String(20, utf8), nullable=False, unique=False)
    err_msg = db.Column(db.String(300, utf8), nullable=True, unique=False)
    sys_err_msg = db.Column(db.String(300, utf8), nullable=True, unique=False)
    ret_refnum = db.Column(db.String(300, utf8), nullable=True, unique=False)
    local_hash = db.Column(db.String(40, utf8), nullable=False, unique=True)
    remote_hash = db.Column(db.String(40, utf8), nullable=False)
    auth_code = db.Column(db.String(40, utf8), nullable=False)
    batch_num = db.Column(db.String(40, utf8), nullable=False)
    seq_num = db.Column(db.String(40, utf8), nullable=False)
    provision_date = db.Column(db.DateTime(), nullable=False, unique=True)
    card_number_masked = db.Column(db.String(16, utf8), nullable=False, unique=False)
    cardholder_name = db.Column(db.String(100, utf8), nullable=False, unique=False)
    card_type = db.Column(db.String(100, utf8), nullable=True, unique=False)

    invoice_id = db.Column(db.ForeignKey("invoice.invoice_id"))

    invoice = db.relationship("Invoice")


