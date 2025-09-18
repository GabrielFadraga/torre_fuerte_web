import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles
from TFuerte.styles.colors import Text_tx

def header_responsive() -> rx.Component:
    return rx.center(
    rx.vstack(
    rx.hstack(
            rx.heading("Consejo Directivo", size="7"),
            align="start",
            color=Text_tx.Black.value,
        ),
        #1 user
        rx.vstack(
            rx.image(
                src="user1.png", 
                width="200px", 
                height="auto",
            ),
        rx.vstack(
            rx.text("Lic. Maikel Torres López"),
            rx.text("Presidente"),
            width="100%",
            align_items="center",
            color=Text_tx.Black.value,
        ),
        width="100%",
        align_items="center",
    ),
    #1 user

    #1 user
        rx.vstack(
            rx.image(
                src="user1.png", 
                width="200px", 
                height="auto",
            ),
        rx.vstack(
            rx.text("Ing. Euclides Rodríguez Mejías"),
            rx.text("Director Adjunto"),
            width="100%",
            align_items="center",
            color=Text_tx.Black.value,
        ),
        width="100%",
        align_items="center",
    ),
    #1 user

    #1 user
        rx.vstack(
            rx.image(
                src="user1.png", 
                width="200px", 
                height="auto",
            ),
        rx.vstack(
            rx.text("Lic. Meylin Yu Parra"),
            rx.text("Jefa de Área Administrativa"),
            width="100%",
            align_items="center",
            color=Text_tx.Black.value,
        ),
        width="100%",
        align_items="center",
    ),
    #1 user

    #1 user
        rx.vstack(
            rx.image(
                src="user1.png", 
                width="200px", 
                height="auto",
            ),
        rx.vstack(
            rx.text("Ing. Miguel Obregón Salomón"),
            rx.text("Jefe de Área Logística"),
            width="100%",
            align_items="center",
            color=Text_tx.Black.value,
        ),
        width="100%",
        align_items="center",
    ),
    #1 user

    #1 user
        rx.vstack(
            rx.image(
                src="user1.png", 
                width="200px", 
                height="auto",
            ),
        rx.vstack(
            rx.text("Ing. Gilberto Acosta Monjes"),
            rx.text("Jefe de Coordinación"),
            rx.text("Habana-Mayabeque"),
            width="100%",
            align_items="center",
            spacing="1",
            color=Text_tx.Black.value,
        ),
        width="100%",
        align_items="center",
    ),
    #1 user

    #1 user
        rx.vstack(
            rx.image(
                src="user1.png", 
                width="200px", 
                height="auto",
            ),
        rx.vstack(
            rx.text("Ing. Manuel Núñez Brea"),
            rx.text("Jefe de Coordinación Oriente"),
            width="100%",
            align_items="center",
            color=Text_tx.Black.value,
        ),
        width="100%",
        align_items="center",
    ),
    #1 user

    #1 user
        rx.vstack(
            rx.image(
                src="user1.png", 
                width="200px", 
                height="auto",
            ),
        rx.vstack(
            rx.text("T.M Alexander Martínez Elias"),
            rx.text("Jefa de Área Técnica"),
            width="100%",
            align_items="center",
            color=Text_tx.Black.value,
        ),
        width="100%",
        align_items="center",
    ),
    #1 user

    width="100%",
    padding_y="1.5em",
), 
    spacing="5",
    width="100%",
)