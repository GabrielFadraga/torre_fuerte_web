import reflex as rx
from TFuerte.styles.colors import Text_tx, Color_tx
from TFuerte.styles.fonts import FontWeight as FontWeight
from TFuerte.styles.fonts import Fonts_tx as Fonts_tx
from TFuerte.components.title import title as title
import TFuerte.styles.styles as styles
from TFuerte.routes import Route

def navbar_about() -> rx.Component:
    return rx.box(
            rx.hstack(
                rx.link(
                rx.avatar(  fallback="sobre nosotros", 
                    size="4", 
                    src="tf1.png",
                    radius="full",
                    margin=styles.Spacer.LARGE.value,
                    ),
                href=Route.INDEX.value,
            ),
                    rx.vstack(
                    title(
                        "Sobre nosotros"),
                        font_family="Fonts_tx.Default.value",
                        font_weight="FontWeight.Medium.value",
                    
                    align_items="center",
                    ),
                    spacing="1"
                ),
                justify="between",
                align_items="center",
                bg=Color_tx.Content.value,
                padding=styles.Spacer.EXTRA_SMALL.value,
                width="100%",
                style=styles.navbar_title_style,
            )