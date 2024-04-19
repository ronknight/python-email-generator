import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pystache
from dotenv import load_dotenv

load_dotenv()

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Load product data
with open(os.path.join(script_dir, 'product_data.json')) as f:
    data = json.load(f)

# Read email template from Mustache file
with open(os.path.join(script_dir, 'email_template.mustache')) as f:
    template = f.read()

# Replace relative path with absolute path in the template
template = template.replace('generated_banner/template.png', os.path.join(script_dir, 'generated_banner/template.png'))

# Render HTML content from template
html = pystache.render(template, {'products': data})

# Create MIME message
msg = MIMEMultipart()
msg['Subject'] = 'Exciting new products!'
msg['From'] = os.getenv('EMAIL_ADDRESS')
msg['To'] = 'rona@4sgm.com'

# Attach HTML content to email
msg.attach(MIMEText(html, 'html'))

# Send email using pinoyitsolution.com SMTP server
with smtplib.SMTP('pinoyitsolution.com', 587) as server:
    server.starttls()
    server.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
    server.sendmail(msg['From'], msg['To'], msg.as_string())

print("Email sent successfully.")