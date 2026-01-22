# TFuerte/pages/admin_dashboard.py - VERSIÓN CORREGIDA CON PAGINACIÓN
import reflex as rx
from TFuerte.state.admin_auth_state import AdminAuthState
from TFuerte.state.admin_dashboard_state import AdminDashboardState
from TFuerte.components.navbar import navbar
from TFuerte.routes import Route

@rx.page(
    route=Route.ADMIN_DASHBOARD.value,
    title="Dashboard - Administración",
    on_load=[AdminDashboardState.load_data, AdminDashboardState.cargar_admin_username]
)
def admin_dashboard() -> rx.Component:
    """Dashboard para administradores"""
    
    def registro_table() -> rx.Component:
        # Estilo mejorado para la tabla de datos
        return rx.box(
            rx.cond(
                AdminDashboardState.registro_filtered.length() == 0,
                rx.center(
                    rx.vstack(
                        rx.icon("database", size=32, color="#cbd5e1"),
                        rx.text("No hay registros disponibles", 
                               size="3", 
                               color="#64748b",
                               font_weight="500"),
                        spacing="2",
                        align="center"
                    ),
                    padding="3rem",
                    width="100%"
                ),
                rx.scroll_area(
                    rx.data_table(
                        data=AdminDashboardState.registro_filtered,
                        columns=[
                            {"title": "ID", "type": "number", "field": "id", "width": 80},
                            {"title": "Producto", "type": "str", "field": "Producto", "width": 200},
                            {"title": "Fecha E", "type": "str", "field": "Fecha E", "width": 100},
                            {"title": "Cant E", "type": "number", "field": "Cant E", "width": 80},
                            {"title": "Fecha S", "type": "str", "field": "Fecha S", "width": 100},
                            {"title": "Cant S", "type": "number", "field": "Cant S", "width": 80},
                            {"title": "Recibe", "type": "str", "field": "Recibe", "width": 150},
                            {"title": "Destino", "type": "str", "field": "Destino", "width": 150},
                            {"title": "Cliente", "type": "str", "field": "Cliente", "width": 200},
                        ],
                        pagination=True,
                        search=False,
                        sort=False,
                        style={
                            "width": "100%",
                            "min_width": "1000px",
                        }
                    ),
                    type="always",
                    scrollbars="horizontal",
                    style={
                        "width": "100%",
                        "height": "500px",
                        "overflow_y": "auto",
                        "border": "1px solid #e2e8f0",
                        "border_radius": "10px",
                        "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                    }
                )
            ),
            width="100%"
        )
    
    def solicitudes_table() -> rx.Component:
        # Estilo mejorado para la tabla de solicitudes - CON ANCHOS FIJOS
        header_style = {
            "background": "linear-gradient(135deg, #0f766e 0%, #115e59 100%)",
            "color": "white",
            "font_weight": "600",
            "padding": "14px 8px",
            "border": "none",
            "font_size": "13px",
            "text_transform": "uppercase",
            "letter_spacing": "0.5px",
            "white_space": "nowrap",
            "overflow": "hidden",
            "text_overflow": "ellipsis",
        }
        
        cell_style = {
            "padding": "12px 8px",
            "border_bottom": "1px solid #e2e8f0",
            "vertical_align": "middle",
            "font_size": "13px",
            "color": "#1e293b",
            "background": "white",
            "white_space": "nowrap",
            "overflow": "hidden",
            "text_overflow": "ellipsis",
        }
        
        def solicitud_row(solicitud):
            # Manejo de observaciones vacías
            observacion_cell = rx.cond(
                solicitud["Observacion"] == "",
                rx.text("-", color="#94a3b8", font_style="italic", style={"white_space": "nowrap", "overflow": "hidden", "text_overflow": "ellipsis"}),
                rx.text(solicitud["Observacion"], color="#1e293b", style={"white_space": "nowrap", "overflow": "hidden", "text_overflow": "ellipsis"})
            )
            
            # Celda de destino con ancho fijo
            destino_cell = rx.text(
                solicitud["Destino"], 
                color="#1e293b",
                style={"white_space": "nowrap", "overflow": "hidden", "text_overflow": "ellipsis"}
            )
            
            return rx.table.row(
                rx.table.cell(
                    rx.text(solicitud["id"], color="#1e293b", font_weight="600"),
                    style={**cell_style, "width": "70px", "min_width": "70px", "max_width": "70px"}
                ),
                rx.table.cell(
                    rx.text(solicitud["Descripcion"], color="#1e293b", style={"white_space": "nowrap", "overflow": "hidden", "text_overflow": "ellipsis"}),
                    style={**cell_style, "width": "220px", "min_width": "220px", "max_width": "220px"}
                ),
                rx.table.cell(
                    rx.text(
                        solicitud["Cantidad"], 
                        color="#1e293b", 
                        font_weight="600",
                        style={"text_align": "center"}
                    ),
                    style={**cell_style, "width": "80px", "min_width": "80px", "max_width": "80px", "text_align": "center"}
                ),
                rx.table.cell(
                    observacion_cell,
                    style={**cell_style, "width": "180px", "min_width": "180px", "max_width": "180px"}
                ),
                rx.table.cell(
                    destino_cell,
                    style={**cell_style, "width": "150px", "min_width": "150px", "max_width": "150px"}
                ),
                rx.table.cell(
                    rx.box(
                        rx.hstack(
                            rx.button(
                                "✅",
                                on_click=lambda: AdminDashboardState.open_aprobar_dialog(solicitud),
                                color_scheme="green",
                                size="1",
                                variant="solid",
                                style={
                                    "font_weight": "500",
                                    "padding": "4px 8px",
                                    "min_width": "40px",
                                    "background": "linear-gradient(135deg, #10b981 0%, #059669 100%)"
                                }
                            ),
                            rx.button(
                                "❌",
                                on_click=lambda: AdminDashboardState.open_rechazar_dialog(solicitud),
                                color_scheme="red",
                                size="1",
                                variant="solid",
                                style={
                                    "font_weight": "500",
                                    "padding": "4px 8px",
                                    "min_width": "40px",
                                    "background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)"
                                }
                            ),
                            spacing="2",
                            justify="center"
                        ),
                        style={"display": "flex", "justify_content": "center", "width": "100%"}
                    ),
                    style={**cell_style, "width": "100px", "min_width": "100px", "max_width": "100px", "text_align": "center"}
                ),
                _hover={
                    "background_color": "#f8fafc",
                },
            )
        
        # Calcular índices para mostrar - USANDO .length() EN LUGAR DE len()
        total_items = AdminDashboardState.solicitudes_pendientes.length()
        current_page = AdminDashboardState.current_page_solicitudes
        items_per_page = AdminDashboardState.items_per_page_solicitudes
        
        # Cálculo de índices usando operadores de Reflex
        start_idx = (current_page - 1) * items_per_page
        end_idx = rx.cond(
            total_items > 0,
            rx.cond(
                start_idx + items_per_page > total_items,
                total_items,
                start_idx + items_per_page
            ),
            0
        )
        
        # Función auxiliar para crear botones de página
        def create_page_button(page_num):
            """Crea un botón de página individual"""
            return rx.button(
                # Usamos page_num directamente sin str() - Reflex maneja la conversión
                rx.text(page_num, size="2", font_weight="500"),
                on_click=lambda: AdminDashboardState.go_to_page_solicitudes(page_num),
                variant="soft",
                size="2",
                style=rx.cond(
                    AdminDashboardState.current_page_solicitudes == page_num,
                    {
                        "background": "#0f766e",
                        "color": "white",
                        "border": "1px solid #0f766e",
                        "_hover": {"background": "#115e59"}
                    },
                    {
                        "background": "white",
                        "border": "1px solid #e2e8f0",
                        "color": "#1e293b",
                        "_hover": {
                            "background": "#f8fafc",
                            "border": "1px solid #cbd5e1"
                        }
                    }
                )
            )
        
        # Renderizar la paginación usando los números de página del estado
        def render_pagination():
            """Renderiza la paginación completa"""
            # Obtener números de página del estado
            page_numbers = AdminDashboardState.page_numbers_solicitudes
            
            return rx.hstack(
                # Botón "Previous"
                rx.button(
                    "Anterior",
                    on_click=AdminDashboardState.previous_page_solicitudes,
                    variant="soft",
                    size="2",
                    is_disabled=AdminDashboardState.current_page_solicitudes == 1,
                    style={
                        "background": "white",
                        "border": "1px solid #e2e8f0",
                        "color": "#1e293b",
                        "_hover": {
                            "background": "#f8fafc",
                            "border": "1px solid #cbd5e1"
                        }
                    }
                ),
                
                # Botones de números de página
                rx.foreach(
                    page_numbers,
                    lambda page_num: create_page_button(page_num)
                ),
                
                # Botón "Next"
                rx.button(
                    "Siguiente",
                    on_click=AdminDashboardState.next_page_solicitudes,
                    variant="soft",
                    size="2",
                    is_disabled=AdminDashboardState.current_page_solicitudes == AdminDashboardState.total_pages_solicitudes,
                    style={
                        "background": "white",
                        "border": "1px solid #e2e8f0",
                        "color": "#1e293b",
                        "_hover": {
                            "background": "#f8fafc",
                            "border": "1px solid #cbd5e1"
                        }
                    }
                ),
                
                spacing="1",
                align="center",
                wrap="wrap"
            )
        
        return rx.box(
            rx.cond(
                AdminDashboardState.solicitudes_pendientes.length() == 0,
                rx.center(
                    rx.vstack(
                        rx.icon("file_text", size=32, color="#cbd5e1"),
                        rx.text("No hay solicitudes pendientes", 
                            size="3", 
                            color="#64748b",
                            font_weight="500"),
                        spacing="2",
                        align="center"
                    ),
                    padding="3rem",
                    width="100%"
                ),
                rx.vstack(
                    # Tabla de datos
                    rx.scroll_area(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("ID", style={**header_style, "width": "70px", "min_width": "70px", "max_width": "70px"}),
                                    rx.table.column_header_cell("Descripción", style={**header_style, "width": "220px", "min_width": "220px", "max_width": "220px"}),
                                    rx.table.column_header_cell("Cantidad", style={**header_style, "width": "80px", "min_width": "80px", "max_width": "80px"}),
                                    rx.table.column_header_cell("Observación", style={**header_style, "width": "180px", "min_width": "180px", "max_width": "180px"}),
                                    rx.table.column_header_cell("Destino", style={**header_style, "width": "120px", "min_width": "120px", "max_width": "100px"}),
                                    rx.table.column_header_cell("Acciones", style={**header_style, "width": "150px", "min_width": "150px", "max_width": "150px", "text_align": "center"}),
                                )
                            ),
                            rx.table.body(
                                rx.foreach(
                                    AdminDashboardState.solicitudes_paginated,
                                    solicitud_row
                                )
                            ),
                            style={
                                "width": "100%",
                                "min_width": "800px",
                                "table_layout": "fixed",
                                "border_collapse": "collapse",
                            }
                        ),
                        type="always",
                        scrollbars="horizontal",
                        style={
                            "width": "100%",
                            "height": "500px",
                            "overflow_y": "auto",
                            "border": "1px solid #e2e8f0",
                            "border_radius": "10px",
                            "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                        }
                    ),
                    
                    # PAGINACIÓN
                    rx.box(
                        rx.hstack(
                            # Texto de resultados
                            rx.text(
                                # Versión corregida usando string interpolation con rx.cond
                                rx.cond(
                                    AdminDashboardState.solicitudes_pendientes.length() > 0,
                                    rx.text(
                                        "Mostrando ",
                                        rx.cond(
                                            AdminDashboardState.current_page_solicitudes == 1,
                                            "1",
                                            rx.text(
                                                (AdminDashboardState.current_page_solicitudes - 1) * AdminDashboardState.items_per_page_solicitudes + 1
                                            )
                                        ),
                                        " a ",
                                        rx.cond(
                                            AdminDashboardState.current_page_solicitudes * AdminDashboardState.items_per_page_solicitudes > AdminDashboardState.solicitudes_pendientes.length(),
                                            AdminDashboardState.solicitudes_pendientes.length(),
                                            AdminDashboardState.current_page_solicitudes * AdminDashboardState.items_per_page_solicitudes
                                        ),
                                        " de ",
                                        AdminDashboardState.solicitudes_pendientes.length(),
                                        " resultados"
                                    ),
                                    "Mostrando 0 a 0 de 0 resultados"
                                ),
                                size="2",
                                color="#64748b",
                                font_weight="500"
                            ),
                            
                            rx.spacer(),
                            
                            # Botones de paginación
                            render_pagination(),
                            
                            width="100%",
                            align="center",
                            spacing="4",
                            wrap="wrap"
                        ),
                        padding="1.5rem 1rem",
                        border_top="1px solid #e2e8f0",
                        background="#f8fafc"
                    ),
                    
                    spacing="0",
                    width="100%"
                )
            ),
            width="100%"
        )
    
    def aprobar_dialog():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Aprobar Solicitud", color="#212121"),
                rx.dialog.description(
                    rx.cond(
                        AdminDashboardState.selected_solicitud,
                        rx.text(f"¿Aprobar solicitud #{AdminDashboardState.selected_solicitud['id']}?", color="#212121"),
                        "Aprobar solicitud"
                    )
                ),
                rx.cond(
                    AdminDashboardState.selected_solicitud,
                    rx.vstack(
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("Producto:", size="2", color="#64748b", width="100px"),
                                    rx.text(
                                        AdminDashboardState.selected_solicitud["Descripcion"], 
                                        size="2", 
                                        color="#1e293b",
                                        font_weight="500"
                                    ),
                                    spacing="3",
                                    align="center"
                                ),
                                rx.hstack(
                                    rx.text("Cantidad:", size="2", color="#64748b", width="100px"),
                                    rx.text(
                                        AdminDashboardState.selected_solicitud["Cantidad"],
                                        size="2", 
                                        color="#1e293b",
                                        font_weight="500"
                                    ),
                                    spacing="3",
                                    align="center"
                                ),
                                rx.hstack(
                                    rx.text("Destino:", size="2", color="#64748b", width="100px"),
                                    rx.text(
                                        AdminDashboardState.selected_solicitud["Destino"], 
                                        size="2", 
                                        color="#1e293b"
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
                        "✅ Aprobar Solicitud",
                        on_click=AdminDashboardState.aprobar_solicitud,
                        color_scheme="green",
                        size="2",
                        variant="solid",
                        style={
                            "background": "linear-gradient(135deg, #10b981 0%, #059669 100%)"
                        }
                    ),
                    spacing="2",
                    justify="center",
                ),
                max_width="500px",
                style={
                    "background": "white",
                    "border_radius": "12px",
                    "box_shadow": "0 20px 25px -5px rgba(0, 0, 0, 0.1)"
                }
            ),
            open=AdminDashboardState.show_aprobar_dialog,
            on_open_change=AdminDashboardState.set_show_aprobar_dialog,
        )
    
    def rechazar_dialog():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Rechazar Solicitud", color="#212121"),
                rx.dialog.description(
                    rx.cond(
                        AdminDashboardState.selected_solicitud,
                        rx.text(f"¿Rechazar solicitud #{AdminDashboardState.selected_solicitud['id']}?", color="#212121"),
                        "Rechazar solicitud"
                    )
                ),
                rx.vstack(
                    rx.dialog.close(
                        rx.button("Cancelar", variant="soft", size="2"),
                    ),
                    rx.button(
                        "❌ Rechazar Solicitud",
                        on_click=AdminDashboardState.rechazar_solicitud,
                        color_scheme="red",
                        size="2",
                        variant="solid",
                        style={
                            "background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)"
                        }
                    ),
                    spacing="2",
                    justify="center",
                ),
                max_width="400px",
                style={
                    "background": "white",
                    "border_radius": "12px",
                    "box_shadow": "0 20px 25px -5px rgba(0, 0, 0, 0.1)"
                }
            ),
            open=AdminDashboardState.show_rechazar_dialog,
            on_open_change=AdminDashboardState.set_show_rechazar_dialog,
        )
    
    def dashboard_content():
        return rx.box(
            navbar("Panel de Administración"),
            rx.vstack(
                # Encabezado principal
                rx.box(
                    rx.hstack(
                        rx.vstack(
                            rx.heading(
                                "📊 Panel de Administración",
                                size="7",
                                color="#1e293b",
                                style={
                                    "background": "linear-gradient(135deg, #0f766e 0%, #115e59 100%)",
                                    "background_clip": "text",
                                    "webkit_background_clip": "text",
                                    "color": "transparent",
                                    "font_weight": "800",
                                    "letter_spacing": "-0.5px",
                                }
                            ),
                            rx.text(
                                "Gestión de solicitudes y registro de movimientos",
                                size="4",
                                color="#64748b"
                            ),
                            align="start",
                            spacing="1"
                        ),
                        rx.spacer(),
                        rx.button(
                            "🔄 Actualizar",
                            on_click=AdminDashboardState.load_data,
                            loading=AdminDashboardState.loading,
                            variant="soft",
                            size="2",
                            style={
                                "background": "#f1f5f9",
                                "border": "1px solid #e2e8f0",
                                "font_weight": "500"
                            }
                        ),
                        width="100%",
                        align="center",
                        wrap="wrap",
                        spacing="3"
                    ),
                    width="100%",
                    padding_bottom="1.5rem",
                    border_bottom="1px solid #e2e8f0"
                ),
                
                # Tabs principales
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger(
                            "📋 Solicitudes Pendientes", 
                            value="solicitudes",
                            style={
                                "font_weight": "600", 
                                "padding": "0.75rem 1.5rem",
                                "color": "#1e293b",
                                "border_bottom": "2px solid transparent",
                                "_selected": {
                                    "border_bottom": "2px solid #0f766e",
                                    "color": "#0f766e"
                                }
                            }
                        ),
                        rx.tabs.trigger(
                            "📜 Historial RegistroTF", 
                            value="registro",
                            style={
                                "font_weight": "600", 
                                "padding": "0.75rem 1.5rem",
                                "color": "#1e293b",
                                "border_bottom": "2px solid transparent",
                                "_selected": {
                                    "border_bottom": "2px solid #0f766e",
                                    "color": "#0f766e"
                                }
                            }
                        ),
                        rx.tabs.trigger(
                            "👤 Mi Perfil", 
                            value="perfil",
                            style={
                                "font_weight": "600", 
                                "padding": "0.75rem 1.5rem",
                                "color": "#1e293b",
                                "border_bottom": "2px solid transparent",
                                "_selected": {
                                    "border_bottom": "2px solid #0f766e",
                                    "color": "#0f766e"
                                }
                            }
                        ),
                    ),
                    rx.tabs.content(
                        rx.vstack(
                            # Barra de búsqueda - RESPONSIVA
                            rx.box(
                                rx.vstack(
                                    rx.hstack(
                                        rx.input(
                                            placeholder="Buscar solicitudes...",
                                            on_change=AdminDashboardState.filter_solicitudes,
                                            width=["100%", "100%", "400px", "400px"],
                                            size="3",
                                            style={
                                                "background": "gray",
                                                "border": "1px solid #d1d5db",
                                                "border_radius": "8px",
                                                "color": "#1e293b",
                                                "flex": "1",
                                                "min_width": "0"  # Importante para flexbox
                                            }
                                        ),
                                        rx.hstack(
                                            rx.badge(
                                                f"{AdminDashboardState.solicitudes_pendientes.length()} pendientes",
                                                color_scheme="amber",
                                                variant="soft",
                                                size="2"
                                            ),
                                            spacing="2",
                                            align="center"
                                        ),
                                        spacing="2",
                                        width="100%",
                                        justify="between",
                                        wrap="wrap"
                                    ),
                                    spacing="2"
                                ),
                                width="100%",
                                padding_bottom="1.5rem"
                            ),
                            
                            # Contenido de solicitudes
                            rx.cond(
                                AdminDashboardState.loading,
                                rx.center(
                                    rx.vstack(
                                        rx.spinner(size="3", color="#0f766e"),
                                        rx.text("Cargando solicitudes...", 
                                               margin_top="1rem", 
                                               color="#64748b"),
                                        spacing="3",
                                        align="center"
                                    ),
                                    height="300px", 
                                    width="100%",
                                ),
                                solicitudes_table()
                            ),
                            
                            # Info de búsqueda
                            rx.cond(
                                AdminDashboardState.search_solicitudes != "",
                                rx.box(
                                    rx.hstack(
                                        rx.icon("search", size=16, color="#0f766e"),
                                        rx.text(
                                            f"Filtrando por: '{AdminDashboardState.search_solicitudes}'",
                                            size="2",
                                            color="#64748b"
                                        ),
                                        rx.button(
                                            "Limpiar filtro",
                                            on_click=lambda: AdminDashboardState.filter_solicitudes(""),
                                            size="1",
                                            variant="ghost",
                                            style={"margin_left": "auto"}
                                        ),
                                        spacing="2",
                                        align="center",
                                        width="100%"
                                    ),
                                    width="100%",
                                    padding="0.75rem",
                                    border_radius="8px",
                                    background="#f0fdfa",
                                    border="1px solid #a7f3d0",
                                    margin_top="1rem",
                                ),
                            ),
                            
                            spacing="3",
                            align="start",
                            width="100%"
                        ),
                        value="solicitudes",
                        style={"padding": "1.5rem 0"}
                    ),
                    rx.tabs.content(
                        rx.vstack(
                            # Barra de búsqueda para registros - RESPONSIVA
                            rx.box(
                                rx.vstack(
                                    rx.hstack(
                                        rx.input(
                                            placeholder="Buscar en registros...",
                                            on_change=AdminDashboardState.filter_registro,
                                            width=["100%", "100%", "400px", "400px"],
                                            size="3",
                                            style={
                                                "background": "gray",
                                                "border": "1px solid #d1d5db",
                                                "border_radius": "8px",
                                                "color": "#1e293b",
                                                "flex": "1",
                                                "min_width": "0"
                                            }
                                        ),
                                        rx.hstack(
                                            rx.badge(
                                                f"{AdminDashboardState.registro_filtered.length()} mostrados",
                                                color_scheme="blue",
                                                variant="soft",
                                                size="2"
                                            ),
                                            spacing="2",
                                            align="center"
                                        ),
                                        spacing="2",
                                        width="100%",
                                        justify="between",
                                        wrap="wrap"
                                    ),
                                    spacing="2"
                                ),
                                width="100%",
                                padding_bottom="1.5rem"
                            ),
                            
                            # Contenido de registros
                            rx.cond(
                                AdminDashboardState.loading,
                                rx.center(
                                    rx.vstack(
                                        rx.spinner(size="3", color="#0f766e"),
                                        rx.text("Cargando registros...", 
                                               margin_top="1rem", 
                                               color="#64748b"),
                                        spacing="3",
                                        align="center"
                                    ),
                                    height="300px", 
                                    width="100%",
                                ),
                                registro_table()
                            ),
                            
                            # Info de búsqueda
                            rx.cond(
                                AdminDashboardState.search_registro != "",
                                rx.box(
                                    rx.hstack(
                                        rx.icon("search", size=16, color="#0f766e"),
                                        rx.text(
                                            f"Filtrando por: '{AdminDashboardState.search_registro}'",
                                            size="2",
                                            color="#64748b"
                                        ),
                                        rx.button(
                                            "Limpiar filtro",
                                            on_click=lambda: AdminDashboardState.filter_registro(""),
                                            size="1",
                                            variant="ghost",
                                            style={"margin_left": "auto"}
                                        ),
                                        spacing="2",
                                        align="center",
                                        width="100%"
                                    ),
                                    width="100%",
                                    padding="0.75rem",
                                    border_radius="8px",
                                    background="#f0fdfa",
                                    border="1px solid #a7f3d0",
                                    margin_top="1rem",
                                ),
                            ),
                            
                            spacing="3",
                            align="start",
                            width="100%"
                        ),
                        value="registro",
                        style={"padding": "1.5rem 0"}
                    ),
                    rx.tabs.content(
                        rx.vstack(
                            # Perfil del administrador
                            rx.card(
                                rx.vstack(
                                    rx.hstack(
                                        rx.icon("user", size=24, color="#0f766e"),
                                        rx.vstack(
                                            rx.text(
                                                "Administrador del Sistema",
                                                size="4",
                                                font_weight="700",
                                                color="#1e293b"
                                            ),
                                            rx.text(
                                                rx.cond(
                                                    AdminAuthState.current_admin,
                                                    f"Usuario: {AdminAuthState.current_admin['user']}",
                                                    "Usuario: No disponible"
                                                ),
                                                size="2",
                                                color="#64748b"
                                            ),
                                            align="start",
                                            spacing="1"
                                        ),
                                        spacing="3",
                                        align="center"
                                    ),
                                    rx.divider(margin_y="1rem"),
                                    rx.vstack(
                                        rx.text("📋 Permisos:", size="3", font_weight="600", color="#1e293b"),
                                        rx.list(
                                            rx.list.item("✓ Aprobar/Rechazar solicitudes"),
                                            rx.list.item("✓ Ver historial completo de registros"),
                                            rx.list.item("✓ Acceso completo al sistema"),
                                            spacing="2",
                                            style={"color": "#64748b"}
                                        ),
                                        spacing="2",
                                        align="start"
                                    ),
                                    spacing="3",
                                    align="start"
                                ),
                                width="100%",
                                style={
                                    "background": "white",
                                    "border_radius": "12px",
                                    "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                                    "border": "1px solid #e2e8f0"
                                }
                            ),
                            
                            # Acciones
                            rx.card(
                                rx.vstack(
                                    rx.text("🔒 Acciones de Cuenta", size="3", font_weight="600", color="#1e293b"),
                                    rx.hstack(
                                        rx.button(
                                            "🚪 Cerrar Sesión",
                                            on_click=AdminAuthState.sign_out,
                                            color_scheme="red",
                                            variant="solid",
                                            size="2",
                                            style={
                                                "background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)"
                                            }
                                        ),
                                        rx.button(
                                            "🔄 Recargar Datos",
                                            on_click=AdminDashboardState.load_data,
                                            variant="soft",
                                            size="2"
                                        ),
                                        spacing="3",
                                        wrap="wrap"
                                    ),
                                    spacing="3",
                                    align="start"
                                ),
                                width="100%",
                                style={
                                    "background": "white",
                                    "border_radius": "12px",
                                    "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                                    "border": "1px solid #e2e8f0"
                                }
                            ),
                            
                            # Estadísticas
                            rx.card(
                                rx.vstack(
                                    rx.text("📈 Estadísticas del Sistema", size="3", font_weight="600", color="#1e293b"),
                                    rx.grid(
                                        rx.box(
                                            rx.vstack(
                                                rx.text("Solicitudes Pendientes", size="2", color="#64748b"),
                                                rx.text(
                                                    AdminDashboardState.solicitudes_pendientes.length(),
                                                    size="4",
                                                    font_weight="700",
                                                    color="#d97706"
                                                ),
                                                spacing="1",
                                                align="center"
                                            ),
                                            style={
                                                "background": "#fffbeb",
                                                "padding": "1rem",
                                                "border_radius": "8px",
                                                "border": "1px solid #fde68a",
                                                "text_align": "center"
                                            }
                                        ),
                                        rx.box(
                                            rx.vstack(
                                                rx.text("Registros Mostrados", size="2", color="#64748b"),
                                                rx.text(
                                                    AdminDashboardState.registro_filtered.length(),
                                                    size="4",
                                                    font_weight="700",
                                                    color="#2563eb"
                                                ),
                                                spacing="1",
                                                align="center"
                                            ),
                                            style={
                                                "background": "#eff6ff",
                                                "padding": "1rem",
                                                "border_radius": "8px",
                                                "border": "1px solid #dbeafe",
                                                "text_align": "center"
                                            }
                                        ),
                                        rx.box(
                                            rx.vstack(
                                                rx.text("Total de Registros", size="2", color="#64748b"),
                                                rx.text(
                                                    # MOSTRAMOS EL TOTAL DE REGISTROS (sin filtrar)
                                                    AdminDashboardState.registro_data.length(),
                                                    size="4",
                                                    font_weight="700",
                                                    color="#7c3aed"
                                                ),
                                                spacing="1",
                                                align="center"
                                            ),
                                            style={
                                                "background": "#f5f3ff",
                                                "padding": "1rem",
                                                "border_radius": "8px",
                                                "border": "1px solid #ddd6fe",
                                                "text_align": "center"
                                            }
                                        ),
                                        rx.box(
                                            rx.vstack(
                                                rx.text("Todas las Solicitudes", size="2", color="#64748b"),
                                                rx.text(
                                                    AdminDashboardState.solicitudes_data.length(),
                                                    size="4",
                                                    font_weight="700",
                                                    color="#059669"
                                                ),
                                                spacing="1",
                                                align="center"
                                            ),
                                            style={
                                                "background": "#f0fdfa",
                                                "padding": "1rem",
                                                "border_radius": "8px",
                                                "border": "1px solid #a7f3d0",
                                                "text_align": "center"
                                            }
                                        ),
                                        columns="2",
                                        spacing="3",
                                        width="100%"
                                    ),
                                    spacing="3",
                                    align="start"
                                ),
                                width="100%",
                                style={
                                    "background": "white",
                                    "border_radius": "12px",
                                    "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                                    "border": "1px solid #e2e8f0"
                                }
                            ),
                            
                            spacing="4",
                            align="start",
                            width="100%"
                        ),
                        value="perfil",
                        style={"padding": "1.5rem 0"}
                    ),
                    default_value="solicitudes",
                    width="100%",
                    style={
                        "background": "white",
                        "border_radius": "12px",
                        "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                        "padding": "1rem"
                    }
                ),
                
                # Diálogos modales
                aprobar_dialog(),
                rechazar_dialog(),
                
                # Pie de página
                rx.box(
                    rx.hstack(
                        rx.text("© 2026 Sistema de Gestión de Almacén", 
                               size="1", 
                               color="#64748b"),
                        rx.spacer(),
                        rx.text(
                            "Panel de Administración - Acceso Restringido",
                            size="1",
                            color="#64748b"
                        ),
                        width="100%",
                        padding="1rem 0",
                        border_top="1px solid #e2e8f0"
                    ),
                    width="100%",
                    margin_top="2rem"
                ),
                
                spacing="4",
                padding=["1rem", "1.5rem", "2rem", "3rem"],  # Padding más conservador
                width="100%",
                max_width="none",
                align="start",
                min_height="100vh"
            ),
            width="100%",
            style={
                "background": "linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
                "min_height": "100vh",
            }
        )
    
    return rx.cond(
        AdminAuthState.is_authenticated,
        dashboard_content(),
        rx.center(
            rx.vstack(
                rx.spinner(size="3", color="#0f766e"),
                rx.text("Redirigiendo al login...", 
                       margin_top="1rem", 
                       color="#64748b",
                       text_align="center",
                       font_weight="500"),
                rx.button("Ir al Login", 
                         on_click=lambda: rx.redirect(Route.ADMIN_LOGIN_NEW.value), 
                         margin_top="2rem", 
                         width="200px",
                         variant="solid",
                         style={
                             "background": "linear-gradient(135deg, #0f766e 0%, #115e59 100%)"
                         }),
                spacing="3", 
                align="center", 
                width="100%", 
                max_width="400px", 
                padding="2rem",
            ),
            height="100vh", 
            width="100%",
            background="linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
        )
    )