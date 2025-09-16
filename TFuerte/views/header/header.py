import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles

def header() -> rx.Component:
    return rx.center(
    rx.vstack(
    rx.hstack(
        rx.image( 
                src="sf.png",
                radius="none",
            ),
        
        rx.vstack(
            rx.heading("Con la mirada en lo alto"),
            rx.text("maidomm78@gmail.com", size="2"),
            spacing="1",
            padding_y=styles.Spacer.VERY_BIG.value,
            ),
            align_items="start",
            width="100%",
        ),

    #rx.flex(
        #    rx.vstack(
        #    info_text("+5", "años de experiencia"),
        #    rx.spacer(),
        #    info_text("+50", "profesionales dando servicio en Cuba"),
        #    spacing="1",
        #    ),
        #     width="100%",
        #),
        rx.vstack(
        rx.text(
                """Nos dedicamos a brindar servicios de reparación, mantenimiento y rehabilitación de 
                equipos industriales en las especialidades de mecánica, electricidad y automática. 
                Además contamos con talleres de mecánica industrial con máquinas y herramientas.""" ),
            spacing="4",
            ),
        
    spacing="5",
    width="100%",
    align_items="start",

    ),
)
