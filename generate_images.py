import json
from PIL import Image, ImageDraw, ImageFont

def generate_product_image(product_data):
    template_img = Image.open("image_templates/" + product_data['image_template'])
    product_img = Image.open(product_data['image_url'])

    # Resize product image if needed 
    # ...

    template_img.paste(product_img, (product_data['image_position']['x'], product_data['image_position']['y']))

    draw = ImageDraw.Draw(template_img)
    for element in product_data.get('text_elements', []):
        font = ImageFont.truetype("arial.ttf", size=element['font_size'])
        draw.text((element['x'], element['y']), element['text'], font=font, fill=element['color'])

    template_img.save(product_data['image_url'])

if __name__ == "__main__":
    with open('product_data.json') as f:
        data = json.load(f)

    for product in data:
        generate_product_image(product)
