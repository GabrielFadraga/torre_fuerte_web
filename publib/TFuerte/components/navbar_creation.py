import reflex as rx
from TFuerte.styles.colors import Text_tx, Color_tx
from TFuerte.styles.fonts import FontWeight as FontWeight
from TFuerte.styles.fonts import Fonts_tx as Fonts_tx
from TFuerte.components.title import title as title
import TFuerte.styles.styles as styles
from TFuerte.routes import Route

def creation() -> rx.Component:
    return rx.desktop_only(
        rx.box(
            rx.center(
                rx.hstack(
                    
                    # Navegación principal con efectos mejorados
                    rx.hstack(
                        _nav_item("Inicio", Route.INDEX.value),
                        _nav_item("Nosotros", Route.ABOUT.value),
                        _nav_item("Servicios", Route.SERVICES.value),
                        _nav_item("Cartera", Route.PROJECTS.value),
                        _nav_item("Grupo", Route.TEAM.value),
                        _nav_item("Taller", Route.TALLER.value),
                        spacing="5",
                        align="end",
                        justify="end",
                        width="100%"
                    ),
                    
                    align="center",
                    width="100%",
                    #max_width="1200px",
                    padding_x=styles.Spacer.LARGE.value,
                ),
            ),
            
            # Estilos del navbar - MODIFICADO: sin posición fija y con padding ajustado
            width="100%",
            padding=styles.Spacer.DEFAULT.value,  # Padding vertical ajustado
            background="linear-gradient(135deg, #194264 0%, #152a40 100%)",
            box_shadow="0 4px 20px rgba(0,0,0,0.15)",
            # ELIMINADO: position="fixed", top="0", z_index="1000"
            border_bottom="1px solid rgba(255,255,255,0.1)",
            align="end",
            justify="end",
        ),
        #padding=styles.Spacer.DEFAULT.value,
        align="end",
        justify="end",
        top="0",
        z_index="1000",
        width="100%"
    )

def _nav_item(text: str, href: str) -> rx.Component:
    return rx.box(
        rx.link(
            rx.text(
                text,
                color="rgba(255,255,255,0.85)",
                font_weight="500",
                size="3",
                letter_spacing="0.5px",
                padding_x="12px",
                padding_y="10px",
                transition="all 0.3s ease",
                position="relative",
            ),
            href=href,
            position="relative",
            _hover={"text_decoration": "none"},
        ),
        position="relative",
        # Efecto de subrayado animado
        _after={
            "content": "''",
            "position": "absolute",
            "bottom": "0",
            "left": "50%",
            "width": "0%",
            "height": "2px",
            "background": "linear-gradient(90deg, transparent, #ff6b35, transparent)",
            "transition": "all 0.3s ease",
            "transform": "translateX(-50%)",
            "border_radius": "2px",
        },
        # Efecto de fondo al hover
        _before={
            "content": "''",
            "position": "absolute",
            "top": "50%",
            "left": "50%",
            "width": "0%",
            "height": "0%",
            "background": "rgba(255,255,255,0.05)",
            "border_radius": "8px",
            "transition": "all 0.3s ease",
            "transform": "translate(-50%, -50%)",
        },
        # Unimos todos los efectos hover en un solo diccionario
        _hover={
            "& .nav-text": {
                "color": "white",
            },
            "_after": {
                "width": "80%",
            },
            "_before": {
                "width": "100%",
                "height": "100%",
            }
        },
    )