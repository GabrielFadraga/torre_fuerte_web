import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles

def header_projects() -> rx.Component:
    return rx.center(
    rx.vstack(
    rx.hstack(
        rx.vstack(
            rx.heading("Trayectoria de la empresa"),
            rx.text("""Ser referente nacional en el mantenimiento, reparación y rehabilitación de equipos 
                        industriales, promoviendo la eficiencia y ofreciendo soluciones que impulsen la eficacia, 
                        calidad y rentabilidad, creando un entorno de trabajo seguro, saludable y 
                        sostenible para minimizar el impacto ambiental.""", 
                    size="4"),

                    
                #padding_y=styles.Spacer.VERY_BIG.value,
                spacing="4",
                width="100%",
            ),
            align_items="start",
            width="100%",
        ),
        
    #spacing="5",
    width="100%",
    align_items="start",

    ),
)