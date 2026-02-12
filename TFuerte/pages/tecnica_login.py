# TFuerte/pages/tecnica_login.py
import reflex as rx
from TFuerte.state.tecnica_state import TecnicaState
from TFuerte.routes import Route

@rx.page(
    route=Route.TECNICA_LOGIN.value,
    title="Login - Jefe de Área Técnica",
)
def tecnica_login() -> rx.Component:
    """Página de login para Jefe de Área Técnica (Alexander)"""
    
    return rx.center(
        rx.box(
            rx.vstack(
                rx.heading(
                    "🔧 Login Área Técnica",
                    size="7",
                    margin_bottom="1rem",
                    style={
                        "background": "linear-gradient(135deg, #059669 0%, #047857 100%)",
                        "background_clip": "text",
                        "webkit_background_clip": "text",
                        "color": "transparent",
                        "font_weight": "800",
                    }
                ),
                rx.text(
                    "Acceso exclusivo para Jefe de Área Técnica",
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
                            on_change=TecnicaState.set_username,
                        ),
                        rx.input(
                            type="password",
                            placeholder="Contraseña",
                            name="password",
                            required=True,
                            size="3",
                            margin_bottom="2rem",
                            on_change=TecnicaState.set_password,
                        ),
                        rx.button(
                            "Ingresar",
                            type="submit",
                            size="3",
                            width="100%",
                            loading=TecnicaState.loading,
                            style={
                                "background": "linear-gradient(135deg, #059669 0%, #047857 100%)",
                                "color": "white",
                                "font_weight": "600",
                            }
                        ),
                        spacing="1",
                    ),
                    on_submit=TecnicaState.sign_in,
                    reset_on_submit=False,
                ),
                
                rx.cond(
                    TecnicaState.error_message != "",
                    rx.callout(
                        TecnicaState.error_message,
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
        background="linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%)",
    )