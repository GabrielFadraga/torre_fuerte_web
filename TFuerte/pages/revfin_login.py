# TFuerte/pages/revfin_login.py
import reflex as rx
from TFuerte.state.financiamiento_state import FinanciamientoState
from TFuerte.routes import Route

@rx.page(
    route=Route.REVFIN_LOGIN.value,
    title="Login - Revisor Financiero",
)
def revfin_login() -> rx.Component:
    """Página de login para Revisor Financiero"""
    
    return rx.center(
        rx.box(
            rx.vstack(
                rx.heading(
                    "💰 Login Revisor Financiero",
                    size="7",
                    margin_bottom="1rem",
                    style={
                        "background": "linear-gradient(135deg, #0d9488 0%, #0f766e 100%)",
                        "background_clip": "text",
                        "webkit_background_clip": "text",
                        "color": "transparent",
                        "font_weight": "800",
                    }
                ),
                rx.text(
                    "Acceso exclusivo para Revisor Financiero",
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
                            on_change=FinanciamientoState.set_username_revfin,
                        ),
                        rx.input(
                            type="password",
                            placeholder="Contraseña",
                            name="password",
                            required=True,
                            size="3",
                            margin_bottom="2rem",
                            on_change=FinanciamientoState.set_password_revfin,
                        ),
                        rx.button(
                            "Ingresar",
                            type="submit",
                            size="3",
                            width="100%",
                            loading=FinanciamientoState.loading_revfin,
                            style={
                                "background": "linear-gradient(135deg, #0d9488 0%, #0f766e 100%)",
                                "color": "white",
                                "font_weight": "600",
                            }
                        ),
                        spacing="1",
                    ),
                    on_submit=FinanciamientoState.sign_in_revfin,
                    reset_on_submit=False,
                ),
                
                rx.cond(
                    FinanciamientoState.error_message_revfin != "",
                    rx.callout(
                        FinanciamientoState.error_message_revfin,
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
        background="linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%)",
    )