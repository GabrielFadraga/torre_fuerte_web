import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles
from TFuerte.styles.colors import Text_tx


def service_card(title: str, description: str, index: int) -> rx.Component:
    return rx.card(
        rx.vstack(
            # Encabezado de la tarjeta con número y título
            rx.hstack(
                # Número del servicio con diseño circular mejorado
                rx.center(
                    rx.text(
                        str(index),
                        font_size=styles.Spacer.BIG.value,
                        font_weight="bold",
                        color="white",
                    ),
                    background="linear-gradient(135deg, #194264FF 0%, #2a5a8a 100%)",
                    border_radius="50%",
                    width="60px",
                    height="60px",
                    box_shadow="0 4px 8px rgba(25, 66, 100, 0.3)",
                    flex_shrink="0",
                ),
                
                rx.heading(
                    title,
                    font_size=styles.Spacer.BIG.value,
                    color="#194264FF",
                    text_align="left",
                    margin_left=styles.Spacer.MEDIUM.value,
                    flex="1",
                ),
                align_items="center",
                width="100%",
                margin_bottom=styles.Spacer.MEDIUM.value,
            ),
            
            # Descripción del servicio
            rx.text(
                description,
                font_size=styles.Spacer.LARGE.value,
                color="#4A5568",
                text_align="left",
                line_height="1.6",
            ),
            
            # Indicador visual sutil en la parte inferior
            rx.box(
                width="100%",
                height="4px",
                background="linear-gradient(90deg, #194264FF 0%, #2a5a8a 100%)",
                border_radius="2px",
                margin_top=styles.Spacer.MEDIUM.value,
            ),
            
            align_items="start",
            spacing="4",  # Valor numérico fijo para spacing
            width="100%",
        ),
        background_color="white",
        border="1px solid #E2E8F0",
        border_radius="16px",
        padding=styles.Spacer.LARGE.value,
        box_shadow="0 4px 12px rgba(0, 0, 0, 0.08)",
        _hover={
            "box_shadow": "0 8px 25px rgba(25, 66, 100, 0.15)",
            "transform": "translateY(-4px)",
            "transition": "all 0.3s ease-in-out",
            "border": "1px solid #194264FF"
        },
        width="100%",
        margin_bottom=styles.Spacer.LARGE.value,
    )

