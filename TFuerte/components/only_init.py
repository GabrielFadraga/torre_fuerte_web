import reflex as rx
from TFuerte.styles.colors import Text_tx, Color_tx
from TFuerte.styles.fonts import FontWeight as FontWeight
from TFuerte.styles.fonts import Fonts_tx as Fonts_tx
from TFuerte.components.title import title as title
import TFuerte.styles.styles as styles
from TFuerte.routes import Route
from TFuerte.components.link_button import link_button

def init() -> rx.Component:
    return rx.desktop_only(
        rx.link(
            rx.button(
                rx.icon(
                    "house",
                    stroke_width=2,
                    size=20
                ),
                variant="surface",
                #color="#194264FF",
                high_contrast=True,
                radius="large"

            ),
            href=Route.INDEX.value,
            justify="end",
            align="end"
        ),
        justify="end",
        align="end",
        )