import reflex as rx
from TFuerte.routes import Route
from TFuerte.state.auth_state import AuthState
import TFuerte.styles.styles as styles

def auth_login() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.center(
                rx.image(
                    src="sf.png", width="3.5em", height="auto", border_radius="25%"
                ),
                rx.heading(
                    "Iniciar Sesión",
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
                rx.hstack(
                    rx.text("Contraseña", size="3", weight="medium", color="#1C1C1C"),
                    #rx.link("¿Olvidaste tu contraseña?", href="#", size="3", color="#1C1C1C"),
                    justify="between",
                    width="100%",
                ),
                rx.input(
                    placeholder="Ingresa tu contraseña",
                    type="password",
                    size="3",
                    width="100%",
                    value=AuthState.password,
                    on_change=AuthState.set_password,
                    is_disabled=AuthState.loading,
                ),
                spacing="2",
                width="100%",
            ),
            
            # En la función auth_login(), cambiar el botón de "Sign in" a:
        rx.button(
            "Iniciar Sesión", 
            size="3", 
            width="100%",
            on_click=AuthState.sign_in,  # Usar el método del estado
            loading=AuthState.loading,   # Mostrar loading mientras autentica
            is_disabled=AuthState.loading,
        ),
            
            #rx.center(
            #    rx.text("¿Nuevo aquí?", size="3", color="#1C1C1C"),
            #    rx.link("Regístrate", href=Route.ADMIN_SIGNUP.value, size="3"),
            #    opacity="0.8",
            #    spacing="2",
            #    direction="row",
            #),
            
            spacing="6",
            width="100%",
        ),
        size="4",
        max_width="28em",
        width="100%",
        margin=styles.Spacer.SMALL.value
    )