# Python Email Generator

This project is a Python-based email generator that creates and sends product promotion emails.

## Project Structure
- .env
- .gitignore
- email_template.mustache
- fonts/
    - arial.ttf
    - impact.ttf
- generate_images.py
- generated_banner/
- image_templates/
- product_data.json
- products/
- README.md
- send_email.py

## Key Files

- [`email_template.mustache`](email_template.mustache): This is the HTML template for the emails. It uses the Mustache templating language to insert product data into the email.

- [`.env`](.env): This file contains environment variables, including the email address and password used to send the emails. This file is not tracked by Git.

- [`generate_images.py`](generate_images.py): This Python script generates images for the emails.

- [`send_email.py`](send_email.py): This Python script sends the emails.

## Usage

Before running the scripts, make sure to set your email address and password in the `.env` file:

```env
EMAIL_ADDRESS=your-email@example.com
EMAIL_PASSWORD=your-password