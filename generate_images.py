from PIL import Image, ImageDraw, ImageFont
import json
import os
import datetime

# Function to generate a product image and paste it onto the template image
def generate_product_image(product_data, template_img, draw, index, total_products, padding, spacing):
    try:
        # Open the product image
        product_img = Image.open(product_data['image_url']).convert('RGBA')

        # Calculate the maximum width and height for product images
        max_product_width = template_img.width // total_products
        max_product_height = int(template_img.height * 0.8)

        # Calculate the aspect ratio
        width_ratio = max_product_width / product_img.width
        height_ratio = max_product_height / product_img.height
        ratio = min(width_ratio, height_ratio)

        # Resize the product image while maintaining the aspect ratio
        product_img = product_img.resize((int(product_img.width * ratio), int(product_img.height * ratio)))

        # Calculate the y-coordinate of the product to align it to the bottom with padding
        product_y = template_img.height - product_img.height - padding

        # Calculate the x-coordinate of the product
        product_x = int(spacing * (index + 1) - product_img.width // 2)

        # Paste the product image onto the template image with padding
        template_img.paste(product_img, (product_x - padding, product_y - padding), product_img)

        # Open the background image for the product name
        name_bg_img = Image.open('products/product-name-bg.png').convert('RGBA')

        # Paste the background image onto the template image
        name_bg_x = product_x - padding
        name_bg_y = product_y + padding
        template_img.paste(name_bg_img, (name_bg_x, name_bg_y), name_bg_img)

        # Draw the product name with white color
        font = ImageFont.truetype("fonts/arial.ttf", size=16)
        draw.text((int(product_x - padding), int(product_y + padding)),
                  product_data['name'], font=font, fill='white')

        # Draw the product price
        font = ImageFont.truetype("fonts/arial.ttf", size=14)
        draw.text((int(product_x - padding), int(product_y + 16 + padding)),
                  product_data['price'], font=font, fill='black')

        # Draw the outlines of clickable links if specified
        if product_data.get('draw_link_outlines', False):
            for link in product_data.get('links', []):
                draw.rectangle([int(link['x'] + product_x), int(link['y'] + product_y),
                                int(link['x'] + link['width'] + product_x),
                                int(link['y'] + link['height'] + product_y)], outline='red')
    except Exception as e:
        print(f"Error generating image: {e}")

# Main function to generate product images and save the final image
if __name__ == "__main__":
    # Load the product data from a JSON file
    with open('product_data.json') as f:
        data = json.load(f)
        template_path = "image_templates/" + data['template']
        products = data['products']

    # Open the template image
    template_img = Image.open(template_path).convert('RGBA')
    draw = ImageDraw.Draw(template_img)

    # Count the total number of products
    total_products = len(products)

    # Set the padding and spacing
    padding = 20
    spacing = (template_img.width - 2 * padding) // total_products

    # Generate the product images and paste them onto the template image
    for index, product in enumerate(products):
        generate_product_image(product, template_img, draw, index, total_products, padding, spacing)

    # Create the output directory if it doesn't exist
    output_dir = 'generated_banner'
    os.makedirs(output_dir, exist_ok=True)

    # Save the final image
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = os.path.join(output_dir, f"output_{timestamp}.png")
    template_img.save(output_path)

    # Print the path of the saved image
    print(f"Image saved at: {output_path}")
