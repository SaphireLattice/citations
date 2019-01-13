from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple
import math
import re

from . import defaults, themes


class Factory:
    """
        :param width: width of the image, works better if it's even
        :param min_height: minimal height of the image
        :param multiplier: image pixels size multiplier

        .. warnings:: The built in stamp only work with multiplier == 2
    """
    def __init__(self, theme=themes.named[defaults.theme], condensed: bool = False, use_alt_font: bool = False,
                 main_font: str = defaults.main_font_file, alt_font: str = defaults.alt_font_file,
                 stamp_filename=defaults.stamp_filename, stamp_background=defaults.stamp_bg_filename,
                 width=defaults.width, min_height=defaults.height, multiplier: int = defaults.multiplier):
        self.width = width
        self.min_height = min_height
        self.multiplier = multiplier

        self.theme = theme

        self.use_alt_font = use_alt_font
        self.condensed = condensed

        self.min_lines = 3
        self.line_height = 10
        if self.condensed:
            self.min_lines = 4
            self.line_height = 9

        # Ideally, there should be a stack of stamp images/bitmaps that you can
        # just layer over one another.
        self.stamp_img_bg = Image.open(stamp_background)
        self.stamp_img = Image.open(stamp_filename)

        self.alt_font_file = alt_font
        self.body_font_file = main_font

        self.body_font = ImageFont.truetype(main_font, 16)
        if use_alt_font:
            self.title_font = ImageFont.truetype(alt_font, 16)
        else:
            self.title_font = self.body_font

        self.title_align = 0

        # 0, 1 -> right, left
        if self._align_line(0) == 0:
            self.barcode_align = 0
        elif self._align_line(0) == 2:
            self.barcode_align = 1

        # Those should be set manually
        # WARNING: might not work properly with text wrapping! Proceed with caution
        self.body_align = 0  # 0, 1, 2 -> left, center, right
        self.wrap_by_char = False
        self.split_at_newline = False
        self.pattern = None

    def generate_file(self, filename, filetype='PNG', **options):
        img = self.generate_image(**options)
        img.save(filename, filetype)

    def generate_image(self, content: List[str], penalty: str, title: str, barcode: List[int] = ()):
        lines, content_height = self._process_lines(content)
        height = max(content_height, self.min_height)
        img = Image.new('RGB', (self.width * self.multiplier, height * self.multiplier), self.theme.background)
        draw = ImageDraw.Draw(img)
        self._generate(draw, height, lines, penalty, title, barcode)
        return img

    def _generate(self, draw: ImageDraw, height: int, lines: List[str], penalty: str, title: str, barcode: List[int]):
        """Internal method to draw on already generated image.

        Draws on supplied PIL.ImageDraw canvas. No promises if
        you use it on your own, the text might not fit. Use
        generate_file or generate_image instead.
        """
        self._stamp(draw, height, self.stamp_img_bg)
        self._stamp(draw, height, self.stamp_img, self.theme.background)
        self._dots_row(draw, 0, (0, 0))
        self._roll(draw, height)
        self._rect(draw, self.width - 1, 0, self.width, height, self.theme.details)
        self._dots_row(draw, height - 1, (1, 0))

        self._print_barcode(draw, barcode)

        # Header separator line
        self._dots_row(draw, 17, (8, 10), self.theme.foreground)
        self._text_line(draw, 0, title.upper())

        offset = 1
        for index, line in enumerate(lines):
            self._text_line(draw, index + offset, line)

        # Footer separator line
        if self.condensed:
            self._dots_row(draw, height - 22 - 1, (8, 10), self.theme.foreground)
        else:
            self._dots_row(draw, height - 26 - 1, (8, 10), self.theme.foreground)

        self._footer(draw, height, penalty)

    def _process_lines(self, input_lines):
        lines = []
        if self.split_at_newline:
            newlines = []
            for x in input_lines:
                newlines.extend(x.split("\n"))
            lines = newlines
        else:
            lines.extend(input_lines)

        newlines = []
        margin = (11, 12)
        for x in lines:
            out = self._trim_line_length(x, self.body_font, margin, self.wrap_by_char)
            newlines.append(out[0])
            while len(out[1]) != 0:
                out = self._trim_line_length(out[1], self.body_font, margin, self.wrap_by_char)
                newlines.append(out[0])
        lines = newlines

        new_height = self.min_height + max(0, len(lines) - self.min_lines) * self.line_height
        return lines, new_height

    def _trim_line_length(self, text: str, font: ImageFont, margins: Tuple[int, int], wrap_by_char: bool = False,
                          width: int = None):
        if width is None:
            width = self.width
        max_w = (width - margins[0] - margins[1]) * self.multiplier

        #  Let's get line length in chosen font
        size = font.getsize(text)
        if size[0] <= max_w:
            return text, ""  # Yay, we can just return the whole string. Crisis averted
        #  Or maybe not

        chars = 0
        if self.pattern is None:
            self.pattern = re.compile(r"\W?[\w,'-]+\W?")
        match = re.search(self.pattern, text)

        if match is not None:
            size = font.getsize(text[:match.end()])
        else:
            wrap_by_char = True

        if size[0] > max_w or wrap_by_char:  # Word is longer than string, whoops.
            if match is not None:
                chars = match.end()
            else:
                chars = len(text)

            while size[0] > max_w:
                size = font.getsize(text[:chars])
                chars -= 1
            return text[:chars], text[chars:]

        while size[0] < max_w:
            # We don't have any words left! Let the by-char match take it over
            if match is None:
                break
            size = font.getsize(text[:chars + match.start()])
            # Checks if the start of the word is already past sensible mark.
            if size[0] > max_w:
                break
            size = font.getsize(text[:chars + match.end()])
            if size[0] > max_w:
                break
            chars += match.end()
            match = re.search(self.pattern, text[chars:])
        line = text[:chars]
        remaining = text[chars:]
        if remaining[0:1] == " ":
            remaining = remaining[1:]
        return line, remaining

    def _dots_row(self, draw: ImageDraw, line: int, margin: Tuple[int, int], color: str = None):
        m = self.multiplier
        if color is None:
            color = self.theme.details
        start = margin[0]
        end = self.width - 1 - margin[1]
        num = 0
        for x in range((end - start + 1) // 2 + 1):
            c = [start * m + num * m * 2, line * m,
                 start * m + num * m * 2 + m - 1, line * m + m - 1]
            draw.rectangle(c, color)
            num += 1
        return

    def _rect(self, draw: ImageDraw, x: int, y: int, w: int, h: int, color: str = None):
        m = self.multiplier
        if color is None:
            color = self.theme.details
        draw.rectangle([x * m,
                        y * m,
                        (x + w) * m - 1,
                        (y + h) * m - 1], color)
        # The `- 1` here is to not have aliasing artifacts. Might
        # break if the chosen multiplier is not divisible by 2

    def _roll(self, draw: ImageDraw, height: int):
        for x in range((height + 3) // 9):
            self._rect(draw,
                       2, 3 + 9 * x,
                       3, 3)
            self._rect(draw,
                       self.width - 7, 3 + 9 * x,
                       3, 3)

    # Could be overriden/extended to provide per-line alignment
    def _align_line(self, line_num):
        if line_num == 0 and self.title_align is not None:
            return self.title_align
        return self.body_align

    def _text_line(self, draw: ImageDraw, line_num: int, text: str, color: str = None):
        mult = self.multiplier
        if color is None:
            color = self.theme.foreground
        offset = 4
        if line_num != 0:
            offset = 22 + (line_num - 1) * self.line_height

        font = self.body_font
        if line_num == 0 and self.use_alt_font:
            text = text.replace(" ", "    ")
            font = self.title_font
            offset = 3

        align = self._align_line(line_num)
        if align == 0:
            draw.text((11 * mult - 1, offset * mult), text,
                      font=font, fill=color)
        else:
            size = self.body_font.getsize(text)
            if align == 1:
                x = (self.width - 11 + 12 - (size[0] // mult)) // 2
                draw.text((x * mult - 1, offset * mult), text,
                          font=font, fill=color)
            else:
                x = self.width - 12 - (size[0] // mult)
                draw.text((x * mult - 1, offset * mult), text,
                          font=font, fill=color)

    def _stamp(self, draw: ImageDraw, height: int, img: Image, color: str = None):  # 32x32 at 150x44
        if color is None:
            color = self.theme.details
        draw.bitmap(((self.width * self.multiplier - img.width) // 2 - 1, (height - 4 - 32) * self.multiplier),
                    img, color)

    def _footer(self, draw: ImageDraw, height: int, text: str, color: str = None):
        m = self.multiplier
        if color is None:
            color = self.theme.foreground
        text = text.upper()
        y = (height - 15) * m
        size = self.body_font.getsize(text)

        x = math.ceil((self.width - 6 - 10 - (size[0] - 1) // m) / 2) * m + 6 * m
        draw.text((x - 1, y), text, font=self.body_font, fill=color)
        return

    def _print_barcode(self, draw: ImageDraw, spec: List[int], color: str = None):
        if color is None:
            color = self.theme.foreground
        end = self.width - 11
        width = 2
        for x in spec:
            width += 1 + x
        offset = 0
        if self.barcode_align == 0:
            for x in reversed(spec):
                self._rect(draw, end - offset - x, 3, x, 6, color)
                offset += 1 + x
            self._rect(draw, end - offset - 2, 3, 2, 3, color)
        else:
            end = 11
            for x in spec:
                self._rect(draw, end + offset, 3, x, 6, color)
                offset += 1 + x
            self._rect(draw, end + offset, 3, 2, 3, color)
