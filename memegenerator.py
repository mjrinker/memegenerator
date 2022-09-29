# -*- coding: utf-8 -*-

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import subprocess
import sys

fonts_path = ''
open_folder_args = []
if sys.platform in ['linux', 'linux2']:
    fonts_path = '/usr/share/fonts'
    open_folder_args = ['nautilus', '--select']
elif sys.platform == 'darwin':
    fonts_path = '/Library/Fonts'
    open_folder_args = ['open', '-R']
elif sys.platform == 'win32':
    fonts_path = 'C:/Windows/Fonts'
    open_folder_args = ['explorer.exe', '/select,']


def make_meme(top_string, bottom_string, filename):
    font_path = f'{fonts_path}/Impact.ttf'
    img = Image.open(filename)
    image_size = img.size

    # find biggest font size that works
    font_size = int(image_size[1]/5)
    font = ImageFont.truetype(font_path, font_size)
    top_text_size = font.getsize(top_string)
    bottom_text_size = font.getsize(bottom_string)
    while top_text_size[0] > image_size[0]-20 or bottom_text_size[0] > image_size[0]-20:
        font_size = font_size - 1
        font = ImageFont.truetype(font_path, font_size)
        top_text_size = font.getsize(top_string)
        bottom_text_size = font.getsize(bottom_string)

    # find top centered position for top text
    top_text_position_x = (image_size[0]/2) - (top_text_size[0]/2)
    top_text_position_y = 0
    top_text_position = (top_text_position_x, top_text_position_y)

    # find bottom centered position for bottom text
    bottom_text_position_x = (image_size[0]/2) - (bottom_text_size[0]/2)
    bottom_text_position_y = image_size[1] - bottom_text_size[1]
    bottom_text_position = (bottom_text_position_x, bottom_text_position_y)

    draw = ImageDraw.Draw(img)

    # draw outlines
    # there may be a better way
    outline_range = int(font_size/15)
    for x in range(-outline_range, outline_range+1):
        for y in range(-outline_range, outline_range+1):
            draw.text((top_text_position[0]+x, top_text_position[1]+y), top_string, (0,0,0), font=font)
            draw.text((bottom_text_position[0]+x, bottom_text_position[1]+y), bottom_string, (0,0,0), font=font)

    draw.text(top_text_position, top_string, (255,255,255), font=font)
    draw.text(bottom_text_position, bottom_string, (255,255,255), font=font)

    img.save('temp.png')
    subprocess.call(open_folder_args + ['temp.png'])


def get_upper(some_data):
    '''
    Handle Python 2/3 differences in argv encoding
    '''
    result = ''
    try:
        result = some_data.decode('utf-8').upper()
    except:
        result = some_data.upper()
    return result


def get_lower(some_data):
    '''
    Handle Python 2/3 differences in argv encoding
    '''
    result = ''
    try:
        result = some_data.decode('utf-8').lower()
    except:
        result = some_data.lower()		

    return result


if __name__ == '__main__':
    args_len = len(sys.argv)
    top_string = ''
    meme = 'standard'

    if args_len == 1:
        # no args except the launch of the script
        print('at least one argument is required')

    elif args_len == 2:
        # only one argument, use standard meme
        bottom_string = get_upper(sys.argv[-1])

    elif args_len == 3:
        # args give meme and one line
        bottom_string = get_upper(sys.argv[-1])
        meme = get_lower(sys.argv[1])

    elif args_len == 4:
        # args give meme and two lines
        top_string = get_upper(sys.argv[-2])
        bottom_string = get_upper(sys.argv[-1])
        meme = get_lower(sys.argv[1])
    else:
        # so many args
        # what do they mean
        # too intense
        print('too many arguments (max: 4)')

    print(meme)	
    filename = f'{meme}.jpg'
    make_meme(top_string, bottom_string, filename)	

