import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles
from TFuerte.styles.colors import Text_tx, Color_tx

class GalleryState(rx.State):
    """Estado para manejar el lightbox de imágenes de proyectos"""
    selected_image: str = ""
    show_lightbox: bool = False
    filter_category: str = "Todos"
    
    def open_lightbox(self, image: str):
        self.selected_image = image
        self.show_lightbox = True
    
    def close_lightbox(self):
        self.show_lightbox = False
        self.selected_image = ""
    
    def set_filter_category(self, category: str):
        self.filter_category = category

def creative_project_card(project: dict, delay: float, rotation: float) -> rx.Component:
    """Tarjeta de proyecto creativa con efectos 3D - COMPLETAMENTE RESPONSIVE"""
    return rx.box(
        rx.vstack(
            # Contenedor de imagen del proyecto - MISMOS PARÁMETROS QUE EL TALLER
            rx.box(
                rx.image(
                    src=project["image"],  # CAMBIADO: Usar directamente el nombre del archivo como en el taller
                    width="100%",
                    height="250px",
                    object_fit="cover",
                    border_radius="15px",
                    transition="all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94)",
                    filter="brightness(0.95) contrast(1.1)",
                    _hover={
                        "filter": "brightness(1.05) contrast(1.2)",
                    }
                ),
                # Overlay de información creativo - SOLO DESKTOP
                rx.box(
                    rx.vstack(
                        rx.badge(
                            project["category"],
                            color_scheme=_get_color_scheme(project["category"]),
                            variant="solid",
                            size="1",
                            margin_bottom="8px"
                        ),
                        rx.text(
                            project["title"],
                            font_size="18px",
                            font_weight="black",
                            color="white",
                            text_align="center",
                            text_shadow="0 2px 8px rgba(0,0,0,0.8)",
                        ),
                        rx.text(
                            project["year"],
                            font_size="14px",
                            color="rgba(255,255,255,0.9)",
                            text_align="center",
                            text_shadow="0 1px 4px rgba(0,0,0,0.6)",
                        ),
                        rx.box(
                            rx.text(
                                "👆 Click para ampliar",
                                font_size="10px",
                                color="rgba(255,255,255,0.7)",
                                text_align="center",
                            ),
                            background="rgba(0,0,0,0.5)",
                            padding="4px 8px",
                            border_radius="10px",
                            margin_top="8px",
                        ),
                        align_items="center",
                        spacing="2",
                    ),
                    position="absolute",
                    bottom="0",
                    left="0",
                    right="0",
                    padding="20px",
                    background="linear-gradient(transparent, rgba(0,0,0,0.8))",
                    border_radius="0 0 15px 15px",
                    opacity="0",
                    transition="all 0.3s ease",
                    class_name="info-overlay"
                ),
                # Efecto de brillo al hover - SOLO DESKTOP
                rx.box(
                    background=f"linear-gradient(45deg, transparent, {_get_color(project['category'])}30, transparent)",
                    position="absolute",
                    top="0",
                    left="-100%",
                    width="100%",
                    height="100%",
                    transition="all 0.6s ease",
                    border_radius="15px",
                    opacity="0",
                    class_name="shine-effect"
                ),
                position="relative",
                overflow="hidden",
                width="100%",
                height="100%",
                cursor="pointer",
                on_click=GalleryState.open_lightbox(project["image"]),  # CAMBIADO: Pasar solo el nombre del archivo
                _hover={
                    ".info-overlay": {
                        "opacity": "1",
                    },
                    ".shine-effect": {
                        "left": "100%",
                        "opacity": "1",
                    }
                }
            ),
            # Información para móvil/tablet - SIEMPRE VISIBLE
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.badge(
                            project["category"],
                            color_scheme=_get_color_scheme(project["category"]),
                            variant="solid",
                            size="1"
                        ),
                        rx.spacer(),
                        rx.text(
                            project["year"],
                            font_size="12px",
                            color=Text_tx.Black.value,
                            font_weight="medium",
                        ),
                        width="100%",
                    ),
                    rx.text(
                        project["title"],
                        font_size="16px",
                        font_weight="bold",
                        color=Text_tx.Black.value,
                        text_align="left",
                        margin_top="8px",
                    ),
                    rx.text(
                        project["description"],
                        font_size="14px",
                        color=Text_tx.Black.value,
                        text_align="left",
                        line_height="1.4",
                        margin_top="4px",
                    ),
                    # Características del proyecto
                    rx.vstack(
                        *[
                            rx.hstack(
                                rx.box(
                                    width="6px",
                                    height="6px",
                                    background=_get_color(project["category"]),
                                    border_radius="50%",
                                    margin_right="8px"
                                ),
                                rx.text(
                                    feature,
                                    size="2",
                                    color=Text_tx.Black.value,
                                ),
                                align_items="center",
                                margin_top="4px"
                            )
                            for feature in project["features"][:2]  # Mostrar solo 2 características
                        ],
                        align_items="start",
                        width="100%",
                        margin_top="12px"
                    ),
                    align_items="start",
                    spacing="2",
                    width="100%",
                    padding_x="10px",
                    padding_bottom="15px",
                    padding_top="15px",
                ),
                class_name="mobile-info"
            ),
            align_items="center",
            spacing="0",
            width="100%",
        ),
        # Efectos de la tarjeta creativa - RESPONSIVE
        transform=f"rotate({rotation}deg) scale(0.98)",
        transition="all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)",
        animation=f"creativeEntrance 1s ease-out {delay}s both",
        _hover={
            "transform": f"rotate({rotation * 0.7}deg) scale(1.03)",
        },
        box_shadow=f"0 20px 40px {_get_color(project['category'])}25, 0 0 0 1px rgba(255,255,255,0.1), inset 0 1px 0 rgba(255,255,255,0.1)",
        border_radius="18px",
        background="white",
        class_name="creative-project-card",
        width="100%",
        max_width="400px",
    )

