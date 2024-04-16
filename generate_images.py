from PIL import Image, ImageDraw, ImageFont
import json
import os
import datetime

def generate_product_image(product_data):
    try:
        template_img = Image.open("image_templates/" + product_data['template']).convert('RGBA')
        product_img = Image.open(product_data['image_url']).convert('RGBA')  

        # Resize product image 
        product_img = product_img.resize((product_data['image_size']['width'], product_data['image_size']['height']))

        # Composite the product image
        product_x = product_data['image_position']['x']
        product_y = product_data['image_position']['y']
        template_img.paste(product_img, (product_x, product_y), product_img) 

        # Draw text elements 
        draw = ImageDraw.Draw(template_img)
        for element in product_data.get('text_elements', []):
            font = ImageFont.truetype(element['font'], size=element['font_size']) 
            draw.text((element['x'], element['y']), element['text'], font=font, fill=element['color'])
        
        # Draw product name
        font = ImageFont.truetype("fonts/arial.ttf", size=16)  
        draw.text((product_data['name_position']['x'], product_data['name_position']['y']), 
                  product_data['name'], font=font, fill='black')  

        # Draw product price
        font = ImageFont.truetype("fonts/arial.ttf", size=14)  
        draw.text((product_data['price_position']['x'], product_data['price_position']['y']), 
                  product_data['price'], font=font, fill='black')  
        
        if product_data.get('draw_link_outlines', False):  
            for link in product_data.get('links', []):
                draw.rectangle([link['x'], link['y'], link['x'] + link['width'], link['y'] + link['height']], outline='red') 


        # Unique filename with timestamp
        base_name, ext = os.path.splitext(product_data['image_url'])
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"{base_name}_{timestamp}{ext}"

        template_img.save(new_filename) 

    except Exception as e:
        print(f"Error generating image: {e}")

if __name__ == "__main__":
    with open('product_data.json') as f:
        data = json.load(f)
    for product in data:
        generate_product_image(product)