#!/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import math
import argparse
import re
import colors

m = 2
w, h = 183, 80
stamp_name = "moa.png"
main_font = "BMmini.ttf"
use_alt_font = False



parser = argparse.ArgumentParser(description='Generates Papers Please citation cards.')
parser.add_argument('lines', nargs=1,
                   help='lines of the citation, separated by ;')
parser.add_argument('penalty', nargs="?", default="No penalty - warning issued",
                   help='penalty text')
parser.add_argument('--title', '-t', default="M.O.A. Citation",
                   help='title of the citation (default "M.O.A. CITATION")')
parser.add_argument('--stamp', '-s', default="moa.png",
                   help='name of stamp .png file (default: moa)')
parser.add_argument('--altfont', action="store_true",
                   help='use alternative (old) font for the title')
parser.add_argument('--condensed', action="store_true",
                   help='use smaller spacing for lines')
parser.add_argument('--barcode', default="1,1,1,2,2",
                   help='barcode format to use in widths of lines as comma separated list')
parser.add_argument('--theme', '-c', default = "default",
                   help='color scheme - can be overriden by individual color settings',
                   choices = [x for x in dir(colors) if x[0:2] != '__'])
parser.add_argument('--foreground', '--fg', default = None,
                   help='hex color to use for foreground text and elements')
parser.add_argument('--background', '--bg', default = None,
                   help='hex color to use for background')
parser.add_argument('--details', '--det', default = None,
                   help='hex color to use for background details')

args = parser.parse_args()
stamp_name = args.stamp
lines = args.lines[0].split(";")
use_alt_font = args.altfont
condensed = args.condensed
theme = getattr(colors, args.theme)
c_bg   = args.background or theme[0]
c_fg   = args.foreground or theme[1]
c_elem = args.details    or theme[2]

minlines = 3
lineheight = 10
if condensed:
    minlines = 4
    lineheight = 9

def line_bind(text):
    max_w = (w - 11 - 12) * m
    size = bm.getsize(text)
    if size[0] <= max_w:
        return (text, "")
    chars = 1
    size = bm.getsize(text[:chars])
    while size[0] < max_w:
        size = bm.getsize(text[:chars])
        chars += 1
    return (text[:chars - 1], text[chars - 1:])

bm = ImageFont.truetype(main_font, 16)

newlines = []
for x in lines:
    newlines.extend(x.split("\n"))
lines = newlines
newlines = []
for x in lines:
    out = line_bind(x)
    newlines.append(out[0])
    while len(out[1]) != 0:
        out = line_bind(out[1])
        newlines.append(out[0])
lines = newlines 

if len(lines) > minlines:
    h += (len(lines) - minlines) * lineheight


im = Image.new("RGB",(w*m, h*m), c_bg)
draw = ImageDraw.Draw(im)
if use_alt_font == True:
    global tbm
    tbm = ImageFont.truetype("Megan_Serif.ttf", 16)

def dots(line, offset, color = c_elem):
    start = offset[0]
    end   = w - 1 - offset[1]
    num = 0
    for x in range((end - start + 1) // 2 + 1):
        c = [start*m + num*m*2, line*m, start*m + num*m*2 + m - 1, line*m + m - 1]
        draw.rectangle(c, color)
        num += 1
    return


def rect(x, y, w, h, color = c_elem):
    draw.rectangle([x * m, y * m, (x + w) * m - 1, (y + h) * m - 1], color)


def roll():
    for x in range((h + 3) // 9):
        rect(2, 3 + 9 * x, 3, 3)
        rect(w - 7, 3 + 9 * x, 3, 3)


def line(on, text, color=c_fg):
    offset = 4
    remaining = ""
    if on != 0:
        offset = 22 + (on - 1) * lineheight

    if on == 0 and use_alt_font == True:
        offset = 3
        draw.text((11*m - 1, offset*m), text.replace(" ", "    "), font=tbm, fill=color)
    else:
        draw.text((11*m - 1, offset*m), text, font=bm, fill=color)
    return remaining

def stamp(): # 32x32 at 150x44
    stamp_bg = Image.open("stamp_bg.png")
    draw.bitmap((150, (h - 4 - 32) *m), stamp_bg, c_elem)
    stamp_bg.close()
    stamp = Image.open(stamp_name)
    draw.bitmap((150, (h - 4 - 32) *m), stamp, c_bg)
    stamp.close()


def footer(text, color=c_fg):
    text = text.upper()
    y = (h - 15) * m
    size = bm.getsize(text)

    x = math.ceil((w - 6 - 10 - (size[0] - 1) // m) / 2) * m + 6 * m
    draw.text((x - 1, y), text, font=bm, fill=color)
    return

def barcode(spec, color=c_fg):
    end = 172
    width = 2
    for x in spec:
        width += 1 + x
    offset = 0
    for x in reversed(spec):
        rect(end - offset - x, 3, x, 6, color)
        offset += 1 + x
    rect(end - offset - 2, 3, 2, 3, color)



stamp()
dots(0, (0, 0))
roll()
rect(w - 1, 0, w, h, c_elem)
dots(h - 1, (1, 0))

barcode([int(i) for i in re.findall(r"[\w']+", args.barcode)])

dots(17, (8, 10), c_fg)
line(0, args.title.upper())

offset = 1
for x in range(len(lines)):
    left = line(x + offset, lines[x])
    while len(left) != 0:
        offset += 1
        left = line(x + offset, left)

if condensed:
    dots(h - 22 - 1, (8, 10), c_fg)
else:
    dots(h - 26 - 1, (8, 10), c_fg)
footer(args.penalty)

im.save("citation.png", "PNG")