def lightbox_component() -> rx.Component:
    """Componente de lightbox para mostrar imágenes ampliadas - RESPONSIVE"""
    return rx.cond(
        GalleryState.show_lightbox,
        rx.box(
            rx.box(
                # Overlay de fondo con efecto de desenfoque
                rx.box(
                    width="100%",
                    height="100%",
                    background="rgba(0,0,0,0.92)",
                    position="absolute",
                    top="0",
                    left="0",
                    on_click=GalleryState.close_lightbox,
                    backdrop_filter="blur(10px)",
                ),
                # Contenido del lightbox - MISMOS PARÁMETROS QUE EL TALLER
                rx.center(
                    rx.vstack(
                        rx.box(
                            rx.image(
                                src=GalleryState.selected_image,  # CAMBIADO: Usar directamente el nombre del archivo
                                max_width="85vw",
                                max_height="80vh",
                                object_fit="contain",
                                border_radius="15px",
                                box_shadow="0 40px 80px rgba(0,0,0,0.6)",
                                animation="lightboxEntrance 0.4s ease-out",
                            ),
                            position="relative",
                        ),
                        rx.button(
                            "✕ Cerrar",
                            background="rgba(255,255,255,0.15)",
                            color="white",
                            border="2px solid rgba(255,255,255,0.3)",
                            padding_x="25px",
                            padding_y="12px",
                            border_radius="10px",
                            margin_top="25px",
                            font_weight="bold",
                            font_size="16px",
                            _hover={
                                "background": "rgba(255,255,255,0.25)",
                                "transform": "scale(1.05)",
                            },
                            transition="all 0.3s ease",
                            on_click=GalleryState.close_lightbox,
                        ),
                        align_items="center",
                        spacing="4",
                    ),
                    position="relative",
                    z_index="1000",
                    padding_x="20px",
                ),
                # Botón de cerrar en esquina
                rx.button(
                    "✕",
                    position="absolute",
                    top="25px",
                    right="25px",
                    background="rgba(255,255,255,0.15)",
                    color="white",
                    border_radius="50%",
                    width="55px",
                    height="55px",
                    font_size="22px",
                    _hover={
                        "background": "rgba(255,255,255,0.25)",
                        "transform": "scale(1.1) rotate(90deg)",
                    },
                    transition="all 0.3s ease",
                    on_click=GalleryState.close_lightbox,
                    z_index="1001",
                ),
                position="fixed",
                top="0",
                left="0",
                width="100%",
                height="100%",
                z_index="9999",
                display="flex",
                align_items="center",
                justify_content="center",
                animation="fadeIn 0.3s ease-out",
            )
        ),
        rx.box()
    )

