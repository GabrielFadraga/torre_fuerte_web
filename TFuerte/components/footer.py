import reflex as rx
import datetime
from TFuerte.styles.colors import Text_tx
from TFuerte.components.link_sponsor import link_sponsor

def footer() -> rx.Component:
    return rx.hstack(
    rx.stack(
    link_sponsor(
            "navegacion.png",
            "https://www.gemar.transnet.cu/es/empresas/empresa-de-navegacion-caribe",
            ),
    link_sponsor(
            "salud.png",
            "https://salud.msp.gob.cu/",
            ),
    link_sponsor(
            "engi.png",
            "https://www.engimov.pt/es/grupo/engimov-caribe",
            ),
        
        padding_x="2.5em",
        padding_y="2.5em",
        spacing="7",
        width="22%",
        align="center",
        justify="start"
    ),
        rx.hstack(
        rx.vstack(
        rx.image(src="torre.png", border_radius="15px 15px", height="50px"),
        rx.link(f"2024 - {datetime.date.today().year} © Torre Fuerte - Todos los derechos reservados", 
                href="https://www.instagram.com/torre_fuerte_surl?igsh=NGdkZDJxZnluNnM=",
                is_external=True,
                color=Text_tx.Footer.value,
                ),

        align_items="center",
        margin_bottom="32px",
        font_size="20px",
        spacing="1",
        color=Text_tx.Footer.value,
        width="80%",
        padding_y="3.5em",
    ),
    width="100%",
    align="start"
),
        justify="start",
        align="start",
        background_color="#194264FF",
        z_index="1000",
        width="100%",
),