from flask import Flask
app = Flask(__name__)

import ST7735
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont
import logging
from time import sleep
import sys

disp = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)

disp.begin()

WIDTH = disp.width
HEIGHT = disp.height

img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

font_size = 25
font = ImageFont.truetype(UserFont, font_size)
text_colour = (255, 255, 255)
back_colour = (0, 170, 170)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/message/<body>')
def message(body):
    
    message = body
    size_x, size_y = draw.textsize(message, font)

    x = (WIDTH - size_x) / 2 -2
    y = (HEIGHT / 2) - (size_y / 2)

    for i in range(int(-(WIDTH/2)), int(abs(x)+WIDTH/2), 1):
        draw.rectangle((0, 0, 160, 80), back_colour)
        draw.text((-i*2, y), message, font=font, fill=text_colour)
        disp.display(img)
    
    return body