import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pystache

from dotenv import load_dotenv  
import os  

load_dotenv()  

with open('product_data.json') as f:
    data = json.load(f)

with open('email_template.mustache') as f:
    template = f.read()

msg = MIMEMultipart()
msg['Subject'] = 'Exciting new products!'
msg['From'] = os.getenv('EMAIL_ADDRESS')  
msg['To'] = 'recipient_email@example.com'

html = pystache.render(template, {'products': data})
msg.attach(MIMEText(html, 'html'))

for product in data:
    with open(product['image_url'], 'rb') as fp:
        img = MIMEImage(fp.read())
        msg.attach(img)

with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD')) 
    server.sendmail(msg['From'], msg['To'], msg.as_string())
