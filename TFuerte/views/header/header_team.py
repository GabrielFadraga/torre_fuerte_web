import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles
from TFuerte.views.header.header_responsive import header_responsive
from TFuerte.styles.colors import Text_tx

def header_team() -> rx.Component:
    return rx.center(
        rx.vstack(
        rx.desktop_only(
        rx.hstack(
            rx.heading("Consejo Directivo", size="9"),
            align="start",
            margin=styles.Spacer.SMALL.value,
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
            rx.text("Lic Maikel Torres López", size="7"),
            rx.text("Presidente", size="6"),
            width="100%",
            align_items="center",
            color=Text_tx.Black.value,
        ),
        width="100%",
        align_items="center",
        padding_y="1em"
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
            rx.text("Ing. Euclides Rodríguez Mejías", size="7"),
            rx.text("Director Adjunto", size="6"),
            width="100%",
            align_items="center",
            color=Text_tx.Black.value,
        ),
        width="100%",
        align_items="center",
        padding_y="1em"
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
            rx.text("Lic. Meylin Yu Parra", size="7"),
            rx.text("Jefa de Área Administrativa", size="6"),
            width="100%",
            align_items="center",
            color=Text_tx.Black.value,
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
            rx.text("Ing. Miguel Obregón Salomón", size="7"),
            rx.text("Jefe de Área Logística", size="6"),
            width="100%",
            align_items="center",
            color=Text_tx.Black.value,
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
    padding_y="1em"
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
            rx.text("Ing. Gilberto Acosta Monjes", size="7"),
            rx.text("Jefe de Coordinación Habana-Mayabeque", size="6"),
            width="100%",
            align_items="center",
            color=Text_tx.Black.value,
        ),
        width="100%",
        align_items="center",
    ),

    rx.spacer(),
    rx.spacer(),

            rx.vstack(
            rx.image(
                src="user1.png", 
                width="200px", 
                height="auto",
            ),
        rx.vstack(
            rx.text("Ing. Manuel Núñez Brea", size="7"),
            rx.text("Jefe de Coordinación Oriente", size="6"),
            width="100%",
            align_items="center",
            color=Text_tx.Black.value,
        ),
        width="100%",
        align_items="center",
    ),

    rx.spacer(),
    rx.spacer(),

    rx.vstack(
            rx.image(
                src="user1.png", 
                width="200px", 
                height="auto",
            ),
        rx.vstack(
            rx.text("T.M Alexander Martínez Elias", size="7"),
            rx.text("Jefa de Área Técnica", size="6"),
            width="100%",
            align_items="center",
            color=Text_tx.Black.value,
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
    padding_y="1em",
),

    ),
    #3user
    rx.mobile_and_tablet(
        header_responsive(),
    ),
    align="center",
    width="100%",
    spacing="6",
), 
    spacing="6",
    width="100%",
)