import reflex as rx
from TFuerte.components.navbar import navbar
from TFuerte.routes import Route
from TFuerte.state.admin_tf_state import AdminTFState

# =============================================================================
# TARJETAS ORIGINALES PARA GESTIÓN DE ALMACÉN (SIN MODIFICACIONES DE ESTILO)
# =============================================================================
def admin_card():
    return rx.card(
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
                    rx.icon("chevron_right", size=16, color="#059669"),
                    rx.text("Aprobar/Rechazar solicitudes", size="2", color="#1e293b"),
                    spacing="2",
                    align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#059669"),
                    rx.text("Ver historial completo", size="2", color="#1e293b"),
                    spacing="2",
                    align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#059669"),
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

def almacen_card():
    return rx.card(
        rx.vstack(
            rx.icon(
                "warehouse", 
                size=70, 
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
                    rx.icon("chevron_right", size=16, color="#2563eb"),
                    rx.text("Registrar entradas al almacén", size="2", color="#1e293b"),
                    spacing="2",
                    align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#2563eb"),
                    rx.text("Registrar salidas aprobadas", size="2", color="#1e293b"),
                    spacing="2",
                    align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#2563eb"),
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

def solicitante_card():
    return rx.card(
        rx.vstack(
            rx.icon(
                "file-text", 
                size=70, 
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
                    rx.icon("chevron_right", size=16, color="#7c3aed"),
                    rx.text("Crear nuevas solicitudes", size="2", color="#1e293b"),
                    spacing="2",
                    align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#7c3aed"),
                    rx.text("Ver estado de solicitudes", size="2", color="#1e293b"),
                    spacing="2",
                    align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#7c3aed"),
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

# =============================================================================
# NUEVAS TARJETAS PARA SOLICITUD DE RECURSOS Y FINANCIAMIENTO
# =============================================================================

def admin_rm_card():
    return rx.card(
        rx.vstack(
            rx.icon(
                "crown", 
                size=70, 
                color="#7c3aed",
                style={
                    "background": "linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%)",
                    "padding": "20px",
                    "border_radius": "50%",
                    "margin_bottom": "20px"
                }
            ),
            rx.heading("Administrador RM", size="6", color="#1e293b", font_weight="700"),
            rx.text(
                "Aprobación de solicitudes de recursos y financiamiento. Gestión completa.",
                size="2", 
                color="#64748b",
                text_align="center",
                line_height="1.5"
            ),
            rx.divider(margin_y="1rem"),
            rx.vstack(
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#7c3aed"),
                    rx.text("Aprobar/Rechazar RM", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#7c3aed"),
                    rx.text("Aprobar/Rechazar FIN", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#7c3aed"),
                    rx.text("Generar documentos Word", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                spacing="2", align="start"
            ),
            rx.button(
                "Acceder como Administrador RM",
                on_click=lambda: rx.redirect(Route.ADMIN_RM_LOGIN.value),
                size="3", variant="solid",
                style={
                    "background": "linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)",
                    "color": "white", "font_weight": "600", "width": "100%",
                    "margin_top": "1.5rem",
                    "_hover": {
                        "background": "linear-gradient(135deg, #6d28d9 0%, #5b21b6 100%)",
                        "transform": "translateY(-2px)",
                        "box_shadow": "0 10px 25px -5px rgba(124, 58, 237, 0.3)"
                    }
                }
            ),
            spacing="4", align="center", width="100%"
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
            "height": "100%",
            "width": "100%"
        }
    )

def tecnica_card():
    return rx.card(
        rx.vstack(
            rx.icon(
                "wrench", 
                size=70, 
                color="#059669",
                style={
                    "background": "linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)",
                    "padding": "20px",
                    "border_radius": "50%",
                    "margin_bottom": "20px"
                }
            ),
            rx.heading("Área Técnica", size="6", color="#1e293b", font_weight="700"),
            rx.text(
                "Revisión y aprobación técnica de solicitudes de recursos.",
                size="2", 
                color="#64748b",
                text_align="center",
                line_height="1.5"
            ),
            rx.divider(margin_y="1rem"),
            rx.vstack(
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#059669"),
                    rx.text("Revisar solicitudes", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#059669"),
                    rx.text("Aprobar técnicamente", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#059669"),
                    rx.text("Rechazar solicitudes", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                spacing="2", align="start"
            ),
            rx.button(
                "Acceder como Área Técnica",
                on_click=lambda: rx.redirect(Route.TECNICA_LOGIN.value),
                size="3", variant="solid",
                style={
                    "background": "linear-gradient(135deg, #059669 0%, #047857 100%)",
                    "color": "white", "font_weight": "600", "width": "100%",
                    "margin_top": "1.5rem",
                    "_hover": {
                        "background": "linear-gradient(135deg, #047857 0%, #065f46 100%)",
                        "transform": "translateY(-2px)",
                        "box_shadow": "0 10px 25px -5px rgba(5, 150, 105, 0.3)"
                    }
                }
            ),
            spacing="4", align="center", width="100%"
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
            "height": "100%",
            "width": "100%"
        }
    )

def logistica_card():
    return rx.card(
        rx.vstack(
            rx.icon(
                "truck", 
                size=70, 
                color="#2563eb",
                style={
                    "background": "linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)",
                    "padding": "20px",
                    "border_radius": "50%",
                    "margin_bottom": "20px"
                }
            ),
            rx.heading("Logística", size="6", color="#1e293b", font_weight="700"),
            rx.text(
                "Aprobación final y generación de documentos. Gestión de precios.",
                size="2", 
                color="#64748b",
                text_align="center",
                line_height="1.5"
            ),
            rx.divider(margin_y="1rem"),
            rx.vstack(
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#2563eb"),
                    rx.text("Aprobar solicitudes finales", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#2563eb"),
                    rx.text("Generar documentos Word", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#2563eb"),
                    rx.text("Gestionar precios", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                spacing="2", align="start"
            ),
            rx.button(
                "Acceder como Logística",
                on_click=lambda: rx.redirect(Route.LOGISTICA_LOGIN.value),
                size="3", variant="solid",
                style={
                    "background": "linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)",
                    "color": "white", "font_weight": "600", "width": "100%",
                    "margin_top": "1.5rem",
                    "_hover": {
                        "background": "linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%)",
                        "transform": "translateY(-2px)",
                        "box_shadow": "0 10px 25px -5px rgba(37, 99, 235, 0.3)"
                    }
                }
            ),
            spacing="4", align="center", width="100%"
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
            "height": "100%",
            "width": "100%"
        }
    )

def revfin_card():
    return rx.card(
        rx.vstack(
            rx.icon(
                "dollar-sign", 
                size=70, 
                color="#0d9488",
                style={
                    "background": "linear-gradient(135deg, #f0fdfa 0%, #ccfbf1 100%)",
                    "padding": "20px",
                    "border_radius": "50%",
                    "margin_bottom": "20px"
                }
            ),
            rx.heading("Revisor Financiero", size="6", color="#1e293b", font_weight="700"),
            rx.text(
                "Revisión y aprobación de solicitudes de financiamiento.",
                size="2", 
                color="#64748b",
                text_align="center",
                line_height="1.5"
            ),
            rx.divider(margin_y="1rem"),
            rx.vstack(
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#0d9488"),
                    rx.text("Revisar solicitudes FIN", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#0d9488"),
                    rx.text("Aprobar/Rechazar FIN", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#0d9488"),
                    rx.text("Control presupuestario", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                spacing="2", align="start"
            ),
            rx.button(
                "Acceder como Revisor Financiero",
                on_click=lambda: rx.redirect(Route.REVFIN_LOGIN.value),
                size="3", variant="solid",
                style={
                    "background": "linear-gradient(135deg, #0d9488 0%, #0f766e 100%)",
                    "color": "white", "font_weight": "600", "width": "100%",
                    "margin_top": "1.5rem",
                    "_hover": {
                        "background": "linear-gradient(135deg, #0f766e 0%, #115e59 100%)",
                        "transform": "translateY(-2px)",
                        "box_shadow": "0 10px 25px -5px rgba(13, 148, 136, 0.3)"
                    }
                }
            ),
            spacing="4", align="center", width="100%"
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
            "height": "100%",
            "width": "100%"
        }
    )

def solicitante_rm_card():
    return rx.card(
        rx.vstack(
            rx.icon(
                "clipboard-list", 
                size=70, 
                color="#f59e0b",
                style={
                    "background": "linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)",
                    "padding": "20px",
                    "border_radius": "50%",
                    "margin_bottom": "20px"
                }
            ),
            rx.heading("Solicitante RM", size="6", color="#1e293b", font_weight="700"),
            rx.text(
                "Crear solicitudes de recursos y financiamiento para obras.",
                size="2", 
                color="#64748b",
                text_align="center",
                line_height="1.5"
            ),
            rx.divider(margin_y="1rem"),
            rx.vstack(
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#f59e0b"),
                    rx.text("Crear solicitudes RM", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#f59e0b"),
                    rx.text("Crear solicitudes FIN", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#f59e0b"),
                    rx.text("Ver historial", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                spacing="2", align="start"
            ),
            rx.button(
                "Acceder como Solicitante RM",
                on_click=lambda: rx.redirect(Route.SOLICITANTERM_LOGIN.value),
                size="3", variant="solid",
                style={
                    "background": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
                    "color": "white", "font_weight": "600", "width": "100%",
                    "margin_top": "1.5rem",
                    "_hover": {
                        "background": "linear-gradient(135deg, #d97706 0%, #b45309 100%)",
                        "transform": "translateY(-2px)",
                        "box_shadow": "0 10px 25px -5px rgba(245, 158, 11, 0.3)"
                    }
                }
            ),
            spacing="4", align="center", width="100%"
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
            "height": "100%",
            "width": "100%"
        }
    )

# =============================================================================
# TARJETAS PARA GESTIÓN COMERCIAL
# =============================================================================
def comercial_card():
    return rx.card(
        rx.vstack(
            rx.icon(
                "shopping-cart", 
                size=70, 
                color="#f97316",
                style={
                    "background": "linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%)",
                    "padding": "20px",
                    "border_radius": "50%",
                    "margin_bottom": "20px"
                }
            ),
            rx.heading("Gestión Comercial", size="6", color="#1e293b", font_weight="700"),
            rx.text(
                "Administración de clientes, proveedores y contratos comerciales.",
                size="2", 
                color="#64748b",
                text_align="center",
                line_height="1.5"
            ),
            rx.divider(margin_y="1rem"),
            rx.vstack(
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#f97316"),
                    rx.text("Gestión de clientes", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#f97316"),
                    rx.text("Gestión de proveedores", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#f97316"),
                    rx.text("Contratos con clientes", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#f97316"),
                    rx.text("Contratos con proveedores", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                spacing="2", align="start"
            ),
            rx.button(
                "Acceder como Gestión Comercial",
                on_click=lambda: rx.redirect(Route.COMMERCIAL_LOGIN.value),
                size="3", variant="solid",
                style={
                    "background": "linear-gradient(135deg, #f97316 0%, #ea580c 100%)",
                    "color": "white", "font_weight": "600", "width": "100%",
                    "margin_top": "1.5rem",
                    "_hover": {
                        "background": "linear-gradient(135deg, #ea580c 0%, #c2410c 100%)",
                        "transform": "translateY(-2px)",
                        "box_shadow": "0 10px 25px -5px rgba(249, 115, 22, 0.3)"
                    }
                }
            ),
            spacing="4", align="center", width="100%"
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
            "height": "100%",
            "width": "100%"
        }
    )

def comercial_admin_card():
    return rx.card(
        rx.vstack(
            rx.icon(
                "eye", 
                size=70, 
                color="#4f46e5",
                style={
                    "background": "linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%)",
                    "padding": "20px",
                    "border_radius": "50%",
                    "margin_bottom": "20px"
                }
            ),
            rx.heading("Administración Comercial", size="6", color="#1e293b", font_weight="700"),
            rx.text(
                "Panel de solo lectura para supervisión completa del área comercial.",
                size="2", 
                color="#64748b",
                text_align="center",
                line_height="1.5"
            ),
            rx.divider(margin_y="1rem"),
            rx.vstack(
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#4f46e5"),
                    rx.text("Visualización de todos los registros", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#4f46e5"),
                    rx.text("Filtros y ordenamiento", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#4f46e5"),
                    rx.text("Descarga de datos en CSV", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                rx.hstack(
                    rx.icon("chevron_right", size=16, color="#4f46e5"),
                    rx.text("Acceso exclusivo para administradores", size="2", color="#1e293b"),
                    spacing="2", align="center"
                ),
                spacing="2", align="start"
            ),
            rx.button(
                "Acceder como Administrador Comercial",
                on_click=lambda: rx.redirect(Route.COMMERCIAL_ADMIN_LOGIN.value),
                size="3", variant="solid",
                style={
                    "background": "linear-gradient(135deg, #4f46e5 0%, #4338ca 100%)",
                    "color": "white", "font_weight": "600", "width": "100%",
                    "margin_top": "1.5rem",
                    "_hover": {
                        "background": "linear-gradient(135deg, #4338ca 0%, #3730a3 100%)",
                        "transform": "translateY(-2px)",
                        "box_shadow": "0 10px 25px -5px rgba(79, 70, 229, 0.3)"
                    }
                }
            ),
            spacing="4", align="center", width="100%"
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
            "height": "100%",
            "width": "100%"
        }
    )

# =============================================================================
# PÁGINA PRINCIPAL
# =============================================================================

@rx.page(
    route=Route.ADMIN_PAGE.value,
    title="Sistema de Gestión de Almacén - Selección de Usuario",
    description="Seleccione su tipo de usuario para acceder al sistema",
    on_load=AdminTFState.load_data if hasattr(AdminTFState, 'load_data') else None
)
def user_selection() -> rx.Component:
    """Página de selección de tipo de usuario - PROTEGIDA"""
    
    def not_authenticated():
        return rx.box(
            navbar("Acceso Restringido"),
            rx.center(
                rx.vstack(
                    rx.icon("lock", size=48, color="#dc2626"),
                    rx.heading("Acceso No Autorizado", size="6", color="#1e293b"),
                    rx.text(
                        "Debe iniciar sesión para acceder a esta página",
                        size="3", 
                        color="#64748b",
                        text_align="center"
                    ),
                    rx.button(
                        "Ir al Login",
                        on_click=lambda: rx.redirect(Route.ADMIN_LOGIN_PANEL.value),
                        size="3",
                        variant="solid",
                        style={
                            "background": "linear-gradient(135deg, #0f766e 0%, #115e59 100%)",
                            "color": "white",
                            "font_weight": "600",
                            "margin_top": "1.5rem",
                            "_hover": {
                                "background": "linear-gradient(135deg, #115e59 0%, #134e4a 100%)"
                            }
                        }
                    ),
                    spacing="4",
                    align="center",
                    max_width="400px",
                    padding="2rem",
                    background="white",
                    border_radius="12px",
                    box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)"
                ),
                height="70vh",
                width="100%"
            ),
            width="100%",
            min_height="100vh",
            style={
                "background": "linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)"
            }
        )
    
    def main_content_authenticated():
        return rx.box(
            navbar("Selección de Usuario"),
            
            # Contenido principal
            rx.vstack(
                # Encabezado con información de usuario
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.heading(
                                f"👋 Bienvenido, {AdminTFState.admin_name}",
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
                            rx.hstack(
                                rx.badge(
                                    f"ID: {AdminTFState.admin_id}",
                                    color_scheme="teal",
                                    variant="soft"
                                ),
                                rx.badge(
                                    "Sesión Activa",
                                    color_scheme="green",
                                    variant="soft"
                                ),
                                spacing="2",
                                justify="center"
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
                
                # ========== SECCIÓN 1: GESTIÓN DE ALMACÉN ==========
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.heading(
                                "📋 Gestión de Almacén",
                                size="6",
                                color="#1e293b",
                                text_align="center",
                                margin_bottom="2rem"
                            ),
                            # Móvil
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
                            # Escritorio
                            rx.box(
                                rx.hstack(
                                    admin_card(),
                                    almacen_card(),
                                    solicitante_card(),
                                    spacing="6",
                                    width="100%",
                                    max_width="1200px",
                                    justify="center",
                                    align="stretch",
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
                    padding="2rem 1rem"
                ),
                
                # ========== SECCIÓN 2: SOLICITUD DE RECURSOS Y FINANCIAMIENTO ==========
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.heading(
                                "📋 Solicitud de Recursos y Financiamiento",
                                size="6",
                                color="#1e293b",
                                text_align="center",
                                margin_bottom="2rem"
                            ),
                            # Móvil
                            rx.box(
                                rx.vstack(
                                    admin_rm_card(),
                                    tecnica_card(),
                                    logistica_card(),
                                    revfin_card(),
                                    solicitante_rm_card(),
                                    spacing="6",
                                    width="100%",
                                    max_width="400px"
                                ),
                                display=["block", "block", "none"]
                            ),
                            # Escritorio: dos filas con anchos iguales
                            rx.box(
                                rx.vstack(
                                    # Primera fila: 3 tarjetas
                                    rx.hstack(
                                        admin_rm_card(),
                                        tecnica_card(),
                                        logistica_card(),
                                        spacing="6",
                                        width="100%",
                                        max_width="1200px",
                                        justify="center",
                                        align="stretch",
                                    ),
                                    # Segunda fila: 2 tarjetas centradas
                                    rx.hstack(
                                        revfin_card(),
                                        solicitante_rm_card(),
                                        spacing="6",
                                        width="100%",
                                        max_width="1200px",
                                        justify="center",
                                        align="stretch",
                                    ),
                                    spacing="6",
                                    width="100%"
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
                    padding="2rem 1rem",
                    border_top="1px solid #e2e8f0",
                    margin_top="2rem"
                ),

                # ========== SECCIÓN 3: GESTIÓN COMERCIAL (DOS TARJETAS) ==========
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.heading(
                                "🏢 Gestión Comercial",
                                size="6",
                                color="#1e293b",
                                text_align="center",
                                margin_bottom="2rem"
                            ),
                            # Móvil
                            rx.box(
                                rx.vstack(
                                    comercial_card(),
                                    comercial_admin_card(),
                                    spacing="6",
                                    width="100%",
                                    max_width="400px"
                                ),
                                display=["block", "block", "none"]
                            ),
                            # Escritorio: dos tarjetas en fila
                            rx.box(
                                rx.hstack(
                                    comercial_card(),
                                    comercial_admin_card(),
                                    spacing="6",
                                    width="100%",
                                    max_width="1200px",
                                    justify="center",
                                    align="stretch",
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
                    padding="2rem 1rem",
                    border_top="1px solid #e2e8f0",
                    margin_top="2rem"
                ),
                
                # Información adicional y cierre de sesión
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.heading(
                                "ℹ️ Información del Sistema",
                                size="5",
                                color="#1e293b",
                                text_align="center",
                                margin_bottom="2rem"
                            ),
                            rx.text(
                                "Usted ha iniciado sesión como administrador del sistema. "
                                "Desde aquí puede acceder a los diferentes módulos según su necesidad.",
                                size="2",
                                color="#64748b",
                                text_align="center",
                                max_width="600px",
                                line_height="1.6"
                            ),
                            rx.button(
                                "Cerrar Sesión",
                                on_click=AdminTFState.sign_out,
                                size="2",
                                variant="soft",
                                color_scheme="red",
                                margin_top="1.5rem"
                            ),
                            spacing="3",
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
                                "🏢 Sistema de Gestión de Almacén",
                                size="3",
                                font_weight="600",
                                color="#1e293b"
                            ),
                            rx.text(
                                f"© 2026 - Sesión activa para: {AdminTFState.admin_name}",
                                size="2",
                                color="#64748b"
                            ),
                            rx.hstack(
                                rx.text("Versión 1.0", size="1", color="#94a3b8"),
                                rx.text("•", size="1", color="#94a3b8"),
                                rx.text("Acceso Seguro", size="1", color="#94a3b8"),
                                rx.text("•", size="1", color="#94a3b8"),
                                rx.text(f"ID: {AdminTFState.admin_id}", size="1", color="#94a3b8"),
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
    
    return rx.cond(
        AdminTFState.is_authenticated,
        main_content_authenticated(),
        not_authenticated()
    )