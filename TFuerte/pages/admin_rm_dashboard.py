import reflex as rx
from TFuerte.state.admin_rm_state import AdminRMState
from TFuerte.components.navbar import navbar
from TFuerte.routes import Route

@rx.page(
    route=Route.ADMIN_RM_DASHBOARD.value,
    title="Dashboard - Administración RM",
    on_load=[AdminRMState.reset_loading_states, AdminRMState.load_data, AdminRMState.load_data_fin]
)
def admin_rm_dashboard() -> rx.Component:
    """Dashboard para Administrador/Presidente (Maikel)"""
    
    def estado_badge_rm(estado: str):
        return rx.cond(
            estado == "aprobado_tecnica",
            rx.badge("APROBADO TÉCNICA", color_scheme="blue", variant="soft"),
            rx.cond(
                estado == "aprobado_admin",
                rx.badge("APROBADO ADMIN", color_scheme="green", variant="soft"),
                rx.badge("RECHAZADA", color_scheme="red", variant="soft")
            )
        )
    
    def estado_badge_fin(estado: str):
        return rx.cond(
            estado == "aprobado_revfin",
            rx.badge("APROBADO REV. FIN", color_scheme="blue", variant="soft"),
            rx.cond(
                estado == "completada",
                rx.badge("COMPLETADA", color_scheme="green", variant="soft"),
                rx.badge("RECHAZADA", color_scheme="red", variant="soft")
            )
        )
    
    # ==================== TABLA DE RECURSOS CON PAGINACIÓN ====================
    def solicitudes_table() -> rx.Component:
        """Tabla de solicitudes RM pendientes con paginación."""
        
        # Botón de página individual
        def create_page_button_recursos(page_num: int):
            return rx.button(
                rx.text(page_num, size="2", font_weight="500"),
                on_click=lambda: AdminRMState.go_to_page_recursos(page_num),
                variant="soft",
                size="2",
                style=rx.cond(
                    AdminRMState.recursos_current_page == page_num,
                    {
                        "background": "#7c3aed",
                        "color": "white",
                        "border": "1px solid #7c3aed",
                        "_hover": {"background": "#6d28d9"},
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
        
        def render_pagination_recursos():
            return rx.hstack(
                rx.button(
                    rx.icon("chevron-left", size=16),
                    on_click=AdminRMState.previous_page_recursos,
                    variant="soft",
                    size="2",
                    is_disabled=AdminRMState.recursos_current_page == 1,
                    style={
                        "background": "white",
                        "border": "1px solid #e2e8f0",
                        "color": "#1e293b",
                        "flex_shrink": 0,
                        "min_width": "32px",
                        "padding": "0 8px",
                    }
                ),
                rx.box(
                    rx.hstack(
                        rx.cond(
                            (AdminRMState.recursos_current_page > 3) & (AdminRMState.recursos_total_pages > 4),
                            rx.hstack(
                                create_page_button_recursos(1),
                                rx.text("...", size="2", color="#64748b", padding_x="1"),
                                spacing="1",
                                flex_shrink=0,
                            ),
                        ),
                        rx.cond(
                            AdminRMState.recursos_page_numbers.length() > 0,
                            rx.hstack(
                                rx.foreach(
                                    AdminRMState.recursos_page_numbers,
                                    create_page_button_recursos
                                ),
                                spacing="1",
                                wrap="nowrap",
                                flex_shrink=0,
                            ),
                            rx.text(
                                f"Pág. {AdminRMState.recursos_current_page}",
                                size="2",
                                color="#64748b",
                                padding_x="2",
                                flex_shrink=0,
                            ),
                        ),
                        rx.cond(
                            (AdminRMState.recursos_current_page < AdminRMState.recursos_total_pages - 2) & (AdminRMState.recursos_total_pages > 4),
                            rx.hstack(
                                rx.text("...", size="2", color="#64748b", padding_x="1"),
                                create_page_button_recursos(AdminRMState.recursos_total_pages),
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
                rx.button(
                    rx.hstack(
                        rx.icon("chevron-right", size=16),
                        width="100%",
                        spacing="0",
                        justify="end",
                        align="end",
                    ),
                    on_click=AdminRMState.next_page_recursos,
                    variant="soft",
                    size="2",
                    is_disabled=AdminRMState.recursos_current_page == AdminRMState.recursos_total_pages,
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
        
        def solicitud_row(solicitud):
            fecha_aprobacion = rx.cond(
                (solicitud.get("fecha_aprobacion_tecnica") != None) & (solicitud.get("fecha_aprobacion_tecnica") != ""),
                rx.text(solicitud.get("fecha_aprobacion_tecnica"), color="#070E0C"),
                rx.text("-", color="#94a3b8", font_style="italic")
            )
            
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
                        solicitud.get("Descripcion", "-"),
                        color="#070E0C",
                        style={
                            "max_width": "150px",
                            "overflow": "hidden",
                            "text_overflow": "ellipsis",
                            "white_space": "nowrap"
                        }
                    ),
                    style={"padding": "8px 4px", "min_width": "150px"}
                ),
                rx.table.cell(
                    rx.text(solicitud.get("Cantidad", "-"), color="#070E0C"),
                    style={"padding": "8px 4px", "min_width": "80px"}
                ),
                rx.table.cell(
                    rx.text(solicitud.get("UM", "-"), color="#070E0C"),
                    style={"padding": "8px 4px", "min_width": "80px"}
                ),
                rx.table.cell(
                    fecha_aprobacion,
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                rx.table.cell(
                    estado_badge_rm(solicitud.get("estado", "aprobado_tecnica")),
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                rx.table.cell(
                    rx.box(
                        rx.vstack(
                            rx.button(
                                "✅ Aprobar",
                                on_click=lambda: AdminRMState.open_aprobar_dialog(solicitud),
                                color_scheme="green",
                                size="1",
                                variant="solid",
                                width="100%"
                            ),
                            rx.button(
                                "❌ Rechazar",
                                on_click=lambda: AdminRMState.open_rechazar_dialog(solicitud),
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
            "background": "#7c3aed",
            "color": "white",
            "font_weight": "600",
            "padding": "12px 4px",
            "text_align": "left",
            "white_space": "nowrap"
        }
        
        return rx.cond(
            AdminRMState.solicitudes_pendientes.length() == 0,
            rx.center(
                rx.vstack(
                    rx.icon("file_text", size=32, color="#cbd5e1"),
                    rx.text("No hay solicitudes pendientes de aprobación", size="3", color="#64748b"),
                    spacing="2",
                    align="center"
                ),
                padding="3rem",
                width="100%"
            ),
            rx.vstack(
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
                                    rx.table.column_header_cell("Aprobado Técnica", style=header_style),
                                    rx.table.column_header_cell("Estado", style=header_style),
                                    rx.table.column_header_cell("Acciones", style=header_style),
                                )
                            ),
                            rx.table.body(
                                rx.foreach(
                                    AdminRMState.recursos_paginated,
                                    solicitud_row
                                )
                            ),
                            style={
                                "width": "100%",
                                "min_width": "1100px",
                                "table_layout": "auto"
                            }
                        ),
                        type="always",
                        scrollbars="horizontal",
                        style={
                            "width": "100%",
                            "max_height": "650px",
                            "height": "auto",
                            "overflow_y": "auto",
                            "border": "1px solid #e2e8f0",
                            "border_radius": "8px"
                        }
                    ),
                    width="100%",
                ),
                rx.cond(
                    AdminRMState.solicitudes_pendientes.length() > AdminRMState.recursos_items_per_page,
                    rx.box(
                        rx.hstack(
                            rx.text(
                                rx.cond(
                                    AdminRMState.solicitudes_pendientes.length() > 0,
                                    rx.cond(
                                        AdminRMState.recursos_current_page == 1,
                                        "Mostrando 1 a " + rx.cond(
                                            AdminRMState.recursos_items_per_page > AdminRMState.solicitudes_pendientes.length(),
                                            AdminRMState.solicitudes_pendientes.length().to(str),
                                            AdminRMState.recursos_items_per_page.to(str)
                                        ) + " de " + AdminRMState.solicitudes_pendientes.length().to(str) + " resultados",
                                        "Mostrando " + ((AdminRMState.recursos_current_page - 1) * AdminRMState.recursos_items_per_page + 1).to(str) + " a " + rx.cond(
                                            AdminRMState.recursos_current_page * AdminRMState.recursos_items_per_page > AdminRMState.solicitudes_pendientes.length(),
                                            AdminRMState.solicitudes_pendientes.length().to(str),
                                            (AdminRMState.recursos_current_page * AdminRMState.recursos_items_per_page).to(str)
                                        ) + " de " + AdminRMState.solicitudes_pendientes.length().to(str) + " resultados"
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
                                render_pagination_recursos(),
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
        )
    
    # ==================== TABLA DE FINANCIAMIENTO CON PAGINACIÓN ====================
    def solicitudes_fin_table() -> rx.Component:
        """Tabla de solicitudes de financiamiento pendientes con paginación."""
        
        def create_page_button_fin(page_num: int):
            return rx.button(
                rx.text(page_num, size="2", font_weight="500"),
                on_click=lambda: AdminRMState.go_to_page_fin(page_num),
                variant="soft",
                size="2",
                style=rx.cond(
                    AdminRMState.fin_current_page == page_num,
                    {
                        "background": "#059669",
                        "color": "white",
                        "border": "1px solid #059669",
                        "_hover": {"background": "#047857"},
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
        
        def render_pagination_fin():
            return rx.hstack(
                rx.button(
                    rx.icon("chevron-left", size=16),
                    on_click=AdminRMState.previous_page_fin,
                    variant="soft",
                    size="2",
                    is_disabled=AdminRMState.fin_current_page == 1,
                    style={
                        "background": "white",
                        "border": "1px solid #e2e8f0",
                        "color": "#1e293b",
                        "flex_shrink": 0,
                        "min_width": "32px",
                        "padding": "0 8px",
                    }
                ),
                rx.box(
                    rx.hstack(
                        rx.cond(
                            (AdminRMState.fin_current_page > 3) & (AdminRMState.fin_total_pages > 4),
                            rx.hstack(
                                create_page_button_fin(1),
                                rx.text("...", size="2", color="#64748b", padding_x="1"),
                                spacing="1",
                                flex_shrink=0,
                            ),
                        ),
                        rx.cond(
                            AdminRMState.fin_page_numbers.length() > 0,
                            rx.hstack(
                                rx.foreach(
                                    AdminRMState.fin_page_numbers,
                                    create_page_button_fin
                                ),
                                spacing="1",
                                wrap="nowrap",
                                flex_shrink=0,
                            ),
                            rx.text(
                                f"Pág. {AdminRMState.fin_current_page}",
                                size="2",
                                color="#64748b",
                                padding_x="2",
                                flex_shrink=0,
                            ),
                        ),
                        rx.cond(
                            (AdminRMState.fin_current_page < AdminRMState.fin_total_pages - 2) & (AdminRMState.fin_total_pages > 4),
                            rx.hstack(
                                rx.text("...", size="2", color="#64748b", padding_x="1"),
                                create_page_button_fin(AdminRMState.fin_total_pages),
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
                rx.button(
                    rx.hstack(
                        rx.icon("chevron-right", size=16),
                        width="100%",
                        spacing="0",
                        justify="end",
                        align="end",
                    ),
                    on_click=AdminRMState.next_page_fin,
                    variant="soft",
                    size="2",
                    is_disabled=AdminRMState.fin_current_page == AdminRMState.fin_total_pages,
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
        
        def solicitud_row(solicitud):
            return rx.table.row(
                rx.table.cell(
                    rx.text(solicitud["numero_solicitud"], font_weight="600", color="#070E0C"),
                    style={"padding": "8px 4px"}
                ),
                rx.table.cell(
                    rx.text(solicitud.get("Area solicitante", "-"), color="#070E0C"),
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                rx.table.cell(
                    rx.text(solicitud.get("Fecha", "-"), color="#070E0C"),
                    style={"padding": "8px 4px", "min_width": "100px"}
                ),
                rx.table.cell(
                    rx.text(solicitud.get("Orden de trabajo", "-"), color="#070E0C"),
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                rx.table.cell(
                    rx.text(
                        f"{solicitud.get('num_recursos', 1)} productos",
                        color="#070E0C",
                    ),
                    style={"padding": "8px 4px", "min_width": "100px"}
                ),
                rx.table.cell(
                    rx.text(f"${solicitud.get('Total', 0):.2f}", color="#070E0C", font_weight="600"),
                    style={"padding": "8px 4px", "min_width": "100px"}
                ),
                rx.table.cell(
                    estado_badge_fin(solicitud.get("estado", "aprobado_revfin")),
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                rx.table.cell(
                    rx.box(
                        rx.vstack(
                            rx.button(
                                "✅ Aprobar",
                                on_click=lambda: AdminRMState.open_aprobar_dialog_fin(solicitud),
                                color_scheme="green",
                                size="1",
                                variant="solid",
                                width="100%"
                            ),
                            rx.button(
                                "❌ Rechazar",
                                on_click=lambda: AdminRMState.open_rechazar_dialog_fin(solicitud),
                                color_scheme="red",
                                size="1",
                                variant="solid",
                                width="100%"
                            ),
                            rx.button(
                                "📄 Generar Word",
                                on_click=lambda: AdminRMState.open_generar_dialog_fin(solicitud),
                                color_scheme="blue",
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
            AdminRMState.solicitudes_fin_pendientes.length() == 0,
            rx.center(
                rx.vstack(
                    rx.icon("dollar_sign", size=32, color="#cbd5e1"),
                    rx.text("No hay solicitudes de financiamiento pendientes", size="3", color="#64748b"),
                    spacing="2",
                    align="center"
                ),
                padding="3rem",
                width="100%"
            ),
            rx.vstack(
                rx.box(
                    rx.scroll_area(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("N° Solicitud", style=header_style),
                                    rx.table.column_header_cell("Área", style=header_style),
                                    rx.table.column_header_cell("Fecha", style=header_style),
                                    rx.table.column_header_cell("Orden Trabajo", style=header_style),
                                    rx.table.column_header_cell("Productos", style=header_style),
                                    rx.table.column_header_cell("Total", style=header_style),
                                    rx.table.column_header_cell("Estado", style=header_style),
                                    rx.table.column_header_cell("Acciones", style=header_style),
                                )
                            ),
                            rx.table.body(
                                rx.foreach(
                                    AdminRMState.financiamiento_paginated,
                                    solicitud_row
                                )
                            ),
                            style={
                                "width": "100%",
                                "min_width": "900px",
                                "table_layout": "auto"
                            }
                        ),
                        type="always",
                        scrollbars="horizontal",
                        style={
                            "width": "100%",
                            "max_height": "700px",
                            "height": "auto",
                            "overflow_y": "auto",
                            "border": "1px solid #e2e8f0",
                            "border_radius": "8px"
                        }
                    ),
                    width="100%",
                ),
                rx.cond(
                    AdminRMState.solicitudes_fin_pendientes.length() > AdminRMState.fin_items_per_page,
                    rx.box(
                        rx.hstack(
                            rx.text(
                                rx.cond(
                                    AdminRMState.solicitudes_fin_pendientes.length() > 0,
                                    rx.cond(
                                        AdminRMState.fin_current_page == 1,
                                        "Mostrando 1 a " + rx.cond(
                                            AdminRMState.fin_items_per_page > AdminRMState.solicitudes_fin_pendientes.length(),
                                            AdminRMState.solicitudes_fin_pendientes.length().to(str),
                                            AdminRMState.fin_items_per_page.to(str)
                                        ) + " de " + AdminRMState.solicitudes_fin_pendientes.length().to(str) + " resultados",
                                        "Mostrando " + ((AdminRMState.fin_current_page - 1) * AdminRMState.fin_items_per_page + 1).to(str) + " a " + rx.cond(
                                            AdminRMState.fin_current_page * AdminRMState.fin_items_per_page > AdminRMState.solicitudes_fin_pendientes.length(),
                                            AdminRMState.solicitudes_fin_pendientes.length().to(str),
                                            (AdminRMState.fin_current_page * AdminRMState.fin_items_per_page).to(str)
                                        ) + " de " + AdminRMState.solicitudes_fin_pendientes.length().to(str) + " resultados"
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
                                render_pagination_fin(),
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
        )
    
    # ==================== DIÁLOGOS (sin cambios) ====================
    def aprobar_dialog():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Aprobar Solicitud", color="#212121"),
                rx.dialog.description(
                    rx.cond(
                        (AdminRMState.selected_solicitud["id"] != "") & (AdminRMState.selected_solicitud["id"] != None),
                        rx.hstack(
                            rx.text("¿Aprobar solicitud #"),
                            rx.text(AdminRMState.selected_solicitud["id"], font_weight="600"),
                            rx.text("?"),
                            spacing="1"
                        ),
                        rx.text("Aprobar solicitud")
                    ),
                    color="#212121"
                ),
                rx.cond(
                    (AdminRMState.selected_solicitud["id"] != "") & (AdminRMState.selected_solicitud["id"] != None),
                    rx.vstack(
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("Solicitante:", size="2", color="#64748b", width="100px"),
                                    rx.cond(
                                        AdminRMState.selected_solicitud.get("solicitante_id") != "",
                                        rx.hstack(
                                            rx.text("ID: ", size="2", color="#1e293b"),
                                            rx.text(AdminRMState.selected_solicitud.get("solicitante_id"), size="2", color="#1e293b"),
                                            spacing="0"
                                        ),
                                        rx.text("N/A", size="2", color="#1e293b")
                                    ),
                                    spacing="3",
                                    align="center"
                                ),
                                rx.hstack(
                                    rx.text("Descripción:", size="2", color="#64748b", width="100px"),
                                    rx.text(
                                        AdminRMState.selected_solicitud.get("Descripcion", "Sin descripción"),
                                        size="2", 
                                        color="#1e293b",
                                        font_weight="500"
                                    ),
                                    spacing="3",
                                    align="center"
                                ),
                                rx.hstack(
                                    rx.text("Aprobado por:", size="2", color="#64748b", width="100px"),
                                    rx.text(
                                        "Área Técnica (Alexander)", 
                                        size="2", 
                                        color="#1e293b",
                                        font_weight="500"
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
                        on_click=AdminRMState.aprobar_solicitud,
                        color_scheme="green",
                        size="2",
                        variant="solid",
                        style={
                            "background": "linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)"
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
            open=AdminRMState.show_aprobar_dialog,
            on_open_change=AdminRMState.set_show_aprobar_dialog,
        )
    
    def rechazar_dialog():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Rechazar Solicitud", color="#212121"),
                rx.dialog.description(
                    rx.cond(
                        AdminRMState.selected_solicitud["id"] != "",
                        rx.hstack(
                            rx.text("¿Rechazar solicitud #"),
                            rx.text(AdminRMState.selected_solicitud["id"], font_weight="600"),
                            rx.text("?"),
                            spacing="1"
                        ),
                        rx.text("¿Rechazar solicitud?")
                    ),
                    color="#212121"
                ),
                rx.vstack(
                    rx.text(
                        "Por favor, proporciona el motivo del rechazo (opcional):",
                        size="2",
                        color="#64748b"
                    ),
                    rx.text_area(
                        placeholder="Motivo del rechazo...",
                        value=AdminRMState.motivo_rechazo,
                        on_change=AdminRMState.set_motivo_rechazo,
                        width="100%",
                        size="2",
                        min_height="100px"
                    ),
                    spacing="2",
                    width="100%",
                    margin_y="1rem"
                ),
                rx.vstack(
                    rx.dialog.close(
                        rx.button("Cancelar", variant="soft", size="2"),
                    ),
                    rx.button(
                        "❌ Rechazar",
                        on_click=AdminRMState.rechazar_solicitud,
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
                max_width="500px",
                style={
                    "background": "white",
                    "border_radius": "12px",
                    "box_shadow": "0 20px 25px -5px rgba(0, 0, 0, 0.1)"
                }
            ),
            open=AdminRMState.show_rechazar_dialog,
            on_open_change=AdminRMState.set_show_rechazar_dialog,
        )
    
    def aprobar_dialog_fin():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Aprobar Solicitud de Financiamiento", color="#212121"),
                rx.dialog.description(
                    rx.cond(
                        AdminRMState.selected_solicitud_fin["numero_solicitud"] != "",
                        rx.hstack(
                            rx.text("¿Aprobar solicitud #"),
                            rx.text(AdminRMState.selected_solicitud_fin["numero_solicitud"], font_weight="600"),
                            rx.text("?"),
                            spacing="1"
                        ),
                        rx.text("Aprobar solicitud")
                    ),
                    color="#212121"
                ),
                rx.cond(
                    AdminRMState.selected_solicitud_fin["numero_solicitud"] != "",
                    rx.vstack(
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("Área:", size="2", color="#64748b", width="100px"),
                                    rx.text(
                                        AdminRMState.selected_solicitud_fin.get("Area solicitante", "-"), 
                                        size="2", 
                                        color="#1e293b",
                                        font_weight="500"
                                    ),
                                    spacing="3",
                                    align="center"
                                ),
                                rx.hstack(
                                    rx.text("Total:", size="2", color="#64748b", width="100px"),
                                    rx.text(
                                        f"${AdminRMState.selected_solicitud_fin.get('Total', 0):.2f}",
                                        size="2", 
                                        color="#1e293b",
                                        font_weight="600"
                                    ),
                                    spacing="3",
                                    align="center"
                                ),
                                rx.hstack(
                                    rx.text("Productos:", size="2", color="#64748b", width="100px"),
                                    rx.text(
                                        f"{AdminRMState.selected_solicitud_fin.get('num_recursos', 1)} productos",
                                        size="2", 
                                        color="#1e293b",
                                        font_weight="500"
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
                        on_click=AdminRMState.aprobar_solicitud_fin,
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
            open=AdminRMState.show_aprobar_dialog_fin,
            on_open_change=AdminRMState.set_show_aprobar_dialog_fin,
        )
    
    def rechazar_dialog_fin():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Rechazar Solicitud de Financiamiento", color="#212121"),
                rx.dialog.description(
                    rx.cond(
                        AdminRMState.selected_solicitud_fin["numero_solicitud"] != "",
                        rx.hstack(
                            rx.text("¿Rechazar solicitud #"),
                            rx.text(AdminRMState.selected_solicitud_fin["numero_solicitud"], font_weight="600"),
                            rx.text("?"),
                            spacing="1"
                        ),
                        rx.text("Rechazar solicitud")
                    ),
                    color="#212121"
                ),
                rx.vstack(
                    rx.text(
                        "Por favor, proporciona el motivo del rechazo (opcional):",
                        size="2",
                        color="#64748b"
                    ),
                    rx.text_area(
                        placeholder="Motivo del rechazo...",
                        value=AdminRMState.motivo_rechazo_fin,
                        on_change=AdminRMState.set_motivo_rechazo_fin,
                        width="100%",
                        size="2",
                        min_height="100px"
                    ),
                    spacing="2",
                    width="100%",
                    margin_y="1rem"
                ),
                rx.vstack(
                    rx.dialog.close(
                        rx.button("Cancelar", variant="soft", size="2"),
                    ),
                    rx.button(
                        "❌ Rechazar",
                        on_click=AdminRMState.rechazar_solicitud_fin,
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
                max_width="500px",
                style={
                    "background": "white",
                    "border_radius": "12px",
                    "box_shadow": "0 20px 25px -5px rgba(0, 0, 0, 0.1)"
                }
            ),
            open=AdminRMState.show_rechazar_dialog_fin,
            on_open_change=AdminRMState.set_show_rechazar_dialog_fin,
        )
    
    def generar_dialog_fin():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Generar Documento de Financiamiento", color="#212121"),
                rx.dialog.description(
                    rx.cond(
                        AdminRMState.selected_solicitud_fin["numero_solicitud"] != "",
                        rx.hstack(
                            rx.text("¿Generar documento para solicitud #"),
                            rx.text(AdminRMState.selected_solicitud_fin["numero_solicitud"], font_weight="600"),
                            rx.text("?"),
                            spacing="1"
                        ),
                        rx.text("Generar documento")
                    ),
                    color="#212121"
                ),
                rx.cond(
                    AdminRMState.selected_solicitud_fin["numero_solicitud"] != "",
                    rx.vstack(
                        rx.text(
                            "Se generará un documento Word con todos los productos de esta solicitud.",
                            size="2",
                            color="#64748b"
                        ),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("Total:", size="2", color="#64748b", width="100px"),
                                    rx.text(
                                        f"${AdminRMState.selected_solicitud_fin.get('Total', 0):.2f}",
                                        size="2", 
                                        color="#1e293b",
                                        font_weight="600"
                                    ),
                                    spacing="3",
                                    align="center"
                                ),
                                rx.hstack(
                                    rx.text("Productos:", size="2", color="#64748b", width="100px"),
                                    rx.text(
                                        f"{AdminRMState.selected_solicitud_fin.get('num_recursos', 1)} productos",
                                        size="2", 
                                        color="#1e293b",
                                        font_weight="500"
                                    ),
                                    spacing="3",
                                    align="center"
                                ),
                                spacing="3",
                                align="start",
                                padding="1rem",
                                border_radius="md",
                                background="#f0f9ff",
                                border="1px solid #bae6fd",
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
                        "📄 Generar Word",
                        on_click=AdminRMState.generar_documento_fin,
                        color_scheme="blue",
                        size="2",
                        variant="solid",
                        loading=AdminRMState.loading_fin,
                        style={
                            "background": "linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%)"
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
            open=AdminRMState.show_generar_dialog_fin,
            on_open_change=AdminRMState.set_show_generar_dialog_fin,
        )
    
    def dashboard_content():
        return rx.box(
            navbar("Panel de Administración RM"),
            rx.vstack(
                # Encabezado responsivo
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.vstack(
                                rx.heading(
                                    "👑 Panel de Administración",
                                    size="7",
                                    color="#1e293b",
                                    style={
                                        "background": "linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)",
                                        "background_clip": "text",
                                        "webkit_background_clip": "text",
                                        "color": "transparent",
                                        "font_weight": "800",
                                    }
                                ),
                                rx.text(
                                    "Gestión de solicitudes de recursos y financiamiento",
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
                                rx.hstack(
                                    rx.text(AdminRMState.solicitudes_count),
                                    rx.text(" RM pendientes"),
                                    spacing="0"
                                ),
                                color_scheme="purple",
                                variant="soft",
                                size="2"
                            ),
                            rx.badge(
                                rx.hstack(
                                    rx.text(AdminRMState.solicitudes_fin_count),
                                    rx.text(" FIN pendientes"),
                                    spacing="0"
                                ),
                                color_scheme="green",
                                variant="soft",
                                size="2"
                            ),
                            rx.button(
                                "🔄 Actualizar",
                                on_click=[AdminRMState.load_data, AdminRMState.load_data_fin],
                                loading=AdminRMState.loading | AdminRMState.loading_fin,
                                variant="soft",
                                size="2"
                            ),
                            rx.button(
                                "🚪 Cerrar Sesión",
                                on_click=AdminRMState.sign_out,
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
                
                # Tabs
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger("📦 Recursos y Materiales", value="recursos", color="#1e293b"),
                        rx.tabs.trigger("💰 Financiamiento", value="financiamiento", color="#1e293b"),
                    ),
                    
                    # Pestaña de Recursos
                    rx.tabs.content(
                        rx.vstack(
                            # Búsqueda
                            rx.box(
                                rx.hstack(
                                    rx.input(
                                        placeholder="Buscar solicitudes RM...",
                                        on_change=AdminRMState.filter_solicitudes,
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
                            
                            # Tabla
                            rx.cond(
                                AdminRMState.loading,
                                rx.center(
                                    rx.vstack(
                                        rx.spinner(size="3", color="#7c3aed"),
                                        rx.text("Cargando solicitudes RM...", margin_top="1rem", color="#64748b"),
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
                                AdminRMState.search_value != "",
                                rx.box(
                                    rx.hstack(
                                        rx.icon("search", size=16, color="#7c3aed"),
                                        rx.text(
                                            f"Filtrando por: '{AdminRMState.search_value}'",
                                            size="2",
                                            color="#64748b"
                                        ),
                                        rx.button(
                                            "Limpiar filtro",
                                            on_click=lambda: AdminRMState.filter_solicitudes(""),
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
                                    background="#faf5ff",
                                    border="1px solid #ddd6fe",
                                    margin_top="1rem",
                                ),
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        value="recursos",
                        style={"padding": "1.5rem 0"}
                    ),
                    
                    # Pestaña de Financiamiento
                    rx.tabs.content(
                        rx.vstack(
                            # Búsqueda
                            rx.box(
                                rx.hstack(
                                    rx.input(
                                        placeholder="Buscar solicitudes de financiamiento...",
                                        on_change=AdminRMState.filter_solicitudes_fin,
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
                            
                            # Tabla
                            rx.cond(
                                AdminRMState.loading_fin,
                                rx.center(
                                    rx.vstack(
                                        rx.spinner(size="3", color="#059669"),
                                        rx.text("Cargando solicitudes de financiamiento...", margin_top="1rem", color="#64748b"),
                                        spacing="3",
                                        align="center"
                                    ),
                                    height="300px", 
                                    width="100%",
                                ),
                                solicitudes_fin_table()
                            ),
                            
                            # Información de búsqueda
                            rx.cond(
                                AdminRMState.search_value_fin != "",
                                rx.box(
                                    rx.hstack(
                                        rx.icon("search", size=16, color="#059669"),
                                        rx.text(
                                            f"Filtrando por: '{AdminRMState.search_value_fin}'",
                                            size="2",
                                            color="#64748b"
                                        ),
                                        rx.button(
                                            "Limpiar filtro",
                                            on_click=lambda: AdminRMState.filter_solicitudes_fin(""),
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
                                    background="#f0fdf4",
                                    border="1px solid #bbf7d0",
                                    margin_top="1rem",
                                ),
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        value="financiamiento",
                        style={"padding": "1.5rem 0"}
                    ),
                    
                    default_value="recursos",
                    width="100%",
                ),
                
                # Diálogos
                aprobar_dialog(),
                rechazar_dialog(),
                aprobar_dialog_fin(),
                rechazar_dialog_fin(),
                generar_dialog_fin(),
                
                # Pie de página
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.text("© 2026 Sistema de Gestión de Recursos", 
                                   size="1", 
                                   color="#64748b"),
                            rx.spacer(),
                            rx.text(
                                "Administrador/Presidente - Maikel",
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
        AdminRMState.is_authenticated,
        dashboard_content(),
        rx.center(
            rx.vstack(
                rx.spinner(size="3", color="#7c3aed"),
                rx.text("Redirigiendo al login...", margin_top="1rem", color="#64748b"),
                rx.button(
                    "Ir al Login", 
                    on_click=lambda: rx.redirect(Route.ADMIN_RM_LOGIN.value), 
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