import reflex as rx
import TFuerte.styles.styles as styles
from TFuerte.pages.index import index
from TFuerte.pages.about import about
from TFuerte.pages.services import services
from TFuerte.pages.projects import projects
from TFuerte.pages.team import team
from TFuerte.pages.taller import taller
from TFuerte.pages.eventos import event

from rxconfig import config
from TFuerte.api.api import hello


app = rx.App(
    stylesheets=styles.StyleSheets,
    style=styles.BASE_STYLES
)