def header_services() -> rx.Component:
    services = [
        {
            "title": "Mantenimiento y reparación de equipos de lavandería",
            "description": "Nos especializamos en la diagnosis y solución de fallas en lavadoras, secadoras y planchadoras industriales de cualquier marca y capacidad. Realizamos mantenimiento preventivo para alargar su vida útil y reparaciones correctivas rápidas y eficaces, minimizando los tiempos de parada en su operación comercial o hotelera."
        },
        {
            "title": "Mantenimiento y reparación de equipos dinámicos",
            "description": "Ofrecemos servicios completos para bombas, compresores de aire, ventiladores y extractores, que incluyen: balanceo dinámico, alineación mecánica, cambio de sellos y empaquetaduras, y reparación de impulsores. Garantizamos que su equipo opere con la eficiencia energética y confiabilidad que su negocio requiere."
        },
        {
            "title": "Mantenimiento y reparación de turbo generadores",
            "description": "Proporcionamos mantenimiento especializado de alto nivel para turbinas y generadores. Nuestros servicios abarcan desde revisiones programadas y análisis de vibraciones hasta reparaciones mayores (overhaul) y puestas a punto, asegurando que su fuente de energía eléctrica sea constante, segura y rentable."
        },
        {
            "title": "Mantenimiento y reparación de calderas de baja presión",
            "description": "Realizamos inspecciones meticulosas, limpieza química y mecánica interna, reparación de refractarios, y pruebas hidrostáticas para garantizar que su caldera opere dentro de los parámetros de seguridad y eficiencia definidos por la normativa, optimizando el consumo de combustible."
        },
        {
            "title": "Soldadura especializada en acero negro y acero inoxidable",
            "description": "Contamos con soldadores certificados y los procedimientos más exigentes para ejecutar trabajos de la más alta calidad. Ya sea para reparar equipos críticos, fabricar estructuras o unir tuberías, garantizamos soldaduras limpias, resistentes y con la penetración adecuada, cumpliendo con los códigos ASME y AWS según sea necesario."
        },
        {
            "title": "Mantenimiento y reparación de equipos y sistemas de clima",
            "description": "Ofrecemos servicios completos para sus equipos de aire acondicionado y refrigeración: instalación, mantenimiento preventivo (limpieza de coils, cambio de filtros, recarga de gas), y diagnosis y reparación de fallas electrónicas y mecánicas."
        },
        {
            "title": "Fabricación de piezas de repuesto en taller de maquinado",
            "description": "Cuando una pieza falla o está obsoleta, nosotros la fabricamos. Nuestro taller de maquinado cuenta con tornos, fresadoras y equipos de corte para diseñar y producir repuestos, componentes personalizados o adaptaciones con precisión, rapidez y los materiales especificados, reduciendo costos y tiempos de espera."
        },
        {
            "title": "Mantenimiento y reparación de circuitos eléctricos fabriles y edificaciones",
            "description": "Solucionamos cualquier problema en sus sistemas eléctricos. Diagnosticamos y reparamos fallas en cuadros de distribución, cableados, breakers y sistemas de iluminación industrial, garantizando la seguridad de las personas y la continuidad operativa de su negocio."
        },
        {
            "title": "Mantenimiento y reparación de circuitos electro automáticos navales",
            "description": "Entendemos las exigentes condiciones del entorno marino. Somos especialistas en la troubleshooting, reparación y puesta a punto de sistemas de control, automatización y potencia eléctrica específicos de embarcaciones, cumpliendo con los estrictos estándares de la industria naval."
        },
        {
            "title": "Mantenimiento y reparación de esquemas automáticos fabriles",
            "description": "Diagnosticamos y reparamos fallas en sistemas de control basados en PLCs (Controladores Lógicos Programables), sensores, actuadores y variadores de frecuencia. Nos aseguramos de que sus líneas de producción automatizadas funcionen de manera sincronizada y eficiente."
        },
        {
            "title": "Palería de estructuras, planchas e isométricos",
            "description": "Transformamos planos en estructuras y componentes reales. Nuestros expertos en palería realizan el trazado y desarrollo preciso de planchas metálicas para la fabricación de ductos, tolvas, tanques, estructuras y tuberías, interpretando planos isométricos y estructurales con la máxima fidelidad."
        }
    ]
    
    return rx.vstack(
        # Encabezado principal
        rx.center(
            rx.vstack(
                rx.heading(
                    "Nuestros Servicios Técnicos",
                    font_size=styles.Spacer.VERY_BIG.value,
                    color="#194264FF",
                    text_align="center",
                    font_weight="bold",
                    margin_bottom=styles.Spacer.SMALL.value,
                ),
                rx.text(
                    "Soluciones integrales y especializadas para mantener sus operaciones en óptimas condiciones",
                    font_size=styles.Spacer.LARGE.value,
                    color="#4A5568",
                    text_align="center",
                    max_width="800px",
                    line_height="1.5",
                ),
                rx.divider(
                    width="100px",
                    height="4px",
                    background="linear-gradient(90deg, #194264FF 0%, #2a5a8a 100%)",
                    border_radius="2px",
                    margin_top=styles.Spacer.MEDIUM.value,
                ),
                align_items="center",
                spacing="4",  # Valor numérico fijo
            ),
            width="100%",
            padding_y=styles.Spacer.VERY_BIG.value,
            background="linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 100%)",
            margin_bottom=styles.Spacer.LARGE.value,
        ),
        
        # Contenedor de servicios
        rx.box(
            *[
                service_card(service["title"], service["description"], i + 1)
                for i, service in enumerate(services)
            ],
            width="100%",
            max_width="1400px",
            padding_x=styles.Spacer.LARGE.value,
        ),
        
        # Llamada a la acción
        rx.center(
            rx.vstack(
                rx.heading(
                    "¿Necesita alguno de nuestros servicios?",
                    font_size=styles.Spacer.BIG.value,
                    color="white",
                    text_align="center",
                    margin_bottom=styles.Spacer.SMALL.value,
                ),
                rx.text(
                    "Contáctenos para una evaluación gratuita de sus necesidades",
                    font_size=styles.Spacer.LARGE.value,
                    color="rgba(255, 255, 255, 0.9)",
                    text_align="center",
                    margin_bottom=styles.Spacer.MEDIUM.value,
                    max_width="600px",
                ),
                rx.button(
                    "Solicitar Presupuesto",
                    background="linear-gradient(135deg, #FFFFFF 0%, #F7FAFC 100%)",
                    color="#194264FF",
                    border_radius="8px",
                    padding_x=styles.Spacer.LARGE.value,
                    padding_y=styles.Spacer.MEDIUM.value,
                    font_size=styles.Spacer.LARGE.value,
                    font_weight="bold",
                    box_shadow="0 4px 12px rgba(255, 255, 255, 0.3)",
                    _hover={
                        "box_shadow": "0 6px 18px rgba(255, 255, 255, 0.4)",
                        "transform": "translateY(-2px)",
                        "background": "linear-gradient(135deg, #F7FAFC 0%, #EDF2F7 100%)",
                    },
                ),
                align_items="center",
                spacing="4",  # Valor numérico fijo
            ),
            width="100%",
            padding_y=styles.Spacer.VERY_BIG.value,
            background="linear-gradient(135deg, #194264FF 0%, #2a5a8a 100%)",
            margin_top=styles.Spacer.LARGE.value,
        ),
        
        spacing="0",  # Valor numérico fijo
        width="100%",
        align="center",
    )