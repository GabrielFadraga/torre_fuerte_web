import reflex as rx
import TFuerte.styles.styles as styles
from TFuerte.components.title import title
from TFuerte.components.link_sponsor import link_sponsor

def sponsor() -> rx.Component:
    return rx.hstack(
        rx.hstack(
            link_sponsor(
                "navegacion.png",
                "https://www.gemar.transnet.cu/es/empresas/empresa-de-navegacion-caribe",
            ),
            link_sponsor(
                "salud.png",
                "https://salud.msp.gob.cu/",
            ),
            link_sponsor(
                "eng.png",
                "https://www.engimov.pt/es/grupo/engimov-caribe",
            ),
            align="center",
            spacing="6",
            #width="100%",
        ),
            background_color="#194264FF",
            z_index="1000",
            width="100%",
            justify="center",
    )