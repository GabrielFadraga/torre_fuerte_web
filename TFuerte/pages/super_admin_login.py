# TFuerte/pages/super_admin_login.py
import reflex as rx
from TFuerte.state.super_admin_auth_state import SuperAdminAuthState
from TFuerte.routes import Route

@rx.page(route=Route.SUPER_ADMIN_LOGIN.value, title="Login - Super Administrador")
def super_admin_login() -> rx.Component:
    return rx.center(
        rx.box(
            rx.vstack(
                rx.heading(
                    "🔐 Panel de Control de Usuarios",
                    size="7",
                    margin_bottom="1rem",
                    style={
                        "background": "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)",
                        "background_clip": "text",
                        "webkit_background_clip": "text",
                        "color": "transparent",
                        "font_weight": "800",
                    }
                ),
                rx.text(
                    "Acceso exclusivo para superadministradores",
                    size="3",
                    color="gray",
                    margin_bottom="2rem",
                ),
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Usuario",
                            name="username",
                            required=True,
                            size="3",
                            margin_bottom="1rem",
                            on_change=SuperAdminAuthState.set_username,
                            background="gray"
                        ),
                        rx.input(
                            type="password",
                            placeholder="Contraseña",
                            name="password",
                            required=True,
                            size="3",
                            margin_bottom="2rem",
                            on_change=SuperAdminAuthState.set_password,
                            background="gray"
                        ),
                        rx.button(
                            "Ingresar",
                            type="submit",
                            size="3",
                            width="100%",
                            loading=SuperAdminAuthState.loading,
                            style={
                                "background": "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)",
                                "color": "white",
                                "font_weight": "600",
                            }
                        ),
                        spacing="1",
                    ),
                    on_submit=SuperAdminAuthState.login,
                    reset_on_submit=False,
                ),
                rx.cond(
                    SuperAdminAuthState.error_message != "",
                    rx.callout(
                        SuperAdminAuthState.error_message,
                        icon="alert_triangle",
                        color_scheme="red",
                        margin_top="1rem",
                        width="100%",
                    ),
                ),
                rx.divider(margin_y="2rem"),
                rx.link(
                    rx.button(
                        "Volver al inicio",
                        variant="soft",
                        size="2",
                    ),
                    href=Route.INDEX.value,
                ),
                spacing="4",
                align="center",
                width="100%",
            ),
            width="100%",
            max_width="400px",
            padding="2rem",
            border_radius="lg",
            box_shadow="lg",
            background="white",
        ),
        height="100vh",
        background="linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%)",
    )