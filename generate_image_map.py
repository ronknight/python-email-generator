import json

def generate_image_map_html():
    with open('product_data_with_coords.json') as f:
        data = json.load(f)

    map_tag = '<map name="productmap">\n'

    for product in data:
        area_tag = f'  <area shape="rect" coords="{product["x"]},{product["y"]},{product["x"] + product["width"]},{product["y"] + product["height"]}" href="{"https://4sgm.com/product/"+ product["name"] + "/index.html"}" alt="{product["name"]}">\n'
        map_tag += area_tag
        print(area_tag) # Print the area tag after it's generated

    map_tag += '</map>\n'
    return map_tag
