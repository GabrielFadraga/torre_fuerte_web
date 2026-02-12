# TFuerte/pages/tecnica_dashboard.py
import reflex as rx
from TFuerte.state.tecnica_state import TecnicaState
from TFuerte.components.navbar import navbar
from TFuerte.routes import Route

@rx.page(
    route=Route.TECNICA_DASHBOARD.value,
    title="Dashboard - Área Técnica",
    on_load=TecnicaState.load_data
)
def tecnica_dashboard() -> rx.Component:
    """Dashboard para Jefe de Área Técnica (Alexander)"""
    
    def estado_badge_rm(estado: str):
        return rx.cond(
            estado == "pendiente",
            rx.badge("PENDIENTE", color_scheme="amber", variant="soft"),
            rx.cond(
                estado == "aprobado_tecnica",
                rx.badge("APROBADO TÉCNICA", color_scheme="green", variant="soft"),
                rx.badge("RECHAZADA", color_scheme="red", variant="soft")
            )
        )
    
    def solicitudes_table() -> rx.Component:
        """Tabla de solicitudes RM pendientes"""
        
        def solicitud_row(solicitud):
            return rx.table.row(
                rx.table.cell(
                    rx.text(solicitud["id"], font_weight="600", color="#070E0C"),
                    style={"padding": "8px 4px"}
                ),
                rx.table.cell(
                    rx.text(solicitud.get("Centro costo", "-"), color="#070E0C"),
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                rx.table.cell(
                    rx.text(solicitud.get("Fecha", "-"), color="#070E0C"),
                    style={"padding": "8px 4px", "min_width": "100px"}
                ),
                rx.table.cell(
                    rx.text(solicitud.get("Orden trabajo", "-"), color="#070E0C"),
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                rx.table.cell(
                    rx.text(
                        solicitud.get("Descripcion", "-"),  # ¡Ahora funcionará!
                        color="#070E0C",
                        style={
                            "max_width": "180px",
                            "overflow": "hidden",
                            "text_overflow": "ellipsis",
                            "white_space": "nowrap"
                        }
                    ),
                    style={"padding": "8px 4px", "min_width": "180px"}
                ),
                rx.table.cell(
                    rx.text(solicitud.get("Cantidad", "-"), color="#070E0C"),  # ¡Ahora funcionará!
                    style={"padding": "8px 4px", "min_width": "80px"}
                ),
                rx.table.cell(
                    rx.text(solicitud.get("UM", "-"), color="#070E0C"),  # ¡Ahora funcionará!
                    style={"padding": "8px 4px", "min_width": "80px"}
                ),
                rx.table.cell(
                    estado_badge_rm(solicitud.get("estado", "pendiente")),
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                rx.table.cell(
                    rx.box(
                        rx.vstack(
                            rx.button(
                                "✅ Aprobar",
                                on_click=lambda: TecnicaState.open_aprobar_dialog(solicitud),
                                color_scheme="green",
                                size="1",
                                variant="solid",
                                width="100%"
                            ),
                            rx.button(
                                "❌ Rechazar",
                                on_click=lambda: TecnicaState.open_rechazar_dialog(solicitud),
                                color_scheme="red",
                                size="1",
                                variant="solid",
                                width="100%"
                            ),
                            spacing="1",
                            width="100%"
                        ),
                        style={"min_width": "120px"}
                    ),
                    style={"padding": "8px 4px"}
                ),
            )
        
        header_style = {
            "background": "#059669",
            "color": "white",
            "font_weight": "600",
            "padding": "12px 4px",
            "text_align": "left",
            "white_space": "nowrap"
        }
        
        return rx.cond(
            TecnicaState.solicitudes_pendientes.length() == 0,
            rx.center(
                rx.vstack(
                    rx.icon("file_text", size=32, color="#cbd5e1"),
                    rx.text("No hay solicitudes pendientes", size="3", color="#64748b"),
                    spacing="2",
                    align="center"
                ),
                padding="3rem",
                width="100%"
            ),
            rx.box(
                rx.scroll_area(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("ID", style=header_style),
                                rx.table.column_header_cell("Centro Costo", style=header_style),
                                rx.table.column_header_cell("Fecha", style=header_style),
                                rx.table.column_header_cell("Orden Trabajo", style=header_style),
                                rx.table.column_header_cell("Descripción", style=header_style),
                                rx.table.column_header_cell("Cantidad", style=header_style),
                                rx.table.column_header_cell("UM", style=header_style),
                                rx.table.column_header_cell("Estado", style=header_style),
                                rx.table.column_header_cell("Acciones", style=header_style),
                            )
                        ),
                        rx.table.body(
                            rx.foreach(
                                TecnicaState.solicitudes_pendientes,
                                solicitud_row
                            )
                        ),
                        style={
                            "width": "100%",
                            "min_width": "1000px",
                            "table_layout": "auto"
                        }
                    ),
                    type="always",
                    scrollbars="horizontal",
                    style={
                        "width": "100%",
                        "height": "500px",
                        "border": "1px solid #e2e8f0",
                        "border_radius": "8px"
                    }
                ),
                width="100%",
                overflow_x="auto"
            )
        )
    
    def aprobar_dialog():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Aprobar Solicitud", color="#212121"),
                rx.dialog.description(
                    rx.cond(
                        (TecnicaState.selected_solicitud["id"] != "") & (TecnicaState.selected_solicitud["id"] != None),
                        rx.hstack(
                            rx.text("¿Aprobar solicitud #"),
                            rx.text(TecnicaState.selected_solicitud["id"], font_weight="600"),
                            rx.text("?"),
                            spacing="1"
                        ),
                        rx.text("Aprobar solicitud")
                    ),
                    color="#212121"
                ),
                rx.cond(
                    (TecnicaState.selected_solicitud["id"] != "") & (TecnicaState.selected_solicitud["id"] != None),
                    rx.vstack(
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("Centro costo:", size="2", color="#64748b", width="120px"),
                                    rx.text(
                                        TecnicaState.selected_solicitud["Centro costo"], 
                                        size="2", 
                                        color="#1e293b",
                                        font_weight="500"
                                    ),
                                    spacing="3",
                                    align="center"
                                ),
                                rx.hstack(
                                    rx.text("Descripción:", size="2", color="#64748b", width="120px"),
                                    rx.text(
                                        TecnicaState.selected_solicitud.get("Descripcion", "Sin descripción"),
                                        size="2", 
                                        color="#1e293b",
                                        font_weight="500"
                                    ),
                                    spacing="3",
                                    align="center"
                                ),
                                rx.hstack(
                                    rx.text("Cantidad:", size="2", color="#64748b", width="120px"),
                                    rx.hstack(
                                        rx.text(TecnicaState.selected_solicitud.get("Cantidad", "-"), size="2", color="#1e293b"),
                                        rx.text(TecnicaState.selected_solicitud.get("UM", ""), size="2", color="#1e293b"),
                                        spacing="1"
                                    ),
                                    spacing="3",
                                    align="center"
                                ),
                                spacing="3",
                                align="start",
                                padding="1rem",
                                border_radius="md",
                                background="#f8fafc",
                                border="1px solid #e2e8f0",
                            ),
                            width="100%"
                        ),
                        spacing="3",
                        margin_y="1rem"
                    ),
                    rx.text("No hay solicitud seleccionada")
                ),
                rx.vstack(
                    rx.dialog.close(
                        rx.button("Cancelar", variant="soft", size="2"),
                    ),
                    rx.button(
                        "✅ Aprobar",
                        on_click=TecnicaState.aprobar_solicitud,
                        color_scheme="green",
                        size="2",
                        variant="solid",
                        style={
                            "background": "linear-gradient(135deg, #059669 0%, #047857 100%)"
                        }
                    ),
                    spacing="2",
                    justify="end",
                ),
                max_width="500px",
                style={
                    "background": "white",
                    "border_radius": "12px",
                    "box_shadow": "0 20px 25px -5px rgba(0, 0, 0, 0.1)"
                }
            ),
            open=TecnicaState.show_aprobar_dialog,
            on_open_change=TecnicaState.set_show_aprobar_dialog,
        )
    
    def rechazar_dialog():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Rechazar Solicitud", color="#212121"),
                rx.dialog.description(
                    rx.cond(
                        (TecnicaState.selected_solicitud["id"] != "") & (TecnicaState.selected_solicitud["id"] != None),
                        rx.hstack(
                            rx.text("¿Rechazar solicitud #"),
                            rx.text(TecnicaState.selected_solicitud["id"], font_weight="600"),
                            rx.text("?"),
                            spacing="1"
                        ),
                        rx.text("Rechazar solicitud")
                    ),
                    color="#212121"
                ),
                rx.vstack(
                    rx.dialog.close(
                        rx.button("Cancelar", variant="soft", size="2"),
                    ),
                    rx.button(
                        "❌ Rechazar",
                        on_click=TecnicaState.rechazar_solicitud,
                        color_scheme="red",
                        size="2",
                        variant="solid",
                        style={
                            "background": "linear-gradient(135deg, #dc2626 0%, #b91c1c 100%)"
                        }
                    ),
                    spacing="2",
                    justify="end",
                ),
                max_width="400px",
                style={
                    "background": "white",
                    "border_radius": "12px",
                    "box_shadow": "0 20px 25px -5px rgba(0, 0, 0, 0.1)"
                }
            ),
            open=TecnicaState.show_rechazar_dialog,
            on_open_change=TecnicaState.set_show_rechazar_dialog,
        )
    
    def dashboard_content():
        return rx.box(
            navbar("Panel de Área Técnica"),
            rx.vstack(
                # Encabezado responsivo
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.vstack(
                                rx.heading(
                                    "🔧 Panel de Área Técnica",
                                    size="7",
                                    color="#1e293b",
                                    style={
                                        "background": "linear-gradient(135deg, #059669 0%, #047857 100%)",
                                        "background_clip": "text",
                                        "webkit_background_clip": "text",
                                        "color": "transparent",
                                        "font_weight": "800",
                                    }
                                ),
                                rx.text(
                                    "Revisión de solicitudes de recursos y materiales",
                                    size="4",
                                    color="#64748b"
                                ),
                                align="start",
                                spacing="1"
                            ),
                            rx.spacer(),
                            width="100%",
                            align="center"
                        ),
                        rx.hstack(
                            rx.badge(
                                f"{TecnicaState.solicitudes_pendientes.length()} pendientes",
                                color_scheme="amber",
                                variant="soft",
                                size="2"
                            ),
                            rx.button(
                                "🔄 Actualizar",
                                on_click=TecnicaState.load_data,
                                loading=TecnicaState.loading,
                                variant="soft",
                                size="2"
                            ),
                            rx.button(
                                "🚪 Cerrar Sesión",
                                on_click=TecnicaState.sign_out,
                                color_scheme="red",
                                variant="soft",
                                size="2"
                            ),
                            spacing="2",
                            wrap="wrap",
                            width="100%",
                            justify="end"
                        ),
                        spacing="3",
                        width="100%",
                        align="start"
                    ),
                    width="100%",
                    padding_bottom="1.5rem",
                    border_bottom="1px solid #e2e8f0"
                ),
                
                # Búsqueda responsiva
                rx.box(
                    rx.hstack(
                        rx.input(
                            placeholder="Buscar solicitudes...",
                            on_change=TecnicaState.filter_solicitudes,
                            width=["100%", "100%", "400px", "400px"],
                            size="3"
                        ),
                        spacing="2",
                        width="100%",
                        justify="end"
                    ),
                    width="100%",
                    padding_bottom="1.5rem"
                ),
                
                # Contenido principal
                rx.cond(
                    TecnicaState.loading,
                    rx.center(
                        rx.vstack(
                            rx.spinner(size="3", color="#059669"),
                            rx.text("Cargando solicitudes...", margin_top="1rem", color="#64748b"),
                            spacing="3",
                            align="center"
                        ),
                        height="300px", 
                        width="100%",
                    ),
                    solicitudes_table()
                ),
                
                # Información de búsqueda
                rx.cond(
                    TecnicaState.search_value != "",
                    rx.box(
                        rx.hstack(
                            rx.icon("search", size=16, color="#059669"),
                            rx.text(
                                f"Filtrando por: '{TecnicaState.search_value}'",
                                size="2",
                                color="#64748b"
                            ),
                            rx.button(
                                "Limpiar filtro",
                                on_click=lambda: TecnicaState.filter_solicitudes(""),
                                size="1",
                                variant="ghost"
                            ),
                            spacing="2",
                            align="center",
                            width="100%",
                            wrap="wrap"
                        ),
                        width="100%",
                        padding="0.75rem",
                        border_radius="8px",
                        background="#f0fdfa",
                        border="1px solid #a7f3d0",
                        margin_top="1rem",
                    ),
                ),
                
                # Diálogos
                aprobar_dialog(),
                rechazar_dialog(),
                
                # Pie de página responsivo
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.text("© 2026 Sistema de Gestión de Recursos", 
                                   size="1", 
                                   color="#64748b"),
                            rx.spacer(),
                            rx.text(
                                "Jefe de Área Técnica - Alexander",
                                size="1",
                                color="#64748b"
                            ),
                            width="100%",
                            wrap="wrap",
                            spacing="2"
                        ),
                        width="100%",
                        padding="1rem 0",
                        border_top="1px solid #e2e8f0"
                    ),
                    width="100%",
                    margin_top="2rem"
                ),
                
                spacing="4",
                padding=["1rem", "1.5rem", "2rem"],
                width="100%",
                max_width="1400px",
                margin="0 auto",
                align="start",
            ),
            width="100%",
            min_height="100vh",
            background="linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
        )
    
    return rx.cond(
        TecnicaState.is_authenticated,
        dashboard_content(),
        rx.center(
            rx.vstack(
                rx.spinner(size="3", color="#059669"),
                rx.text("Redirigiendo al login...", margin_top="1rem", color="#64748b"),
                rx.button(
                    "Ir al Login", 
                    on_click=lambda: rx.redirect(Route.TECNICA_LOGIN.value), 
                    margin_top="2rem"
                ),
                spacing="3",
                align="center",
                max_width="400px",
                padding="2rem",
            ),
            height="100vh",
            width="100%",
        )
    )