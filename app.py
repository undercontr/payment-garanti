import hashlib
from datetime import datetime
from random import randint

from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from pos_model import GarantiPOS
from config import Config
import xml.etree.ElementTree as XML

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

from payment_model import Payment
from invoice_model import Invoice


@app.route('/')
def index():
	# db.drop_all()
	# db.create_all()
	return str("DB RESET")


@app.route("/addPayment", methods=["GET", "POST"])
def add_payment():
	data = request.form

	invoice = Invoice()

	if request.method == "GET":
		return render_template("add_payment.html")

	if request.method == "POST":
		invoice.invoice_no = data.get("invoice_no")
		invoice.company_title = data.get("company_title")
		invoice.email = data.get("email")
		invoice.billing_address = data.get("billing_address")
		invoice.shipping_address = data.get("shipping_address")
		invoice.price_info = data.get("price_info")
		invoice.payment_type = data.get("payment_type")
		invoice.amount = data.get("amount")
		invoice.currency = data.get("currency")

		invoice.status = "NOT PAID"

		invoice.url = hashlib.md5(str.encode(invoice.amount + invoice.company_title + invoice.invoice_no)).hexdigest()

		db.session.add(invoice)
		db.session.commit()


		return redirect(url_for("view_payment", url=invoice.url))


@app.route("/viewPayment/<url>", methods=["GET"])
def view_payment(url):

	invoice = Invoice()

	invoice = invoice.query.filter_by(url=url).first()

	if len(invoice.payment) > 1:
		payment = invoice.payment[-1]
	elif len(invoice.payment) == 1:
		payment = invoice.payment[0]
	else:
		payment = invoice.payment

	return render_template("view_payment.html", data=invoice, payment=payment, amount=invoice.get_amount)


@app.route("/editPayment/<url>", methods=["GET", "POST"])
def edit_payment(url):

	invoice = Invoice.query.filter_by(url=url).first()
	data = request.form

	if request.method == "GET":
		return render_template("edit_payment.html", data=invoice)

	if request.method == "POST":
		invoice.invoice_no = data.get("invoice_no")
		invoice.company_title = data.get("company_title")
		invoice.email = data.get("email")
		invoice.billing_address = data.get("billing_address")
		invoice.shipping_address = data.get("shipping_address")
		invoice.price_info = data.get("price_info")
		invoice.payment_type = data.get("payment_type")
		invoice.amount = data.get("amount")
		invoice.currency = data.get("currency")
		invoice.status = data.get("status")
		invoice.url = hashlib.md5(str.encode(invoice.amount + invoice.company_title + invoice.invoice_no)).hexdigest()

		db.session.commit()

		return redirect(url_for("list_payments"))


@app.route("/listPayments", methods=["GET"])
def list_payments():
	pay = Payment.query.all()
	inv = Invoice.query.all()

	return render_template("list_payments.html", data_p=pay, data_i=inv)

@app.route("/invActivity/<url>", methods=["GET"])
def inv_activity(url):

	inv = Invoice()

	inv = inv.query.filter_by(url=url).first()

	data = inv.payment

	return render_template("inv_activity.html", data=data, inv=inv)


@app.route('/Payment/<url>', methods=["GET", "POST"])
def payment_index(url):
	# db.drop_all()
	# db.create_all()
	pos = GarantiPOS()
	pay = Payment()
	invoice = Invoice()
	invoice = invoice.query.filter_by(url=url).first()

	if len(invoice.payment) > 1:
		payment = invoice.payment[-1]
	elif len(invoice.payment) == 1:
		payment = invoice.payment[0]
	else:
		payment = invoice.payment

	if request.method == "GET":
		return render_template("payment_index.html", data=invoice, payment=payment, amount=pos.amount)

	if request.method == "POST":
		random_id = randint(0, 999999999)
		random_id2 = randint(0, 999999999)

		data = request.form

		params = dict()
		params["IPAddress"] = request.remote_addr
		params["EmailAddress"] = invoice.email
		params["OrderID"] = str(random_id) if str(random_id) not in [x.order_id for x in Payment.query.all()] else str(
			random_id2)
		params["CardNumber"] = str(data.get("number")).replace(" ", "")
		params["CardExpireDate"] = str(data.get("expiry")).replace(" / ", "")
		params["CardCVV2"] = str(data.get("cvc"))
		params["TransactionAmount"] = invoice.amount

		pos.CurrencyCode = invoice.currency

		pos.set_params(params)
		result = pos.pay()

		res_xml = XML.fromstring(result)

		pay.ip_address = params["IPAddress"]
		pay.email_address = invoice.email
		pay.order_id = params["OrderID"]
		pay.currency = invoice.currency
		pay.status = res_xml.findtext("Transaction/Response/Message")
		pay.err_msg = res_xml.findtext("Transaction/Response/ErrorMsg")
		pay.sys_err_msg = res_xml.findtext("Transaction/Response/SysErrMsg")
		pay.ret_refnum = res_xml.findtext("Transaction/RetrefNum")
		pay.local_hash = pos.HashData
		pay.remote_hash = res_xml.findtext("Transaction/HashData")
		pay.auth_code = res_xml.findtext("Transaction/AuthCode")
		pay.batch_num = res_xml.findtext("Transaction/BatchNum")
		pay.seq_num = res_xml.findtext("Transaction/SequenceNum")
		pay.provision_date = datetime.strptime(res_xml.findtext("Transaction/ProvDate"), "%Y%m%d %H:%M:%S")
		pay.card_number_masked = res_xml.findtext("Transaction/CardNumberMasked")
		pay.cardholder_name = res_xml.findtext("Transaction/CardHolderName")
		pay.card_type = res_xml.findtext("Transaction/CardType")
		pay.invoice_amount = pos.amount(params["TransactionAmount"], pos.CurrencyCode)

		if pay.status == "Approved":
			invoice.status = "PAID"

		pay.invoice_id = invoice.invoice_id

		db.session.add(pay)
		db.session.commit()

		return redirect(url_for("payment_index", url=invoice.url))


if __name__ == '__main__':
	app.run()
