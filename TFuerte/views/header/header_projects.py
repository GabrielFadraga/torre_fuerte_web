import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles

class GalleryState(rx.State):
    show_details: bool = False
    selected_project: int = 0
    
    projects = [
        {
            "title": "Residencia Moderna",
            "category": "Residencial", 
            "description": "Diseño contemporáneo con espacios abiertos y máxima iluminación natural",
            "year": "2023"
        },
        {
            "title": "Oficinas Corporativas",
            "category": "Comercial",
            "description": "Espacios de trabajo innovadores que fomentan la colaboración y productividad", 
            "year": "2024"
        },
        {
            "title": "Centro Comercial Vista",
            "category": "Comercial",
            "description": "Arquitectura comercial que redefine la experiencia de compra",
            "year": "2023"
        },
        {
            "title": "Nave Industrial Smart", 
            "category": "Industrial",
            "description": "Instalaciones industriales con tecnología de punta y eficiencia energética",
            "year": "2024"
        },
        {
            "title": "Casa de Playa",
            "category": "Residencial",
            "description": "Integración perfecta entre arquitectura y naturaleza costera",
            "year": "2023"
        },
        {
            "title": "Casa de Playa",
            "category": "Residencial",
            "description": "Integración perfecta entre arquitectura y naturaleza costera",
            "year": "2023"
        },
        {
            "title": "Casa de Playa",
            "category": "Residencial",
            "description": "Integración perfecta entre arquitectura y naturaleza costera",
            "year": "2023"
        },
        {
            "title": "Casa de Playa",
            "category": "Residencial",
            "description": "Integración perfecta entre arquitectura y naturaleza costera",
            "year": "2023"
        },
        {
            "title": "Oficinas Corporativas",
            "category": "Comercial",
            "description": "Espacios de trabajo innovadores que fomentan la colaboración y productividad", 
            "year": "2024"
        },
        {
            "title": "Oficinas Corporativas",
            "category": "Comercial",
            "description": "Espacios de trabajo innovadores que fomentan la colaboración y productividad", 
            "year": "2024"
        },
        {
            "title": "Oficinas Corporativas",
            "category": "Comercial",
            "description": "Espacios de trabajo innovadores que fomentan la colaboración y productividad", 
            "year": "2024"
        },
        {
            "title": "Oficinas Corporativas",
            "category": "Comercial",
            "description": "Espacios de trabajo innovadores que fomentan la colaboración y productividad", 
            "year": "2024"
        },
        {
            "title": "Oficinas Corporativas",
            "category": "Comercial",
            "description": "Espacios de trabajo innovadores que fomentan la colaboración y productividad", 
            "year": "2024"
        },
        {
            "title": "Oficinas Corporativas",
            "category": "Comercial",
            "description": "Espacios de trabajo innovadores que fomentan la colaboración y productividad", 
            "year": "2024"
        },
        {
            "title": "Planta de Producción",
            "category": "Industrial",
            "description": "Optimización de procesos industriales con diseño inteligente",
            "year": "2024"
        }
    ]

def gallery() -> rx.Component:
    return rx.box(
        # Header
        rx.hstack(
            rx.vstack(
                rx.heading("Portafolio de trabajos realizados", 
                            size="9",
                            font_size=styles.Spacer.VERY_BIG.value,
                            margin=styles.Spacer.EXTRA_SMALL.value),
                spacing="2"
            ),
            width="100%",
            padding_y="4rem",
            background="#194264FF",
            #color="white",
            align_items="center",
            justify="center",
            z_index="1000",
            background_size="cover",
            id="inicio",
        ),
        
        # Projects Grid - Simple and compatible
        rx.box(
            rx.vstack(
                # First row
                rx.hstack(
                    rx.box(_project_card(0)),
                    rx.box(_project_card(1)), 
                    rx.box(_project_card(2)),
                    rx.box(_project_card(3)),
                    rx.box(_project_card(4)),
                    spacing="6",
                    width="100%",
                    justify="center"
                ),
                # Second row  
                rx.hstack(
                    rx.box(_project_card(5)),
                    rx.box(_project_card(6)),
                    rx.box(_project_card(7)),
                    rx.box(_project_card(8)),
                    rx.box(_project_card(9)),
                    spacing="6", 
                    width="100%",
                    justify="center"
                ),
                # Third row  
                rx.hstack(
                    rx.box(_project_card(10)),
                    rx.box(_project_card(11)),
                    rx.box(_project_card(12)),
                    rx.box(_project_card(13)),
                    rx.box(_project_card(14)),
                    spacing="6", 
                    width="100%",
                    justify="center"
                ),
                spacing="6",
                width="100%",
                #max_width="1200px"
            ),
            width="100%",
            padding="2rem"
        ),
        
        # Footer
        rx.center(
            rx.vstack(
                rx.heading("Contáctanos para tu próximo proyecto", size="5", color="black"),
                rx.button("Contactar", size="3"),
                spacing="3"
            ),
            width="100%",
            padding_y="4rem",
            background="#f8fafc"
        ),

        width="100%"
    )

def _project_card(index: int) -> rx.Component:
    project = GalleryState.projects[index]
    
    return rx.box(
        rx.vstack(
            # Header con categoría y año
            rx.hstack(
                rx.badge(
                    project["category"],
                    color_scheme=_get_color(project["category"]),
                    size="2"
                ),
                rx.spacer(),
                rx.text(project["year"], size="2", color="black", weight="bold"),
                width="100%"
            ),
            
            # Título
            rx.heading(
                project["title"],
                size="6",
                color="black",
                margin_top="1.5rem"
            ),
            
            # Imagen placeholder más grande
            rx.box(
                width="100%",
                height="300px",  # Más alta
                background=_get_gradient(project["category"]),
                border_radius="12px",
                margin_top="1rem",
                position="relative",
                overflow="hidden"
            ),
            
            # Información del proyecto
            rx.vstack(
                rx.text(
                    project["description"],
                    size="3",
                    color="black",
                    margin_top="1rem"
                ),
                
                
                # Botón de acción
                rx.button(
                    "Ver Detalles",
                    on_click=lambda: GalleryState.set_selected_project(index),
                    size="3",
                    width="100%",
                    margin_top="2rem",
                    variant="solid"
                ),
                
                spacing="0",
                align="start",
                width="100%"
            ),
            
            spacing="0",
            align="start",
            height="100%"
        ),
        padding="2.5rem",  # Más padding interno
        border="1px solid #e2e8f0", 
        border_radius="16px",
        background="white",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        width="500px",  # Ancho fijo más grande
        min_height="650px",  # Altura mínima
        transition="all 0.3s ease",
        _hover={
            "box_shadow": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
            "transform": "translateY(-4px)"
        }
    )

def _get_gradient(category: str) -> str:
    gradients = {
        "Residencial": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "Comercial": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)", 
        "Industrial": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
    }
    return gradients.get(category, "linear-gradient(135deg, #667eea 0%, #764ba2 100%)")

def _get_color(category: str) -> str:
    colors = {
        "Residencial": "blue",
        "Comercial": "purple",
        "Industrial": "cyan"
    }
    return colors.get(category, "blue")