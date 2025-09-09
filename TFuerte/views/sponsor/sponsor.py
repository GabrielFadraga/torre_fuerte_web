import reflex as rx
import TFuerte.styles.styles as styles
from TFuerte.components.title import title
from TFuerte.components.link_sponsor import link_sponsor

def sponsor() -> rx.Component:
    return rx.vstack(
        title("Nuestros clientes:",
        ),
        rx.grid(
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
            spacing="6",
            columns=rx.breakpoints(initial="1", sm="2", lg="3"),
        ),
        width="100%",
        spacing="5"
    )