def navigation_tabs() -> rx.Component:
    """Pestañas de navegación para filtros - COMPLETAMENTE RESPONSIVE"""
    
    def create_filter_button(category: str) -> rx.Component:
        return rx.button(
            category,
            background=rx.match(
                GalleryState.filter_category,
                (category, f"linear-gradient(135deg, {_get_color(category)} 0%, {_get_dark_color(category)} 100%)"),
                "rgba(255,255,255,0.1)"
            ),
            color=rx.match(
                GalleryState.filter_category,
                (category, "white"),
                "rgba(255,255,255,0.8)"
            ),
            border=rx.match(
                GalleryState.filter_category,
                (category, f"2px solid {_get_color(category)}"),
                "2px solid rgba(255,255,255,0.2)"
            ),
            padding_x="20px",
            padding_y="10px",
            border_radius="12px",
            font_size="14px",
            font_weight="bold",
            transition="all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)",
            _hover={
                "transform": "translateY(-2px)",
                "box_shadow": "0 8px 20px rgba(0,0,0,0.2)",
            },
            on_click=GalleryState.set_filter_category(category),
            white_space="nowrap",
        )
    
    return rx.center(
        rx.box(
            # Desktop - Botones compactos en fila
            rx.hstack(
                create_filter_button("Todos"),
                create_filter_button("Residencial"),
                create_filter_button("Comercial"),
                create_filter_button("Industrial"),
                spacing="5",
                justify="center",
                # Solo visible en desktop (lg en adelante)
                display=["none", "none", "flex"],
                class_name="desktop-navigation"
            ),
            # Mobile/Tablet - Botones en columna
            rx.vstack(
                create_filter_button("Todos"),
                create_filter_button("Residencial"),
                create_filter_button("Comercial"),
                create_filter_button("Industrial"),
                spacing="4",
                justify="center",
                width="100%",
                # Solo visible en móvil y tablet (hasta md)
                display=["flex", "flex", "none"],
                class_name="mobile-navigation"
            ),
            width="100%",
        ),
        width="100%",
        padding_y=styles.Spacer.MEDIUM.value,
        background="linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
        padding_x=["15px", "20px", "0px"],
    )

