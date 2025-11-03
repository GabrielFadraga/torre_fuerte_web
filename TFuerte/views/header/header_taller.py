import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles
from TFuerte.styles.colors import Text_tx, Color_tx

class TallerState(rx.State):
    """Estado para manejar el lightbox de imágenes"""
    selected_image: str = ""
    show_lightbox: bool = False
    active_section: str = "equipos"
    
    def open_lightbox(self, image: str):
        self.selected_image = image
        self.show_lightbox = True
    
    def close_lightbox(self):
        self.show_lightbox = False
        self.selected_image = ""
    
    def set_active_section(self, section: str):
        self.active_section = section

def creative_photo_card(image: str, name: str, description: str, delay: float, rotation: float, is_person: bool = False) -> rx.Component:
    """Tarjeta de foto creativa con efectos 3D y parallax - COMPLETAMENTE RESPONSIVE"""
    return rx.box(
        rx.vstack(
            # Contenedor de imagen
            rx.box(
                rx.image(
                    src=image,
                    width="100%",
                    height="250px" if not is_person else "280px",
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
                        rx.text(
                            name,
                            font_size="18px",
                            font_weight="black",
                            color="white",
                            text_align="center",
                            text_shadow="0 2px 8px rgba(0,0,0,0.8)",
                        ),
                        rx.text(
                            description,
                            font_size="12px",
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
                    background=f"linear-gradient(45deg, transparent, {Color_tx.Primary.value}30, transparent)",
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
                on_click=TallerState.open_lightbox(image),
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
                    rx.text(
                        name,
                        font_size="16px",
                        font_weight="bold",
                        color=Text_tx.Black.value,
                        text_align="center",
                        margin_top="15px",
                    ),
                    rx.text(
                        description,
                        font_size="14px",
                        color=Text_tx.Black.value,
                        text_align="center",
                        line_height="1.4",
                    ),
                    align_items="center",
                    spacing="2",
                    width="100%",
                    padding_x="10px",
                    padding_bottom="15px",
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
        box_shadow=f"0 20px 40px {Color_tx.Primary.value}25, 0 0 0 1px rgba(255,255,255,0.1), inset 0 1px 0 rgba(255,255,255,0.1)",
        border_radius="18px",
        background="white",
        class_name="creative-photo-card",
        width="100%",
    )

def lightbox_component() -> rx.Component:
    """Componente de lightbox para mostrar imágenes ampliadas - RESPONSIVE"""
    return rx.cond(
        TallerState.show_lightbox,
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
                    on_click=TallerState.close_lightbox,
                    backdrop_filter="blur(10px)",
                ),
                # Contenido del lightbox
                rx.center(
                    rx.vstack(
                        rx.box(
                            rx.image(
                                src=TallerState.selected_image,
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
                            on_click=TallerState.close_lightbox,
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
                    on_click=TallerState.close_lightbox,
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
    """Pestañas de navegación creativas - COMPLETAMENTE RESPONSIVE"""
    return rx.center(
        rx.box(
            # Desktop - Botones compactos en fila
            rx.hstack(
                rx.button(
                    "🏭 NUESTROS EQUIPOS",
                    background=rx.cond(
                        TallerState.active_section == "equipos",
                        f"linear-gradient(135deg, {Color_tx.Primary.value} 0%, #2a5a8a 100%)",
                        "rgba(255,255,255,0.1)"
                    ),
                    color=rx.cond(TallerState.active_section == "equipos", "white", "rgba(255,255,255,0.8)"),
                    border=rx.cond(
                        TallerState.active_section == "equipos",
                        f"2px solid {Color_tx.Primary.value}",
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
                    on_click=lambda: TallerState.set_active_section("equipos"),
                    white_space="nowrap",
                ),
                rx.button(
                    "👥 EQUIPO EN ACCIÓN",
                    background=rx.cond(
                        TallerState.active_section == "equipo",
                        f"linear-gradient(135deg, {Color_tx.Primary.value} 0%, #2a5a8a 100%)",
                        "rgba(255,255,255,0.1)"
                    ),
                    color=rx.cond(TallerState.active_section == "equipo", "white", "rgba(255,255,255,0.8)"),
                    border=rx.cond(
                        TallerState.active_section == "equipo",
                        f"2px solid {Color_tx.Primary.value}",
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
                    on_click=lambda: TallerState.set_active_section("equipo"),
                    white_space="nowrap",
                ),
                spacing="5",
                justify="center",
                # Solo visible en desktop (lg en adelante)
                display=["none", "none", "flex"],
                class_name="desktop-navigation"
            ),
            # Mobile/Tablet - Botones en columna
            rx.vstack(
                rx.button(
                    "🏭 NUESTROS EQUIPOS",
                    background=rx.cond(
                        TallerState.active_section == "equipos",
                        f"linear-gradient(135deg, {Color_tx.Primary.value} 0%, #2a5a8a 100%)",
                        "rgba(255,255,255,0.1)"
                    ),
                    color=rx.cond(TallerState.active_section == "equipos", "white", "rgba(255,255,255,0.8)"),
                    border=rx.cond(
                        TallerState.active_section == "equipos",
                        f"2px solid {Color_tx.Primary.value}",
                        "2px solid rgba(255,255,255,0.2)"
                    ),
                    padding_x="25px",
                    padding_y="12px",
                    border_radius="12px",
                    font_size="14px",
                    font_weight="bold",
                    width="100%",
                    max_width="280px",
                    on_click=lambda: TallerState.set_active_section("equipos"),
                ),
                rx.button(
                    "👥 EQUIPO EN ACCIÓN",
                    background=rx.cond(
                        TallerState.active_section == "equipo",
                        f"linear-gradient(135deg, {Color_tx.Primary.value} 0%, #2a5a8a 100%)",
                        "rgba(255,255,255,0.1)"
                    ),
                    color=rx.cond(TallerState.active_section == "equipo", "white", "rgba(255,255,255,0.8)"),
                    border=rx.cond(
                        TallerState.active_section == "equipo",
                        f"2px solid {Color_tx.Primary.value}",
                        "2px solid rgba(255,255,255,0.2)"
                    ),
                    padding_x="25px",
                    padding_y="12px",
                    border_radius="12px",
                    font_size="14px",
                    font_weight="bold",
                    width="100%",
                    max_width="280px",
                    on_click=lambda: TallerState.set_active_section("equipo"),
                ),
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

def taller_creative_section() -> rx.Component:
    """Sección creativa del taller integrando equipo y equipos - COMPLETAMENTE RESPONSIVE"""
    
    # Equipos del taller
    equipos_taller = [
        {
            "image": "torno.png",
            "name": "TORNO INDUSTRIAL",
            "description": "Precisión en mecanizado de piezas de revolución",
            "delay": 0.1,
            "rotation": -2
        },
        {
            "image": "fresadora.png", 
            "name": "FRESADORA CNC",
            "description": "Tecnología avanzada para piezas personalizadas",
            "delay": 0.2,
            "rotation": 1
        },
        {
            "image": "taladrovertical.png",
            "name": "TALADRO VERTICAL",
            "description": "Perforación de máxima precisión y control",
            "delay": 0.3,
            "rotation": -1
        },
        {
            "image": "rectificadora.png",
            "name": "RECTIFICADORA",
            "description": "Acabado superficial de alta precisión",
            "delay": 0.4,
            "rotation": 2
        },
        {
            "image": "amoladora.png",
            "name": "AMOLADORA",
            "description": "Versatilidad en corte y acabado",
            "delay": 0.5,
            "rotation": -3
        },
        {
            "image": "cintasierra.png",
            "name": "SIERRA PARA METALES",
            "description": "Corte preciso de barras metálicas",
            "delay": 0.6,
            "rotation": 1
        },
        {
            "image": "afiladorarectificadora.png",
            "name": "AFILADORA Y RECTIFICADORA",
            "description": "Doble función para herramientas de corte",
            "delay": 0.7,
            "rotation": -2
        }
    ]
    
    # Fotos del equipo trabajando
    equipo_trabajando = [
        {"image": "Randy1.png", "name": "Randy", "description": "Mecánico", "delay": 0.1, "rotation": -2},
        {"image": "Randy2.png", "name": "Randy", "description": "Mecánico", "delay": 0.2, "rotation": 1},
        {"image": "Randy3.png", "name": "Randy", "description": "Mecánico", "delay": 0.3, "rotation": -1},
        {"image": "Randy4.png", "name": "Randy", "description": "Mecánico", "delay": 0.4, "rotation": 2},
        {"image": "Randy5.png", "name": "Randy", "description": "Mecánico", "delay": 0.5, "rotation": -3},
        {"image": "Juan1.png", "name": "Juan", "description": "Tornero", "delay": 0.6, "rotation": -2},
        {"image": "Juan2.png", "name": "Juan", "description": "Tornero", "delay": 0.7, "rotation": 3},
        {"image": "Juan3.png", "name": "Juan", "description": "Tornero", "delay": 0.8, "rotation": -1},
        {"image": "Máximo1.png", "name": "Máximo", "description": "Fresador", "delay": 0.9, "rotation": 2},
    ]
    
    return rx.box(
        rx.vstack(
            # Hero Section Ultra Creativa - RESPONSIVE
            rx.center(
                rx.vstack(
                    rx.box(
                        rx.heading(
                            "TALLER DE EXCELENCIA INDUSTRIAL",
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
                            "Donde la tecnología se encuentra con el talento humano especializado",
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
                                    "Servicios de taller prestados",
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
                                    color="#fa709a",
                                    font_weight="black",
                                    animation="countUp 1s ease-out 0.9s both",
                                    text_shadow="0 0 20px rgba(250,112,154,0.5)",
                                ),
                                rx.text(
                                    "Satisfacción Garantizada",
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
                                        "Servicios de taller prestados",
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
                                        color="#fa709a",
                                        font_weight="black",
                                    ),
                                    rx.text(
                                        "Garantía",
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
            
            # Navegación entre secciones
            navigation_tabs(),
            
            # Sección de Equipos (condicional)
            rx.cond(
                TallerState.active_section == "equipos",
                rx.vstack(
                    # Galería de Equipos
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "TECNOLOGÍA DE PUNTA",
                                font_size="28px",
                                color=Color_tx.Primary.value,
                                text_align="center",
                                font_weight="black",
                                margin_bottom=styles.Spacer.SMALL.value,
                                animation="fadeInUp 0.8s ease-out",
                                class_name="section-heading"
                            ),
                            rx.text(
                                "Equipos especializados para mecanizado de precisión",
                                font_size="16px",
                                color=Text_tx.Black.value,
                                text_align="center",
                                max_width="700px",
                                margin_bottom=styles.Spacer.LARGE.value,
                                animation="fadeInUp 0.8s ease-out 0.2s both",
                                class_name="section-subtitle"
                            ),
                            
                            # Grid de equipos creativo - COMPLETAMENTE RESPONSIVE
                            rx.box(
                                # Grid responsivo
                                rx.grid(
                                    *[
                                        creative_photo_card(
                                            equipo["image"],
                                            equipo["name"],
                                            equipo["description"],
                                            equipo["delay"],
                                            equipo["rotation"]
                                        )
                                        for equipo in equipos_taller
                                    ],
                                    columns="3",
                                    spacing="6",
                                    width="100%",
                                    max_width="1200px",
                                    justify="center",
                                    class_name="equipos-grid"
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
                    width="100%",
                    spacing="0",
                )
            ),
            
            # Sección del Equipo (condicional)
            rx.cond(
                TallerState.active_section == "equipo",
                rx.vstack(
                    # Galería del Equipo
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "NUESTRO EQUIPO ESPECIALIZADO",
                                font_size="28px",
                                color=Color_tx.Primary.value,
                                text_align="center",
                                font_weight="black",
                                margin_bottom=styles.Spacer.SMALL.value,
                                animation="fadeInUp 0.8s ease-out",
                                class_name="section-heading"
                            ),
                            rx.text(
                                "Profesionales comprometidos con la excelencia y la innovación",
                                font_size="16px",
                                color=Text_tx.Black.value,
                                text_align="center",
                                max_width="700px",
                                margin_bottom=styles.Spacer.LARGE.value,
                                animation="fadeInUp 0.8s ease-out 0.2s both",
                                class_name="section-subtitle"
                            ),
                            
                            # Grid del equipo creativo - COMPLETAMENTE RESPONSIVE
                            rx.box(
                                # Grid responsivo
                                rx.grid(
                                    *[
                                        creative_photo_card(
                                            persona["image"],
                                            persona["name"],
                                            persona["description"],
                                            persona["delay"],
                                            persona["rotation"],
                                            True
                                        )
                                        for persona in equipo_trabajando
                                    ],
                                    columns="3",
                                    spacing="6",
                                    width="100%",
                                    max_width="1200px",
                                    justify="center",
                                    class_name="equipo-grid"
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
                    width="100%",
                    spacing="0",
                )
            ),
            
            spacing="0",
            width="100%",
        ),
        # Lightbox para imágenes
        lightbox_component(),
        # Estilos CSS ultra creativos
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
                
                @keyframes cardEntrance {
                    0% {
                        opacity: 0;
                        transform: perspective(1000px) rotateX(90deg) translateY(100px);
                        filter: blur(10px);
                    }
                    100% {
                        opacity: 1;
                        transform: perspective(1000px) rotateX(0) translateY(0);
                        filter: blur(0);
                    }
                }
                
                @keyframes float {
                    0%, 100% {
                        transform: translateY(0px);
                    }
                    50% {
                        transform: translateY(-15px);
                    }
                }
                
                @keyframes countUp {
                    0% {
                        opacity: 0;
                        transform: scale(0.3) rotate(-180deg);
                        text-shadow: 0 0 0 rgba(0,242,254,0);
                    }
                    100% {
                        opacity: 1;
                        transform: scale(1) rotate(0);
                        text-shadow: 0 0 20px rgba(0,242,254,0.5);
                    }
                }
                
                @keyframes pulse {
                    0%, 100% {
                        transform: scale(1);
                        text-shadow: 0 0 20px rgba(0,242,254,0.5);
                    }
                    50% {
                        transform: scale(1.05);
                        text-shadow: 0 0 30px rgba(0,242,254,0.8);
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
                
                .creative-photo-card:hover {
                    z-index: 10 !important;
                }
                
                .feature-card-3d:hover {
                    z-index: 5 !important;
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

                /* Asegurar que los botones desktop no se desborden */
                .desktop-navigation button {
                    flex-shrink: 0;
                    max-width: 200px;
                }

                /* Responsive improvements */
                @media (max-width: 768px) {
                    .creative-photo-card {
                        margin: 0 auto;
                        max-width: 400px;
                        transform: scale(0.98) !important;
                    }
                    
                    .creative-photo-card:hover {
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
                    
                    .desktop-buttons {
                        display: none !important;
                    }
                    
                    .mobile-buttons {
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
                    
                    .cta-heading {
                        font-size: 20px !important;
                    }
                    
                    .cta-subtitle {
                        font-size: 13px !important;
                    }
                    
                    .equipos-grid,
                    .equipo-grid {
                        grid-template-columns: 1fr !important;
                        gap: 16px !important;
                    }
                }
                
                @media (min-width: 769px) and (max-width: 1024px) {
                    .equipos-grid,
                    .equipo-grid {
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
                    
                    .desktop-buttons {
                        display: flex !important;
                    }
                    
                    .mobile-buttons {
                        display: none !important;
                    }
                    
                    /* Ajustes para tablets en navegación */
                    .desktop-navigation button {
                        padding_x: 18px !important;
                        padding_y: 9px !important;
                        font_size: 13px !important;
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
                    
                    .desktop-buttons {
                        display: flex !important;
                    }
                    
                    .mobile-buttons {
                        display: none !important;
                    }
                }
            </style>
        """),
        width="100%",
        padding_y=styles.Spacer.DEFAULT.value,
    )