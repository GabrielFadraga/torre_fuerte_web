import reflex as rx
from TFuerte.routes import Route
from TFuerte.state.auth_state import AuthState
import TFuerte.styles.styles as styles

def auth_signup() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.center(
                rx.image(
                    src="sf.png", width="3.5em", height="auto", border_radius="25%"
                ),
                rx.heading(
                    "Crear Cuenta",
                    size="6",
                    as_="h2",
                    text_align="center",
                    width="100%",
                    color="#1C1C1C",
                ),
                direction="column",
                spacing="5",
                width="100%",
            ),
            
            # Mensajes de error/éxito
            rx.cond(
                AuthState.error_message,
                rx.callout(
                    AuthState.error_message,
                    icon="alert_triangle",
                    color_scheme="red",
                    width="100%",
                ),
            ),
            
            rx.cond(
                AuthState.success_message,
                rx.callout(
                    AuthState.success_message,
                    icon="check_circle",
                    color_scheme="green",
                    width="100%",
                ),
            ),
            
            rx.vstack(
                rx.text(
                    "Email",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                    color="#1C1C1C",
                ),
                rx.input(
                    placeholder="usuario@ejemplo.com",
                    type="email",
                    size="3",
                    width="100%",
                    value=AuthState.email,
                    on_change=AuthState.set_email,
                    is_disabled=AuthState.loading,
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            
            rx.vstack(
                rx.text(
                    "Contraseña",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                    color="#1C1C1C",
                ),
                rx.input(
                    placeholder="Mínimo 6 caracteres",
                    type="password",
                    size="3",
                    width="100%",
                    value=AuthState.password,
                    on_change=AuthState.set_password,
                    is_disabled=AuthState.loading,
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            
            rx.vstack(
                rx.text(
                    "Confirmar Contraseña",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                    color="#1C1C1C",
                ),
                rx.input(
                    placeholder="Repite tu contraseña",
                    type="password",
                    size="3",
                    width="100%",
                    value=AuthState.confirm_password,
                    on_change=AuthState.set_confirm_password,
                    is_disabled=AuthState.loading,
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            
            # Cambiar el botón de "Register" a:
            rx.button(
                "Registrarse",
                size="3",
                width="100%",
                on_click=AuthState.sign_up,  # Usar el método del estado
                loading=AuthState.loading,
                is_disabled=AuthState.loading,
            ),
            
            rx.center(
                rx.text("¿Ya tienes cuenta?", size="3", color="#1C1C1C"),
                rx.link("Inicia Sesión", href=Route.ADMIN_LOGIN.value, size="3"),
                opacity="0.8",
                spacing="2",
                direction="row",
                width="100%",
            ),
            
            spacing="6",
            width="100%",
        ),
        max_width="28em",
        size="4",
        width="100%",
        margin=styles.Spacer.SMALL.value
    )