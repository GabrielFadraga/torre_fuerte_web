import reflex as rx
from TFuerte.state.financiamiento_state import FinanciamientoState
from TFuerte.components.navbar import navbar
from TFuerte.routes import Route

@rx.page(
    route=Route.REVFIN_DASHBOARD.value,
    title="Dashboard - Revisor Financiero",
    on_load=[FinanciamientoState.reset_loading_revfin, FinanciamientoState.load_data_revfin]
)
def revfin_dashboard() -> rx.Component:
    """Dashboard para Revisor Financiero"""
    
    def estado_badge_fin(estado: str):
        return rx.cond(
            estado == "pendiente_revfin",
            rx.badge("PENDIENTE", color_scheme="amber", variant="soft"),
            rx.cond(
                estado == "aprobado_revfin",
                rx.badge("APROBADO REV. FIN", color_scheme="green", variant="soft"),
                rx.badge("RECHAZADA", color_scheme="red", variant="soft")
            )
        )
    
    def solicitudes_table() -> rx.Component:
        """Tabla de solicitudes de financiamiento pendientes con paginación."""
        
        def create_page_button(page_num: int):
            return rx.button(
                rx.text(page_num, size="2", font_weight="500"),
                on_click=lambda: FinanciamientoState.go_to_page_revfin(page_num),
                variant="soft",
                size="2",
                style=rx.cond(
                    FinanciamientoState.revfin_current_page == page_num,
                    {
                        "background": "#0d9488",
                        "color": "white",
                        "border": "1px solid #0d9488",
                        "_hover": {"background": "#0f766e"},
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
        
        def render_pagination():
            return rx.hstack(
                rx.button(
                    rx.icon("chevron-left", size=16),
                    on_click=FinanciamientoState.previous_page_revfin,
                    variant="soft",
                    size="2",
                    is_disabled=FinanciamientoState.revfin_current_page == 1,
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
                            (FinanciamientoState.revfin_current_page > 3) & (FinanciamientoState.revfin_total_pages > 4),
                            rx.hstack(
                                create_page_button(1),
                                rx.text("...", size="2", color="#64748b", padding_x="1"),
                                spacing="1",
                                flex_shrink=0,
                            ),
                        ),
                        rx.cond(
                            FinanciamientoState.revfin_page_numbers.length() > 0,
                            rx.hstack(
                                rx.foreach(
                                    FinanciamientoState.revfin_page_numbers,
                                    create_page_button
                                ),
                                spacing="1",
                                wrap="nowrap",
                                flex_shrink=0,
                            ),
                            rx.text(
                                f"Pág. {FinanciamientoState.revfin_current_page}",
                                size="2",
                                color="#64748b",
                                padding_x="2",
                                flex_shrink=0,
                            ),
                        ),
                        rx.cond(
                            (FinanciamientoState.revfin_current_page < FinanciamientoState.revfin_total_pages - 2) & (FinanciamientoState.revfin_total_pages > 4),
                            rx.hstack(
                                rx.text("...", size="2", color="#64748b", padding_x="1"),
                                create_page_button(FinanciamientoState.revfin_total_pages),
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
                    on_click=FinanciamientoState.next_page_revfin,
                    variant="soft",
                    size="2",
                    is_disabled=FinanciamientoState.revfin_current_page == FinanciamientoState.revfin_total_pages,
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
                    rx.text(solicitud["id"], font_weight="600", color="#070E0C"),
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
                    rx.text(solicitud.get("Servicio", "-"), color="#070E0C"),
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                rx.table.cell(
                    rx.text(
                        solicitud.get("Descripcion", "-"),
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
                    rx.text(solicitud.get("Cantidad", "-"), color="#070E0C"),
                    style={"padding": "8px 4px", "min_width": "80px"}
                ),
                rx.table.cell(
                    rx.text(f"${solicitud.get('Precio unitario', 0):.2f}", color="#070E0C"),
                    style={"padding": "8px 4px", "min_width": "100px"}
                ),
                rx.table.cell(
                    rx.text(f"${solicitud.get('Total', 0):.2f}", color="#070E0C", font_weight="600"),
                    style={"padding": "8px 4px", "min_width": "100px"}
                ),
                rx.table.cell(
                    estado_badge_fin(solicitud.get("estado", "pendiente_revfin")),
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                rx.table.cell(
                    rx.box(
                        rx.vstack(
                            rx.button(
                                "✅ Aprobar",
                                on_click=lambda: FinanciamientoState.open_aprobar_dialog_revfin(solicitud),
                                color_scheme="green",
                                size="1",
                                variant="solid",
                                width="100%"
                            ),
                            rx.button(
                                "❌ Rechazar",
                                on_click=lambda: FinanciamientoState.open_rechazar_dialog_revfin(solicitud),
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
            "background": "#0d9488",
            "color": "white",
            "font_weight": "600",
            "padding": "12px 4px",
            "text_align": "left",
            "white_space": "nowrap"
        }
        
        return rx.cond(
            FinanciamientoState.solicitudes_pendientes_revfin.length() == 0,
            rx.center(
                rx.vstack(
                    rx.icon("dollar_sign", size=32, color="#cbd5e1"),
                    rx.text("No hay solicitudes pendientes", size="3", color="#64748b"),
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
                                    rx.table.column_header_cell("Área", style=header_style),
                                    rx.table.column_header_cell("Fecha", style=header_style),
                                    rx.table.column_header_cell("Servicio", style=header_style),
                                    rx.table.column_header_cell("Descripción", style=header_style),
                                    rx.table.column_header_cell("Cantidad", style=header_style),
                                    rx.table.column_header_cell("Precio Unit.", style=header_style),
                                    rx.table.column_header_cell("Total", style=header_style),
                                    rx.table.column_header_cell("Estado", style=header_style),
                                    rx.table.column_header_cell("Acciones", style=header_style),
                                )
                            ),
                            rx.table.body(
                                rx.foreach(
                                    FinanciamientoState.solicitudes_revfin_paginated,
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
                    FinanciamientoState.solicitudes_pendientes_revfin.length() > FinanciamientoState.revfin_items_per_page,
                    rx.box(
                        rx.hstack(
                            rx.text(
                                rx.cond(
                                    FinanciamientoState.solicitudes_pendientes_revfin.length() > 0,
                                    rx.cond(
                                        FinanciamientoState.revfin_current_page == 1,
                                        "Mostrando 1 a " + rx.cond(
                                            FinanciamientoState.revfin_items_per_page > FinanciamientoState.solicitudes_pendientes_revfin.length(),
                                            FinanciamientoState.solicitudes_pendientes_revfin.length().to(str),
                                            FinanciamientoState.revfin_items_per_page.to(str)
                                        ) + " de " + FinanciamientoState.solicitudes_pendientes_revfin.length().to(str) + " resultados",
                                        "Mostrando " + ((FinanciamientoState.revfin_current_page - 1) * FinanciamientoState.revfin_items_per_page + 1).to(str) + " a " + rx.cond(
                                            FinanciamientoState.revfin_current_page * FinanciamientoState.revfin_items_per_page > FinanciamientoState.solicitudes_pendientes_revfin.length(),
                                            FinanciamientoState.solicitudes_pendientes_revfin.length().to(str),
                                            (FinanciamientoState.revfin_current_page * FinanciamientoState.revfin_items_per_page).to(str)
                                        ) + " de " + FinanciamientoState.solicitudes_pendientes_revfin.length().to(str) + " resultados"
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
                                render_pagination(),
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
    
    def aprobar_dialog():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Aprobar Solicitud", color="#212121"),
                rx.dialog.description(
                    rx.cond(
                        (FinanciamientoState.selected_solicitud_revfin["id"] != "") & (FinanciamientoState.selected_solicitud_revfin["id"] != None),
                        rx.hstack(
                            rx.text("¿Aprobar solicitud #"),
                            rx.text(FinanciamientoState.selected_solicitud_revfin["id"], font_weight="600"),
                            rx.text("?"),
                            spacing="1"
                        ),
                        rx.text("Aprobar solicitud")
                    ),
                    color="#212121"
                ),
                rx.cond(
                    (FinanciamientoState.selected_solicitud_revfin["id"] != "") & (FinanciamientoState.selected_solicitud_revfin["id"] != None),
                    rx.vstack(
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("Área:", size="2", color="#64748b", width="100px"),
                                    rx.text(
                                        FinanciamientoState.selected_solicitud_revfin.get("Area solicitante", "-"), 
                                        size="2", 
                                        color="#1e293b",
                                        font_weight="500"
                                    ),
                                    spacing="3",
                                    align="center"
                                ),
                                rx.hstack(
                                    rx.text("Descripción:", size="2", color="#64748b", width="100px"),
                                    rx.text(
                                        FinanciamientoState.selected_solicitud_revfin.get("Descripcion", "Sin descripción"),
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
                                        f"${FinanciamientoState.selected_solicitud_revfin.get('Total', 0):.2f}",
                                        size="2", 
                                        color="#1e293b",
                                        font_weight="600"
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
                        on_click=FinanciamientoState.aprobar_solicitud_revfin,
                        color_scheme="green",
                        size="2",
                        variant="solid",
                        style={
                            "background": "linear-gradient(135deg, #0d9488 0%, #0f766e 100%)"
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
            open=FinanciamientoState.show_aprobar_dialog_revfin,
            on_open_change=FinanciamientoState.set_show_aprobar_dialog_revfin,
        )
    
    def rechazar_dialog():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Rechazar Solicitud", color="#212121"),
                rx.dialog.description(
                    rx.cond(
                        (FinanciamientoState.selected_solicitud_revfin["id"] != "") & (FinanciamientoState.selected_solicitud_revfin["id"] != None),
                        rx.hstack(
                            rx.text("¿Rechazar solicitud #"),
                            rx.text(FinanciamientoState.selected_solicitud_revfin["id"], font_weight="600"),
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
                        value=FinanciamientoState.motivo_rechazo_revfin,
                        on_change=FinanciamientoState.set_motivo_rechazo_revfin,
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
                        on_click=FinanciamientoState.rechazar_solicitud_revfin,
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
            open=FinanciamientoState.show_rechazar_dialog_revfin,
            on_open_change=FinanciamientoState.set_show_rechazar_dialog_revfin,
        )
    
    def dashboard_content():
        return rx.box(
            navbar("Panel de Revisor Financiero"),
            rx.vstack(
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.vstack(
                                rx.heading(
                                    "💰 Panel de Revisor Financiero",
                                    size="7",
                                    color="#1e293b",
                                    style={
                                        "background": "linear-gradient(135deg, #0d9488 0%, #0f766e 100%)",
                                        "background_clip": "text",
                                        "webkit_background_clip": "text",
                                        "color": "transparent",
                                        "font_weight": "800",
                                    }
                                ),
                                rx.text(
                                    "Revisión de solicitudes de financiamiento",
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
                                f"{FinanciamientoState.solicitudes_count_revfin} pendientes",
                                color_scheme="amber",
                                variant="soft",
                                size="2"
                            ),
                            rx.button(
                                "🔄 Actualizar",
                                on_click=FinanciamientoState.load_data_revfin,
                                loading=FinanciamientoState.loading_revfin,
                                variant="soft",
                                size="2"
                            ),
                            rx.button(
                                "🚪 Cerrar Sesión",
                                on_click=FinanciamientoState.sign_out_revfin,
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
                
                rx.box(
                    rx.hstack(
                        rx.input(
                            placeholder="Buscar solicitudes...",
                            on_change=FinanciamientoState.filter_solicitudes_revfin,
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
                
                rx.cond(
                    FinanciamientoState.loading_revfin,
                    rx.center(
                        rx.vstack(
                            rx.spinner(size="3", color="#0d9488"),
                            rx.text("Cargando solicitudes...", margin_top="1rem", color="#64748b"),
                            spacing="3",
                            align="center"
                        ),
                        height="300px", 
                        width="100%",
                    ),
                    solicitudes_table()
                ),
                
                rx.cond(
                    FinanciamientoState.search_value_revfin != "",
                    rx.box(
                        rx.hstack(
                            rx.icon("search", size=16, color="#0d9488"),
                            rx.text(
                                f"Filtrando por: '{FinanciamientoState.search_value_revfin}'",
                                size="2",
                                color="#64748b"
                            ),
                            rx.button(
                                "Limpiar filtro",
                                on_click=lambda: FinanciamientoState.filter_solicitudes_revfin(""),
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
                        border="1px solid #99f6e4",
                        margin_top="1rem",
                    ),
                ),
                
                aprobar_dialog(),
                rechazar_dialog(),
                
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.text("© 2026 Sistema de Gestión de Recursos", 
                                   size="1", 
                                   color="#64748b"),
                            rx.spacer(),
                            rx.text(
                                f"Revisor Financiero - {FinanciamientoState.revfin_name}",
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
        FinanciamientoState.is_authenticated_revfin,
        dashboard_content(),
        rx.center(
            rx.vstack(
                rx.spinner(size="3", color="#0d9488"),
                rx.text("Redirigiendo al login...", margin_top="1rem", color="#64748b"),
                rx.button(
                    "Ir al Login", 
                    on_click=lambda: rx.redirect(Route.REVFIN_LOGIN.value), 
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