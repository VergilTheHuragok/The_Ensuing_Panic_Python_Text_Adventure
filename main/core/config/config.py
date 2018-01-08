abbreviations = \
"# Command on left, abbreviation in brackets on right \n\
{ \n\
    'yes': ['y', 'ok', 'sure'], \n\
    'no': ['n', 'nope'], \n\
    'list': ['l', 'help', '?'] \n\
}"

settings = \
"# Setting name on left, value on right  \n\
{ \n\
    # Input settings \n\
    'unshifted keys': '`1234567890-=[];,./\\\\\\\'', \n\
    'shifted keys':   '~!@#$%^&*()_+{}:<>?|\\\"', \n\
    'key tick': 5, \n\
    'key repeat delay': 20, \n\
    'max keys pressed': 3, \n\
    'scroll amount': 20, \n\
    \n\
    # Application settings \n\
    'screen size': [800, 450], \n\
    'fps': 100, \n\
    'cursor blink rate': 500, \n\
    'cursor blink': True, \n\
    'cursor symbol': '|', \n\
    'cursor centered': True, \n\
    'dashes enabled': True, \n\
}"

customization = \
"# Setting name on left, value on right \n\
{ \n\
    # Input Font \n\
    'input font': 'ebrima', \n\
    'input font size': 18, \n\
    'input font color': (255,255,255), \n\
    \n\
    # System Font \n\
    'system font': 'ebrima', \n\
    'system font size': 18, \n\
    'system text color': (165, 120, 82), \n\
    'system date color': (125,125,255), \n\
    \n\
    # Window colors \n\
    'border color': (200,200,200), \n\
    'background color': (0,0,0), \n\
    'cursor color': (255,255,255), \n\
    'scroll bar color': (125, 125, 255), \n\
    \n\
    'temp font size': 'random.randint(10,20)' \n\
}"

window_layout = \
"# Name of window on left, x1, x2, y1, and y2 values on the right. \n\
# Use LEFT, RIGHT, TOP, and BOTTOM for respective sides of screen \n\
# Use MARGIN for the margin size declared in layout_variables.txt \n\
# DO NOT CHANGE UNLESS YOU KNOW WHAT YOU ARE DOING! \n\
# Not really, go crazy. If it messes something up, delete this file and it will be reloaded. \n\
{ \n\
    'events box':['LEFT', 'TOP', 'RIGHT/2', 'BOTTOM - MARGIN'], \n\
    'input box':['LEFT', 'BOTTOM - MARGIN', 'RIGHT', 'BOTTOM'], \n\
    'info pane':['RIGHT/2', 'TOP', 'RIGHT', 'BOTTOM - MARGIN*4'], \n\
    'objects box':['RIGHT/2', 'BOTTOM - MARGIN*4', 'RIGHT', 'BOTTOM - MARGIN*2.5'], \n\
    'actions box':['RIGHT/2', 'BOTTOM - MARGIN*2.5', 'RIGHT', 'BOTTOM - MARGIN'], \n\
}"

layout_variables = \
"# Layout setting name on left, value on right \n\
{ \n\
    'margin size': 60, \n\
    'horizontal padding': 2, \n\
    'vertical padding': .5, \n\
}"
