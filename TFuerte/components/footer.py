import reflex as rx
import datetime
from TFuerte.styles.colors import Text_tx, Color_tx
import TFuerte.styles.styles as styles

def footer() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Contenido principal del footer - una sola fila
            rx.hstack(
                # Logo y nombre
                rx.hstack(
                    rx.image(
                        src="torre.png", 
                        height="50px",
                        width="auto",
                        border_radius="10px",
                        filter="drop-shadow(0 2px 8px rgba(0,0,0,0.2))",
                    ),
                    rx.vstack(
                        rx.heading(
                            "Torre Fuerte SURL",
                            size="5",
                            color="white",
                            font_weight="bold",
                        ),
                        rx.text(
                            "Excelencia en Soluciones Industriales",
                            size="1",
                            color="rgba(255,255,255,0.7)",
                        ),
                        align_items="start",
                        spacing="1",
                    ),
                    align_items="center",
                    spacing="3",
                    flex="1",
                ),
                
                # Información de contacto y redes sociales
                rx.hstack(
                    # Información de contacto
                    rx.vstack(
                        rx.text(
                            "Calle C, e/Calle 15 y Calle 13, Vedado",
                            size="2",
                            color="rgba(255,255,255,0.8)",
                            font_weight="medium",
                        ),
                        rx.text(
                            "Plaza de la Revolución, La Habana, Cuba",
                            size="2", 
                            color="rgba(255,255,255,0.7)",
                        ),
                        align_items="end",
                        spacing="1",
                    ),
                    
                    # Espaciador
                    rx.box(width="40px"),
                    
                    # Redes sociales - CORREGIDO: con z-index para estar por encima
                    rx.hstack(
                        # Instagram
                        rx.link(
                            rx.box(
                                rx.icon(
                                    tag="instagram",
                                    color="rgba(255,255,255,0.8)",
                                    font_size="24px",
                                    transition="all 0.3s ease",
                                ),
                                padding="8px",
                                background="rgba(255,255,255,0.1)",
                                border_radius="8px",
                                transition="all 0.3s ease",
                                _hover={
                                    "background": "rgba(255,255,255,0.2)",
                                    "transform": "translateY(-2px)",
                                }
                            ),
                            href="https://www.instagram.com/torre_fuerte_surl?igsh=NGdkZDJxZnluNnM=",
                            is_external=True,
                            position="relative",  # Añadido
                            z_index="10",  # Añadido para estar por encima
                        ),
                        
                        # Espacio entre íconos
                        rx.box(width="20px"),
                        
                        # Facebook
                        rx.link(
                            rx.box(
                                rx.icon(
                                    tag="facebook",
                                    color="rgba(255,255,255,0.8)",
                                    font_size="24px",
                                    transition="all 0.3s ease",
                                ),
                                padding="8px",
                                background="rgba(255,255,255,0.1)",
                                border_radius="8px",
                                transition="all 0.3s ease",
                                _hover={
                                    "background": "rgba(255,255,255,0.2)",
                                    "transform": "translateY(-2px)",
                                }
                            ),
                            href="https://www.facebook.com/torrefuerte.surl",
                            is_external=True,
                            position="relative",  # Añadido
                            z_index="10",  # Añadido para estar por encima
                        ),
                        align_items="center",
                    ),
                    
                    align_items="center",
                    justify="end",
                    flex="1",
                ),
                
                align_items="center",
                spacing="4",
                width="100%",
                max_width="1200px",
                padding_x=styles.Spacer.LARGE.value,
            ),
            
            # Línea divisoria
            rx.center(
                rx.box(
                    width="100%",
                    height="1px",
                    background="linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent)",
                    margin_y=styles.Spacer.MEDIUM.value,
                ),
                width="100%",
                max_width="1200px",
            ),
            
            # Copyright
            rx.center(
                rx.text(
                    f"© 2024 - {datetime.date.today().year} Torre Fuerte SURL - Todos los derechos reservados",
                    size="1",
                    color="rgba(255,255,255,0.6)",
                    text_align="center",
                ),
                width="100%",
            ),
            
            spacing="4",
            width="100%",
            padding_y=styles.Spacer.LARGE.value,
        ),
        background="linear-gradient(135deg, #194264 0%, #152a40 100%)",
        width="100%",
        position="relative",
        overflow="hidden",
        # Pseudo-elemento corregido con z-index más bajo
        _before={
            "content": "''",
            "position": "absolute",
            "top": "0",
            "left": "0",
            "right": "0",
            "bottom": "0",
            "background": "radial-gradient(circle at 80% 20%, rgba(255,255,255,0.05) 0%, transparent 50%)",
            "z_index": "1",  # Añadido z-index bajo
            "pointer_events": "none",  # IMPORTANTE: permite clics a través de este elemento
        }
    )

