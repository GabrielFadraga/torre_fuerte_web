import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles
from TFuerte.views.header.header_responsive import header_responsive
from TFuerte.styles.colors import Text_tx, Color_tx

def member_card(name: str, position: str, region: str = None, image: str = "user1.png") -> rx.Component:
    """Componente de tarjeta para cada miembro del equipo"""
    return rx.card(
        rx.vstack(
            rx.avatar(
                src=image,
                size="8",
                radius="full",
                border=f"4px solid {Color_tx.Primary.value}",
                margin_bottom="1em",
            ),
            rx.vstack(
                rx.text(
                    name,
                    size="6",
                    weight="bold",
                    color=Text_tx.Black.value,
                    text_align="center",
                ),
                rx.text(
                    position,
                    size="5",
                    color=Text_tx.Black.value,
                    text_align="center",
                ),
                rx.cond(
                    region,
                    rx.text(
                        region,
                        size="4",
                        color=Text_tx.Black.value,
                        text_align="center",
                    ),
                ),
                align_items="center",
                spacing="2",
            ),
            align_items="center",
            padding="1.5em",
        ),
        variant="ghost",
        width="100%",
        max_width="220px",
        height="100%",
        _hover={
            "transform": "translateY(-5px)",
            "box_shadow": "0 10px 25px rgba(0,0,0,0.1)",
            "transition": "all 0.3s ease",
        },
    )

def header_team() -> rx.Component:
    return rx.vstack(
        # Título
        rx.heading(
            "Principales contactos",
            size="9",
            text_align="center",
            margin_bottom="2em",
            color=Text_tx.Black.value,
        ),
        
        # Versión escritorio
        rx.desktop_only(
            rx.vstack(
                # Presidente - En la cima, centrado
                rx.center(
                    member_card(
                        "Lic Maikel Torres López",
                        "Presidente"
                    ),
                    width="100%",
                    margin_bottom="2em",
                ),
                
                # Director Adjunto - Abajo y más centrado (aumenté el padding_left)
                rx.box(
                    member_card(
                        "Ing. Euclides Rodríguez Mejías", 
                        "Director Adjunto"
                    ),
                    width="100%",
                    display="flex",
                    justify_content="left",
                    padding_left="20em",  # Aumenté de 2em a 8em
                    margin_bottom="3em",
                ),
                
                # Equipo directivo - Los cinco como estaban
                rx.box(
                    rx.flex(
                        member_card(
                            "Lic. Meylin Yu Parra",
                            "Jefa de Área Administrativa"
                        ),
                        member_card(
                            "Ing. Miguel Obregón Salomón",
                            "Jefe de Área Logística"
                        ),
                        member_card(
                            "Ing. Gilberto Acosta Monjes",
                            "Jefe de Coordinación",
                            "Habana-Mayabeque"
                        ),
                        member_card(
                            "Ing. Manuel Núñez Brea",
                            "Jefe de Coordinación Oriente"
                        ),
                        member_card(
                            "T.M Alexander Martínez Elias",
                            "Jefe de Área Técnica"
                        ),
                        direction="row",
                        wrap="wrap",
                        justify="center",
                        spacing="5",
                        width="100%",
                    ),
                    width="100%",
                ),
                align_items="center",
                width="100%",
            )
        ),
        
        # Versión móvil y tablet
        rx.mobile_and_tablet(
            rx.vstack(
                member_card("Lic Maikel Torres López", "Presidente"),
                member_card("Ing. Euclides Rodríguez Mejías", "Director Adjunto"),
                member_card("Lic. Meylin Yu Parra", "Jefa de Área Administrativa"),
                member_card("Ing. Miguel Obregón Salomón", "Jefe de Área Logística"),
                member_card("Ing. Gilberto Acosta Monjes", "Jefe de Coordinación", "Habana-Mayabeque"),
                member_card("Ing. Manuel Núñez Brea", "Jefe de Coordinación Oriente"),
                member_card("T.M Alexander Martínez Elias", "Jefe de Área Técnica"),
                spacing="4",
                width="100%",
            )
        ),
        
        # Estilos generales
        align_items="center",
        width="100%",
        padding_y="3em",
        spacing="6",
        background="linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)",
    )