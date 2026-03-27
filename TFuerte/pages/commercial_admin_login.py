import reflex as rx
from TFuerte.state.commercial_admin_auth_state import CommercialAdminAuthState
from TFuerte.routes import Route

@rx.page(
    route=Route.COMMERCIAL_ADMIN_LOGIN.value,
    title="Login - Administración Comercial",
)
def commercial_admin_login() -> rx.Component:
    """Página de login para el panel de administración comercial"""
    
    return rx.center(
        rx.box(
            rx.vstack(
                rx.heading(
                    "📊 Administración Comercial",
                    size="7",
                    margin_bottom="1rem",
                    style={
                        "background": "linear-gradient(135deg, #0f766e 0%, #115e59 100%)",
                        "background_clip": "text",
                        "webkit_background_clip": "text",
                        "color": "transparent",
                        "font_weight": "800",
                    }
                ),
                rx.text(
                    "Acceso exclusivo para administradores",
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
                            on_change=CommercialAdminAuthState.set_username,
                            background="gray"
                        ),
                        rx.input(
                            type="password",
                            placeholder="Contraseña",
                            name="password",
                            required=True,
                            size="3",
                            margin_bottom="2rem",
                            on_change=CommercialAdminAuthState.set_password,
                            background="gray"
                        ),
                        rx.button(
                            "Ingresar",
                            type="submit",
                            size="3",
                            width="100%",
                            loading=CommercialAdminAuthState.loading,
                            style={
                                "background": "linear-gradient(135deg, #0f766e 0%, #115e59 100%)",
                                "color": "white",
                                "font_weight": "600",
                            }
                        ),
                        spacing="1",
                    ),
                    on_submit=CommercialAdminAuthState.login,
                    reset_on_submit=False,
                ),
                
                rx.cond(
                    CommercialAdminAuthState.error_message != "",
                    rx.callout(
                        CommercialAdminAuthState.error_message,
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
        background="linear-gradient(135deg, #e6f7f5 0%, #cfe9e6 100%)",
    )