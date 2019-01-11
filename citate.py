#!/bin/env python3
import argparse
import citations
import re

main_font = "BMmini.ttf"
altfont = "Megan_Serif.ttf"

parser = argparse.ArgumentParser(description='Generates Papers Please citation cards.')
parser.add_argument('lines', nargs=1,
                    help='lines of the citation, separated by ; or newline')
parser.add_argument('penalty', nargs="?", default=citations.defaults.penalty,
                    help='penalty text')
parser.add_argument('--title', '-t', default=citations.defaults.title,
                    help='title of the citation (default "M.O.A. CITATION")')
parser.add_argument('--stamp', '-s', default=citations.defaults.stamp_filename,
                    help='name of stamp .png file (default: moa)')
parser.add_argument('--altfont', '-a', action="store_true",
                    help='use alternative (old) font for the title')
parser.add_argument('--condensed', '-o', action="store_true",
                    help='use alternative smaller spacing for lines')
parser.add_argument('--barcode', '-r', default=citations.defaults.barcode_str,
                    help='barcode format to use in widths of lines as comma separated list')
parser.add_argument('--theme', '-c', default="default",
                    help='color scheme - can be overriden by individual color settings',
                    choices=[x for x in dir(citations.themes) if x[0:2] != '__'])
parser.add_argument('--foreground', '--fg', '-f', default=None,
                    help='hex color to use for foreground text and elements')
parser.add_argument('--background', '--bg', '-b', default=None,
                    help='hex color to use for background')
parser.add_argument('--details', '--det', '-d', default=None,
                    help='hex color to use for background details')

args = parser.parse_args()


if __name__ == '__main__':
    lines = args.lines[0].split(";")  # Might have a few problems if the lines contain ;
    theme = getattr(citations.themes, args.theme)
    theme = [args.background or theme[0],
             args.foreground or theme[1],
             args.details or theme[2]]
    barcode_str = args.barcode
    barcode = [int(width) for width in re.findall(r"[\w']+", args.barcode)]
    factory = citations.Factory(lines, penalty=args.penalty, title=args.title,
                                stamp_filename=args.stamp, use_alt_font=args.altfont,
                                condensed=args.condensed, theme=theme, barcode=barcode)
    factory.generate_file("citation.png")
