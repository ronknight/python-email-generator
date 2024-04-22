from PIL import Image, ImageDraw, ImageFont, ImageColor
import json
import os
import datetime

class ProductImageGenerator:
    def __init__(self, template_path, product_data_path):
        self.product_data_path = product_data_path
        self.template_img = None
        self.draw = None
        self.products = []
        self.text_elements = []
        self.template_name = None  # Added template_name attribute

    def load_product_data(self):
        with open(self.product_data_path) as f:
            data = json.load(f)
            self.template_name = data['template']  # Extract template name from JSON
            self.text_elements = data['text_elements']
            self.products = data['products']

    def load_template_image(self):
        # Construct full path to the template image
        template_path = os.path.join("images", self.template_name)
        self.template_img = Image.open(template_path).convert('RGBA')
        self.draw = ImageDraw.Draw(self.template_img)

    def generate_product_image(self, product_data, index, total_products, spacing):
        try:
            # Load the product image and resize
            product_img = Image.open(product_data['image_url']).convert('RGBA')
            max_product_width = self.template_img.width // total_products
            max_product_height = int(self.template_img.height * 0.7)
            ratio = min(max_product_width / product_img.width, max_product_height / product_img.height)
            product_img = product_img.resize((int(product_img.width * ratio), int(product_img.height * ratio)))

            # Calculate product's y-coordinate (align to bottom)
            product_y = self.template_img.height - product_img.height - 30

            # Calculate product's x-coordinate (with spacing)
            product_x = int(spacing * (index + 1) - product_img.width // 2)

            # Paste product image
            self.template_img.paste(product_img, (product_x, product_y), product_img)

            # Load font
            price_font = ImageFont.truetype("fonts/impact.ttf", size=18)

            # Draw the product price
            price_text = product_data['price']
            price_bbox = price_font.getbbox(price_text)
            price_width = price_bbox[2] - price_bbox[0]
            price_height = price_bbox[3] - price_bbox[1]
            price_x = product_x + (product_img.width - price_width) // 2
            price_y = product_y - price_height  # Adjusted to be above the product image
            # Adjust position slightly lower
            price_y += 80
            price_x += -30

            # Load the sticker image
            sticker_img = Image.open("images/sticker.png")

            # Calculate aspect ratio
            sticker_aspect_ratio = sticker_img.width / sticker_img.height

            # Calculate sticker size proportional to price text size
            sticker_width = price_width + 85  # Add some padding
            sticker_height = int(sticker_width / sticker_aspect_ratio)

            sticker_img = sticker_img.resize((sticker_width, sticker_height))

            # Paste sticker image
            self.template_img.paste(sticker_img, (price_x - 9, price_y - 8), sticker_img)

            # Draw text on top of sticker
            self.draw.text((price_x, price_y), price_text, font=price_font, fill='red')

            # Calculate the position for the additional information
            other_info_text = product_data.get('other_info', '')  # Get the additional information from product_data
            other_info_bbox = price_font.getbbox(
                other_info_text)  # Calculate the bounding box for the additional information
            other_info_width = other_info_bbox[2] - other_info_bbox[
                0]  # Calculate the width of the additional information text
            other_info_height = other_info_bbox[3] - other_info_bbox[
                1]  # Calculate the height of the additional information text
            other_info_x = product_x + (
                    product_img.width - other_info_width) // 2  # Calculate the x-coordinate for the additional information
            other_info_y = product_y - other_info_height - 10  # Calculate the y-coordinate for the additional information, 10 pixels above the product image

            other_info_y += 90
            other_info_x += 45

            other_info_font = ImageFont.truetype("fonts/arial.ttf", size=15)

            # Draw the additional information text beside the price
            self.draw.text((other_info_x, other_info_y), other_info_text, font=other_info_font, fill='white')

            # Load font
            name_font = ImageFont.truetype("fonts/arial.ttf", size=16)

            # Draw product name with blue background below the product image
            text_bbox = name_font.getbbox(product_data['name'])
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            background_width = text_width + 4
            background_height = text_height + 4
            x1 = product_x
            y1 = product_y + product_img.height  # Adjusted for the text to be below the product image
            x2 = x1 + background_width
            y2 = y1 + background_height
            background_color = ImageColor.getrgb("#003366")
            self.draw.rectangle([x1, y1, x2, y2], fill=background_color)

            # Draw text with slight offset within the background
            self.draw.text((product_x, y1),
                           product_data['name'], font=name_font, fill='white')


        except Exception as e:
            print(f"Error generating image: {e}")

    def draw_text_elements(self):
        # Calculate total width required for all text elements
        total_width = sum(ImageFont.truetype(text_element['font'], size=text_element['font_size']).getbbox(text_element['text'])[2] - ImageFont.truetype(text_element['font'], size=text_element['font_size']).getbbox(text_element['text'])[0] for text_element in self.text_elements)
        # Calculate total height of text elements
        max_height = max(ImageFont.truetype(text_element['font'], size=text_element['font_size']).getbbox(text_element['text'])[3] - ImageFont.truetype(text_element['font'], size=text_element['font_size']).getbbox(text_element['text'])[1] for text_element in self.text_elements)
        # Calculate spacing between text elements
        spacing = (self.template_img.width - total_width) / (len(self.text_elements) + 1)
        # Start x-coordinate for the first text element
        current_x = (self.template_img.width - total_width - spacing * (len(self.text_elements) - 1)) / 2
        # Set a default value for y-coordinate
        default_y = 0
        # Iterate over each text element
        for text_element in self.text_elements:
            text = text_element['text']
            font_size = text_element['font_size']
            font = ImageFont.truetype(text_element['font'], size=font_size)
            color = ImageColor.getrgb(text_element['color'])
            # Use default value if 'y' coordinate is missing
            y = text_element.get('y', default_y)
            # Calculate the width and height of the text element
            bbox = font.getbbox(text)
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            # Check if the width exceeds the template width
            if total_width > self.template_img.width:
                # If width exceeds, scale down the width of the text elements
                scale_factor = self.template_img.width / total_width
                width *= scale_factor
                height *= scale_factor
            # Draw text
            self.draw.text((current_x, y), text, font=font, fill=color)
            # Update current_x for the next text element
            current_x += width + spacing

    def generate_images(self):
        self.load_product_data()
        self.load_template_image()
        self.draw_text_elements()
        
        total_products = len(self.products)
        spacing = self.template_img.width // (total_products + 0.98)
        
        for index, product in enumerate(self.products):
            self.generate_product_image(product, index, total_products, spacing)

        output_dir = 'generated_banner'
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "template.png")
        self.template_img.save(output_path)
        print(f"Image saved at: {output_path}")

if __name__ == "__main__":
    # Load JSON data and extract template name
    with open("product_data.json") as f:
        data = json.load(f)
        template_name = data['template']

    # Create instance of ProductImageGenerator with the template name and product data path
    generator = ProductImageGenerator(template_name, "product_data.json")
    generator.generate_images()