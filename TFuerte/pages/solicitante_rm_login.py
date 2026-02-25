# TFuerte/pages/solicitante_rm_login.py
import reflex as rx
from TFuerte.state.solicitante_rm_state import SolicitanteRMState
from TFuerte.routes import Route

@rx.page(
    route=Route.SOLICITANTERM_LOGIN.value,
    title="Login - Solicitante",
)
def solicitante_login() -> rx.Component:
    """Página de login para Solicitantes (específico para RM)"""
    
    return rx.center(
        rx.box(
            rx.vstack(
                rx.heading(
                    "👤 Login Solicitante RM",
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
                    "Acceso para solicitantes de recursos y materiales",
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
                            on_change=SolicitanteRMState.set_usuario_rm,  # Cambiado
                            background="gray"
                        ),
                        rx.input(
                            type="password",
                            placeholder="Contraseña",
                            name="password",
                            required=True,
                            size="3",
                            margin_bottom="2rem",
                            on_change=SolicitanteRMState.set_clave_rm,  # Cambiado
                            background="gray"
                        ),
                        rx.button(
                            "Ingresar",
                            type="submit",
                            size="3",
                            width="100%",
                            loading=SolicitanteRMState.loading_auth_rm,  # Cambiado
                            style={
                                "background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
                                "color": "white",
                                "font_weight": "600",
                            }
                        ),
                        spacing="1",
                    ),
                    on_submit=SolicitanteRMState.sign_in_rm,  # Cambiado
                    reset_on_submit=False,
                ),
                
                rx.cond(
                    SolicitanteRMState.error_message_rm != "",  # Cambiado
                    rx.callout(
                        SolicitanteRMState.error_message_rm,  # Cambiado
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