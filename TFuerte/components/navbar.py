import reflex as rx
from TFuerte.styles.colors import Text_tx, Color_tx
from TFuerte.styles.fonts import FontWeight as FontWeight
from TFuerte.styles.fonts import Fonts_tx as Fonts_tx
from TFuerte.components.title import title as title
import TFuerte.styles.styles as styles
from TFuerte.routes import Route

def navbar(text: str) -> rx.Component:
    return rx.box(
            rx.hstack(
                rx.link(
                rx.avatar(  fallback="TF", 
                    size="6", 
                    src="tf2.png",
                    radius="full",
                    margin="1.3em",        #styles.Spacer.LARGE.value,
                    #padding_x="11px"
                    ),
                href=Route.INDEX.value,
            ),
                    rx.vstack(
                    title(
                        text=text),
                        #font_family="Fonts_tx.Default.value",
                        #font_weight="FontWeight.Medium.value",
                    
                    align_items="center",
                    ),
                ),
                justify="between",
                align_items="center",
                bg=Color_tx.Content.value,
                padding=styles.Spacer.EXTRA_SMALL.value,
                width="100%",
                style=styles.navbar_title_style,
            )
