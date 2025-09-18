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
                    rx.vstack(
                    title(
                        text=text),
                        #font_family="Fonts_tx.Default.value",
                        #font_weight="FontWeight.Medium.value",
                    
                    
                    align="start"
                    
                    ),
                    width="100%",
                    top="0",
                    z_index="1000",
                    #margin="1em",
                ),
                justify="start",
                background_color="#194264FF",
                padding=styles.Spacer.DEFAULT.value,
                width="100%",
                style=styles.navbar_title_style,
            )
