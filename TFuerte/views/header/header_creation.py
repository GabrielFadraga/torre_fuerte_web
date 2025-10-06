import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles
from TFuerte.components.sidebar import sidebar

def headcreat() -> rx.Component:
    return rx.vstack(
                rx.hstack(
                    rx.mobile_and_tablet(
                    sidebar(),
            ),
            width="100%",
            
        ),
                rx.heading(
                    "Somos Torre Fuerte SURL", 
                    size="9", 
                    color="white",
                    text_align="center",
                    width="100%",
                    font_size=styles.Spacer.VERY_BIG.value,
                    margin=styles.Spacer.EXTRA_SMALL.value
                ),
                rx.text(
                    """Nos dedicamos a brindar servicios de reparación, mantenimiento y 
                    rehabilitación de equipos industriales en las especialidades de 
                    mecánica, electricidad y automática.""",
                    #margin_top="0.5em",
                    size="7",
                    color="white",
                    text_align="center",
                    max_width="50rem",
                    width="100%",
                    font_size=styles.Spacer.LARGE.value,
                    margin=styles.Spacer.SMALL.value
                ),
                #rx.spacer(),
                rx.vstack(
                rx.link(
                    rx.button(
                        "Contáctanos",
                        background_color="orange",
                        color="white",
                        _hover={"background_color": "orange"},
                        style=styles.button_title_style,
                        body=styles.button_body_style,
                        size="4",
                        variant="outline",
                ),
                spacing="4",
                align="center",
                href="https://wa.me/message/OKIP2WN55MKEK1",
                is_external=True,
                
            ),
            width="100%",
            margin=styles.Spacer.SMALL.value,
            align="center",
    ),
            background_image="linear-gradient(#194264FF)",
            background_size="cover",
            background_position="center",
            width="100%",
            id="inicio",
            align="center",

    )