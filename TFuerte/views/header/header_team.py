import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles
from TFuerte.views.header.header_responsive import header_responsive

def header_team() -> rx.Component:
    return rx.center(
        rx.vstack(
        rx.desktop_only(
        rx.hstack(
            rx.heading("Consejo Directivo"),
            align_items="start",
            margin=styles.Spacer.SMALL.value,
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
            rx.text("Jefa de Área Administrativa"),
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
            rx.text("Ing. Gilberto Acosta Monjes"),
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

    ),
    #3user
    rx.mobile_and_tablet(
        header_responsive(),
    ),

    width="100%",
    spacing="6",
), 
    spacing="6",
    width="100%",
)