import reflex as rx
import datetime
from TFuerte.styles.colors import Text_tx
from TFuerte.components.link_sponsor import link_sponsor

def footer() -> rx.Component:
        return rx.hstack(
        rx.vstack(
        rx.spacer(),
        rx.image(src="torre.png", border_radius="15px 15px", height="50px"),
        rx.link(f"2024 - {datetime.date.today().year} © Torre Fuerte SURL - Todos los derechos reservados", 
                href="https://www.instagram.com/torre_fuerte_surl?igsh=NGdkZDJxZnluNnM=",
                is_external=True,
                color=Text_tx.Footer.value,
                ),

        align_items="center",
        #margin_bottom="32px",
        font_size="20px",
        spacing="1",
        color=Text_tx.Footer.value,
        width="100%",
        padding_y="2em",
        ),
        width="100%",
        align="start",
        spacing="7",
        justify="start",
        background_color="#194264FF",
        z_index="1000",
)


