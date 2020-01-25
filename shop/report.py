import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Report:
    def __init__(self, e_mail_login, e_mail_pass, storage):
        self.e_mail_login = e_mail_login
        self.e_mail_pass = e_mail_pass
        self.storage = storage

    def orders_email(self, stmp="poczta.interia.pl", port=587):
        msg = MIMEMultipart()
        msg['Subject'] = "orders"
        body = self.get_e_mail_body()
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        mail = smtplib.SMTP(stmp, port)
        mail.ehlo()
        mail.starttls()
        mail.login(self.e_mail_login, self.e_mail_pass)
        mail.sendmail(self.e_mail_login, "orders@shop.pl", text)
        mail.close()

    def get_product_name(self, product_id):
        product_db = self.storage["products"]
        return product_db.find({"_id": product_id}).next()['name']

    def get_address_info(self, customer_id):
        try:
            users_db = self.storage["users"]
            address = users_db.find({"_id": customer_id}).next()
            return f'''
Shipping address: 
Street: {address.get('Street')} 
city: {address.get('city')}
zip_code: {address.get('zip_code')}
house_number: {address.get('house_number')}
name: {address.get('name')}
surname: {address.get('surname')}
        '''
        except StopIteration:
            return ""

    def get_e_mail_body(self):
        orders_db = self.storage["orders"]
        order_list = orders_db.find({"completed": False})
        report = ""
        for order in order_list:
            report = report + "\n" + f'  Order {order.get("user_id")}  \n'
            for product_id, quantity in order['products']:
                report = report + self.get_product_name(product_id) + "  " + str(quantity) + "\n"
            report = report + self.get_address_info(order.get('user_id'))
        return report


