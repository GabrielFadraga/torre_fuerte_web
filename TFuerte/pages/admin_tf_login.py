import reflex as rx
from TFuerte.state.admin_tf_state import AdminTFState
from TFuerte.components.navbar import navbar
from TFuerte.routes import Route

@rx.page(
    route=Route.ADMIN_LOGIN_PANEL.value,
    title="Login - Panel de Administración",
    description="Acceso al sistema de gestión de almacén"
)
def admin_tf_login() -> rx.Component:
    """Página de login para el panel de administración"""
    
    def login_form():
        return rx.card(
            rx.vstack(
                rx.center(
                    rx.vstack(
                        rx.icon(
                            "shield", 
                            size=70, 
                            color="#0f766e",
                            style={
                                "background": "linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%)",
                                "padding": "20px",
                                "border_radius": "50%",
                                "margin_bottom": "20px"
                            }
                        ),
                        rx.heading(
                            "🔐 Acceso Administrativo",
                            size="6",
                            color="#1e293b",
                            font_weight="700",
                            text_align="center"
                        ),
                        rx.text(
                            "Ingrese sus credenciales para acceder al panel de administración",
                            size="2", 
                            color="#64748b",
                            text_align="center",
                            margin_bottom="2rem"
                        ),
                        spacing="2",
                        align="center",
                        width="100%"
                    )
                ),
                
                rx.form(
                    rx.vstack(
                        rx.vstack(
                            rx.text(
                                "Usuario",
                                size="2",
                                font_weight="600",
                                color="#1e293b",
                                align="left",
                                width="100%"
                            ),
                            rx.input(
                                placeholder="Ingrese su usuario",
                                value=AdminTFState.username,
                                on_change=AdminTFState.set_username,
                                size="3",
                                width="100%",
                                style={
                                    "background": "gray",
                                    "border": "1px solid #e2e8f0",
                                    "_focus": {
                                        "border": "1px solid #0f766e",
                                        "box_shadow": "0 0 0 2px rgba(15, 118, 110, 0.1)"
                                    }
                                }
                            ),
                            spacing="1",
                            align="start",
                            width="100%"
                        ),
                        
                        rx.vstack(
                            rx.text(
                                "Contraseña",
                                size="2",
                                font_weight="600",
                                color="#1e293b",
                                align="left",
                                width="100%"
                            ),
                            rx.input(
                                type="password",
                                placeholder="Ingrese su contraseña",
                                value=AdminTFState.password,
                                on_change=AdminTFState.set_password,
                                size="3",
                                width="100%",
                                style={
                                    "background": "gray",
                                    "border": "1px solid #e2e8f0",
                                    "_focus": {
                                        "border": "1px solid #0f766e",
                                        "box_shadow": "0 0 0 2px rgba(15, 118, 110, 0.1)"
                                    }
                                }
                            ),
                            spacing="1",
                            align="start",
                            width="100%"
                        ),
                        
                        rx.cond(
                            AdminTFState.error_message != "",
                            rx.callout(
                                AdminTFState.error_message,
                                icon="alert_circle",
                                color_scheme="red",
                                role="alert",
                                width="100%"
                            )
                        ),
                        
                        rx.button(
                            "Iniciar Sesión",
                            type="submit",
                            size="3",
                            width="100%",
                            loading=AdminTFState.loading,
                            style={
                                "background": "linear-gradient(135deg, #0f766e 0%, #115e59 100%)",
                                "color": "white",
                                "font_weight": "600",
                                "margin_top": "1.5rem",
                                "_hover": {
                                    "background": "linear-gradient(135deg, #115e59 0%, #134e4a 100%)",
                                    "transform": "translateY(-2px)",
                                    "box_shadow": "0 10px 25px -5px rgba(15, 118, 110, 0.3)"
                                }
                            }
                        ),
                        
                        rx.divider(margin_y="1rem"),
                        
                        rx.text(
                            "Nota: Esta es la entrada al panel administrativo del sistema. ",
                            size="1", 
                            color="#94a3b8",
                            text_align="center",
                            line_height="1.5"
                        ),
                        
                        spacing="4",
                        align="center",
                        width="100%"
                    ),
                    on_submit=AdminTFState.sign_in,
                ),
                
                spacing="4",
                align="center",
                width="100%"
            ),
            style={
                "background": "white",
                "border_radius": "16px",
                "box_shadow": "0 10px 40px rgba(0, 0, 0, 0.08)",
                "border": "1px solid #e2e8f0",
                "padding": "2rem",
                "width": "100%",
                "max_width": "400px"
            }
        )
    
    def main_content():
        return rx.box(
            navbar("Acceso seguro"),
            
            rx.vstack(
                # Encabezado
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.heading(
                                "🏢 Sistema de Gestión Empresarial",
                                size="8",
                                color="#1e293b",
                                text_align="center",
                                style={
                                    "background": "linear-gradient(135deg, #0f766e 0%, #115e59 100%)",
                                    "background_clip": "text",
                                    "webkit_background_clip": "text",
                                    "color": "transparent",
                                    "font_weight": "800",
                                    "margin_bottom": "0.5rem"
                                }
                            ),
                            rx.text(
                                "Panel de Administración - Acceso Seguro",
                                size="5",
                                color="#64748b",
                                text_align="center",
                                margin_bottom="0.5rem"
                            ),
                            spacing="2",
                            align="center",
                            width="100%"
                        ),
                        width="100%"
                    ),
                    width="100%",
                    padding="4rem 1rem",
                    background="linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
                    border_bottom="1px solid #e2e8f0"
                ),
                
                # Formulario de login
                rx.box(
                    rx.center(
                        rx.vstack(
                            
                            login_form(),
                            spacing="4",
                            align="center",
                            width="100%"
                        ),
                        width="100%"
                    ),
                    width="100%",
                    padding="4rem 1rem"
                ),
                
                # Información de seguridad
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.heading(
                                "ℹ️ Información de Seguridad",
                                size="4",
                                color="#1e293b",
                                text_align="center",
                                margin_bottom="2rem"
                            ),
                            rx.hstack(
                                rx.vstack(
                                    rx.icon("shield", size=24, color="#0f766e"),
                                    rx.text("Acceso Restringido", size="2", font_weight="600", color="#1e293b"),
                                    rx.text("Solo personal autorizado", size="1", color="#64748b", text_align="center"),
                                    align="center",
                                    spacing="1"
                                ),
                                rx.vstack(
                                    rx.icon("lock", size=24, color="#0f766e"),
                                    rx.text("Conexión Segura", size="2", font_weight="600", color="#1e293b"),
                                    rx.text("Datos encriptados", size="1", color="#64748b", text_align="center"),
                                    align="center",
                                    spacing="1"
                                ),
                                rx.vstack(
                                    rx.icon("eye_off", size=24, color="#0f766e"),
                                    rx.text("Privacidad", size="2", font_weight="600", color="#1e293b"),
                                    rx.text("Credenciales protegidas", size="1", color="#64748b", text_align="center"),
                                    align="center",
                                    spacing="1"
                                ),
                                spacing="6",
                                justify="center",
                                wrap="wrap"
                            ),
                            spacing="4",
                            align="center",
                            width="100%"
                        ),
                        width="100%"
                    ),
                    width="100%",
                    padding="4rem 1rem",
                    background="#f8fafc",
                    border_top="1px solid #e2e8f0"
                ),
                
                # Pie de página
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.text(
                                "🏢 Sistema de Gestión Empresarial",
                                size="2",
                                font_weight="600",
                                color="#1e293b"
                            ),
                            rx.text(
                                "© 2026 - Todos los derechos reservados",
                                size="1",
                                color="#64748b"
                            ),
                            rx.hstack(
                                rx.text("Versión 1.0", size="1", color="#94a3b8"),
                                rx.text("•", size="1", color="#94a3b8"),
                                rx.text("Acceso Seguro", size="1", color="#94a3b8"),
                                spacing="2",
                                wrap="wrap",
                                justify="center"
                            ),
                            spacing="1",
                            align="center",
                            width="100%"
                        ),
                        width="100%"
                    ),
                    width="100%",
                    padding="2rem 1rem",
                    border_top="1px solid #e2e8f0",
                    background="white"
                ),
                
                spacing="0",
                align="start",
                width="100%"
            ),
            width="100%",
            min_height="100vh",
            style={
                "background": "linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)"
            }
        )
    
    return main_content()