import reflex as rx
from TFuerte.styles.colors import Text_tx, Color_tx
from TFuerte.styles.fonts import FontWeight as FontWeight
from TFuerte.styles.fonts import Fonts_tx as Fonts_tx
from TFuerte.components.title import title as title
import TFuerte.styles.styles as styles
from TFuerte.routes import Route

# Estado para controlar el drawer móvil con setters explícitos
class SidebarState(rx.State):
    show_drawer: bool = False

    def toggle_drawer(self):
        self.show_drawer = not self.show_drawer
    
    # Setter explícito para show_drawer
    def set_show_drawer(self, value: bool):
        self.show_drawer = value

# Componente para cada item del sidebar
def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=20),
            rx.text(text, size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            border_radius="0.5em",
            _hover={
                "background_color": rx.color("accent", 4),
                "color": rx.color("accent", 11),
            },
        ),
        href=href,
        underline="none",
        font_weight="medium",
        width="100%",
    )

# Grupo de items del sidebar
def sidebar_items() -> rx.Component:
    return rx.vstack(
        sidebar_item("Inicio", "layout-dashboard", Route.INDEX.value),
        sidebar_item("Nosotros", "building-2", Route.ABOUT.value),
        sidebar_item("Servicios", "notebook-tabs", Route.SERVICES.value),
        sidebar_item("Cartera", "folder-open-dot", Route.PROJECTS.value),
        sidebar_item("Grupo", "user-round", Route.TEAM.value),
        sidebar_item("Taller", "pickaxe", Route.TALLER.value),
        sidebar_item("Eventos", "cctv", Route.EVENTOS.value),
        sidebar_item("Admin", "user_check", Route.ADMIN_PAGE.value),
        spacing="2",
        width="100%",
    )

def sidebar() -> rx.Component:
    return rx.box(
        rx.mobile_and_tablet(
            rx.menu.root(
                rx.menu.trigger(
                    rx.icon_button(
                        rx.icon("menu"),
                        position="relative",
                        top="1rem",
                        left="0.7rem",
                        z_index="100",
                        background_color="#194264FF",
                    )
                ),
                rx.menu.content(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Menú", size="5"),
                            width="100%",
                            justify="between",
                            padding_bottom="1em",
                        ),
                        sidebar_items(),
                        align="start",
                        width="100%",
                    ),
                    background_color=rx.color("accent", 2),
                    width="80vw",
                    max_width="300px",
                    position="fixed",
                    left="0",
                    top="0",
                    height="100vh",
                    border_radius="0",
                ),
            ),
        ),
    )