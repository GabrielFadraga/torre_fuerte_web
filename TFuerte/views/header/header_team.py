import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles

def header_team() -> rx.Component:
    return rx.center(
    rx.vstack(
        rx.hstack(
            rx.heading("Principales miembros"),
            align_items="start",
        ),
        #1 user
        rx.vstack(
            rx.image(
                src="user1.png", 
                width="200px", 
                height="auto",
            ),
        rx.vstack(
            rx.text("Lic Maikel Torres López"),
            rx.text("Presidente"),
            width="100%",
            align_items="center",
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
        ),
        width="100%",
        align_items="center",
    ),
    #1 user

        #2 users
    
        rx.vstack(
            rx.hstack(
            rx.vstack(
            rx.image(
                src="user1.png", 
                width="200px", 
                height="auto",
            ),
            rx.vstack(
            rx.text("Lic. Meylin Yu Parra"),
            rx.text("Jefa de Ärea Administrativa"),
            width="100%",
            align_items="center",
        ),
        width="100%",
        align_items="center",
    ),
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
        ),
        width="100%",
        align_items="center",
    ),
        width="85%",
        align_items="center",
        spacing="1",
    ),
    width="100%",
    align_items="center",
),
    #2user

#3 users
    
        rx.vstack(
            rx.hstack(
            rx.vstack(
            rx.image(
                src="user1.png", 
                width="200px", 
                height="auto",
            ),
            rx.vstack(
            rx.text("Ing Gilberto Acosta Monjes"),
            rx.text("Jefe de Coordinación Habana-Mayabeque"),
            width="100%",
            align_items="center",
        ),
        width="100%",
        align_items="center",
    ),
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
        ),
        width="100%",
        align_items="center",
    ),

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
        ),
        width="100%",
        align_items="center",
    ),
        width="100%",
        align_items="center",
        spacing="9",
    ),
    width="100%",
    align_items="center",
),
    #3user
    width="100%",
), 
    spacing="5",
    width="100%",
)