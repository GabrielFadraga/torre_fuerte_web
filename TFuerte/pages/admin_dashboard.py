import reflex as rx
from TFuerte.state.admin_auth_state import AdminAuthState
from TFuerte.state.admin_dashboard_state import AdminDashboardState
from TFuerte.state.almacen_view_state import AlmacenViewState
from TFuerte.components.navbar import navbar
from TFuerte.components.almacen_readonly_table import almacen_readonly_table
from TFuerte.routes import Route


@rx.page(
    route=Route.ADMIN_DASHBOARD.value,
    title="Dashboard - Administración",
    on_load=[AdminDashboardState.cargar_admin_username, AdminDashboardState.load_data, AlmacenViewState.load_data]
)
def admin_dashboard() -> rx.Component:
    """Dashboard para administradores"""

    # ==================== TABLA DE REGISTROS CON PAGINACIÓN UNIFICADA ====================
    def registro_table() -> rx.Component:
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
        }
        cell_style = {
            "padding": "12px 8px",
            "border_bottom": "1px solid #e2e8f0",
            "vertical_align": "middle",
            "font_size": "13px",
            "color": "#1e293b",
            "background": "white",
            "white_space": "nowrap",
        }

        def registro_row(item):
            return rx.table.row(
                rx.table.cell(rx.text(item["id"]), style=cell_style),
                rx.table.cell(rx.text(item["Producto"]), style=cell_style),
                rx.table.cell(rx.text(item.get("Fecha E", "")), style=cell_style),
                rx.table.cell(rx.text(item.get("Cant E", 0)), style=cell_style),
                rx.table.cell(rx.text(item.get("Fecha S", "")), style=cell_style),
                rx.table.cell(rx.text(item.get("Cant S", 0)), style=cell_style),
                rx.table.cell(rx.text(item.get("Recibe", "")), style=cell_style),
                rx.table.cell(rx.text(item.get("Destino", "")), style=cell_style),
                rx.table.cell(rx.text(item.get("Cliente", "")), style=cell_style),
            )

        # --- Botón de página individual ---
        def create_page_button_registro(page_num: int):
            return rx.button(
                rx.text(page_num, size="2", font_weight="500"),
                on_click=lambda: AdminDashboardState.go_to_page_registro(page_num),
                variant="soft",
                size="2",
                style=rx.cond(
                    AdminDashboardState.current_page_registro == page_num,
                    {
                        "background": "#0f766e",
                        "color": "white",
                        "border": "1px solid #0f766e",
                        "_hover": {"background": "#115e59"},
                        "flex_shrink": 0,
                        "min_width": "32px",
                        "padding": "0 8px",
                    },
                    {
                        "background": "white",
                        "border": "1px solid #e2e8f0",
                        "color": "#1e293b",
                        "_hover": {
                            "background": "#f8fafc",
                            "border": "1px solid #cbd5e1"
                        },
                        "flex_shrink": 0,
                        "min_width": "32px",
                        "padding": "0 8px",
                    }
                )
            )

        # --- Controles de paginación (estilo unificado) ---
        def render_pagination_registro():
            return rx.hstack(
                # Botón anterior
                rx.button(
                    rx.icon("chevron-left", size=16),
                    on_click=AdminDashboardState.previous_page_registro,
                    variant="soft",
                    size="2",
                    is_disabled=AdminDashboardState.current_page_registro == 1,
                    style={
                        "background": "white",
                        "border": "1px solid #e2e8f0",
                        "color": "#1e293b",
                        "flex_shrink": 0,
                        "min_width": "32px",
                        "padding": "0 8px",
                    }
                ),
                # Contenedor de números
                rx.box(
                    rx.hstack(
                        # Primera página + "..." si estamos lejos del inicio
                        rx.cond(
                            (AdminDashboardState.current_page_registro > 3) &
                            (AdminDashboardState.total_pages_registro > 4),
                            rx.hstack(
                                create_page_button_registro(1),
                                rx.text("...", size="2", color="#64748b", padding_x="1"),
                                spacing="1",
                                flex_shrink=0,
                            ),
                        ),
                        # Páginas del rango calculado (máximo 4)
                        rx.cond(
                            AdminDashboardState.page_numbers_registro.length() > 0,
                            rx.hstack(
                                rx.foreach(
                                    AdminDashboardState.page_numbers_registro,
                                    create_page_button_registro
                                ),
                                spacing="1",
                                wrap="nowrap",
                                flex_shrink=0,
                            ),
                            rx.text(
                                f"Pág. {AdminDashboardState.current_page_registro}",
                                size="2",
                                color="#64748b",
                                padding_x="2",
                                flex_shrink=0,
                            ),
                        ),
                        # Última página + "..." si estamos lejos del final
                        rx.cond(
                            (AdminDashboardState.current_page_registro < AdminDashboardState.total_pages_registro - 2) &
                            (AdminDashboardState.total_pages_registro > 4),
                            rx.hstack(
                                rx.text("...", size="2", color="#64748b", padding_x="1"),
                                create_page_button_registro(AdminDashboardState.total_pages_registro),
                                spacing="1",
                                flex_shrink=0,
                            ),
                        ),
                        spacing="1",
                        wrap="nowrap",
                        align="center",
                    ),
                    overflow_x="auto",
                    flex_grow=0,
                    flex_shrink=1,
                    max_width="100%",
                ),
                # Botón siguiente
                rx.button(
                    rx.hstack(
                        rx.icon("chevron-right", size=16),
                        width="100%",
                        spacing="0",
                        justify="end",
                        align="end",
                    ),
                    on_click=AdminDashboardState.next_page_registro,
                    variant="soft",
                    size="2",
                    is_disabled=AdminDashboardState.current_page_registro == AdminDashboardState.total_pages_registro,
                    style={
                        "background": "white",
                        "border": "1px solid #e2e8f0",
                        "color": "#1e293b",
                        "flex_shrink": 0,
                        "min_width": "32px",
                        "padding": "0 8px",
                    }
                ),
                spacing="2",
                wrap="nowrap",
                align="center",
                justify="end",
                width="100%",
            )

        return rx.box(
            rx.cond(
                AdminDashboardState.registro_filtered.length() == 0,
                rx.center(
                    rx.vstack(
                        rx.icon("database", size=32, color="#cbd5e1"),
                        rx.text("No hay registros disponibles", size="3", color="#64748b"),
                        spacing="2",
                    ),
                    padding="3rem",
                ),
                rx.vstack(
                    # Tabla
                    rx.scroll_area(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("ID", style={**header_style, "width": "70px"}),
                                    rx.table.column_header_cell("Producto", style={**header_style, "width": "200px"}),
                                    rx.table.column_header_cell("Fecha E", style={**header_style, "width": "100px"}),
                                    rx.table.column_header_cell("Cant E", style={**header_style, "width": "80px"}),
                                    rx.table.column_header_cell("Fecha S", style={**header_style, "width": "100px"}),
                                    rx.table.column_header_cell("Cant S", style={**header_style, "width": "80px"}),
                                    rx.table.column_header_cell("Recibe", style={**header_style, "width": "150px"}),
                                    rx.table.column_header_cell("Destino", style={**header_style, "width": "150px"}),
                                    rx.table.column_header_cell("Cliente", style={**header_style, "width": "200px"}),
                                )
                            ),
                            rx.table.body(
                                rx.foreach(
                                    AdminDashboardState.registro_paginated,
                                    registro_row
                                )
                            ),
                            style={"width": "100%", "min_width": "1200px", "table_layout": "fixed"},
                        ),
                        type="always",
                        scrollbars="horizontal",
                        style={
                            "width": "100%",
                            "max_height": "600px",
                            "height": "auto",
                            "overflow_y": "auto",
                            "border": "1px solid #e2e8f0",
                            "border_radius": "10px",
                        }
                    ),
                    # Controles de paginación
                    rx.cond(
                        AdminDashboardState.registro_filtered.length() > AdminDashboardState.items_per_page_registro,
                        rx.box(
                            rx.hstack(
                                rx.text(
                                    rx.cond(
                                        AdminDashboardState.registro_filtered.length() > 0,
                                        rx.cond(
                                            AdminDashboardState.current_page_registro == 1,
                                            "Mostrando 1 a " + rx.cond(
                                                AdminDashboardState.items_per_page_registro > AdminDashboardState.registro_filtered.length(),
                                                AdminDashboardState.registro_filtered.length().to(str),
                                                AdminDashboardState.items_per_page_registro.to(str)
                                            ) + " de " + AdminDashboardState.registro_filtered.length().to(str) + " resultados",
                                            "Mostrando " + ((AdminDashboardState.current_page_registro - 1) * AdminDashboardState.items_per_page_registro + 1).to(str) + " a " + rx.cond(
                                                AdminDashboardState.current_page_registro * AdminDashboardState.items_per_page_registro > AdminDashboardState.registro_filtered.length(),
                                                AdminDashboardState.registro_filtered.length().to(str),
                                                (AdminDashboardState.current_page_registro * AdminDashboardState.items_per_page_registro).to(str)
                                            ) + " de " + AdminDashboardState.registro_filtered.length().to(str) + " resultados"
                                        ),
                                        "Mostrando 0 a 0 de 0 resultados"
                                    ),
                                    size="2",
                                    color="#64748b",
                                    font_weight="500",
                                    flex_shrink=0,
                                    margin_right="13rem",
                                ),
                                rx.spacer(),
                                rx.box(
                                    render_pagination_registro(),
                                    flex_shrink=0,
                                    margin_left="0.5rem",
                                ),
                                width="100%",
                                align="center",
                                spacing="6",
                                wrap="wrap",
                            ),
                            padding="1.5rem 1rem",
                            border_top="1px solid #e2e8f0",
                            background="#f8fafc",
                        ),
                        rx.box(height="1rem")
                    ),
                    spacing="0",
                    width="100%"
                )
            ),
            width="100%"
        )

    # ==================== TABLA DE SOLICITUDES CON PAGINACIÓN UNIFICADA ====================
    def solicitudes_table() -> rx.Component:
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
            observacion_cell = rx.cond(
                solicitud["Observacion"] == "",
                rx.text("-", color="#94a3b8", font_style="italic", style={"white_space": "nowrap", "overflow": "hidden", "text_overflow": "ellipsis"}),
                rx.text(solicitud["Observacion"], color="#1e293b", style={"white_space": "nowrap", "overflow": "hidden", "text_overflow": "ellipsis"})
            )
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

        # --- Botón de página individual ---
        def create_page_button_solicitudes(page_num: int):
            return rx.button(
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
                        "_hover": {"background": "#115e59"},
                        "flex_shrink": 0,
                        "min_width": "32px",
                        "padding": "0 8px",
                    },
                    {
                        "background": "white",
                        "border": "1px solid #e2e8f0",
                        "color": "#1e293b",
                        "_hover": {
                            "background": "#f8fafc",
                            "border": "1px solid #cbd5e1"
                        },
                        "flex_shrink": 0,
                        "min_width": "32px",
                        "padding": "0 8px",
                    }
                )
            )

        # --- Controles de paginación (estilo unificado) ---
        def render_pagination_solicitudes():
            return rx.hstack(
                # Botón anterior
                rx.button(
                    rx.icon("chevron-left", size=16),
                    on_click=AdminDashboardState.previous_page_solicitudes,
                    variant="soft",
                    size="2",
                    is_disabled=AdminDashboardState.current_page_solicitudes == 1,
                    style={
                        "background": "white",
                        "border": "1px solid #e2e8f0",
                        "color": "#1e293b",
                        "flex_shrink": 0,
                        "min_width": "32px",
                        "padding": "0 8px",
                    }
                ),
                # Contenedor de números
                rx.box(
                    rx.hstack(
                        # Primera página + "..." si estamos lejos del inicio
                        rx.cond(
                            (AdminDashboardState.current_page_solicitudes > 3) &
                            (AdminDashboardState.total_pages_solicitudes > 4),
                            rx.hstack(
                                create_page_button_solicitudes(1),
                                rx.text("...", size="2", color="#64748b", padding_x="1"),
                                spacing="1",
                                flex_shrink=0,
                            ),
                        ),
                        # Páginas del rango calculado (máximo 4)
                        rx.cond(
                            AdminDashboardState.page_numbers_solicitudes.length() > 0,
                            rx.hstack(
                                rx.foreach(
                                    AdminDashboardState.page_numbers_solicitudes,
                                    create_page_button_solicitudes
                                ),
                                spacing="1",
                                wrap="nowrap",
                                flex_shrink=0,
                            ),
                            rx.text(
                                f"Pág. {AdminDashboardState.current_page_solicitudes}",
                                size="2",
                                color="#64748b",
                                padding_x="2",
                                flex_shrink=0,
                            ),
                        ),
                        # Última página + "..." si estamos lejos del final
                        rx.cond(
                            (AdminDashboardState.current_page_solicitudes < AdminDashboardState.total_pages_solicitudes - 2) &
                            (AdminDashboardState.total_pages_solicitudes > 4),
                            rx.hstack(
                                rx.text("...", size="2", color="#64748b", padding_x="1"),
                                create_page_button_solicitudes(AdminDashboardState.total_pages_solicitudes),
                                spacing="1",
                                flex_shrink=0,
                            ),
                        ),
                        spacing="1",
                        wrap="nowrap",
                        align="center",
                    ),
                    overflow_x="auto",
                    flex_grow=0,
                    flex_shrink=1,
                    max_width="100%",
                ),
                # Botón siguiente
                rx.button(
                    rx.hstack(
                        rx.icon("chevron-right", size=16),
                        width="100%",
                        spacing="0",
                        justify="end",
                        align="end",
                    ),
                    on_click=AdminDashboardState.next_page_solicitudes,
                    variant="soft",
                    size="2",
                    is_disabled=AdminDashboardState.current_page_solicitudes == AdminDashboardState.total_pages_solicitudes,
                    style={
                        "background": "white",
                        "border": "1px solid #e2e8f0",
                        "color": "#1e293b",
                        "flex_shrink": 0,
                        "min_width": "32px",
                        "padding": "0 8px",
                    }
                ),
                spacing="2",
                wrap="nowrap",
                align="center",
                justify="end",
                width="100%",
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
                            "max_height": "600px",
                            "height": "auto",
                            "overflow_y": "auto",
                            "border": "1px solid #e2e8f0",
                            "border_radius": "10px",
                            "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                        }
                    ),
                    # Controles de paginación
                    rx.cond(
                        AdminDashboardState.solicitudes_pendientes.length() > AdminDashboardState.items_per_page_solicitudes,
                        rx.box(
                            rx.hstack(
                                rx.text(
                                    rx.cond(
                                        AdminDashboardState.solicitudes_pendientes.length() > 0,
                                        rx.cond(
                                            AdminDashboardState.current_page_solicitudes == 1,
                                            "Mostrando 1 a " + rx.cond(
                                                AdminDashboardState.items_per_page_solicitudes > AdminDashboardState.solicitudes_pendientes.length(),
                                                AdminDashboardState.solicitudes_pendientes.length().to(str),
                                                AdminDashboardState.items_per_page_solicitudes.to(str)
                                            ) + " de " + AdminDashboardState.solicitudes_pendientes.length().to(str) + " resultados",
                                            "Mostrando " + ((AdminDashboardState.current_page_solicitudes - 1) * AdminDashboardState.items_per_page_solicitudes + 1).to(str) + " a " + rx.cond(
                                                AdminDashboardState.current_page_solicitudes * AdminDashboardState.items_per_page_solicitudes > AdminDashboardState.solicitudes_pendientes.length(),
                                                AdminDashboardState.solicitudes_pendientes.length().to(str),
                                                (AdminDashboardState.current_page_solicitudes * AdminDashboardState.items_per_page_solicitudes).to(str)
                                            ) + " de " + AdminDashboardState.solicitudes_pendientes.length().to(str) + " resultados"
                                        ),
                                        "Mostrando 0 a 0 de 0 resultados"
                                    ),
                                    size="2",
                                    color="#64748b",
                                    font_weight="500",
                                    flex_shrink=0,
                                    margin_right="8rem",
                                ),
                                rx.spacer(),
                                rx.box(
                                    render_pagination_solicitudes(),
                                    flex_shrink=0,
                                    margin_left="0.5rem",
                                ),
                                width="100%",
                                align="center",
                                spacing="6",
                                wrap="wrap",
                            ),
                            padding="1.5rem 1rem",
                            border_top="1px solid #e2e8f0",
                            background="#f8fafc",
                        ),
                        rx.box(height="1rem")
                    ),
                    spacing="0",
                    width="100%"
                )
            ),
            width="100%"
        )

    # ==================== DIÁLOGOS (sin cambios) ====================
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

    # ==================== CONTENIDO DE ALMACÉN (sin cambios) ====================
    def almacen_content():
        return rx.vstack(
            rx.box(
                rx.hstack(
                    rx.vstack(
                        rx.heading("📦 Productos en Almacén", size="5", color="#1e293b"),
                        rx.text("Visualización de todos los productos disponibles", size="2", color="#64748b"),
                        align="start",
                        spacing="1"
                    ),
                    rx.spacer(),
                    rx.badge(
                        f"{AlmacenViewState.total_productos} productos",
                        color_scheme="blue",
                        variant="soft",
                        size="2"
                    ),
                    width="100%",
                    align="center"
                ),
                width="100%",
                padding_bottom="1.5rem",
                border_bottom="1px solid #e2e8f0",
                margin_bottom="1.5rem"
            ),
            almacen_readonly_table(),
            spacing="3",
            align="start",
            width="100%"
        )

    # ==================== CONTENIDO PRINCIPAL DEL DASHBOARD ====================
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
                            "📦 Productos en Almacén", 
                            value="almacen",
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
                    # Pestaña Solicitudes
                    rx.tabs.content(
                        rx.vstack(
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
                                                "min_width": "0"
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
                    # Pestaña Registros
                    rx.tabs.content(
                        rx.vstack(
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
                    # Pestaña Almacén
                    rx.tabs.content(
                        almacen_content(),
                        value="almacen",
                        style={"padding": "1.5rem 0"}
                    ),
                    # Pestaña Perfil
                    rx.tabs.content(
                        rx.vstack(
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

                aprobar_dialog(),
                rechazar_dialog(),

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
                padding=["1rem", "1.5rem", "2rem", "3rem"],
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