import reflex as rx
from enum import Enum

from .colors import Color_tx as tx
from .colors import Text_tx as texttx
from .fonts import Fonts_tx as fonttx
from .fonts import FontWeight as FontWeight

#Constants
MAX_WIDTH="5000px"

ABOUT_WIDTH="95em"

TEAM_WIDTH="200em"

#Sizes
class Spacer(Enum):
    EXTRA_SMALL="0.1em"
    SMALL="0.5em"
    MEDIUM="0.8em"
    DEFAULT="1em"
    LARGE="1.5em"
    BIG="2em"
    VERY_BIG="3em"
    SMS_P="5.5em"

#StylesSheets
StyleSheets = [
    "https://fonts.googleapis.com/css2?family=Poppins:wght@300;500&display=swap",
    "https://fonts.googleapis.com/css2?family=Comfortaa:wght@500&display=swap"
]

#Styles
BASE_STYLES = {
    "font_family" : fonttx.Default.value,
    "font_weight" : FontWeight.Light.value,
    "background_color" : tx.New.value,

    rx.button: {
        "width":"100%",
        "height":"100%",
        "display":"Block",
        "color": texttx.Header.value,
        #"background_color" : tx.Content.value,
        "padding":Spacer.SMALL.value,
        "border_radius":Spacer.DEFAULT.value,
        "white_space":"normal",
        "text_align":"normal",
        "_hover": {
        #"background_color" : tx.Secondary.value
        }
    },
    rx.link: {
        "text_decoration":"none",
        "_hover": {}
    }
}
navbar_title_style = dict(
    font_family=fonttx.Default.value,
    font_weight=FontWeight.Light.value,
)

title_style = dict(
    #size="lg",
    width="100%",
    #padding_top=Spacer.DEFAULT.value,
    font_family= fonttx.Default.value,
    font_weight= FontWeight.Light.value,

)

button_title_style = dict(
    font_family= fonttx.Title.value,
    font_size=Spacer.LARGE.value
)

button_body_style = dict(
    font_family= fonttx.Default.value,
    font_size=Spacer.MEDIUM.value
)