# El resto del código (footer_mobile y footer_final) se mantiene igual...

# Versión móvil optimizada (sin cambios)
def footer_mobile() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Logo y nombre
            rx.hstack(
                rx.image(
                    src="torre.png",
                    height="40px",
                    width="auto",
                    border_radius="8px",
                ),
                rx.vstack(
                    rx.heading(
                        "Torre Fuerte SURL",
                        size="4",
                        color="white",
                        font_weight="bold",
                    ),
                    rx.text(
                        "Excelencia Industrial",
                        size="1",
                        color="rgba(255,255,255,0.7)",
                    ),
                    align_items="start",
                    spacing="1",
                ),
                align_items="center",
                spacing="3",
                width="100%",
                justify="center",
            ),
            
            # Información de contacto
            rx.vstack(
                rx.text(
                    "Calle C, e/Calle 15 y Calle 13, Vedado",
                    size="1",
                    color="rgba(255,255,255,0.8)",
                    text_align="center",
                    font_weight="medium",
                ),
                rx.text(
                    "Plaza de la Revolución, La Habana, Cuba",
                    size="1",
                    color="rgba(255,255,255,0.7)",
                    text_align="center",
                ),
                align_items="center",
                spacing="1",
            ),
            
            # Redes sociales con más espacio
            rx.hstack(
                rx.link(
                    rx.box(
                        rx.icon(
                            tag="instagram",
                            color="rgba(255,255,255,0.8)",
                            font_size="24px",
                            transition="all 0.3s ease",
                        ),
                        padding="8px",
                        background="rgba(255,255,255,0.1)",
                        border_radius="8px",
                        transition="all 0.3s ease",
                        _hover={
                            "background": "rgba(255,255,255,0.2)",
                        }
                    ),
                    href="https://www.instagram.com/torre_fuerte_surl?igsh=NGdkZDJxZnluNnM=",
                    is_external=True,
                ),
                
                # Espacio generoso entre íconos
                rx.box(width="30px"),
                
                rx.link(
                    rx.box(
                        rx.icon(
                            tag="facebook",
                            color="rgba(255,255,255,0.8)",
                            font_size="24px",
                            transition="all 0.3s ease",
                        ),
                        padding="8px",
                        background="rgba(255,255,255,0.1)",
                        border_radius="8px",
                        transition="all 0.3s ease",
                        _hover={
                            "background": "rgba(255,255,255,0.2)",
                        }
                    ),
                    href="https://www.facebook.com/torrefuerte.surl",
                    is_external=True,
                ),
                spacing="0",
                justify="center",
            ),
            
            # Copyright
            rx.text(
                f"© 2024 - {datetime.date.today().year} Torre Fuerte SURL",
                size="1",
                color="rgba(255,255,255,0.6)",
                text_align="center",
            ),
            rx.text(
                "Todos los derechos reservados",
                size="1",
                color="rgba(255,255,255,0.6)",
                text_align="center",
            ),
            
            spacing="4",
            width="100%",
            padding=styles.Spacer.LARGE.value,
        ),
        background="linear-gradient(135deg, #194264 0%, #152a40 100%)",
        width="100%",
    )

# Componente final con responsive
def footer_final() -> rx.Component:
    return rx.box(
        rx.desktop_only(footer()),
        rx.mobile_and_tablet(footer_mobile()),
        width="100%",
    )