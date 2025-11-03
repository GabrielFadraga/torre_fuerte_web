import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles
from TFuerte.components.sidebar import sidebar
from TFuerte.styles.colors import Text_tx, Color_tx

def headcreat() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Sidebar para móvil y tablet
            rx.mobile_and_tablet(
                sidebar(),
                width="100%",
            ),
            
            # Contenido principal del hero
            rx.center(
                rx.vstack(
                    # Badge moderno
                    rx.box(
                        "EXCELENCIA INDUSTRIAL",
                        background="linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.1) 100%)",
                        color="white",
                        padding_x="24px",
                        padding_y="10px",
                        border_radius="20px",
                        font_size="14px",
                        font_weight="bold",
                        letter_spacing="2px",
                        margin_bottom="30px",
                        border="1px solid rgba(255,255,255,0.3)",
                        backdrop_filter="blur(10px)",
                        opacity="0",
                        animation="fadeInDown 0.8s ease-out 0.2s forwards",
                    ),
                    
                    # Título principal con animación
                    rx.heading(
                        "Torre Fuerte SURL",
                        size="9",
                        color="white",
                        text_align="center",
                        font_weight="bold",
                        line_height="1.1",
                        margin_bottom="20px",
                        text_shadow="0 2px 10px rgba(0,0,0,0.3)",
                        opacity="0",
                        animation="fadeInUp 0.8s ease-out 0.4s forwards",
                    ),
                    
                    # Subtítulo destacado
                    rx.text(
                        "Líderes en Soluciones Industriales Integrales",
                        size="6",
                        color="rgba(255,255,255,0.9)",
                        text_align="center",
                        font_weight="medium",
                        margin_bottom="40px",
                        opacity="0",
                        animation="fadeInUp 0.8s ease-out 0.6s forwards",
                    ),
                    
                    # Descripción con fondo semitransparente
                    rx.box(
                        rx.text(
                            "Nos dedicamos a brindar servicios de reparación, mantenimiento y "
                            "rehabilitación de equipos industriales en las especialidades de "
                            "mecánica, electricidad y automática.",
                            size="5",
                            color="white",
                            text_align="center",
                            line_height="1.6",
                            max_width="600px",
                        ),
                        width="100%",
                        padding="30px",
                        background="linear-gradient(135deg, rgba(25, 66, 100, 0.4) 0%, rgba(42, 90, 138, 0.3) 100%)",
                        border_radius="16px",
                        border="1px solid rgba(255,255,255,0.2)",
                        backdrop_filter="blur(10px)",
                        margin_bottom="40px",
                        opacity="0",
                        animation="fadeInUp 0.8s ease-out 0.8s forwards",
                    ),
                    
                    # Botón con animación hover
                    rx.box(
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.text("Contáctanos"),
                                    rx.icon(
                                        tag="arrow_forward",
                                        size=20,
                                        margin_left="8px",
                                    ),
                                    align_items="center",
                                    spacing="2",
                                ),
                                background="linear-gradient(135deg, #FF6B35 0%, #FF8E53 100%)",
                                color="white",
                                padding_x="40px",
                                padding_y="20px",
                                font_size="18px",
                                font_weight="bold",
                                border_radius="12px",
                                box_shadow="0 8px 25px rgba(255, 107, 53, 0.3)",
                                transition="all 0.3s ease",
                                _hover={
                                    "transform": "translateY(-3px)",
                                    "box_shadow": "0 12px 35px rgba(255, 107, 53, 0.5)",
                                    "background": "linear-gradient(135deg, #FF8E53 0%, #FF6B35 100%)",
                                },
                            ),
                            href="https://wa.me/message/OKIP2WN55MKEK1",
                            is_external=True,
                        ),
                        opacity="0",
                        animation="fadeInUp 0.8s ease-out 1s forwards",
                    ),
                    
                    # Elementos decorativos
                    rx.hstack(
                        rx.box(
                            width="60px",
                            height="3px",
                            background="linear-gradient(90deg, #FF6B35, transparent)",
                            opacity="0.7",
                        ),
                        rx.box(
                            width="20px",
                            height="3px",
                            background="#FF6B35",
                        ),
                        rx.box(
                            width="60px",
                            height="3px",
                            background="linear-gradient(90deg, transparent, #FF6B35)",
                            opacity="0.7",
                        ),
                        justify="center",
                        margin_top="40px",
                        opacity="0",
                        animation="fadeIn 1s ease-out 1.2s forwards",
                    ),
                    
                    align_items="center",
                    spacing="6",
                    width="100%",
                    padding_y=styles.Spacer.DEFAULT.value,
                ),
                width="100%",
                min_height="100vh",
                padding_x=styles.Spacer.LARGE.value,
                position="relative",
            ),
            
            # Efectos de fondo animados
            _before={
                "content": "''",
                "position": "absolute",
                "top": "0",
                "left": "0",
                "right": "0",
                "bottom": "0",
                "background": "linear-gradient(135deg, #194264 0%, #2a5a8a 100%)",
                "z_index": "-2",
            },
            _after={
                "content": "''",
                "position": "absolute",
                "top": "0",
                "left": "0",
                "right": "0",
                "bottom": "0",
                "background": "radial-gradient(circle at 20% 80%, rgba(255,255,255,0.1) 0%, transparent 50%), radial-gradient(circle at 80% 20%, rgba(255,107,53,0.1) 0%, transparent 50%)",
                "z_index": "-1",
                "animation": "pulse 6s ease-in-out infinite alternate",
            },
            
            # Animaciones CSS
            style={
                "@keyframes fadeInDown": {
                    "0%": {
                        "opacity": "0",
                        "transform": "translateY(-30px)"
                    },
                    "100%": {
                        "opacity": "1",
                        "transform": "translateY(0)"
                    }
                },
                "@keyframes fadeInUp": {
                    "0%": {
                        "opacity": "0",
                        "transform": "translateY(30px)"
                    },
                    "100%": {
                        "opacity": "1",
                        "transform": "translateY(0)"
                    }
                },
                "@keyframes fadeIn": {
                    "0%": {
                        "opacity": "0"
                    },
                    "100%": {
                        "opacity": "1"
                    }
                },
                "@keyframes pulse": {
                    "0%": {
                        "opacity": "0.5"
                    },
                    "100%": {
                        "opacity": "1"
                    }
                }
            },
            
            width="100%",
            position="relative",
            overflow="hidden",
        ),
        id="inicio",
    )

