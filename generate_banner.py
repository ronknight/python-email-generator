from PIL import Image, ImageDraw, ImageFont, ImageColor
import json
import os

class ProductImageGenerator:
    def __init__(self, template_name, product_data_path):
        self.template_name = str(template_name)  # Convert to string
        if self.template_name.isdigit():  # Check if template_name is a digit
            # Map template value "1" to "template1.png"
            if self.template_name == "1":
                self.template_name = "template1.png"
            elif self.template_name == "2":
                self.template_name = "template2.png"
            # Add more elif blocks for other template numbers as needed
        else:
            # Assume template_name is already in the correct format (e.g., "template1.png")
            pass
        self.product_data_path = product_data_path  # Assign product_data_path as an attribute

    def load_product_data(self):
        with open(self.product_data_path) as f:
            data = json.load(f)
            self.template_name = data['template']  # Extract template name from JSON
            self.text_elements = data['text_elements']
            self.products = data['products']

    def load_template_image(self):
        # Load the template image
        template_path = os.path.join("images", "template" + str(self.template_name) + ".png")
        self.template_img = Image.open(template_path).convert('RGBA')
        self.draw = ImageDraw.Draw(self.template_img)
        
        # Load the logo image
        logo_path = os.path.join("images", "4sgmlogo.png")
        logo_img = Image.open(logo_path).convert('RGBA')

        # Resize the logo to 50% of its original size
        logo_width, logo_height = logo_img.size
        new_logo_width = int(logo_width * 0.5)
        new_logo_height = int(logo_height * 0.5)
        logo_img = logo_img.resize((new_logo_width, new_logo_height))
        
        # Paste the logo onto the template image
        self.template_img.paste(logo_img, (10, 10), logo_img)

    def generate_product_image(self, product_data, index, total_products):
        try:
            # Load the product image and resize
            product_img_path = os.path.join("products", f"{product_data['name']}.png")
            product_img = Image.open(product_img_path).convert('RGBA')
            max_product_width = self.template_img.width // total_products
            max_product_height = int(self.template_img.height * 0.7)
            ratio = min(max_product_width / product_img.width, max_product_height / product_img.height)
            product_img = product_img.resize((int(product_img.width * ratio), int(product_img.height * ratio)))

            # Check if the current product is one of the last two products
            if index >= total_products - 2:
                # Calculate the maximum width and height for the last two products
                max_last_product_width = max_product_width * 1.2
                max_last_product_height = max_product_height
                # Calculate the ratio for resizing while maintaining aspect ratio
                width_ratio = max_last_product_width / product_img.width
                height_ratio = max_last_product_height / product_img.height
                # Choose the smaller ratio to ensure that both dimensions fit within the template area
                ratio = min(width_ratio, height_ratio)
            else:
                # Calculate the ratio for resizing while maintaining aspect ratio
                ratio = min(max_product_width / product_img.width, max_product_height / product_img.height)

            # Resize the product image
            product_img = product_img.resize((int(product_img.width * ratio), int(product_img.height * ratio)))

            # Calculate product's y-coordinate (align to bottom)
            product_y = self.template_img.height - product_img.height - 30

            # Calculate product's x-coordinate (with spacing)
            product_x = int((self.template_img.width / total_products) * (index + 0.5) - product_img.width / 2)

            # Apply stacking modification only if using template 2
            if self.template_name == 2 and index == total_products - 2:
                product_y -= product_img.height // 2  # Adjust y-coordinate to stack on top of the last item

            # Paste product image
            self.template_img.paste(product_img, (product_x, product_y), product_img)

            # Load font for price
            price_font = ImageFont.truetype("fonts/impact.ttf", size=18)

            # Draw the product price
            price_text = product_data['price']
            price_bbox = price_font.getbbox(price_text)
            price_width = price_bbox[2] - price_bbox[0]
            price_height = price_bbox[3] - price_bbox[1]
            # Calculate the new price position
            price_x = product_x + (product_img.width - price_width) // 2  # Center horizontally
            price_y = product_y - price_height  # Adjusted to be above the product image
            price_y += 90  # Adjust vertically (increase or decrease as needed)
            price_x += -30  # Adjust horizontally (increase or decrease as needed)

            # Load the sticker image
            sticker_img = Image.open("images/sticker.png")

            # Calculate aspect ratio
            sticker_aspect_ratio = sticker_img.width / sticker_img.height

            # Calculate sticker size proportional to price text size
            sticker_width = price_width + 85  # Add some padding
            sticker_height = int(sticker_width / sticker_aspect_ratio)

            # Make the sticker slightly smaller
            sticker_width = int(sticker_width * 0.8)
            sticker_height = int(sticker_height * 0.8)

            sticker_img = sticker_img.resize((sticker_width, sticker_height))

            # Paste sticker image
            self.template_img.paste(sticker_img, (price_x - 9, price_y - 8), sticker_img)

            # Draw text on top of sticker (current price)
            self.draw.text((price_x, price_y), price_text, font=price_font, fill='red')

            # Draw "Reg:" label
            reg_label_font = ImageFont.truetype("fonts/arial.ttf", size=8)
            reg_label_text = "Reg.: "
            reg_label_bbox = reg_label_font.getbbox(reg_label_text)
            reg_label_width = reg_label_bbox[2] - reg_label_bbox[0]
            reg_label_height = reg_label_bbox[3] - reg_label_bbox[1]
            reg_label_x = price_x  # Same x-coordinate as current price
            reg_label_y = price_y + 19 # Below the current price
            self.draw.text((reg_label_x, reg_label_y), reg_label_text, font=reg_label_font, fill='black')

            # Draw original price without the "Reg.:" label
            original_price_font = ImageFont.truetype("fonts/arial.ttf", size=8)
            original_price_text = f"{product_data['original_price']}"
            original_price_bbox = original_price_font.getbbox(original_price_text)
            original_price_width = original_price_bbox[2] - original_price_bbox[0]
            original_price_height = original_price_bbox[3] - original_price_bbox[1]
            original_price_x = price_x + reg_label_width  # Adjust x-coordinate to start after the "Reg.:" label
            original_price_y = price_y + 19  # Below the current price
            # Draw the original price with strike-through
            self.draw.text((original_price_x, original_price_y), original_price_text, font=original_price_font,
                           fill='grey')
            self.draw.line((original_price_x, original_price_y + original_price_height // 2,
                            original_price_x + original_price_width, original_price_y + original_price_height // 2),
                           fill='grey', width=1)  # Draw strike-through line

            # Calculate the position for the additional information
            discount_text = product_data.get('discount', '')  # Get the additional information from product_data
            discount_bbox = price_font.getbbox(
                discount_text)  # Calculate the bounding box for the additional information
            discount_width = discount_bbox[2] - discount_bbox[
                0]  # Calculate the width of the additional information text
            discount_height = discount_bbox[3] - discount_bbox[
                1]  # Calculate the height of the additional information text
            discount_x = product_x + (
                    product_img.width - discount_width) // 2  # Calculate the x-coordinate for the additional information
            discount_y = product_y - discount_height - 10  # Calculate the y-coordinate for the additional information, 10 pixels above the product image

            discount_y += 98
            discount_x += 17

            discount_font = ImageFont.truetype("fonts/arial.ttf", size=15)

            # Draw the additional information text beside the price
            self.draw.text((discount_x, discount_y), discount_text, font=discount_font, fill='white')

            # Load font for product name
            name_font = ImageFont.truetype("fonts/arial.ttf", size=16)

            # Add hashtag to the product name
            product_name_with_hashtag = "#" + product_data['name']
            # Draw product name with blue background below the product image
            text_bbox = name_font.getbbox(product_name_with_hashtag)
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
                           product_name_with_hashtag, font=name_font, fill='white')

            # Add the coordinates and dimensions to the product data
            product_data['x'] = product_x
            product_data['y'] = product_y
            product_data['width'] = product_img.width
            product_data['height'] = product_img.height

        except Exception as e:
            print(f"Error generating image: {e}")

    def draw_text_elements(self):
        # Load logo image to get its height
        logo_path = os.path.join("images", "4sgmlogo.png")
        logo_img = Image.open(logo_path).convert('RGBA')
        logo_height = logo_img.height

        # Calculate total width required for all text elements
        total_width = sum(
            ImageFont.truetype(os.path.join("fonts", text_element['font']), size=text_element['font_size']).getbbox(
                text_element['text'])[2] -
            ImageFont.truetype(os.path.join("fonts", text_element['font']), size=text_element['font_size']).getbbox(
                text_element['text'])[0] for text_element in self.text_elements)

        # Calculate total height of text elements
        max_height = max(
            ImageFont.truetype(os.path.join("fonts", text_element['font']), size=text_element['font_size']).getbbox(
                text_element['text'])[3] -
            ImageFont.truetype(os.path.join("fonts", text_element['font']), size=text_element['font_size']).getbbox(
                text_element['text'])[1] for text_element in self.text_elements)

        # Calculate spacing between text elements
        spacing = (self.template_img.width - total_width) / (len(self.text_elements) + 1)

        # Start x-coordinate for the first text element
        current_x = (self.template_img.width - total_width - spacing * (len(self.text_elements) - 1)) / 2

        # Set a default value for y-coordinate
        default_y = logo_height - 30  # Adjust the default y-coordinate

        # Iterate over each text element
        for text_element in self.text_elements:
            text = text_element['text']
            font_size = text_element['font_size']
            font_path = os.path.join("fonts", text_element['font'])
            font = ImageFont.truetype(font_path, size=text_element['font_size'])
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

        # Count total products
        if int(self.template_name) == 1:
            total_products = 8
        elif int(self.template_name) == 2:
            total_products = 6
        # Add more conditions for other templates

        for index, product in enumerate(self.products[:total_products]):
            self.generate_product_image(product, index, total_products)

        output_dir = 'generated_banner'
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "template.png")
        self.template_img.save(output_path)
        print(f"Image saved at: {output_path}")

        # Save the product data with the coordinates and dimensions
        with open('product_data_with_coords.json', 'w') as f:
            json.dump(self.products, f)


if __name__ == "__main__":
    # Load JSON data and extract template name
    with open("product_data.json") as f:
        data = json.load(f)
        template_name = data['template']

    # Create instance of ProductImageGenerator with the template name and product data path
    # generator = ProductImageGenerator(template_name, "product_data-layout.json")
    generator = ProductImageGenerator(template_name, "product_data.json")
    # generator = ProductImageGenerator(template_name, "product_data-2.json")


    generator.generate_images()
