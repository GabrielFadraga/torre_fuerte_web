import reflex as rx
import datetime
from TFuerte.styles.colors import Text_tx 

def icon() -> rx.Component:
    return rx.hstack(
            rx.link(
            rx.icon(
                size=40,
                tag="facebook",
                color="red",
                stroke_width=1.5,
            ),
            href="https://www.facebook.com/torrefuerte.surl",
        ),

            rx.link(
            rx.icon(
                size=40,
                tag="Instagram",
                color="red",
                stroke_width=1.5,
            ),
            href="https://www.instagram.com/torre_fuerte_surl?igsh=NGdkZDJxZnluNnM=",
        ),
        width="100%",
        justify="center",
        spacing="5",
    ),