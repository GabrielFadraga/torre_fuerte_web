# TFuerte/pages/user_selection.py
import reflex as rx
from TFuerte.components.navbar import navbar
from TFuerte.routes import Route

@rx.page(
    route=Route.ADMIN_PAGE.value,
    title="Sistema de Gestión de Almacén - Selección de Usuario",
    description="Seleccione su tipo de usuario para acceder al sistema"
)
def user_selection() -> rx.Component:
    """Página de selección de tipo de usuario"""
    
    # Tarjeta para Administrador
    def admin_card():
        return rx.card(
            rx.vstack(
                rx.icon(
                    "shield", 
                    size=48, 
                    color="#0f766e",
                    style={
                        "background": "linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%)",
                        "padding": "20px",
                        "border_radius": "50%",
                        "margin_bottom": "20px"
                    }
                ),
                rx.heading("Administrador", size="6", color="#1e293b", font_weight="700"),
                rx.text(
                    "Gestión y aprobación de solicitudes de recursos. Control completo del sistema.",
                    size="2", 
                    color="#64748b",
                    text_align="center",
                    line_height="1.5"
                ),
                rx.divider(margin_y="1rem"),
                rx.vstack(
                    rx.hstack(
                        rx.icon("check-circle", size=16, color="#059669"),
                        rx.text("Aprobar/Rechazar solicitudes", size="2", color="#1e293b"),
                        spacing="2",
                        align="center"
                    ),
                    rx.hstack(
                        rx.icon("check-circle", size=16, color="#059669"),
                        rx.text("Ver historial completo", size="2", color="#1e293b"),
                        spacing="2",
                        align="center"
                    ),
                    rx.hstack(
                        rx.icon("check-circle", size=16, color="#059669"),
                        rx.text("Control de usuarios", size="2", color="#1e293b"),
                        spacing="2",
                        align="center"
                    ),
                    spacing="2",
                    align="start"
                ),
                rx.button(
                    "Acceder como Administrador",
                    on_click=lambda: rx.redirect(Route.ADMIN_LOGIN_NEW.value),
                    size="3",
                    variant="solid",
                    style={
                        "background": "linear-gradient(135deg, #0f766e 0%, #115e59 100%)",
                        "color": "white",
                        "font_weight": "600",
                        "width": "100%",
                        "margin_top": "1.5rem",
                        "_hover": {
                            "background": "linear-gradient(135deg, #115e59 0%, #134e4a 100%)",
                            "transform": "translateY(-2px)",
                            "box_shadow": "0 10px 25px -5px rgba(15, 118, 110, 0.3)"
                        }
                    }
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
                "transition": "all 0.3s ease",
                "_hover": {
                    "transform": "translateY(-5px)",
                    "box_shadow": "0 20px 60px rgba(0, 0, 0, 0.12)"
                },
                "height": "100%"
            }
        )
    
    # Tarjeta para Almacén
    def almacen_card():
        return rx.card(
            rx.vstack(
                rx.icon(
                    "warehouse", 
                    size=48, 
                    color="#2563eb",
                    style={
                        "background": "linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)",
                        "padding": "20px",
                        "border_radius": "50%",
                        "margin_bottom": "20px"
                    }
                ),
                rx.heading("Almacén", size="6", color="#1e293b", font_weight="700"),
                rx.text(
                    "Gestión de entradas y salidas de productos. Control de inventario físico.",
                    size="2", 
                    color="#64748b",
                    text_align="center",
                    line_height="1.5"
                ),
                rx.divider(margin_y="1rem"),
                rx.vstack(
                    rx.hstack(
                        rx.icon("check-circle", size=16, color="#2563eb"),
                        rx.text("Registrar entradas al almacén", size="2", color="#1e293b"),
                        spacing="2",
                        align="center"
                    ),
                    rx.hstack(
                        rx.icon("check-circle", size=16, color="#2563eb"),
                        rx.text("Registrar salidas aprobadas", size="2", color="#1e293b"),
                        spacing="2",
                        align="center"
                    ),
                    rx.hstack(
                        rx.icon("check-circle", size=16, color="#2563eb"),
                        rx.text("Control de inventario", size="2", color="#1e293b"),
                        spacing="2",
                        align="center"
                    ),
                    spacing="2",
                    align="start"
                ),
                rx.button(
                    "Acceder como Almacén",
                    on_click=lambda: rx.redirect(Route.ADMIN_LOGIN.value),
                    size="3",
                    variant="solid",
                    style={
                        "background": "linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)",
                        "color": "white",
                        "font_weight": "600",
                        "width": "100%",
                        "margin_top": "1.5rem",
                        "_hover": {
                            "background": "linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%)",
                            "transform": "translateY(-2px)",
                            "box_shadow": "0 10px 25px -5px rgba(37, 99, 235, 0.3)"
                        }
                    }
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
                "transition": "all 0.3s ease",
                "_hover": {
                    "transform": "translateY(-5px)",
                    "box_shadow": "0 20px 60px rgba(0, 0, 0, 0.12)"
                },
                "height": "100%"
            }
        )
    
    # Tarjeta para Solicitante
    def solicitante_card():
        return rx.card(
            rx.vstack(
                rx.icon(
                    "file-text", 
                    size=48, 
                    color="#7c3aed",
                    style={
                        "background": "linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%)",
                        "padding": "20px",
                        "border_radius": "50%",
                        "margin_bottom": "20px"
                    }
                ),
                rx.heading("Solicitante", size="6", color="#1e293b", font_weight="700"),
                rx.text(
                    "Crear solicitudes de recursos. Seguimiento de solicitudes enviadas.",
                    size="2", 
                    color="#64748b",
                    text_align="center",
                    line_height="1.5"
                ),
                rx.divider(margin_y="1rem"),
                rx.vstack(
                    rx.hstack(
                        rx.icon("check-circle", size=16, color="#7c3aed"),
                        rx.text("Crear nuevas solicitudes", size="2", color="#1e293b"),
                        spacing="2",
                        align="center"
                    ),
                    rx.hstack(
                        rx.icon("check-circle", size=16, color="#7c3aed"),
                        rx.text("Ver estado de solicitudes", size="2", color="#1e293b"),
                        spacing="2",
                        align="center"
                    ),
                    rx.hstack(
                        rx.icon("check-circle", size=16, color="#7c3aed"),
                        rx.text("Historial de solicitudes", size="2", color="#1e293b"),
                        spacing="2",
                        align="center"
                    ),
                    spacing="2",
                    align="start"
                ),
                rx.button(
                    "Acceder como Solicitante",
                    on_click=lambda: rx.redirect(Route.SOLICITANTE_LOGIN.value),
                    size="3",
                    variant="solid",
                    style={
                        "background": "linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)",
                        "color": "white",
                        "font_weight": "600",
                        "width": "100%",
                        "margin_top": "1.5rem",
                        "_hover": {
                            "background": "linear-gradient(135deg, #6d28d9 0%, #5b21b6 100%)",
                            "transform": "translateY(-2px)",
                            "box_shadow": "0 10px 25px -5px rgba(124, 58, 237, 0.3)"
                        }
                    }
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
                "transition": "all 0.3s ease",
                "_hover": {
                    "transform": "translateY(-5px)",
                    "box_shadow": "0 20px 60px rgba(0, 0, 0, 0.12)"
                },
                "height": "100%"
            }
        )
    
    # Contenido principal - VERSIÓN SIMPLIFICADA Y FUNCIONAL
    def main_content():
        return rx.box(
            # Navbar
            navbar("Selección de Usuario"),
            
            # Contenido principal
            rx.vstack(
                # Encabezado
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.heading(
                                "👋 Bienvenido al Sistema",
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
                                "Seleccione su tipo de usuario para continuar",
                                size="5",
                                color="#64748b",
                                text_align="center",
                                margin_bottom="0.5rem"
                            ),
                            rx.text(
                                "El sistema de gestión de almacén le permite solicitar, aprobar y gestionar recursos de manera eficiente",
                                size="3",
                                color="#94a3b8",
                                text_align="center",
                                max_width="600px"
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
                
                # Tarjetas de selección - USANDO DISEÑO RESPONSIVE SIMPLE
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.heading(
                                "📋 Seleccione su Rol",
                                size="6",
                                color="#1e293b",
                                text_align="center",
                                margin_bottom="3rem"
                            ),
                            # Para móviles: una columna
                            rx.box(
                                rx.vstack(
                                    admin_card(),
                                    almacen_card(),
                                    solicitante_card(),
                                    spacing="6",
                                    width="100%",
                                    max_width="400px"
                                ),
                                display=["block", "block", "none"]
                            ),
                            # Para escritorio: tres columnas
                            rx.box(
                                rx.hstack(
                                    admin_card(),
                                    almacen_card(),
                                    solicitante_card(),
                                    spacing="6",
                                    width="100%",
                                    max_width="1200px",
                                    justify="center",
                                    align="start"
                                ),
                                display=["none", "none", "flex"]
                            ),
                            spacing="4",
                            align="center",
                            width="100%"
                        ),
                        width="100%"
                    ),
                    width="100%",
                    padding="4rem 1rem"
                ),
                
                # Información sobre los roles
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.heading(
                                "ℹ️ Información sobre los Roles",
                                size="5",
                                color="#1e293b",
                                text_align="center",
                                margin_bottom="3rem"
                            ),
                            # Para móviles: una columna
                            rx.box(
                                rx.vstack(
                                    rx.box(
                                        rx.vstack(
                                            rx.hstack(
                                                rx.icon("shield", size=24, color="#0f766e"),
                                                rx.text("Administrador", size="4", font_weight="700", color="#1e293b"),
                                                spacing="3",
                                                align="center"
                                            ),
                                            rx.text(
                                                "Responsable de revisar y autorizar las solicitudes de recursos. Tiene acceso completo al sistema para ver el historial, gestionar usuarios y supervisar todo el flujo.",
                                                size="2",
                                                color="#64748b",
                                                line_height="1.6"
                                            ),
                                            spacing="3",
                                            align="start"
                                        ),
                                        padding="2rem",
                                        border_radius="12px",
                                        background="white",
                                        border="1px solid #e2e8f0",
                                        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                                        width="100%"
                                    ),
                                    rx.box(
                                        rx.vstack(
                                            rx.hstack(
                                                rx.icon("warehouse", size=24, color="#2563eb"),
                                                rx.text("Almacén", size="4", font_weight="700", color="#1e293b"),
                                                spacing="3",
                                                align="center"
                                            ),
                                            rx.text(
                                                "Encargado del control físico del inventario. Registra las entradas de nuevos productos y procesa las salidas de recursos previamente aprobadas por el administrador.",
                                                size="2",
                                                color="#64748b",
                                                line_height="1.6"
                                            ),
                                            spacing="3",
                                            align="start"
                                        ),
                                        padding="2rem",
                                        border_radius="12px",
                                        background="white",
                                        border="1px solid #e2e8f0",
                                        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                                        width="100%"
                                    ),
                                    rx.box(
                                        rx.vstack(
                                            rx.hstack(
                                                rx.icon("file-text", size=24, color="#7c3aed"),
                                                rx.text("Solicitante", size="4", font_weight="700", color="#1e293b"),
                                                spacing="3",
                                                align="center"
                                            ),
                                            rx.text(
                                                "Usuarios que necesitan recursos para sus actividades. Crean solicitudes especificando producto, cantidad, destino y observaciones, y pueden hacer seguimiento a su estado.",
                                                size="2",
                                                color="#64748b",
                                                line_height="1.6"
                                            ),
                                            spacing="3",
                                            align="start"
                                        ),
                                        padding="2rem",
                                        border_radius="12px",
                                        background="white",
                                        border="1px solid #e2e8f0",
                                        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                                        width="100%"
                                    ),
                                    spacing="4",
                                    width="100%",
                                    max_width="400px"
                                ),
                                display=["block", "block", "none"]
                            ),
                            # Para escritorio: tres columnas
                            rx.box(
                                rx.hstack(
                                    rx.box(
                                        rx.vstack(
                                            rx.hstack(
                                                rx.icon("shield", size=24, color="#0f766e"),
                                                rx.text("Administrador", size="4", font_weight="700", color="#1e293b"),
                                                spacing="3",
                                                align="center"
                                            ),
                                            rx.text(
                                                "Responsable de revisar y autorizar las solicitudes de recursos. Tiene acceso completo al sistema para ver el historial, gestionar usuarios y supervisar todo el flujo.",
                                                size="2",
                                                color="#64748b",
                                                line_height="1.6"
                                            ),
                                            spacing="3",
                                            align="start"
                                        ),
                                        padding="2rem",
                                        border_radius="12px",
                                        background="white",
                                        border="1px solid #e2e8f0",
                                        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                                        width="32%",
                                        min_height="200px"
                                    ),
                                    rx.box(
                                        rx.vstack(
                                            rx.hstack(
                                                rx.icon("warehouse", size=24, color="#2563eb"),
                                                rx.text("Almacén", size="4", font_weight="700", color="#1e293b"),
                                                spacing="3",
                                                align="center"
                                            ),
                                            rx.text(
                                                "Encargado del control físico del inventario. Registra las entradas de nuevos productos y procesa las salidas de recursos previamente aprobadas por el administrador.",
                                                size="2",
                                                color="#64748b",
                                                line_height="1.6"
                                            ),
                                            spacing="3",
                                            align="start"
                                        ),
                                        padding="2rem",
                                        border_radius="12px",
                                        background="white",
                                        border="1px solid #e2e8f0",
                                        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                                        width="32%",
                                        min_height="200px"
                                    ),
                                    rx.box(
                                        rx.vstack(
                                            rx.hstack(
                                                rx.icon("file-text", size=24, color="#7c3aed"),
                                                rx.text("Solicitante", size="4", font_weight="700", color="#1e293b"),
                                                spacing="3",
                                                align="center"
                                            ),
                                            rx.text(
                                                "Usuarios que necesitan recursos para sus actividades. Crean solicitudes especificando producto, cantidad, destino y observaciones, y pueden hacer seguimiento a su estado.",
                                                size="2",
                                                color="#64748b",
                                                line_height="1.6"
                                            ),
                                            spacing="3",
                                            align="start"
                                        ),
                                        padding="2rem",
                                        border_radius="12px",
                                        background="white",
                                        border="1px solid #e2e8f0",
                                        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                                        width="32%",
                                        min_height="200px"
                                    ),
                                    spacing="4",
                                    width="100%",
                                    max_width="1200px",
                                    justify="center"
                                ),
                                display=["none", "none", "flex"]
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
                
                # Flujo del sistema
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.heading(
                                "🔄 Flujo del Sistema",
                                size="5",
                                color="#1e293b",
                                text_align="center",
                                margin_bottom="3rem"
                            ),
                            # Para móviles: vertical
                            rx.box(
                                rx.vstack(
                                    rx.vstack(
                                        rx.icon("file-text", size=32, color="#7c3aed"),
                                        rx.text("1. Solicitud", size="3", font_weight="600", color="#1e293b"),
                                        rx.text("El solicitante crea una solicitud", size="2", color="#64748b", text_align="center"),
                                        align="center",
                                        spacing="2"
                                    ),
                                    rx.icon("arrow-down", size=24, color="#94a3b8", margin_y="1rem"),
                                    rx.vstack(
                                        rx.icon("shield", size=32, color="#0f766e"),
                                        rx.text("2. Aprobación", size="3", font_weight="600", color="#1e293b"),
                                        rx.text("El administrador aprueba/rechaza", size="2", color="#64748b", text_align="center"),
                                        align="center",
                                        spacing="2"
                                    ),
                                    rx.icon("arrow-down", size=24, color="#94a3b8", margin_y="1rem"),
                                    rx.vstack(
                                        rx.icon("warehouse", size=32, color="#2563eb"),
                                        rx.text("3. Ejecución", size="3", font_weight="600", color="#1e293b"),
                                        rx.text("El almacén procesa la salida", size="2", color="#64748b", text_align="center"),
                                        align="center",
                                        spacing="2"
                                    ),
                                    spacing="2",
                                    align="center",
                                    width="100%",
                                    max_width="300px"
                                ),
                                display=["block", "block", "none"]
                            ),
                            # Para escritorio: horizontal
                            rx.box(
                                rx.hstack(
                                    rx.vstack(
                                        rx.icon("file-text", size=32, color="#7c3aed"),
                                        rx.text("1. Solicitud", size="3", font_weight="600", color="#1e293b"),
                                        rx.text("El solicitante crea una solicitud", size="2", color="#64748b", text_align="center"),
                                        align="center",
                                        spacing="2"
                                    ),
                                    rx.icon("arrow-right", size=24, color="#94a3b8", margin_x="2rem"),
                                    rx.vstack(
                                        rx.icon("shield", size=32, color="#0f766e"),
                                        rx.text("2. Aprobación", size="3", font_weight="600", color="#1e293b"),
                                        rx.text("El administrador aprueba/rechaza", size="2", color="#64748b", text_align="center"),
                                        align="center",
                                        spacing="2"
                                    ),
                                    rx.icon("arrow-right", size=24, color="#94a3b8", margin_x="2rem"),
                                    rx.vstack(
                                        rx.icon("warehouse", size=32, color="#2563eb"),
                                        rx.text("3. Ejecución", size="3", font_weight="600", color="#1e293b"),
                                        rx.text("El almacén procesa la salida", size="2", color="#64748b", text_align="center"),
                                        align="center",
                                        spacing="2"
                                    ),
                                    spacing="2",
                                    align="center",
                                    justify="center",
                                    width="100%",
                                    max_width="800px"
                                ),
                                display=["none", "none", "flex"]
                            ),
                            spacing="4",
                            align="center",
                            width="100%"
                        ),
                        width="100%"
                    ),
                    width="100%",
                    padding="4rem 1rem",
                    background="white"
                ),
                
                # Pie de página
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.text(
                                "🏢 Sistema de Gestión de Almacén",
                                size="3",
                                font_weight="600",
                                color="#1e293b"
                            ),
                            rx.text(
                                "© 2024 - Todos los derechos reservados",
                                size="2",
                                color="#64748b"
                            ),
                            rx.hstack(
                                rx.text("Versión 1.0", size="1", color="#94a3b8"),
                                rx.text("•", size="1", color="#94a3b8"),
                                rx.text("Acceso Seguro", size="1", color="#94a3b8"),
                                rx.text("•", size="1", color="#94a3b8"),
                                rx.text("Soporte Técnico: soporte@empresa.com", size="1", color="#94a3b8"),
                                spacing="2",
                                wrap="wrap",
                                justify="center"
                            ),
                            spacing="2",
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