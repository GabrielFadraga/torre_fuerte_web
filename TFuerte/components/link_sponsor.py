import reflex as rx
import TFuerte.styles.styles as styles

def link_sponsor(imagen: str, url: str) -> rx.Component:
    return rx.link(
        rx.image(
            height="7.5em",
            src=imagen
        ),
        href=url,
        is_external=True,
        #align_items="start",
        width="100%"
    )