import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pystache
from dotenv import load_dotenv
from generate_image_map import generate_image_map_html


load_dotenv()

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Load text_elements from product_data.json
with open('product_data.json') as f:
    data = json.load(f)
    text_elements = data.get('text_elements')

# Load product data with coordinates
with open('product_data_with_coords.json') as f:
    products_coords_data = json.load(f)  # Use a distinct name to avoid conflicts

# Load email template from Mustache file
with open('email_template.mustache') as f:
    template = f.read()

# Replace relative path with absolute path in the template
template = template.replace('generated_banner/template.png', os.path.join(os.getcwd(), 'generated_banner/template.png'))  # Ensure correct path

# Generate the image map HTML
image_map_html = generate_image_map_html()

# Render HTML content from template with product data
html = pystache.render(template, {
    'products': products_coords_data,  # Use product data with coordinates
    'image_map_html': image_map_html,
    'text_elements': text_elements
})

# Create MIME message
msg = MIMEMultipart()
msg['Subject'] = f"{text_elements[0]['text']} - {text_elements[1]['text']}"
msg['From'] = os.getenv('EMAIL_ADDRESS')
msg['To'] = 'rona@4sgm.com, mp@4sgm.com, ron.aduna@gmail.com, mparidehpour@gmail.com'

# Attach HTML content to email
msg.attach(MIMEText(html, 'html'))

# Send email using SMTP server
with smtplib.SMTP(os.getenv('EMAIL_SERVER'), 587) as server:  # Replace with your SMTP server details
    server.starttls()
    server.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
    server.sendmail(msg['From'], msg['To'], msg.as_string())

print("Email sent successfully.")