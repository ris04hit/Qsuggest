# Creates icon of different size from default icon

from PIL import Image

icon = Image.open('chrome_extensions/icons/icon.png')

sizes = [16, 32, 48, 128]

for size in sizes:
    new_icon = icon.resize((size, size))
    new_icon.save(f'chrome_extensions/icons/icon{size}.png')