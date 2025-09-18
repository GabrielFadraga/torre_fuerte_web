import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles

def header_about() -> rx.Component:
        return rx.center(
        rx.vstack(
                rx.heading("Misión", color="black", size="8"),
                rx.text("""Ser referente nacional en el mantenimiento, reparación y rehabilitación de equipos 
                        industriales, promoviendo la eficiencia y ofreciendo soluciones que impulsen la eficacia, 
                        calidad y rentabilidad, creando un entorno de trabajo seguro, saludable y 
                        sostenible para minimizar el impacto ambiental.""", 
                        size="7", color="black"),
                rx.spacer(),

                rx.heading("Visión", color="black", size="8"),
                rx.text("""Aspiramos a transformar la gestión de activos industriales, 
                        garantizando la máxima disponibilidad de maquinarias y equipos, 
                        reduciendo costos y contribuyendo a un futuro industrial más seguro.""", 
                        size="7", color="black"),

                rx.spacer(),

                rx.heading("Valores", color="black", size="8"),
                rx.text("""Como empresa especializada en servicios técnicos industriales,
                        nuestros valores reflejan la integración del capital humano 
                        (obreros, técnicos e ingenieros) con la excelencia operativa 
                        y el compromiso social: """,
                        size="7", color="black"),
                rx.text("1. Seguridad y Prevención",
                size="6", color="black"),
                rx.text("2. Excelencia Técnica",
                size="6", color="black"),
                rx.text("3. Trabajo en Equipo Multidisciplinar",
                size="6", color="black"),
                rx.text("4. Innovación Responsable",
                size="6", color="black"),
                rx.text("5. Compromiso Social y Ético",
                size="6", color="black"),
                #padding_y=styles.Spacer.VERY_BIG.value,
                
                spacing="4",
                width="100%",
                justify="center",
                max_width=styles.ABOUT_WIDTH

        ),
        align="center",
        width="100%",
        justify="center",
)