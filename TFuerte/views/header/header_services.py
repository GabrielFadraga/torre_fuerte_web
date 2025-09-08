import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles

def header_services() -> rx.Component:
    return rx.center(
    rx.vstack(
    rx.hstack(
        rx.vstack(
            rx.heading("Catálogo de actividades"),
            rx.text("1. Mantenimiento y reparación de equipos de lavandería. ", 
                    size="4"),
            rx.text("2. Mantenimiento y reparación de equipos dinámicos (bombas, compresores, ventiladores, extractores, etc). ", 
                    size="4"),
            rx.text("3. Mantenimiento y reparación de turbo generadores.", 
                    size="4"),
            rx.text("4. Mantenimiento y reparación de calderas de baja presión. ", 
                    size="4"),
            rx.text("5. Soldadura especializada en acero negro y acero inoxidable. ", 
                    size="4"),
            rx.text("6. Mantenimiento y reparación de equipos y sistemas de clima.", 
                    size="4"),
            rx.text("7. Fabricación de piezas de repuesto en taller de maquinado.", 
                    size="4"),
            rx.text("8. Mantenimiento y reparación de equipos médicos de baja complejidad (autoclaves). ", 
                    size="4"),
            rx.text("9. Mantenimiento y reparación de circuitos y esquemas eléctricos fabriles y edificaciones.", 
                    size="4"),
            rx.text("10. Mantenimiento y reparación de circuitos y esquemas electro automáticos navales. ", 
                    size="4"),
            rx.text("11. Mantenimiento y reparación de esquemas automáticos fabriles.", 
                    size="4"),
            rx.text("12. Palería de estructuras, planchas e isométricos.", 
                    size="4"),

                    
                #padding_y=styles.Spacer.VERY_BIG.value,
                spacing="3",
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