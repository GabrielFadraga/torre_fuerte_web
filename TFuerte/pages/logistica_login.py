# TFuerte/pages/logistica_login.py
import reflex as rx
from TFuerte.state.logistica_state import LogisticaState
from TFuerte.routes import Route

@rx.page(
    route=Route.LOGISTICA_LOGIN.value,
    title="Login - Jefe de Logística",
)
def logistica_login() -> rx.Component:
    """Página de login para Jefe de Logística (Miguel)"""
    
    return rx.center(
        rx.box(
            rx.vstack(
                rx.heading(
                    "🚚 Login Logística",
                    size="7",
                    margin_bottom="1rem",
                    style={
                        "background": "linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)",
                        "background_clip": "text",
                        "webkit_background_clip": "text",
                        "color": "transparent",
                        "font_weight": "800",
                    }
                ),
                rx.text(
                    "Acceso exclusivo para Jefe de Logística",
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
                            on_change=LogisticaState.set_username,
                            background="gray"
                        ),
                        rx.input(
                            type="password",
                            placeholder="Contraseña",
                            name="password",
                            required=True,
                            size="3",
                            margin_bottom="2rem",
                            on_change=LogisticaState.set_password,
                            background="gray"
                        ),
                        rx.button(
                            "Ingresar",
                            type="submit",
                            size="3",
                            width="100%",
                            loading=LogisticaState.loading,
                            style={
                                "background": "linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)",
                                "color": "white",
                                "font_weight": "600",
                            }
                        ),
                        spacing="1",
                    ),
                    on_submit=LogisticaState.sign_in,
                    reset_on_submit=False,
                ),
                
                rx.cond(
                    LogisticaState.error_message != "",
                    rx.callout(
                        LogisticaState.error_message,
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
        background="linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)",
    )