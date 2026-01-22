# TFuerte/pages/solicitante_login.py
import reflex as rx
from TFuerte.state.solicitante_auth_state import SolicitanteAuthState
from TFuerte.routes import Route

@rx.page(
    route=Route.SOLICITANTE_LOGIN.value,
    title="Login - Solicitantes",
)
def solicitante_login() -> rx.Component:
    """Página de login para solicitantes"""
    
    return rx.center(
        rx.box(
            rx.vstack(
                rx.heading(
                    "👤 Login Solicitantes",
                    size="7",
                    margin_bottom="1rem",
                    style={
                        "background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
                        "background_clip": "text",
                        "webkit_background_clip": "text",
                        "color": "transparent",
                        "font_weight": "800",
                    }
                ),
                rx.text(
                    "Acceso para personal autorizado a solicitar materiales",
                    size="3",
                    color="gray",
                    margin_bottom="2rem",
                ),
                
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Usuario",
                            name="usuario",
                            required=True,
                            size="3",
                            margin_bottom="1rem",
                            on_change=SolicitanteAuthState.set_usuario,
                        ),
                        rx.input(
                            type="password",
                            placeholder="Clave",
                            name="clave",
                            required=True,
                            size="3",
                            margin_bottom="2rem",
                            on_change=SolicitanteAuthState.set_clave,
                        ),
                        rx.button(
                            "Ingresar",
                            type="submit",
                            size="3",
                            width="100%",
                            loading=SolicitanteAuthState.loading,
                            style={
                                "background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
                                "color": "white",
                                "font_weight": "600",
                            }
                        ),
                        spacing="1",
                    ),
                    on_submit=SolicitanteAuthState.sign_in,
                    reset_on_submit=False,
                ),
                
                rx.cond(
                    SolicitanteAuthState.error_message != "",
                    rx.callout(
                        SolicitanteAuthState.error_message,
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
        background="linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)",
    )