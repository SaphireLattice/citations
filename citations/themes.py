from collections import namedtuple

Theme = namedtuple('Theme', 'background foreground details')

named = {
    'pink': Theme("#f3d7e6", "#5a5559", "#bfa8a8"),
    'gold': Theme("#292929", "#C5B067", "#171717"),
    'gray': Theme("#cbe2f3", "#555758", "#a1afba"),
    'blue': Theme("#B5D3FF", "#54575c", "#88ade7")
}
