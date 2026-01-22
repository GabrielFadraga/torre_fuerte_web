import reflex as rx
from TFuerte.state.solicitante_auth_state import SolicitanteAuthState
from TFuerte.state.solicitante_dashboard_state import SolicitanteDashboardState
from TFuerte.components.navbar import navbar
from TFuerte.routes import Route

@rx.page(
    route=Route.SOLICITANTE_DASHBOARD.value,
    title="Dashboard - Solicitante",
    on_load=SolicitanteDashboardState.on_load
)
def solicitante_dashboard() -> rx.Component:
    """Dashboard para solicitantes"""
    
    def estado_badge(estado_var):
        return rx.cond(
            estado_var == "pendiente",
            rx.badge("PENDIENTE", color_scheme="amber", variant="soft"),
            rx.cond(
                estado_var == "aprobada",
                rx.badge("APROBADA", color_scheme="green", variant="soft"),
                rx.cond(
                    estado_var == "completada",
                    rx.badge("COMPLETADA", color_scheme="blue", variant="soft"),
                    rx.badge("RECHAZADA", color_scheme="red", variant="soft")
                )
            )
        )
    
    def mis_solicitudes_table():
        """Tabla de solicitudes"""
        
        def row_component(solicitud):
            # Mostrar la fecha completa
            return rx.table.row(
                rx.table.cell(rx.text(solicitud["id"]), color="#1F1F1F"),
                rx.table.cell(rx.text(solicitud["Descripcion"]), color="#1F1F1F"),
                rx.table.cell(rx.text(solicitud["Cantidad"]), color="#1F1F1F"),
                rx.table.cell(rx.text(solicitud["Destino"]), color="#1F1F1F"),
                rx.table.cell(estado_badge(solicitud["estado"]), color="#1F1F1F"),
                rx.table.cell(rx.text(solicitud.get("fecha_solicitud", "-")), color="#1F1F1F"),
            )
        
        return rx.cond(
            SolicitanteDashboardState.mis_solicitudes.length() == 0,
            rx.center(
                rx.vstack(
                    rx.icon("file_text", size=32, color="#cbd5e1"),
                    rx.text("No tienes solicitudes realizadas", size="3", color="#64748b"),
                    spacing="2",
                ),
                padding="3rem",
            ),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("ID", color="#1F1F1F"),
                        rx.table.column_header_cell("Descripción", color="#1F1F1F"),
                        rx.table.column_header_cell("Cantidad", color="#1F1F1F"),
                        rx.table.column_header_cell("Destino", color="#1F1F1F"),
                        rx.table.column_header_cell("Estado", color="#1F1F1F"),
                        rx.table.column_header_cell("Fecha", color="#1F1F1F"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        SolicitanteDashboardState.mis_solicitudes,
                        row_component
                    )
                ),
                variant="surface",
                size="3"
            )
        )
    
    def nueva_solicitud_form():
        return rx.card(
            rx.vstack(
                rx.heading("Nueva Solicitud de Material", size="5", color="#1F1F1F"),
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Descripción del producto *",
                            name="descripcion",
                            required=True,
                            value=SolicitanteDashboardState.descripcion,
                            on_change=SolicitanteDashboardState.set_descripcion,
                        ),
                        rx.input(
                            placeholder="Cantidad *",
                            type="number",
                            name="cantidad",
                            required=True,
                            min="1",
                            value=SolicitanteDashboardState.cantidad,
                            on_change=SolicitanteDashboardState.set_cantidad,
                        ),
                        rx.text_area(
                            placeholder="Observaciones (opcional)",
                            name="observacion",
                            value=SolicitanteDashboardState.observacion,
                            on_change=SolicitanteDashboardState.set_observacion,
                        ),
                        rx.input(
                            placeholder="Destino *",
                            name="destino",
                            required=True,
                            value=SolicitanteDashboardState.destino,
                            on_change=SolicitanteDashboardState.set_destino,
                        ),
                        rx.button(
                            "📤 Enviar Solicitud",
                            type="submit",
                            variant="solid",
                            width="100%",
                        ),
                        spacing="3",
                    ),
                    on_submit=SolicitanteDashboardState.crear_solicitud,
                    reset_on_submit=True
                ),
                spacing="3",
            ),
            width="100%"
        )
    
    def dashboard_content():
        return rx.box(
            navbar("Panel de Solicitante"),
            rx.vstack(
                rx.box(
                    rx.hstack(
                        rx.vstack(
                            rx.heading("👤 Panel de Solicitante", size="7", color="#1F1F1F"),
                            rx.text(
                                rx.cond(
                                    SolicitanteAuthState.is_authenticated,
                                    f"Usuario: {SolicitanteAuthState.current_solicitante['usuario']}",
                                    "Usuario: No disponible"
                                ),
                                size="4",
                                color="#64748b"
                            ),
                            align="start",
                            spacing="1"
                        ),
                        rx.spacer(),
                        rx.button("🚪 Cerrar Sesión", on_click=SolicitanteAuthState.sign_out, color_scheme="red"),
                        width="100%",
                        align="center",
                        spacing="3"
                    ),
                    width="100%",
                    padding_bottom="1.5rem",
                    border_bottom="1px solid #e2e8f0"
                ),
                
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger("📋 Mis Solicitudes", value="solicitudes", color="#1F1F1F"),
                        rx.tabs.trigger("➕ Nueva Solicitud", value="nueva", color="#1F1F1F"),
                    ),
                    
                    rx.tabs.content(
                        rx.vstack(
                            rx.hstack(
                                rx.button(
                                    "🔄 Actualizar",
                                    on_click=SolicitanteDashboardState.load_mis_solicitudes,
                                    loading=SolicitanteDashboardState.loading,
                                    variant="soft",
                                ),
                                rx.badge(
                                    f"Total: {SolicitanteDashboardState.computed_total_solicitudes}",
                                    color_scheme="blue",
                                    variant="soft",
                                ),
                                spacing="3",
                                width="100%",
                            ),
                            
                            rx.cond(
                                SolicitanteDashboardState.loading,
                                rx.center(rx.spinner(size="3"), padding="3rem"),
                                mis_solicitudes_table()
                            ),
                            
                            spacing="4",
                            width="100%",
                        ),
                        value="solicitudes",
                        style={"padding": "1.5rem 0"}
                    ),
                    
                    rx.tabs.content(
                        rx.vstack(
                            nueva_solicitud_form(),
                            spacing="4",
                            width="100%",
                        ),
                        value="nueva",
                        style={"padding": "1.5rem 0"}
                    ),
                    
                    default_value="solicitudes",
                    width="100%",
                ),
                
                spacing="4",
                padding="2rem",
                max_width="1200px",
                margin="0 auto",
                align="start",
            ),
            width="100%",
            min_height="100vh",
            background="linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
        )
    
    return rx.cond(
        SolicitanteAuthState.is_authenticated,
        dashboard_content(),
        rx.center(
            rx.vstack(
                rx.spinner(size="3"),
                rx.text("Redirigiendo al login...", margin_top="1rem"),
                rx.button("Ir al Login", on_click=lambda: rx.redirect(Route.SOLICITANTE_LOGIN.value)),
                spacing="3",
                align="center",
                max_width="400px",
                padding="2rem",
            ),
            height="100vh",
            width="100%",
        )
    )