def gallery() -> rx.Component:
    """Sección principal de galería de proyectos - COMPLETAMENTE RESPONSIVE"""
    
    # Lista de proyectos - USANDO EXACTAMENTE EL MISMO FORMATO QUE EL TALLER
    projects = [
        {
            "title": "Residencia Moderna",
            "category": "Residencial", 
            "description": "Diseño contemporáneo con espacios abiertos y máxima iluminación natural",
            "year": "2023",
            "features": ["Diseño sustentable", "Máxima iluminación", "Espacios integrados"],
            "image": "1.jpg",  # SOLO EL NOMBRE DEL ARCHIVO, COMO EN EL TALLER
            "delay": 0.1,
            "rotation": -2
        },
        {
            "title": "Oficinas Corporativas",
            "category": "Comercial",
            "description": "Espacios de trabajo innovadores que fomentan la colaboración", 
            "year": "2024",
            "features": ["Open space", "Áreas colaborativas", "Tecnología integrada"],
            "image": "2.jpg",  # SOLO EL NOMBRE DEL ARCHIVO, COMO EN EL TALLER
            "delay": 0.2,
            "rotation": 1
        },
        {
            "title": "Centro Comercial Vista",
            "category": "Comercial",
            "description": "Arquitectura comercial que redefine la experiencia de compra",
            "year": "2023",
            "features": ["Diseño experiencial", "Circulación fluida", "Fachada innovadora"],
            "image": "3.jpg",  # SOLO EL NOMBRE DEL ARCHIVO, COMO EN EL TALLER
            "delay": 0.3,
            "rotation": -1
        },
        {
            "title": "Nave Industrial Smart", 
            "category": "Industrial",
            "description": "Instalaciones industriales con tecnología de punta",
            "year": "2024",
            "features": ["Eficiencia energética", "Automatización", "Seguridad industrial"],
            "image": "4.jpg",  # SOLO EL NOMBRE DEL ARCHIVO, COMO EN EL TALLER
            "delay": 0.4,
            "rotation": 2
        },
        {
            "title": "Casa de Playa",
            "category": "Residencial",
            "description": "Integración perfecta entre arquitectura y naturaleza costera",
            "year": "2023",
            "features": ["Resistente a corrosión", "Vistas al mar", "Terraza amplia"],
            "image": "5.jpg",  # SOLO EL NOMBRE DEL ARCHIVO, COMO EN EL TALLER
            "delay": 0.5,
            "rotation": -3
        },
        {
            "title": "Edificio Multifamiliar",
            "category": "Residencial", 
            "description": "Complejo residencial con amenities premium",
            "year": "2024",
            "features": ["Amenities", "Áreas verdes", "Estacionamiento inteligente"],
            "image": "6.jpg",  # SOLO EL NOMBRE DEL ARCHIVO, COMO EN EL TALLER
            "delay": 0.6,
            "rotation": 1
        },
        {
            "title": "Restaurante Gourmet",
            "category": "Comercial",
            "description": "Ambiente sofisticado que realza la experiencia gastronómica",
            "year": "2023",
            "features": ["Acústica perfecta", "Iluminación especializada", "Cocina industrial"],
            "image": "7.jpg",  # SOLO EL NOMBRE DEL ARCHIVO, COMO EN EL TALLER
            "delay": 0.7,
            "rotation": -2
        },
        {
            "title": "Planta de Producción",
            "category": "Industrial",
            "description": "Optimización de procesos industriales con diseño inteligente",
            "year": "2024",
            "features": ["Logística optimizada", "Sustentabilidad", "Control de calidad"],
            "image": "8.jpg",  # SOLO EL NOMBRE DEL ARCHIVO, COMO EN EL TALLER
            "delay": 0.8,
            "rotation": 3
        },
        {
            "title": "Vivienda Minimalista",
            "category": "Residencial",
            "description": "Concepto de vida minimal con máximo aprovechamiento del espacio",
            "year": "2023",
            "features": ["Diseño minimalista", "Optimización espacial", "Materiales naturales"],
            "image": "9.jpg",  # SOLO EL NOMBRE DEL ARCHIVO, COMO EN EL TALLER
            "delay": 0.9,
            "rotation": -1
        },
        {
            "title": "Showroom Tecnológico",
            "category": "Comercial",
            "description": "Espacio expositivo con integración tecnológica de vanguardia",
            "year": "2024",
            "features": ["Tecnología inmersiva", "Flexibilidad espacial", "Sostenibilidad"],
            "image": "10.jpg",  # SOLO EL NOMBRE DEL ARCHIVO, COMO EN EL TALLER
            "delay": 1.0,
            "rotation": 2
        }
    ]
    
    # Filtrar proyectos según la categoría seleccionada - USANDO LISTAS ESTÁTICAS
    projects_all = projects
    projects_residencial = [p for p in projects if p["category"] == "Residencial"]
    projects_comercial = [p for p in projects if p["category"] == "Comercial"]
    projects_industrial = [p for p in projects if p["category"] == "Industrial"]
    
    def render_projects_grid(projects_list):
        """Renderiza el grid de proyectos"""
        return rx.grid(
            *[creative_project_card(project, project["delay"], project["rotation"]) for project in projects_list],
            columns="3",
            spacing="6",
            width="100%",
            max_width="1200px",
            justify="center",
            class_name="projects-grid"
        )
    
    return rx.box(
        rx.vstack(
            # Hero Section Ultra Creativa - RESPONSIVE
            rx.center(
                rx.vstack(
                    rx.box(
                        rx.heading(
                            "PORTAFOLIO DE EXCELENCIA ARQUITECTÓNICA",
                            font_size="32px",
                            color="white",
                            text_align="center",
                            font_weight="black",
                            line_height="1.1",
                            margin_bottom=styles.Spacer.MEDIUM.value,
                            text_shadow="0 4px 20px rgba(0,0,0,0.5)",
                            animation="titleEntrance 1.2s ease-out",
                            class_name="hero-heading"
                        ),
                        rx.text(
                            "Transformamos visiones en espacios extraordinarios que inspiran y perduran",
                            font_size="18px",
                            color="rgba(255, 255, 255, 0.9)",
                            text_align="center",
                            max_width="900px",
                            line_height="1.4",
                            animation="subtitleEntrance 1.2s ease-out 0.3s both",
                            text_shadow="0 2px 10px rgba(0,0,0,0.3)",
                            class_name="hero-subtitle"
                        ),
                        align_items="center",
                        spacing="6",
                    ),
                    
                    # Stats creativas - RESPONSIVE
                    rx.box(
                        # Desktop
                        rx.hstack(
                            rx.vstack(
                                rx.heading(
                                    "50+",
                                    font_size="36px",
                                    color="#43e97b",
                                    font_weight="black",
                                    animation="countUp 1s ease-out 0.7s both",
                                    text_shadow="0 0 20px rgba(67,233,123,0.5)",
                                ),
                                rx.text(
                                    "Proyectos Completados",
                                    font_size="14px",
                                    color="rgba(255, 255, 255, 0.8)",
                                    font_weight="600",
                                ),
                                align_items="center",
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.heading(
                                    "8",
                                    font_size="36px",
                                    color="#fa709a",
                                    font_weight="black",
                                    animation="countUp 1s ease-out 0.9s both",
                                    text_shadow="0 0 20px rgba(250,112,154,0.5)",
                                ),
                                rx.text(
                                    "Años de Experiencia",
                                    font_size="14px",
                                    color="rgba(255, 255, 255, 0.8)",
                                    font_weight="600",
                                ),
                                align_items="center",
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.heading(
                                    "100%",
                                    font_size="36px",
                                    color="#4facfe",
                                    font_weight="black",
                                    animation="countUp 1s ease-out 1.1s both",
                                    text_shadow="0 0 20px rgba(79,172,254,0.5)",
                                ),
                                rx.text(
                                    "Clientes Satisfechos",
                                    font_size="14px",
                                    color="rgba(255, 255, 255, 0.8)",
                                    font_weight="600",
                                ),
                                align_items="center",
                                spacing="1",
                            ),
                            spacing="8",
                            justify="center",
                            margin_top=styles.Spacer.LARGE.value,
                            animation="statsEntrance 1s ease-out 0.5s both",
                            class_name="desktop-stats"
                        ),
                        # Mobile/Tablet
                        rx.vstack(
                            rx.hstack(
                                rx.vstack(
                                    rx.heading(
                                        "50+",
                                        font_size="24px",
                                        color="#43e97b",
                                        font_weight="black",
                                    ),
                                    rx.text(
                                        "Proyectos",
                                        font_size="11px",
                                        color="rgba(255, 255, 255, 0.8)",
                                        font_weight="600",
                                    ),
                                    align_items="center",
                                    spacing="1",
                                ),
                                rx.vstack(
                                    rx.heading(
                                        "8",
                                        font_size="24px",
                                        color="#fa709a",
                                        font_weight="black",
                                    ),
                                    rx.text(
                                        "Años Exp.",
                                        font_size="11px",
                                        color="rgba(255, 255, 255, 0.8)",
                                        font_weight="600",
                                    ),
                                    align_items="center",
                                    spacing="1",
                                ),
                                rx.vstack(
                                    rx.heading(
                                        "100%",
                                        font_size="24px",
                                        color="#4facfe",
                                        font_weight="black",
                                    ),
                                    rx.text(
                                        "Clientes",
                                        font_size="11px",
                                        color="rgba(255, 255, 255, 0.8)",
                                        font_weight="600",
                                    ),
                                    align_items="center",
                                    spacing="1",
                                ),
                                spacing="4",
                                justify="center",
                                wrap="wrap",
                                width="100%",
                            ),
                            margin_top=styles.Spacer.MEDIUM.value,
                            spacing="3",
                            class_name="mobile-stats"
                        ),
                    ),
                    
                    align_items="center",
                    spacing="8",
                    position="relative",
                    z_index="2",
                ),
                width="100%",
                padding_y=styles.Spacer.VERY_BIG.value,
                background="linear-gradient(135deg, #0f1a2a 0%, #194264 50%, #2a5a8a 100%)",
                position="relative",
                overflow="hidden",
                _before={
                    "content": "''",
                    "position": "absolute",
                    "top": "0",
                    "left": "0",
                    "right": "0",
                    "bottom": "0",
                    "background": "radial-gradient(circle at 20% 30%, rgba(0, 242, 254, 0.1) 0%, transparent 50%), radial-gradient(circle at 80% 70%, rgba(67, 233, 123, 0.1) 0%, transparent 50%)",
                    "pointer_events": "none",
                }
            ),
            
            # Navegación entre categorías
            navigation_tabs(),
            
            # Galería de Proyectos - USANDO rx.match EN LUGAR DE CONDICIONES
            rx.box(
                rx.vstack(
                    rx.heading(
                        "NUESTROS PROYECTOS DESTACADOS",
                        font_size="28px",
                        color=Color_tx.Primary.value,
                        text_align="center",
                        font_weight="black",
                        margin_bottom=styles.Spacer.SMALL.value,
                        animation="fadeInUp 0.8s ease-out",
                        class_name="section-heading"
                    ),
                    rx.text(
                        "Descubre nuestra trayectoria de innovación y excelencia en arquitectura",
                        font_size="16px",
                        color=Text_tx.Black.value,
                        text_align="center",
                        max_width="700px",
                        margin_bottom=styles.Spacer.LARGE.value,
                        animation="fadeInUp 0.8s ease-out 0.2s both",
                        class_name="section-subtitle"
                    ),
                    
                    # Grid de proyectos creativo - USANDO rx.match PARA FILTRAR
                    rx.box(
                        rx.match(
                            GalleryState.filter_category,
                            ("Todos", render_projects_grid(projects_all)),
                            ("Residencial", render_projects_grid(projects_residencial)),
                            ("Comercial", render_projects_grid(projects_comercial)),
                            ("Industrial", render_projects_grid(projects_industrial)),
                            render_projects_grid(projects_all)  # Default
                        ),
                        width="100%",
                        display="flex",
                        justify_content="center",
                        padding_y=styles.Spacer.LARGE.value,
                        class_name="grid-container"
                    ),
                    
                    align_items="center",
                    spacing="6",
                    width="100%",
                ),
                width="100%",
                padding_y=styles.Spacer.VERY_BIG.value,
                background="linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 50%, #F0F7FF 100%)",
                display="flex",
                justify_content="center",
            ),
            
            # Llamado a la acción
            rx.center(
                rx.vstack(
                    rx.badge(
                        "¿Listo para comenzar?",
                        variant="solid",
                        color_scheme="blue",
                        size="2",
                        padding_x="2rem",
                        padding_y="1rem"
                    ),
                    rx.heading(
                        "Transformemos tu visión en realidad", 
                        size="7", 
                        text_align="center",
                        max_width="600px",
                        color="white"
                    ),
                    rx.text(
                        "Nuestro equipo está listo para crear el espacio perfecto para tus necesidades",
                        size="4",
                        color="rgba(255,255,255,0.8)",
                        text_align="center",
                        max_width="500px"
                    ),
                    rx.hstack(
                        rx.button(
                            "Solicitar Cotización",
                            size="3",
                            variant="solid",
                            color_scheme="blue",
                            padding_x="3rem",
                            _hover={"transform": "translateY(-2px)", "box_shadow": "0 12px 25px -5px rgba(59, 130, 246, 0.4)"},
                            transition="all 0.3s ease"
                        ),
                        rx.button(
                            "Ver Más Proyectos",
                            size="3",
                            variant="outline",
                            color_scheme="gray",
                            padding_x="3rem",
                            _hover={"transform": "translateY(-2px)"},
                            transition="all 0.3s ease"
                        ),
                        spacing="4",
                        margin_top="2rem",
                        flex_wrap="wrap",
                        justify="center"
                    ),
                    spacing="4",
                    align="center"
                ),
                width="100%",
                padding_y="6rem",
                background="linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
                color="white"
            ),
            
            spacing="0",
            width="100%",
        ),
        # Lightbox para imágenes
        lightbox_component(),
        # Estilos CSS ultra creativos (los mismos del taller)
        rx.html("""
            <style>
                /* Todos los estilos de animación del taller */
                @keyframes fadeInUp {
                    from {
                        opacity: 0;
                        transform: translateY(40px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                
                @keyframes titleEntrance {
                    0% {
                        opacity: 0;
                        transform: translateY(-50px) scale(0.8);
                        text-shadow: 0 0 0 rgba(0,242,254,0);
                    }
                    100% {
                        opacity: 1;
                        transform: translateY(0) scale(1);
                        text-shadow: 0 4px 20px rgba(0,0,0,0.5);
                    }
                }
                
                @keyframes subtitleEntrance {
                    0% {
                        opacity: 0;
                        transform: translateY(30px);
                        filter: blur(10px);
                    }
                    100% {
                        opacity: 1;
                        transform: translateY(0);
                        filter: blur(0);
                    }
                }
                
                @keyframes statsEntrance {
                    0% {
                        opacity: 0;
                        transform: scale(0.5) rotateX(90deg);
                    }
                    100% {
                        opacity: 1;
                        transform: scale(1) rotateX(0);
                    }
                }
                
                @keyframes creativeEntrance {
                    0% {
                        opacity: 0;
                        transform: rotate(var(--rotation)) scale(0.8) translateY(100px);
                        filter: blur(20px);
                    }
                    100% {
                        opacity: 1;
                        transform: rotate(var(--rotation)) scale(0.98) translateY(0);
                        filter: blur(0);
                    }
                }
                
                @keyframes lightboxEntrance {
                    0% {
                        opacity: 0;
                        transform: scale(0.8);
                    }
                    100% {
                        opacity: 1;
                        transform: scale(1);
                    }
                }
                
                @keyframes fadeIn {
                    from {
                        opacity: 0;
                    }
                    to {
                        opacity: 1;
                    }
                }
                
                .creative-project-card:hover {
                    z-index: 10 !important;
                }

                /* Estilos específicos para navegación responsive */
                .desktop-navigation {
                    display: none !important;
                }

                .mobile-navigation {
                    display: flex !important;
                }

                @media (min-width: 769px) {
                    .desktop-navigation {
                        display: flex !important;
                    }
                    
                    .mobile-navigation {
                        display: none !important;
                    }
                }

                /* Responsive improvements */
                @media (max-width: 768px) {
                    .creative-project-card {
                        margin: 0 auto;
                        max-width: 400px;
                        transform: scale(0.98) !important;
                    }
                    
                    .creative-project-card:hover {
                        transform: scale(1.02) !important;
                    }
                    
                    .info-overlay {
                        display: none !important;
                    }
                    
                    .shine-effect {
                        display: none !important;
                    }
                    
                    .mobile-info {
                        display: block !important;
                    }
                    
                    .desktop-stats {
                        display: none !important;
                    }
                    
                    .mobile-stats {
                        display: flex !important;
                    }
                    
                    .hero-heading {
                        font-size: 24px !important;
                    }
                    
                    .hero-subtitle {
                        font-size: 14px !important;
                    }
                    
                    .section-heading {
                        font-size: 20px !important;
                    }
                    
                    .section-subtitle {
                        font-size: 13px !important;
                    }
                    
                    .projects-grid {
                        grid-template-columns: 1fr !important;
                        gap: 16px !important;
                    }
                }
                
                @media (min-width: 769px) and (max-width: 1024px) {
                    .projects-grid {
                        grid-template-columns: repeat(2, 1fr) !important;
                        gap: 20px !important;
                    }
                    
                    .mobile-info {
                        display: none !important;
                    }
                    
                    .desktop-stats {
                        display: flex !important;
                    }
                    
                    .mobile-stats {
                        display: none !important;
                    }
                }
                
                @media (min-width: 1025px) {
                    .mobile-info {
                        display: none !important;
                    }
                    
                    .desktop-stats {
                        display: flex !important;
                    }
                    
                    .mobile-stats {
                        display: none !important;
                    }
                }
            </style>
        """),
        width="100%",
        padding_y=styles.Spacer.DEFAULT.value,
    )

def _get_color(category: str) -> str:
    colors = {
        "Residencial": "#3b82f6",  # Azul
        "Comercial": "#8b5cf6",    # Púrpura
        "Industrial": "#10b981",   # Verde
        "Todos": "#6b7280"         # Gris
    }
    return colors.get(category, "#3b82f6")

def _get_dark_color(category: str) -> str:
    colors = {
        "Residencial": "#1d4ed8",  # Azul oscuro
        "Comercial": "#7c3aed",    # Púrpura oscuro
        "Industrial": "#047857",   # Verde oscuro
        "Todos": "#4b5563"         # Gris oscuro
    }
    return colors.get(category, "#1d4ed8")

def _get_color_scheme(category: str) -> str:
    color_schemes = {
        "Residencial": "blue",
        "Comercial": "purple", 
        "Industrial": "green",
        "Todos": "gray"
    }
    return color_schemes.get(category, "blue")