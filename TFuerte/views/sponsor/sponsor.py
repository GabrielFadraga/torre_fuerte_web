import reflex as rx
import TFuerte.styles.styles as styles
from TFuerte.components.title import title
from TFuerte.components.link_sponsor import link_sponsor

def sponsor() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Título de la sección
            rx.center(
                rx.vstack(
                    rx.box(
                        "ALIANZAS ESTRATÉGICAS",
                        background="linear-gradient(135deg, #194264 0%, #2a5a8a 100%)",
                        color="white",
                        padding_x="20px",
                        padding_y="8px",
                        border_radius="20px",
                        font_size="12px",
                        font_weight="bold",
                        letter_spacing="2px",
                        margin_bottom="16px",
                    ),
                    rx.heading(
                        "Nuestros Principales Clientes",
                        size="7",
                        color="white",
                        text_align="center",
                        font_weight="bold",
                        margin_bottom="8px",
                    ),
                    rx.text(
                        "Colaboramos con empresas líderes en diversos sectores industriales",
                        size="5",
                        color="rgba(255,255,255,0.8)",
                        text_align="center",
                        max_width="600px",
                    ),
                    align_items="center",
                    spacing="4",
                ),
                width="100%",
                padding_y=styles.Spacer.LARGE.value,
            ),
            
            # Grid de logos de clientes
            rx.center(
                rx.hstack(
                    # Cliente 1 - Navegación
                    rx.box(
                        rx.link(
                            rx.vstack(
                                rx.image(
                                    src="navegacion.png",
                                    width="120px",
                                    height="60px",
                                    object_fit="contain",
                                    filter="brightness(0) invert(1)",
                                    transition="all 0.3s ease",
                                    _hover={
                                        "transform": "scale(1.1)",
                                        "filter": "brightness(0) invert(1) drop-shadow(0 4px 12px rgba(255,255,255,0.3))",
                                    }
                                ),
                                rx.text(
                                    "Empresa de Navegación Caribe",
                                    font_size="12px",
                                    color="rgba(255,255,255,0.7)",
                                    text_align="center",
                                    margin_top="8px",
                                    font_weight="medium",
                                ),
                                align_items="center",
                                spacing="2",
                            ),
                            href="https://www.gemar.transnet.cu/es/empresas/empresa-de-navegacion-caribe",
                            is_external=True,
                        ),
                        padding="20px",
                        background="linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)",
                        border_radius="12px",
                        border="1px solid rgba(255,255,255,0.1)",
                        backdrop_filter="blur(10px)",
                        transition="all 0.3s ease",
                        _hover={
                            "transform": "translateY(-5px)",
                            "background": "linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%)",
                            "border": "1px solid rgba(255,255,255,0.2)",
                            "box_shadow": "0 10px 30px rgba(0,0,0,0.2)",
                        }
                    ),
                    
                    # Separador decorativo
                    rx.box(
                        width="1px",
                        height="40px",
                        background="linear-gradient(180deg, transparent, rgba(255,255,255,0.3), transparent)",
                        margin_x="20px",
                    ),
                    
                    # Cliente 2 - Salud
                    rx.box(
                        rx.link(
                            rx.vstack(
                                rx.image(
                                    src="salud.png",
                                    width="120px",
                                    height="60px",
                                    object_fit="contain",
                                    filter="brightness(0) invert(1)",
                                    transition="all 0.3s ease",
                                    _hover={
                                        "transform": "scale(1.1)",
                                        "filter": "brightness(0) invert(1) drop-shadow(0 4px 12px rgba(255,255,255,0.3))",
                                    }
                                ),
                                rx.text(
                                    "Ministerio de Salud Pública",
                                    font_size="12px",
                                    color="rgba(255,255,255,0.7)",
                                    text_align="center",
                                    margin_top="8px",
                                    font_weight="medium",
                                ),
                                align_items="center",
                                spacing="2",
                            ),
                            href="https://salud.msp.gob.cu/",
                            is_external=True,
                        ),
                        padding="20px",
                        background="linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)",
                        border_radius="12px",
                        border="1px solid rgba(255,255,255,0.1)",
                        backdrop_filter="blur(10px)",
                        transition="all 0.3s ease",
                        _hover={
                            "transform": "translateY(-5px)",
                            "background": "linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%)",
                            "border": "1px solid rgba(255,255,255,0.2)",
                            "box_shadow": "0 10px 30px rgba(0,0,0,0.2)",
                        }
                    ),
                    
                    # Separador decorativo
                    rx.box(
                        width="1px",
                        height="40px",
                        background="linear-gradient(180deg, transparent, rgba(255,255,255,0.3), transparent)",
                        margin_x="20px",
                    ),
                    
                    # Cliente 3 - Engimov
                    rx.box(
                        rx.link(
                            rx.vstack(
                                rx.image(
                                    src="eng.png",
                                    width="120px",
                                    height="60px",
                                    object_fit="contain",
                                    filter="brightness(0) invert(1)",
                                    transition="all 0.3s ease",
                                    _hover={
                                        "transform": "scale(1.1)",
                                        "filter": "brightness(0) invert(1) drop-shadow(0 4px 12px rgba(255,255,255,0.3))",
                                    }
                                ),
                                rx.text(
                                    "Engimov Caribe",
                                    font_size="12px",
                                    color="rgba(255,255,255,0.7)",
                                    text_align="center",
                                    margin_top="8px",
                                    font_weight="medium",
                                ),
                                align_items="center",
                                spacing="2",
                            ),
                            href="https://www.engimov.pt/es/grupo/engimov-caribe",
                            is_external=True,
                        ),
                        padding="20px",
                        background="linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)",
                        border_radius="12px",
                        border="1px solid rgba(255,255,255,0.1)",
                        backdrop_filter="blur(10px)",
                        transition="all 0.3s ease",
                        _hover={
                            "transform": "translateY(-5px)",
                            "background": "linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%)",
                            "border": "1px solid rgba(255,255,255,0.2)",
                            "box_shadow": "0 10px 30px rgba(0,0,0,0.2)",
                        }
                    ),
                    
                    # Separador decorativo
                    rx.box(
                        width="1px",
                        height="40px",
                        background="linear-gradient(180deg, transparent, rgba(255,255,255,0.3), transparent)",
                        margin_x="20px",
                    ),
                    
                    # Cliente 4 - Prácticos de Puerto (NUEVO)
                    rx.box(
                        rx.link(
                            rx.vstack(
                                rx.image(
                                    src="puerto.png",
                                    width="120px",
                                    height="60px",
                                    object_fit="contain",
                                    filter="brightness(0) invert(1)",
                                    transition="all 0.3s ease",
                                    _hover={
                                        "transform": "scale(1.1)",
                                        "filter": "brightness(0) invert(1) drop-shadow(0 4px 12px rgba(255,255,255,0.3))",
                                    }
                                ),
                                rx.text(
                                    "Prácticos de Puerto",
                                    font_size="12px",
                                    color="rgba(255,255,255,0.7)",
                                    text_align="center",
                                    margin_top="8px",
                                    font_weight="medium",
                                ),
                                align_items="center",
                                spacing="2",
                            ),
                            href="https://www.practicosdepuerto.es",
                            is_external=True,
                        ),
                        padding="20px",
                        background="linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)",
                        border_radius="12px",
                        border="1px solid rgba(255,255,255,0.1)",
                        backdrop_filter="blur(10px)",
                        transition="all 0.3s ease",
                        _hover={
                            "transform": "translateY(-5px)",
                            "background": "linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%)",
                            "border": "1px solid rgba(255,255,255,0.2)",
                            "box_shadow": "0 10px 30px rgba(0,0,0,0.2)",
                        }
                    ),
                    
                    align_items="center",
                    justify="center",
                    spacing="0",
                    width="100%",
                    max_width="1200px",
                ),
                width="100%",
                padding_y=styles.Spacer.LARGE.value,
                padding_x=styles.Spacer.LARGE.value,
            ),
            
            # Línea decorativa inferior
            rx.center(
                rx.box(
                    width="100px",
                    height="3px",
                    background="linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent)",
                    margin_bottom=styles.Spacer.LARGE.value,
                ),
                width="100%",
            ),
            
            spacing="0",
            width="100%",
        ),
        background="linear-gradient(135deg, #194264 0%, #2a5a8a 100%)",
        width="100%",
        position="relative",
        overflow="hidden",
        _before={
            "content": "''",
            "position": "absolute",
            "top": "0",
            "left": "0",
            "right": "0",
            "bottom": "0",
            "background": "radial-gradient(circle at 30% 70%, rgba(255,255,255,0.1) 0%, transparent 50%)",
        }
    )

