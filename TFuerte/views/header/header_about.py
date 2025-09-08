import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles

def header_about() -> rx.Component:
        return rx.center(
        rx.vstack(
        rx.hstack(
        rx.vstack(
                rx.heading("Misión"),
                rx.text("""Ser referente nacional en el mantenimiento, reparación y rehabilitación de equipos 
                        industriales, promoviendo la eficiencia y ofreciendo soluciones que impulsen la eficacia, 
                        calidad y rentabilidad, creando un entorno de trabajo seguro, saludable y 
                        sostenible para minimizar el impacto ambiental.""", 
                        size="4"),
                rx.spacer(),

                rx.heading("Visión"),
                rx.text("""Aspiramos a transformar la gestión de activos industriales, 
                        garantizando la máxima disponibilidad de maquinarias y equipos, 
                        reduciendo costos y contribuyendo a un futuro industrial más seguro.""", 
                        size="4"),

                rx.spacer(),

                rx.heading("Valores"),
                rx.text("""Como empresa especializada en servicios técnicos industriales,
                        nuestros valores reflejan la integración del capital humano 
                        (obreros, técnicos e ingenieros) con la excelencia operativa 
                        y el compromiso social: """,
                        size="4"),
                rx.text("1. Seguridad y Prevención",
                size="4"),
                rx.text("2. Excelencia Técnica",
                size="4"),
                rx.text("3. Trabajo en Equipo Multidisciplinar",
                size="4"),
                rx.text("4. Innovación Responsable",
                size="4"),
                rx.text("5. Compromiso Social y Ético",
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