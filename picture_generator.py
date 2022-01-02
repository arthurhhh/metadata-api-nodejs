import sys
from PIL import Image, ImageDraw, ImageFont
from datetime import date
import random
import math
import cloudinary
import cloudinary.uploader
import io

assert(len(sys.argv) == 4)
author = sys.argv[1]
author_quote = author
last_word = sys.argv[2]
id = sys.argv[3]
date_str = date.today().strftime("%b %d, %Y")

WORDS_SPACING = 28
AUTHOR_SPACING = 21
DATE_GAP_WIDTH = 4

# colors = [(255,255,255,1), (196,83,196,1), (85,148,236,1), (161,222,251,1), (249,56,17,1), (94,164,90,1), (253,164,2,1)]

# generate a random text color based on the string
# random.seed(author)
# random_int = math.floor(random.random() * 100)

# color_drawn = 6

# # 2 4 7 12 19 25 
# if random_int < 2:
#     color_drawn = 0
# elif random_int < 6:
#     color_drawn = 1
# elif random_int < 13:
#     color_drawn = 2
# elif random_int < 25:
#     color_drawn = 3
# elif random_int < 44:
#     color_drawn = 4
# elif random_int < 69:
#     color_drawn = 5

# create a new image
# out = Image.new("RGB", (350, 350), (0, 0, 0))

WORDS_FONT_SIZE = 64
NAME_FONT_SIZE = 48
DATE_FONT_SIZE = 24

# The size of upper/lower case letters and numbers. A size of 1 = the length
# of a line
UPPER_CASE_SIZE_FOR_WORDS = 1.0 / 13
LOWER_CASE_SIZE_FOR_WORDS = 1.0 / 15
NUMBER_SIZE_FOR_WORDS = 1.0 / 13
MAX_NUM_LINES_FOR_WORDS = 7

UPPER_CASE_SIZE_FOR_NAME = 1.0 / 16
LOWER_CASE_SIZE_FOR_NAME = 1.0 / 20
NUMBER_SIZE_FOR_NAME = 1.0 / 16
MAX_NUM_LINES_FOR_NAME = 1

WORDS_COORDINATE = (432, 200)
NAME_COORDINATE = (432, 1091)
DATE_COORDINATE = (432, 1057)

def get_size_of_word(word, upper_size, lower_size, number_size):
    size = 0
    for char in word:
        if char.isupper():
            size += upper_size
        elif char.isnumeric():
            size += number_size
        else:
            size += lower_size
    return size

def break_line_into_multiple(line, upper_size, lower_size, number_size):
    words = line.split(" ")
    broken_lines = []
    accumulated_line = ""
    accumulated_size = 0
    i = 0
    while i < len(words):
        current_word = words[i]
        word_size = get_size_of_word(current_word, upper_size, lower_size, number_size)
        should_append_space = 1 if len(accumulated_line) > 0 else 0
        if word_size >= 1.05 and accumulated_size == 0:
            broken_lines.append(current_word)
            i += 1
        elif accumulated_size + word_size + should_append_space * lower_size >= 1.05:
            broken_lines.append(accumulated_line)
            accumulated_line = ""
            accumulated_size = 0
        else:
            if should_append_space:
                accumulated_line += " "
            accumulated_line += current_word
            accumulated_size += word_size
            i += 1
    if accumulated_size > 0:
        broken_lines.append(accumulated_line)
    return broken_lines
            
def break_text(text, upper_size, lower_size, number_size, max_num_lines):
    lines = text.split("\\n")
    broken_text = []
    for line in lines:
        broken = broken_text.extend(break_line_into_multiple(line, upper_size, lower_size, number_size))
    if len(broken_text) > max_num_lines:
        broken_text = broken_text[0:max_num_lines]
        last_line = broken_text[-1]
        if get_size_of_word(last_line, upper_size, lower_size, number_size) + get_size_of_word("...", upper_size, lower_size, number_size) >= 1.05:
            broken_text[-1] = " ".join(last_line.split(" ")[0:-1])
        broken_text[-1] += "..."
    return "\n".join(broken_text)

def print_with_gap(draw, xpos, ypos, font, text, gap, fill):
    for letter in text:
        draw.text((xpos, ypos), letter, font=font, fill=fill)
        letter_width, _ = draw.textsize(letter, font=font)
        xpos = xpos + letter_width + gap

# get fonts for both name and words
words_font = ImageFont.truetype("./assets/fonts/Quantico-Bold.ttf", WORDS_FONT_SIZE)
name_font = ImageFont.truetype("./assets/fonts/Quantico-Regular.ttf", NAME_FONT_SIZE)
date_font = ImageFont.truetype("./assets/fonts/Quantico-Regular.ttf", DATE_FONT_SIZE)
cloudinary.config( 
  cloud_name = "drdnhdpds", 
  api_key = "179442926732313", 
  api_secret = "f9K6yvqNNVm_r3syY2MoiGUzfm0" 
)
with Image.open("./assets/background/background_card.png") as base:
    image_editable = ImageDraw.Draw(base)
    # Add words
    last_word_broken = break_text(last_word, UPPER_CASE_SIZE_FOR_WORDS, LOWER_CASE_SIZE_FOR_WORDS, NUMBER_SIZE_FOR_WORDS, MAX_NUM_LINES_FOR_WORDS)
    image_editable.text(WORDS_COORDINATE, last_word_broken, font=words_font, fill=(0, 0, 0), spacing=WORDS_SPACING)
    
    # Add author
    author_broken = break_text(author_quote, UPPER_CASE_SIZE_FOR_NAME, LOWER_CASE_SIZE_FOR_NAME, NUMBER_SIZE_FOR_NAME, MAX_NUM_LINES_FOR_NAME)
    image_editable.text(NAME_COORDINATE, author_broken, font=name_font, fill=(0, 0, 0), spacing=AUTHOR_SPACING)
    
    # Add date
    print_with_gap(image_editable, DATE_COORDINATE[0], DATE_COORDINATE[1], date_font, date_str, DATE_GAP_WIDTH, (0,0,0))
    
    # image_path = "./public/images/" + id + ".png"
    # base.save("./public/images/" + id + ".png")
    img_byte_arr = io.BytesIO()
    base.save(img_byte_arr, format="PNG")
    
    # Upload to cloundinray
    result = cloudinary.uploader.upload(img_byte_arr.getbuffer(), public_id="tokens/" + id)
    print(result['url'], end='')
    

 



    