# Versión móvil optimizada
def sponsor_mobile() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Título de la sección
            rx.center(
                rx.vstack(
                    rx.box(
                        "ALIANZAS ESTRATÉGICAS",
                        background="linear-gradient(135deg, #194264 0%, #2a5a8a 100%)",
                        color="white",
                        padding_x="16px",
                        padding_y="6px",
                        border_radius="16px",
                        font_size="10px",
                        font_weight="bold",
                        letter_spacing="1.5px",
                        margin_bottom="12px",
                    ),
                    rx.heading(
                        "Nuestros Principales Clientes",
                        size="6",
                        color="white",
                        text_align="center",
                        font_weight="bold",
                        margin_bottom="8px",
                    ),
                    rx.text(
                        "Colaboramos con empresas líderes en diversos sectores industriales",
                        size="4",
                        color="rgba(255,255,255,0.8)",
                        text_align="center",
                    ),
                    align_items="center",
                    spacing="3",
                ),
                width="100%",
                padding_y=styles.Spacer.LARGE.value,
                padding_x=styles.Spacer.MEDIUM.value,
            ),
            
            # Grid de logos en móvil
            rx.vstack(
                # Cliente 1
                rx.box(
                    rx.link(
                        rx.vstack(
                            rx.image(
                                src="navegacion.png",
                                width="100px",
                                height="50px",
                                object_fit="contain",
                                filter="brightness(0) invert(1)",
                            ),
                            rx.text(
                                "Empresa de Navegación Caribe",
                                font_size="11px",
                                color="rgba(255,255,255,0.7)",
                                text_align="center",
                                margin_top="6px",
                                font_weight="medium",
                            ),
                            align_items="center",
                            spacing="2",
                        ),
                        href="https://www.gemar.transnet.cu/es/empresas/empresa-de-navegacion-caribe",
                        is_external=True,
                    ),
                    padding="16px",
                    background="linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)",
                    border_radius="10px",
                    border="1px solid rgba(255,255,255,0.1)",
                    width="100%",
                    max_width="250px",
                ),
                
                # Cliente 2
                rx.box(
                    rx.link(
                        rx.vstack(
                            rx.image(
                                src="salud.png",
                                width="100px",
                                height="50px",
                                object_fit="contain",
                                filter="brightness(0) invert(1)",
                            ),
                            rx.text(
                                "Ministerio de Salud Pública",
                                font_size="11px",
                                color="rgba(255,255,255,0.7)",
                                text_align="center",
                                margin_top="6px",
                                font_weight="medium",
                            ),
                            align_items="center",
                            spacing="2",
                        ),
                        href="https://salud.msp.gob.cu/",
                        is_external=True,
                    ),
                    padding="16px",
                    background="linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)",
                    border_radius="10px",
                    border="1px solid rgba(255,255,255,0.1)",
                    width="100%",
                    max_width="250px",
                ),
                
                # Cliente 3
                rx.box(
                    rx.link(
                        rx.vstack(
                            rx.image(
                                src="eng.png",
                                width="100px",
                                height="50px",
                                object_fit="contain",
                                filter="brightness(0) invert(1)",
                            ),
                            rx.text(
                                "Engimov Caribe",
                                font_size="11px",
                                color="rgba(255,255,255,0.7)",
                                text_align="center",
                                margin_top="6px",
                                font_weight="medium",
                            ),
                            align_items="center",
                            spacing="2",
                        ),
                        href="https://www.engimov.pt/es/grupo/engimov-caribe",
                        is_external=True,
                    ),
                    padding="16px",
                    background="linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)",
                    border_radius="10px",
                    border="1px solid rgba(255,255,255,0.1)",
                    width="100%",
                    max_width="250px",
                ),
                
                # Cliente 4 - Prácticos de Puerto (NUEVO)
                rx.box(
                    rx.link(
                        rx.vstack(
                            rx.image(
                                src="puerto.png",
                                width="100px",
                                height="50px",
                                object_fit="contain",
                                filter="brightness(0) invert(1)",
                            ),
                            rx.text(
                                "Prácticos de Puerto",
                                font_size="11px",
                                color="rgba(255,255,255,0.7)",
                                text_align="center",
                                margin_top="6px",
                                font_weight="medium",
                            ),
                            align_items="center",
                            spacing="2",
                        ),
                        href="https://www.practicosdepuerto.es",
                        is_external=True,
                    ),
                    padding="16px",
                    background="linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)",
                    border_radius="10px",
                    border="1px solid rgba(255,255,255,0.1)",
                    width="100%",
                    max_width="250px",
                ),
                
                align_items="center",
                spacing="4",
                width="100%",
                padding_y=styles.Spacer.LARGE.value,
            ),
            
            spacing="0",
            width="100%",
        ),
        background="linear-gradient(135deg, #194264 0%, #2a5a8a 100%)",
        width="100%",
    )

# Componente final con responsive
def sponsor_final() -> rx.Component:
    return rx.box(
        rx.desktop_only(sponsor()),
        rx.mobile_and_tablet(sponsor_mobile()),
        width="100%",
    )