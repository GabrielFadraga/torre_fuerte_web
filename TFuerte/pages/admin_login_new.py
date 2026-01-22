# TFuerte/pages/admin_login_new.py
import reflex as rx
from TFuerte.state.admin_auth_state import AdminAuthState
from TFuerte.routes import Route

@rx.page(
    route=Route.ADMIN_LOGIN_NEW.value,
    title="Login - Administradores",
)
def admin_login_new() -> rx.Component:
    """Página de login para administradores"""
    
    return rx.center(
        rx.box(
            rx.vstack(
                rx.heading(
                    "🔐 Login Administradores",
                    size="7",
                    margin_bottom="1rem",
                    style={
                        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        "background_clip": "text",
                        "webkit_background_clip": "text",
                        "color": "transparent",
                        "font_weight": "800",
                    }
                ),
                rx.text(
                    "Acceso exclusivo para administradores autorizados",
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
                            on_change=AdminAuthState.set_username,
                        ),
                        rx.input(
                            type="password",
                            placeholder="Contraseña",
                            name="password",
                            required=True,
                            size="3",
                            margin_bottom="2rem",
                            on_change=AdminAuthState.set_password,
                        ),
                        rx.button(
                            "Ingresar",
                            type="submit",
                            size="3",
                            width="100%",
                            loading=AdminAuthState.loading,
                            style={
                                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                "color": "white",
                                "font_weight": "600",
                            }
                        ),
                        spacing="1",
                    ),
                    on_submit=AdminAuthState.sign_in,
                    reset_on_submit=False,
                ),
                
                rx.cond(
                    AdminAuthState.error_message != "",
                    rx.callout(
                        AdminAuthState.error_message,
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
        background="linear-gradient(135deg, #f5f7ff 0%, #f0f2ff 100%)",
    )