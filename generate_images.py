from PIL import Image, ImageDraw, ImageFont, ImageColor
import json
import os
import datetime


def generate_product_image(product_data, template_img, draw, index, total_products, spacing):
    """
    Generates a single product image and pastes it onto the template image.

    Args:
        product_data (dict): A dictionary containing product data. It should have keys 'image_url', 'name', 'price' and optionally 'draw_link_outlines' and 'links'.
        template_img (PIL.Image.Image): The template image onto which the product image will be pasted.
        draw (PIL.ImageDraw.Draw): An instance of PIL's ImageDraw class for drawing on the template image.
        index (int): The index of the current product in the list of all products.
        total_products (int): The total number of products.
        spacing (int): The spacing between product images.

    Raises:
        Exception: If there is an error in generating the image.
    """
    try:
        # Load the product image and resize
        product_img = Image.open(product_data['image_url']).convert('RGBA')
        max_product_width = template_img.width // total_products
        max_product_height = int(template_img.height * 0.7)
        ratio = min(max_product_width / product_img.width, max_product_height / product_img.height)
        product_img = product_img.resize((int(product_img.width * ratio), int(product_img.height * ratio)))

        # Calculate product's y-coordinate (align to bottom)
        product_y = template_img.height - product_img.height - 30

        # Calculate product's x-coordinate (with spacing)
        product_x = int(spacing * (index + 1) - product_img.width // 2)

        # Paste product image
        template_img.paste(product_img, (product_x, product_y), product_img)

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
        template_img.paste(sticker_img, (price_x - 9, price_y - 8), sticker_img)

        # Draw text on top of sticker
        draw.text((price_x, price_y), price_text, font=price_font, fill='red')

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
        draw.text((other_info_x, other_info_y), other_info_text, font=other_info_font, fill='white')

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
        draw.rectangle([x1, y1, x2, y2], fill=background_color)

        # Draw text with slight offset within the background
        draw.text((product_x, y1),
                  product_data['name'], font=name_font, fill='white')


    except Exception as e:
        print(f"Error generating image: {e}")


def draw_text_elements(template_img, draw, text_elements):
    """
    Draws text elements on the template image.

    Args:
        template_img (PIL.Image.Image): The template image.
        draw (PIL.ImageDraw.Draw): An instance of PIL's ImageDraw class for drawing on the template image.
        text_elements (list): A list of dictionaries containing text element data.

    Returns:
        None
    """
    for text_element in text_elements:
        text = text_element['text']
        font_size = text_element['font_size']
        font = ImageFont.truetype(text_element['font'], size=font_size)
        color = ImageColor.getrgb(text_element['color'])
        x = text_element['x']
        y = text_element['y']

        # Draw text
        draw.text((x, y), text, font=font, fill=color)


if __name__ == "__main__":
    # Load product data from JSON file
    with open('product_data.json') as f:
        data = json.load(f)
        template_path = "images/" + data['template']
        text_elements = data['text_elements']
        products = data['products']

    # Open the template image and create a draw object
    template_img = Image.open(template_path).convert('RGBA')
    draw = ImageDraw.Draw(template_img)

    # Draw text elements on the template image
    draw_text_elements(template_img, draw, text_elements)

    # Calculate the total number of products and the spacing between them
    total_products = len(products)
    spacing = template_img.width // (total_products + 0.98)  # Adjust spacing based on total products

    # Generate and paste each product image onto the template
    for index, product in enumerate(products):
        generate_product_image(product, template_img, draw, index, total_products, spacing)

    # Create the output directory if it doesn't exist
    output_dir = 'generated_banner'
    os.makedirs(output_dir, exist_ok=True)

    # Save the final image with a timestamp in the filename
    # timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = os.path.join(output_dir, "template.png")
    template_img.save(output_path)

    print(f"Image saved at: {output_path}")