# Versión móvil optimizada
def headcreat_mobile() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.mobile_and_tablet(
                sidebar(),
                width="100%",
            ),
            
            rx.center(
                rx.vstack(
                    rx.box(
                        "EXCELENCIA INDUSTRIAL",
                        background="linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.1) 100%)",
                        color="white",
                        padding_x="20px",
                        padding_y="8px",
                        border_radius="16px",
                        font_size="12px",
                        font_weight="bold",
                        letter_spacing="1.5px",
                        margin_bottom="20px",
                        border="1px solid rgba(255,255,255,0.3)",
                    ),
                    
                    rx.heading(
                        "Torre Fuerte SURL",
                        size="8",
                        color="white",
                        text_align="center",
                        font_weight="bold",
                        line_height="1.1",
                        margin_bottom="16px",
                        text_shadow="0 2px 10px rgba(0,0,0,0.3)",
                    ),
                    
                    rx.text(
                        "Líderes en Soluciones Industriales Integrales",
                        size="5",
                        color="rgba(255,255,255,0.9)",
                        text_align="center",
                        font_weight="medium",
                        margin_bottom="30px",
                    ),
                    
                    rx.box(
                        rx.text(
                            "Nos dedicamos a brindar servicios de reparación, mantenimiento y "
                            "rehabilitación de equipos industriales en las especialidades de "
                            "mecánica, electricidad y automática.",
                            size="4",
                            color="white",
                            text_align="center",
                            line_height="1.6",
                        ),
                        width="100%",
                        padding="20px",
                        background="linear-gradient(135deg, rgba(25, 66, 100, 0.4) 0%, rgba(42, 90, 138, 0.3) 100%)",
                        border_radius="12px",
                        border="1px solid rgba(255,255,255,0.2)",
                        margin_bottom="30px",
                    ),
                    
                    rx.box(
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.text("Contáctanos"),
                                    rx.icon(
                                        tag="arrow_forward",
                                        size=18,
                                        margin_left="6px",
                                    ),
                                    align_items="center",
                                    spacing="2",
                                ),
                                background="linear-gradient(135deg, #FF6B35 0%, #FF8E53 100%)",
                                color="white",
                                padding_x="30px",
                                padding_y="16px",
                                font_size="16px",
                                font_weight="bold",
                                border_radius="10px",
                                width="100%",
                            ),
                            href="https://wa.me/message/OKIP2WN55MKEK1",
                            is_external=True,
                            width="100%",
                        ),
                        width="100%",
                        max_width="300px",
                    ),
                    
                    rx.hstack(
                        rx.box(
                            width="40px",
                            height="2px",
                            background="linear-gradient(90deg, #FF6B35, transparent)",
                            opacity="0.7",
                        ),
                        rx.box(
                            width="15px",
                            height="2px",
                            background="#FF6B35",
                        ),
                        rx.box(
                            width="40px",
                            height="2px",
                            background="linear-gradient(90deg, transparent, #FF6B35)",
                            opacity="0.7",
                        ),
                        justify="center",
                        margin_top="30px",
                    ),
                    
                    align_items="center",
                    spacing="5",
                    width="100%",
                ),
                width="100%",
                min_height="100vh",
                padding_x=styles.Spacer.MEDIUM.value,
            ),
            
            width="100%",
            position="relative",
            background="linear-gradient(135deg, #194264 0%, #2a5a8a 100%)",
        ),
        id="inicio",
    )

# Componente final con responsive
def headcreat_final() -> rx.Component:
    return rx.box(
        rx.desktop_only(headcreat()),
        rx.mobile_and_tablet(headcreat_mobile()),
        width="100%",
    )