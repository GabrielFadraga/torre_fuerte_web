import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles

def headcreat() -> rx.Component:
    return rx.center(
            rx.vstack(
                rx.heading(
                    "Somos Torre Fuerte SURL", 
                    size="9", 
                    color="white",
                    text_align="center",
                    width="100%"
                ),
                rx.text(
                    """Nos dedicamos a brindar servicios de reparación, mantenimiento y 
                    rehabilitación de equipos industriales en las especialidades de 
                    mecánica, electricidad y automática.""",
                    margin_top="0.5em",
                    size="7",
                    color="white",
                    text_align="center",
                    max_width="600px",
                    width="100%",
                ),
                rx.link(
                    rx.button(
                        "Contáctanos",
                        background_color="orange",
                        color="white",
                        _hover={"background_color": "orange"},
                        style=styles.button_title_style,
                        body=styles.button_body_style,
                        size="4",
                        variant="outline"
                    ),
                    href="https://wa.me/message/OKIP2WN55MKEK1",
                    is_external=True
                ),
                spacing="5",
                align="center"
            ),
            background_image="linear-gradient(#194264FF)",
            background_size="cover",
            background_position="center",
            height="500px",
            width="100%",
            id="inicio"
        )