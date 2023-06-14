VERSION = '0.4.9'
# Every 'int' value is in pixels
DEFAULT_SCR_WIDTH = 600
DEFAULT_SCR_HEIGHT = 600
DEFAULT_NODE_RADIUS = 25
DEFAULT_THEME = 'BROWN'
BUTTON_HEIGHT = 30
BUTTON_WIDTH = 60
XMARGEN = 7
YMARGEN = 7

# For overlapped edges
MIN_EDGE_SEPARATION = 80
MAX_EDGE_SEPARATION = 220
SEPARATION_RATIO = 5500 # In pixels
SEPARATION_LABEL_RATIO = 3000

THEMES = {
    "BROWN":{
        "BUTTON_COLOR": "#ede4cc",
        "SELECTED_VERTEX_COLOR": "#c2baa7",
        "VERTEX_COLOR": "#e3d7c5",
        "BACKGROUND_CANVAS_COLOR": "#c7b9a5",
        "FRAME_COLOR": "#87715f",
        "AUTHOR_NAME_COLOR": "#301d05"
    },
    "LIGHT":{
        "BUTTON_COLOR": "#a6a6a6",
        "SELECTED_VERTEX_COLOR": "#b3b3b3",
        "VERTEX_COLOR": "#bfbdbd",
        "BACKGROUND_CANVAS_COLOR": "#d4d3d2",
        "FRAME_COLOR": "#b3b3b3",
        "AUTHOR_NAME_COLOR": "#454545"
    },
    "BLUE":{
        "BUTTON_COLOR": "#b7e7e8",
        "VERTEX_COLOR": "#a7d6fc",
        "SELECTED_VERTEX_COLOR": "#91b9ba",
        "BACKGROUND_CANVAS_COLOR": "#b5d9f7",
        "FRAME_COLOR": "#6aaade",
        "AUTHOR_NAME_COLOR": "#0b2d47"
    },
    "DARK":{
        "BUTTON_COLOR": "#6a6a7d",
        "SELECTED_VERTEX_COLOR": "#8d8da6",
        "VERTEX_COLOR": "#7d7d96",
        "BACKGROUND_CANVAS_COLOR": "#404147",
        "FRAME_COLOR": "#272729",
        "AUTHOR_NAME_COLOR": "#7c7c9c"
    },
    "PURPLE":{
        "BUTTON_COLOR": "#f2c8fa",
        "SELECTED_VERTEX_COLOR": "#bf97c7",
        "VERTEX_COLOR": "#e7cdf7",
        "BACKGROUND_CANVAS_COLOR": "#e4c3fa",
        "FRAME_COLOR": "#d899f7",
        "AUTHOR_NAME_COLOR": "#6d1aa3"
    },
    "GREEN":{
        "BUTTON_COLOR": "#B5FFC7",
        "SELECTED_VERTEX_COLOR": "#05331F",
        "VERTEX_COLOR": "#A1FDB3",
        "BACKGROUND_CANVAS_COLOR": "#BFFFCF",
        "FRAME_COLOR": "#80FF99",
        "AUTHOR_NAME_COLOR": "#05331F"
    },
    "DARKGREEN":{
        "BUTTON_COLOR": "#173F2D",
        "SELECTED_VERTEX_COLOR": "#05331F",
        "VERTEX_COLOR": "#215C41",
        "BACKGROUND_CANVAS_COLOR": "#163623",
        "FRAME_COLOR": "#0C2B1A",
        "AUTHOR_NAME_COLOR": "#FFFFFF"
    },
    "UBUNTU":{
        "BUTTON_COLOR": "#b35625",
        "SELECTED_VERTEX_COLOR": "#FFFFFF",
        "VERTEX_COLOR": "#d45102",
        "BACKGROUND_CANVAS_COLOR": "#404040",
        "FRAME_COLOR": "#303030",
        "AUTHOR_NAME_COLOR": "#b35625"
    },
    "LA NOCHE ESTRELLADA":{
        "BUTTON_COLOR": "#9bafaa",
        "SELECTED_VERTEX_COLOR": "#aed4eb",
        "VERTEX_COLOR": "#8fadbf",
        "BACKGROUND_CANVAS_COLOR": "#557491",
        "FRAME_COLOR": "#242d34",
        "AUTHOR_NAME_COLOR": "#d5bc6a"
    },
    "LA GRAN OLA":{
        "BUTTON_COLOR": "#a6a49b",
        "SELECTED_VERTEX_COLOR": "#d5bc6a",
            "VERTEX_COLOR": "#e7e2d2",
        "BACKGROUND_CANVAS_COLOR": "#8599a4",
        "FRAME_COLOR": "#4a5f79",
        "AUTHOR_NAME_COLOR": "#2d3a4a"
    },
    "ANTARTICA":{
        "BUTTON_COLOR": "#9BA4B5",
        "SELECTED_VERTEX_COLOR": "#becde8",
        "VERTEX_COLOR": "#9BA4B5",
        "BACKGROUND_CANVAS_COLOR": "#394867",
        "FRAME_COLOR": "#212A3E",
        "AUTHOR_NAME_COLOR": "#83764F"
    },
    "BREAKING BAD":{
        "BUTTON_COLOR": "#F7E1AE",
        "SELECTED_VERTEX_COLOR": "#b3a37f",
        "VERTEX_COLOR": "#F7E1AE",
        "BACKGROUND_CANVAS_COLOR": "#617A55",
        "FRAME_COLOR": "#3d4d36",
        "AUTHOR_NAME_COLOR": "#000000"
    },
    "SOFT":{
        "BUTTON_COLOR": "#E4D0D0",
        "SELECTED_VERTEX_COLOR": "#a89d9d",
        "VERTEX_COLOR": "#E4D0D0",
        "BACKGROUND_CANVAS_COLOR": "#D5B4B4",
        "FRAME_COLOR": "#867070",
        "AUTHOR_NAME_COLOR": "#000000"
    },
    "TURQUOISE": {
        "BUTTON_COLOR": "#0E8388",
        "SELECTED_VERTEX_COLOR": "#b7c4c1",
        "VERTEX_COLOR": "#83918e",
        "BACKGROUND_CANVAS_COLOR": "#2E4F4F",
        "FRAME_COLOR": "#2C3333",
        "AUTHOR_NAME_COLOR": "#CBE4DE"
    },
    "DEEP PURPLE":{
        "BUTTON_COLOR": "#bdb8ac",
        "SELECTED_VERTEX_COLOR": "#bdb8ac",
        "VERTEX_COLOR": "#bdb8ac",
        "BACKGROUND_CANVAS_COLOR": "#6D5D6E",
        "FRAME_COLOR": "#4F4557",
        "AUTHOR_NAME_COLOR": "#F4EEE0"
    },
    "THIS ONE IS UGLY":{
        "BUTTON_COLOR": "#F67280",
        "SELECTED_VERTEX_COLOR": "#F67280",
        "VERTEX_COLOR": "#C06C84",
        "BACKGROUND_CANVAS_COLOR": "#6C5B7B",
        "FRAME_COLOR": "#355C7D",
        "AUTHOR_NAME_COLOR": "#F67280"
    },
    "FROST": {
        "BUTTON_COLOR": "#00ADB5",
        "SELECTED_VERTEX_COLOR": "#13787d",
        "VERTEX_COLOR": "#00ADB5",
        "BACKGROUND_CANVAS_COLOR": "#393E46",
        "FRAME_COLOR": "#222831",
        "AUTHOR_NAME_COLOR": "#EEEEEE"
    },
    "NEKOS": {
        "BUTTON_COLOR": "#DEFCF9",
        "VERTEX_COLOR": "#CADEFC",
        "SELECTED_VERTEX_COLOR": "#DEFCF9",
        "BACKGROUND_CANVAS_COLOR": "#C3BEF0",
        "FRAME_COLOR": "#CCA8E9",
        "AUTHOR_NAME_COLOR": "#DEFCF9"
    },
    "VAMPIRE": {
        "BUTTON_COLOR": "#FF0000",
        "SELECTED_VERTEX_COLOR": "#FF0000",
        "VERTEX_COLOR": "#FF0000",
        "BACKGROUND_CANVAS_COLOR": "#950101",
        "FRAME_COLOR": "#3D0000",
        "AUTHOR_NAME_COLOR": "#FF0000"
    }
}