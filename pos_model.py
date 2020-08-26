import xml.etree.ElementTree as XML
import hashlib
import requests
import locale


class GarantiPOS:

    def __init__(self):

        #  XML pay fields
        self.Mode = "TEST"
        self.ChannelCode = "S"
        self.Version = "v0.01"
        self.ProvUserID = "PROVAUT"
        self.ProvUserPassword = "123qweASD/"
        self.SecureKey = "12345678"
        self.HashData = ""
        self.UserID = ""
        self.TerminalID = "30691297"
        self.TerminalID_Hash = "0" + self.TerminalID
        self.MerchantID = "7000679"
        self.RemoteIP = ""
        self.EmailAddress = ""  # To be filled in view function
        self.OrderID = ""
        self.CardNumber = ""
        self.CardExpireDate = ""
        self.CardCVV2 = ""
        self.TransactionType = "sales"
        self.TransactionAmount = ""
        self.CurrencyCode = "949"
        self.MotoInd = "N"

        # BIN query information
        self.CardScheme = ""
        self.BankName = ""
        self.BankURL = ""
        self.CardCountry = ""
        self.CardCountryCode = ""


        # 3D Fields
        self.SuccessURL = ""  # To be filled in view function
        self.ErrorURL = ""  # To be filled in view function

        self.ProvisionURL = "https://sanalposprov.garanti.com.tr/VPServlet"
        self.ProvisionTestURL = "https://sanalposprovtest.garanti.com.tr/VPServlet"
        self.Provision3DURL = "https://sanalposprov.garanti.com.tr/servlet/gt3dengine"
        self.Provision3DTestURL = "https://sanalposprovtest.garanti.com.tr/servlet/gt3dengine"

    def set_params(self, params: dict):
        """
        Set parameters for payment w/o 3D Secure
        :param params: Necessary parameters for payment initialize
        """
        self.RemoteIP = params["IPAddress"]
        self.EmailAddress = params["EmailAddress"]
        self.OrderID = params["OrderID"]
        self.CardNumber = params["CardNumber"]
        self.CardExpireDate = params["CardExpireDate"]
        self.CardCVV2 = params["CardCVV2"]
        self.TransactionAmount = params["TransactionAmount"]

        SecurityData = hashlib.sha1(str.encode(self.ProvUserPassword + self.TerminalID_Hash)).hexdigest().upper()
        self.HashData = hashlib.sha1(str.encode(
            self.OrderID + self.TerminalID + self.CardNumber + self.TransactionAmount + SecurityData)).hexdigest().upper()

        params["HashData"] = self.HashData

        return params

    def get_XML(self):
        GVPS_XML = XML.Element("GVPSRequest")

        Mode_XML = XML.SubElement(GVPS_XML, "Mode")
        Mode_XML.text = self.Mode

        ChannelCode_XML = XML.SubElement(GVPS_XML, "ChannelCode")
        ChannelCode_XML.text = self.ChannelCode

        Version_XML = XML.SubElement(GVPS_XML, "Version")
        Version_XML.text = self.Version

        Terminal_XML = XML.SubElement(GVPS_XML, "Terminal")

        ProvUserID_XML = XML.SubElement(Terminal_XML, "ProvUserID")
        ProvUserID_XML.text = self.ProvUserID

        HashData_XML = XML.SubElement(Terminal_XML, "HashData")
        HashData_XML.text = self.HashData

        UserID_XML = XML.SubElement(Terminal_XML, "UserID")
        UserID_XML.text = self.UserID

        ID_XML = XML.SubElement(Terminal_XML, "ID")
        ID_XML.text = self.TerminalID

        MerchantID_XML = XML.SubElement(Terminal_XML, "MerchantID")
        MerchantID_XML.text = self.MerchantID

        Customer_XML = XML.SubElement(GVPS_XML, "Customer")

        IPAddress_XML = XML.SubElement(Customer_XML, "IPAddress")
        IPAddress_XML.text = self.RemoteIP

        EmailAddress_XML = XML.SubElement(Customer_XML, "EmailAddress")
        EmailAddress_XML.text = self.EmailAddress

        Order_XML = XML.SubElement(GVPS_XML, "Order")

        OrderID_XML = XML.SubElement(Order_XML, "OrderID")
        OrderID_XML.text = self.OrderID

        Card_XML = XML.SubElement(GVPS_XML, "Card")

        CardNumber_XML = XML.SubElement(Card_XML, "Number")
        CardNumber_XML.text = self.CardNumber

        CardExpireDate_XML = XML.SubElement(Card_XML, "ExpireDate")
        CardExpireDate_XML.text = self.CardExpireDate

        CardCVV2_XML = XML.SubElement(Card_XML, "CVV2")
        CardCVV2_XML.text = self.CardCVV2

        Transaction_XML = XML.SubElement(GVPS_XML, "Transaction")

        TransType_XML = XML.SubElement(Transaction_XML, "Type")
        TransType_XML.text = self.TransactionType

        TransactionAmount_XML = XML.SubElement(Transaction_XML, "Amount")
        TransactionAmount_XML.text = self.TransactionAmount

        CurrencyCode_XML = XML.SubElement(Transaction_XML, "CurrencyCode")
        CurrencyCode_XML.text = self.CurrencyCode

        MotoInd_XML = XML.SubElement(Transaction_XML, "MotoInd")
        MotoInd_XML.text = self.MotoInd

        GVPS_Payload = XML.tostring(GVPS_XML).decode()

        return GVPS_Payload

    def pay(self):

        payloadXML = self.get_XML()

        headers = {"Content-Type": "applicaton/xml"}
        if self.Mode == "TEST":
            req = requests.post(url=self.ProvisionTestURL, headers=headers, data=payloadXML)
        elif self.Mode == "PROD":
            req = requests.post(url=self.ProvisionURL, headers=headers, data=payloadXML)
        else:
            raise (ValueError, "Lütfen doğru bir ortam kodu girin \"TEST\" veya \"PROD\". Şu anki değer: " + self.Mode)

        return req.content.decode()

    def amount(self, amount: str, currency: str):

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

    def bin_query(self):
        """

        BIN Query for the provided card. Card number will be provided within the class

        :return: JSON data of the BIN Query
        """

        payload = self.CardNumber.replace(" ", "")[:6]

        headers = {"Accept-Version": "3"}

        url = "https://lookup.binlist.net/" + payload

        response = requests.post(url, data=payload, headers=headers)

        self.CardScheme = response.json()["scheme"]
        self.CardCountry = response.json()["country"]["name"]
        self.CardCountryCode = response.json()["country"]["numeric"]
        self.BankName = response.json()["bank"]["name"]
        self.BankURL = response.json()["bank"]["url"]

        return response.json()
