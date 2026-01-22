# TFuerte/components/admin_navbar.py
import reflex as rx
from TFuerte.routes import Route

def admin_navbar(title: str = "Dashboard") -> rx.Component:
    """Navbar para dashboards administrativas"""
    return rx.box(
        rx.hstack(
            rx.heading(
                f"🏢 {title}",
                size="6",
                style={
                    "background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
                    "background_clip": "text",
                    "webkit_background_clip": "text",
                    "color": "transparent",
                    "font_weight": "700",
                }
            ),
            rx.spacer(),
            rx.hstack(
                rx.link(
                    rx.button("📦 Almacén", variant="ghost", size="2"),
                    href=Route.ADMIN1.value,
                ),
                rx.link(
                    rx.button("🏠 Inicio", variant="ghost", size="2"),
                    href=Route.INDEX.value,
                ),
                rx.button(
                    "🚪 Cerrar Sesión",
                    variant="solid",
                    color_scheme="red",
                    size="2",
                    on_click=lambda: rx.redirect(Route.ADMIN_AUTH.value)
                ),
                spacing="3",
            ),
            width="100%",
            padding="1rem 2rem",
            border_bottom="1px solid #e2e8f0",
            background="white",
            position="sticky",
            top="0",
            z_index="1000",
        )
    )