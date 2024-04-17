from PIL import Image, ImageDraw, ImageFont
import json
import os
import datetime

def generate_product_image(product_data, template_img, draw, index, total_products):
    try:
        # Open product image
        product_img = Image.open(product_data['image_url']).convert('RGBA')

        # Calculate maximum width and height for product images
        max_product_width = template_img.width // total_products
        max_product_height = template_img.height

        # Calculate aspect ratio
        width_ratio = max_product_width / product_img.width
        height_ratio = max_product_height / product_img.height
        ratio = min(width_ratio, height_ratio)

        # Resize product image while maintaining aspect ratio and increasing size by 50% more
        product_img = product_img.resize((int(product_img.width * ratio * 1.5), int(product_img.height * ratio * 1.5)))

        # Calculate horizontal spacing between products with equal spaces
        spacing = template_img.width // (total_products + 1)

        # Calculate vertical spacing between product image and name/price
        vertical_spacing = 20

        # Calculate the y-coordinate of the product
        product_y = (template_img.height - product_img.height - vertical_spacing - 16 - 14) // 2

        # Calculate the x-coordinate of the product
        product_x = spacing * (index + 1) - product_img.width // 2

        # Composite the product image
        template_img.paste(product_img, (product_x, product_y), product_img) 

        # Draw text elements 
        for element in product_data.get('text_elements', []):
            font = ImageFont.truetype(element['font'], size=element['font_size']) 
            draw.text((element['x'] + product_x, element['y'] + product_y), element['text'], font=font, fill=element['color'])
        
        # Draw product name
        font = ImageFont.truetype("fonts/arial.ttf", size=16)  
        draw.text((product_x, product_y + product_img.height + vertical_spacing), 
                  product_data['name'], font=font, fill='black')  

        # Draw product price
        font = ImageFont.truetype("fonts/arial.ttf", size=14)  
        draw.text((product_x, product_y + product_img.height + vertical_spacing + 16), 
                  product_data['price'], font=font, fill='black')  

        # Draw outlines of clickable links
        if product_data.get('draw_link_outlines', False):  
            for link in product_data.get('links', []):
                draw.rectangle([link['x'] + product_x, link['y'] + product_y, link['x'] + link['width'] + product_x, link['y'] + link['height'] + product_y], outline='red') 

    except Exception as e:
        print(f"Error generating image: {e}")

if __name__ == "__main__":
    with open('product_data.json') as f:
        data = json.load(f)
        template_path = "image_templates/" + data['template']
        products = data['products']

    # Open the template image
    template_img = Image.open(template_path).convert('RGBA')
    draw = ImageDraw.Draw(template_img)

    # Count total products
    total_products = len(products)
    
    for index, product in enumerate(products):
        generate_product_image(product, template_img, draw, index, total_products)
    
    # Create the directory if it doesn't exist
    output_dir = 'generated_banner'
    os.makedirs(output_dir, exist_ok=True)

    # Save the final image
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = os.path.join(output_dir, f"output_{timestamp}.png")
    template_img.save(output_path)

    print(f"Image saved at: {output_path}")
