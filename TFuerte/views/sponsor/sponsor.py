import reflex as rx
import TFuerte.styles.styles as styles
from TFuerte.components.title import title
from TFuerte.components.link_sponsor import link_sponsor
from typing import List

# Constantes fijas para el carrusel
CARD_WIDTH = 250
CARD_GAP = 16
ITEMS_PER_PAGE = 4
CARD_HEIGHT = 180  # Altura fija para todas las tarjetas

class SponsorCarouselState(rx.State):
    current_index: int = 0

    clients: List[dict] = [
        {"src": "navegacion.png", "name": "Empresa de Navegación Caribe", "href": "https://www.gemar.transnet.cu/es/empresas/empresa-de-navegacion-caribe"},
        {"src": "salud.png", "name": "Ministerio de Salud Pública", "href": "https://salud.msp.gob.cu/"},
        {"src": "eng.png", "name": "Engimov Caribe", "href": "https://www.engimov.pt/es/grupo/engimov-caribe"},
        {"src": "puerto.png", "name": "Prácticos de Puerto", "href": "https://www.practicosdepuerto.es"},
        {"src": "UNE.png", "name": "Unión Eléctrica", "href": "https://www.unionelectrica.cu/"},
        {"src": "MINAL.png", "name": "Ministerio de la Industria Alimentaria", "href": None},
        {"src": "turcos.png", "name": "Karadeniz Holding", "href": "https://www.karadenizholding.com/"},
    ]

    @rx.var
    def total_width(self) -> int:
        return len(self.clients) * CARD_WIDTH + (len(self.clients) - 1) * CARD_GAP

    @rx.var
    def visible_width(self) -> int:
        return ITEMS_PER_PAGE * CARD_WIDTH + (ITEMS_PER_PAGE - 1) * CARD_GAP

    @rx.var
    def translate_x(self) -> str:
        return f"translateX(-{self.current_index * (CARD_WIDTH + CARD_GAP)}px)"

    @rx.var
    def max_index(self) -> int:
        return len(self.clients) - ITEMS_PER_PAGE

    def next(self):
        if self.current_index < self.max_index:
            self.current_index += 1
        else:
            self.current_index = 0

    def next_auto(self):
        self.next()

def client_card(client: dict) -> rx.Component:
    content = rx.vstack(
        rx.image(
            src=client["src"],
            width="120px",
            height="60px",
            object_fit="contain",
            filter="brightness(0) invert(1)",
            transition="all 0.3s ease",
            _hover={
                "transform": "scale(1.1)",
                "filter": "brightness(0) invert(1) drop-shadow(0 4px 12px rgba(255,255,255,0.3))",
            },
        ),
        rx.text(
            client["name"],
            font_size="12px",
            color="rgba(255,255,255,0.7)",
            text_align="center",
            margin_top="8px",
            font_weight="medium",
        ),
        align_items="center",
        justify_content="center",  # Centrado vertical
        spacing="2",
        width="100%",
        height="100%",  # Ocupa toda la altura de la tarjeta
    )
    return rx.box(
        rx.cond(
            client["href"],
            rx.link(content, href=client["href"], is_external=True),
            content,
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
        },
        width=f"{CARD_WIDTH}px",
        height=f"{CARD_HEIGHT}px",  # Altura fija para uniformidad
        flex_shrink=0,
    )

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
            # Carrusel centrado
            rx.center(
                rx.box(
                    rx.hstack(
                        rx.hstack(
                            rx.foreach(
                                SponsorCarouselState.clients,
                                lambda client: client_card(client)
                            ),
                            style={"gap": f"{CARD_GAP}px"},
                            transform=SponsorCarouselState.translate_x,
                            transition="transform 0.5s ease",
                            width=f"{SponsorCarouselState.total_width}px",
                        ),
                        overflow_x="hidden",
                        width=f"{SponsorCarouselState.visible_width}px",
                    ),
                    width="100%",
                    display="flex",
                    justify_content="center",
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
                ),
                width="100%",
                margin_bottom=styles.Spacer.LARGE.value,
            ),
            # Temporizador invisible (cada 5 segundos)
            rx.moment(
                interval=5000,
                on_change=SponsorCarouselState.next_auto,
                display="none",
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
        },
    )

def sponsor_mobile() -> rx.Component:
    return rx.box(
        rx.vstack(
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
            rx.vstack(
                rx.foreach(
                    SponsorCarouselState.clients,
                    lambda client: client_card(client)
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

def sponsor_final() -> rx.Component:
    return rx.box(
        rx.desktop_only(sponsor()),
        rx.mobile_and_tablet(sponsor_mobile()),
        width="100%",
    )