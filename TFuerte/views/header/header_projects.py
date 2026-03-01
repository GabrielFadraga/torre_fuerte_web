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
            # Contenedor de imagen del proyecto
            rx.box(
                rx.image(
                    src=project["image"],
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
                on_click=GalleryState.open_lightbox(project["image"]),
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
                # Contenido del lightbox
                rx.center(
                    rx.vstack(
                        rx.box(
                            rx.image(
                                src=GalleryState.selected_image,
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
            # RESPONSIVE MEJORADO: Padding adaptable para todos los dispositivos
            padding_x=["0.8rem", "1rem", "1.2rem", "1.5rem"],
            padding_y=["0.6rem", "0.7rem", "0.75rem"],
            border_radius="12px",
            # RESPONSIVE MEJORADO: Tamaño de fuente escalable
            font_size=["11px", "12px", "13px", "14px"],
            font_weight="bold",
            transition="all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94)",
            _hover={
                "transform": "translateY(-2px)",
                "box_shadow": "0 8px 20px rgba(0,0,0,0.2)",
            },
            on_click=GalleryState.set_filter_category(category),
            white_space="nowrap",
            # RESPONSIVE MEJORADO: Ancho flexible para móvil/tablet
            width=["100%", "100%", "auto"],
            min_width=["auto", "auto", "120px", "140px"],
            flex=["1", "1", "0 1 auto"],
        )
    
    return rx.center(
        rx.box(
            # Desktop - Botones en fila
            rx.hstack(
                create_filter_button("Todos"),
                create_filter_button("Automatización"),
                create_filter_button("Eléctrica"),
                create_filter_button("Mecánica"),
                spacing="5",
                justify="center",
                align="center",
                flex_wrap="wrap",
                # Solo visible en desktop
                display=["none", "none", "flex"],
                class_name="desktop-navigation",
                width="100%",
                max_width="1200px",
                margin_x="auto",
            ),
            # Mobile/Tablet - Botones en grid 2x2
            rx.box(
                rx.grid(
                    create_filter_button("Todos"),
                    create_filter_button("Automatización"),
                    create_filter_button("Eléctrica"),
                    create_filter_button("Mecánica"),
                    columns="2",
                    spacing="3",
                    width="100%",
                    max_width="400px",
                    justify="center",
                ),
                # Solo visible en móvil y tablet
                display=["flex", "flex", "none"],
                justify_content="center",
                width="100%",
                class_name="mobile-navigation"
            ),
            width="100%",
            display="flex",
            justify_content="center",
        ),
        width="100%",
        padding_y=styles.Spacer.MEDIUM.value,
        background="linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
        # RESPONSIVE MEJORADO: Padding lateral adaptable
        padding_x=["0.8rem", "1rem", "1.5rem", "2rem"],
    )

def gallery() -> rx.Component:
    """Sección principal de galería de proyectos - COMPLETAMENTE RESPONSIVE"""
    
    # Lista de proyectos para AUTOMATIZACIÓN
    projects_automatizacion = [
        {
            "title": "Línea de produccion minisdosis de mantequilla.",
            "category": "Automatización", 
            "description": "Restablecimiento del funcionamiento de máquina envasadora de mantequilla",
            "year": "2025",
            "features": ["Control PLC", "Red industrial", "Red industrial"],
            "image": "auto1.jpg",
            "delay": 0.1,
            "rotation": -2
        },
        {
            "title": "Reparación de equipos de lavandería",
            "category": "Automatización",
            "description": "Defectación, reparación y puesta en marcha de equipos de lavadoras automáticas", 
            "year": "2025",
            "features": ["Lavadoras automáticas", "Programación", "Control de variables"],
            "image": "auto2.jpg",
            "delay": 0.2,
            "rotation": 1
        },
        {
            "title": "Reparación e instalación de VFD",
            "category": "Automatización",
            "description": "Instalación de VFD para control de velocidad de motor",
            "year": "2025",
            "features": ["Control de velocidad de motores", "Alertas automáticas", "Alertas automáticas"],
            "image": "auto3.jpg",
            "delay": 0.3,
            "rotation": -1
        },
        {
            "title": "Defectación de sistema automático de compresor", 
            "category": "Automatización",
            "description": "Diagnóstico del sistema automático de compresor",
            "year": "2025",
            "features": ["Compresores", "Sistema automático", "Detección de errores"],
            "image": "auto4.jpg",
            "delay": 0.4,
            "rotation": 2
        },
        {
            "title": "Reparación de sistema de control automático",
            "category": "Automatización",
            "description": "Defectación y reparación de la automática de una embarcaión",
            "year": "2025",
            "features": ["Programación PLC", "TX/RX de comandos", "Comunicación industrial"],
            "image": "auto5.jpg",
            "delay": 0.5,
            "rotation": -3
        },
        {
            "title": "Optimización del control automático industrial",
            "category": "Automatización", 
            "description": "Reparación y optimización de la automática de máquina envasadora de mantequilla",
            "year": "2025",
            "features": ["Programación PLC", "Optimización automática", "Reportes inteligentes"],
            "image": "auto6.jpg",
            "delay": 0.6,
            "rotation": 1
        },
        {
            "title": "Reparación y mantenimiento de VFD",
            "category": "Automatización",
            "description": "Defectación y mantenimiento de VFD para control de velocidad en motores de embarcaciones",
            "year": "2025",
            "features": ["Manual de usuario VFD", "Puesta en marcha", "Mínimo mantenimiento"],
            "image": "auto7.jpg",
            "delay": 0.7,
            "rotation": -2
        },
        {
            "title": "Implementación de control automático de joystick",
            "category": "Automatización",
            "description": "programación de PLC para control de Joystick de embarcación mediante tren de pulsos",
            "year": "2025",
            "features": ["Automática en embarcaciones", "Programación C/C++", "Estadísticas en tiempo real"],
            "image": "auto8.jpg",
            "delay": 0.8,
            "rotation": 3
        },
    ]
    
    # Lista de proyectos para ELÉCTRICA
    projects_electrica = [
        {
            "title": "Defectación de pizarras de control industrial",
            "category": "Eléctrica", 
            "description": "Diagnóstico de pizzarra de control de compresor industrial",
            "year": "2025",
            "features": ["Diagnóstco detallado", "Protecciones eléctricas", "Pizarras de control"],
            "image": "elec1.jpg",
            "delay": 0.1,
            "rotation": -2
        },
        {
            "title": "Diagnóstico y reparación de pizarra de control",
            "category": "Eléctrica",
            "description": "Defectación, mantenimiento, puesta en marcha de pizarra de control en embarcaciones", 
            "year": "2025",
            "features": ["Trabajo en embarcaciones", "Diagnóstico eléctrico", "Medición de variables eléctricas"],
            "image": "elec2.jpg",
            "delay": 0.2,
            "rotation": 1
        },
        {
            "title": "Panel de control de bombas de un sistema de bombeo",
            "category": "Eléctrica",
            "description": "Panel de control de bombas de un sistema de bombeo de hospital",
            "year": "2023",
            "features": ["Instalaciones eléctricas", "Montaje y puesta en marcha", "Certificación"],
            "image": "elec3.jpg",
            "delay": 0.3,
            "rotation": -1
        },
        {
            "title": "Instalación eléctrica de panel de control", 
            "category": "Eléctrica",
            "description": "Instalación de panel de control eléctrico de una bomba",
            "year": "2024",
            "features": ["Medición de variables eléctricas", "Seguridad operacional", "Mediciones"],
            "image": "elec4.jpg",
            "delay": 0.4,
            "rotation": 2
        },
        {
            "title": "Montaje de pizarra de control",
            "category": "Eléctrica",
            "description": "Reparación e instalación de pizarra de control de grúa",
            "year": "2025",
            "features": ["Instalación eléctrica", "Defectación", "Control remoto"],
            "image": "elec5.jpg",
            "delay": 0.5,
            "rotation": -3
        },
        {
            "title": "Mantenimiento eléctrico de equipos de lavandería",
            "category": "Eléctrica", 
            "description": "Reparación y mantenimiento de sistema eléctrico de secadoras industriales",
            "year": "2025",
            "features": ["Desarme eléctrico", "Medición de variables eléctricas", "Seguridad mejorada"],
            "image": "elec6.jpg",
            "delay": 0.6,
            "rotation": 1
        },
        # Nuevos proyectos eléctricos
        {
            "title": "Mantenimiento de grupo electrógeno - Panadería Río",
            "category": "Eléctrica",
            "description": "Reparación y mantenimiento de grupo electrógeno en panadería de La Habana",
            "year": "2026",
            "features": ["Grupo electrógeno", "Mantenimiento eléctrico", "Puesta en marcha"],
            "image": "Rio.png",
            "delay": 0.7,
            "rotation": -3
        },
        {
            "title": "Mantenimiento de grupo electrógeno - Panadería Bellas Artes",
            "category": "Eléctrica",
            "description": "Reparación y mantenimiento de grupo electrógeno en panadería de La Habana",
            "year": "2026",
            "features": ["Grupo electrógeno", "Sistema eléctrico", "Diagnóstico"],
            "image": "BellasArtes.png",
            "delay": 0.8,
            "rotation": 3
        },
    ]
    
    # Lista de proyectos para MECÁNICA
    projects_mecanica = [
        {
            "title": "Montaje y alineamiento de motor de embarcación",
            "category": "Mecánica", 
            "description": "Defectación, montaje y alineamiento del motor de embarcación",
            "year": "2025",
            "features": ["Diagnóstico técnico", "Montaje de motor", "Puesta en marcha"],
            "image": "meca1.jpg",
            "delay": 0.1,
            "rotation": -2
        },
        {
            "title": "Reparación de motor-generador",
            "category": "Mecánica",
            "description": "Defectación y reparación de motor-generador de embarcación", 
            "year": "2025",
            "features": ["Diagnóstico", "Puesta en marcha", "Monitoreo continuo"],
            "image": "meca2.jpg",
            "delay": 0.2,
            "rotation": 1
        },
        {
            "title": "Reparación y montaje de bombas de succión",
            "category": "Mecánica",
            "description": "Instalación de bombas de succión en hospitales",
            "year": "2025",
            "features": ["Reparaciones mecánicas", "Montaje especializqado", "Materiales"],
            "image": "meca3.jpg",
            "delay": 0.3,
            "rotation": -1
        },
        {
            "title": "Insulación de líneas de gases", 
            "category": "Mecánica",
            "description": "Aislamiento térmico de líneas de gases de un remolcador",
            "year": "2025",
            "features": ["Aislamiento térmico", "Ahorro de combustible", "Control"],
            "image": "meca4.jpg",
            "delay": 0.4,
            "rotation": 2
        },
        {
            "title": "Defectación y reparación mecánica de equipos de lavandería",
            "category": "Mecánica",
            "description": "Reparación y puesta en marcha de secadoras",
            "year": "2025",
            "features": ["Diagnóstico preciso", "Reparación in-situ", "Garantía de trabajo"],
            "image": "meca5.jpg",
            "delay": 0.5,
            "rotation": -3
        },
        {
            "title": "Reparación de grúa",
            "category": "Mecánica", 
            "description": "Defectación y reparación de sistema mecánico de grúa",
            "year": "2025",
            "features": ["Reparación mecánica", "Mecánica de precisión", "Implementación"],
            "image": "meca6.jpg",
            "delay": 0.6,
            "rotation": 1
        },
        {
            "title": "Traslado de bomba de producto",
            "category": "Mecánica",
            "description": "Traslado de bomba de producto en embarcaciones",
            "year": "2025",
            "features": ["Trabajo de precisión", "Puesta en marcha", "Trabajo en el mar"],
            "image": "meca7.jpg",
            "delay": 0.7,
            "rotation": -2
        },
        # Nuevos proyectos mecánicos
        {
            "title": "Rehabilitación de línea de fertilizantes",
            "category": "Mecánica",
            "description": "Trabajos de pailería, soldadura y taller en fábrica Rayonitro",
            "year": "2026",
            "features": ["Pailería", "Soldadura", "Trabajos de taller"],
            "image": "Rayonitro.png",
            "delay": 0.8,
            "rotation": -2
        },
        {
            "title": "Reparación de plancha de vapor",
            "category": "Mecánica",
            "description": "Mantenimiento y reparación de plancha de vapor en hotel de Varadero",
            "year": "2026",
            "features": ["Reparación de plancha", "Sistema de vapor", "Puesta en marcha"],
            "image": "plancha.png",
            "delay": 0.9,
            "rotation": 1
        },
        {
            "title": "Mantenimiento de secadora automática",
            "category": "Mecánica",
            "description": "Reparación y mantenimiento de secadora industrial en hotel",
            "year": "2026",
            "features": ["Secadora automática", "Mantenimiento preventivo", "Reparación mecánica"],
            "image": "secadora.png",
            "delay": 1.0,
            "rotation": -1
        },
        {
            "title": "Evaluación de duchas para evitar inundaciones",
            "category": "Mecánica",
            "description": "Levantamiento de instalaciones y evaluación para modificación de duchas en sótano",
            "year": "2026",
            "features": ["Instalaciones hidráulicas", "Evaluación técnica", "Prevención de inundaciones"],
            "image": "hospital.png",
            "delay": 1.1,
            "rotation": 2
        },
    ]
    
    # Combinar todos los proyectos
    all_projects = projects_automatizacion + projects_electrica + projects_mecanica
    
    # Filtrar proyectos según la categoría seleccionada
    projects_all = all_projects
    projects_automatizacion_filtered = [p for p in all_projects if p["category"] == "Automatización"]
    projects_electrica_filtered = [p for p in all_projects if p["category"] == "Eléctrica"]
    projects_mecanica_filtered = [p for p in all_projects if p["category"] == "Mecánica"]
    
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
                            "ESPECIALIDADES TÉCNICAS TORRE FUERTE", 
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
                            "Soluciones integrales en automática, eléctrica y mecánica para la industria",
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
                                    "300+",
                                    font_size="36px",
                                    color="#43e97b",
                                    font_weight="black",
                                    animation="countUp 1s ease-out 0.7s both",
                                    text_shadow="0 0 20px rgba(67,233,123,0.5)",
                                ),
                                rx.text(
                                    "Servicios prestados",
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
                                        "300+",
                                        font_size="24px",
                                        color="#43e97b",
                                        font_weight="black",
                                    ),
                                    rx.text(
                                        "Servicios prestados",
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
            
            # Navegación entre especialidades - MEJORADA
            navigation_tabs(),
            
            # Galería de Proyectos - USANDO rx.match PARA FILTRAR
            rx.box(
                rx.vstack(
                    rx.heading(
                        "NUESTROS SERVICIOS EN ESPECIALIDADES TÉCNICAS",
                        font_size="28px",
                        color=Color_tx.Primary.value,
                        text_align="center",
                        font_weight="black",
                        margin_bottom=styles.Spacer.SMALL.value,
                        animation="fadeInUp 0.8s ease-out",
                        class_name="section-heading"
                    ),
                    rx.text(
                        "Soluciones innovadoras en automática, sistemas eléctricos y mecánica industrial",
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
                            ("Automatización", render_projects_grid(projects_automatizacion_filtered)),
                            ("Eléctrica", render_projects_grid(projects_electrica_filtered)),
                            ("Mecánica", render_projects_grid(projects_mecanica_filtered)),
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
                    rx.heading(
                        "Transformemos sus procesos industriales", 
                        size="7", 
                        text_align="center",
                        max_width="600px",
                        color="white"
                    ),
                    rx.text(
                        "Nuestro equipo especializado está listo para optimizar sus operaciones",
                        size="4",
                        color="rgba(255,255,255,0.8)",
                        text_align="center",
                        max_width="500px"
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
        # Estilos CSS ultra creativos MEJORADOS
        rx.html("""
            <style>
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

                /* MEJORAS ESPECÍFICAS PARA NAVEGACIÓN DESKTOP */
                .desktop-navigation {
                    display: none !important;
                }

                .mobile-navigation {
                    display: flex !important;
                }

                /* Desktop: 769px en adelante */
                @media (min-width: 769px) {
                    .desktop-navigation {
                        display: flex !important;
                        flex-wrap: wrap !important;
                        justify-content: center !important;
                        align-items: center !important;
                        gap: 1rem !important;
                        width: 100% !important;
                    }
                    
                    .desktop-navigation button {
                        flex: 0 1 auto !important;
                        min-width: 140px !important;
                    }
                    
                    .mobile-navigation {
                        display: none !important;
                    }
                }

                /* Tablet: 481px a 768px */
                @media (min-width: 481px) and (max-width: 768px) {
                    .mobile-navigation {
                        max-width: 90% !important;
                    }
                    
                    .mobile-navigation .grid {
                        gap: 12px !important;
                    }
                    
                    .mobile-navigation button {
                        font-size: 13px !important;
                        padding: 10px 16px !important;
                    }
                }

                /* Mobile pequeño: hasta 480px */
                @media (max-width: 480px) {
                    .mobile-navigation {
                        max-width: 95% !important;
                    }
                    
                    .mobile-navigation .grid {
                        gap: 10px !important;
                    }
                    
                    .mobile-navigation button {
                        font-size: 11px !important;
                        padding: 8px 12px !important;
                        min-height: 44px !important; /* Para mejor touch */
                    }
                }

                /* Desktop grande: 1024px en adelante */
                @media (min-width: 1024px) {
                    .desktop-navigation {
                        gap: 1.25rem !important;
                    }
                    
                    .desktop-navigation button {
                        min-width: 150px !important;
                    }
                }

                /* Desktop muy grande: 1200px en adelante */
                @media (min-width: 1200px) {
                    .desktop-navigation {
                        gap: 1.5rem !important;
                    }
                    
                    .desktop-navigation button {
                        min-width: 160px !important;
                    }
                }

                /* MEJORAS GENERALES DE RESPONSIVIDAD */
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
                        padding: 0 1rem !important;
                    }
                    
                    .hero-subtitle {
                        font-size: 14px !important;
                        padding: 0 1rem !important;
                    }
                    
                    .section-heading {
                        font_size: 20px !important;
                        padding: 0 1rem !important;
                    }
                    
                    .section-subtitle {
                        font_size: 13px !important;
                        padding: 0 1rem !important;
                    }
                    
                    .projects-grid {
                        grid-template-columns: 1fr !important;
                        gap: 16px !important;
                        padding: 0 1rem !important;
                    }
                }
                
                @media (min-width: 769px) and (max-width: 1024px) {
                    .projects-grid {
                        grid-template-columns: repeat(2, 1fr) !important;
                        gap: 20px !important;
                        padding: 0 1.5rem !important;
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
                    
                    .projects-grid {
                        padding: 0 2rem !important;
                    }
                }

                /* Asegurar que los botones sean táctiles en móvil */
                @media (max-width: 768px) {
                    button {
                        min-height: 44px !important;
                        touch-action: manipulation !important;
                    }
                }
            </style>
        """),
        width="100%",
        padding_y=styles.Spacer.DEFAULT.value,
    )

def _get_color(category: str) -> str:
    colors = {
        "Automatización": "#3b82f6",  # Azul - representa tecnología y control
        "Eléctrica": "#f59e0b",       # Ámbar - representa energía y electricidad  
        "Mecánica": "#10b981",        # Verde - representa ingeniería y precisión
        "Todos": "#6b7280"            # Gris
    }
    return colors.get(category, "#3b82f6")

def _get_dark_color(category: str) -> str:
    colors = {
        "Automatización": "#1d4ed8",  # Azul oscuro
        "Eléctrica": "#d97706",       # Ámbar oscuro
        "Mecánica": "#047857",        # Verde oscuro
        "Todos": "#4b5563"            # Gris oscuro
    }
    return colors.get(category, "#1d4ed8")

def _get_color_scheme(category: str) -> str:
    color_schemes = {
        "Automatización": "blue",
        "Eléctrica": "yellow", 
        "Mecánica": "green",
        "Todos": "gray"
    }
    return color_schemes.get(category, "blue")