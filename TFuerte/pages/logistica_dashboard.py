import reflex as rx
from TFuerte.state.logistica_state import LogisticaState
from TFuerte.components.navbar import navbar
from TFuerte.routes import Route

@rx.page(
    route=Route.LOGISTICA_DASHBOARD.value,
    title="Dashboard - Logística",
    on_load=[LogisticaState.reset_loading_states, LogisticaState.load_data, LogisticaState.load_completadas, LogisticaState.load_precios]
)
def logistica_dashboard() -> rx.Component:
    """Dashboard para Jefe de Logística (Miguel)"""
    
    def estado_badge_rm(estado: str):
        return rx.cond(
            estado == "aprobado_admin",
            rx.badge("APROBADO ADMIN", color_scheme="green", variant="soft"),
            rx.cond(
                estado == "completada",
                rx.badge("COMPLETADA", color_scheme="purple", variant="soft"),
                rx.badge("RECHAZADA", color_scheme="red", variant="soft")
            )
        )
    
    # ==================== TABLA DE PENDIENTES CON PAGINACIÓN ====================
    def solicitudes_table() -> rx.Component:
        """Tabla de solicitudes RM pendientes para logística con paginación"""
        
        # Botón de página individual
        def create_page_button_pendientes(page_num: int):
            return rx.button(
                rx.text(page_num, size="2", font_weight="500"),
                on_click=lambda: LogisticaState.go_to_page_pendientes(page_num),
                variant="soft",
                size="2",
                style=rx.cond(
                    LogisticaState.pendientes_current_page == page_num,
                    {
                        "background": "#2563eb",
                        "color": "white",
                        "border": "1px solid #2563eb",
                        "_hover": {"background": "#1d4ed8"},
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
        
        # Controles de paginación
        def render_pagination_pendientes():
            return rx.hstack(
                # Botón ANTERIOR
                rx.button(
                    rx.icon("chevron-left", size=16),
                    on_click=LogisticaState.previous_page_pendientes,
                    variant="soft",
                    size="2",
                    is_disabled=LogisticaState.pendientes_current_page == 1,
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
                            (LogisticaState.pendientes_current_page > 3) &
                            (LogisticaState.pendientes_total_pages > 4),
                            rx.hstack(
                                create_page_button_pendientes(1),
                                rx.text("...", size="2", color="#64748b", padding_x="1"),
                                spacing="1",
                                flex_shrink=0,
                            ),
                        ),
                        # Páginas del rango calculado (máximo 4 números)
                        rx.cond(
                            LogisticaState.pendientes_page_numbers.length() > 0,
                            rx.hstack(
                                rx.foreach(
                                    LogisticaState.pendientes_page_numbers,
                                    create_page_button_pendientes
                                ),
                                spacing="1",
                                wrap="nowrap",
                                flex_shrink=0,
                            ),
                            # Fallback
                            rx.text(
                                f"Pág. {LogisticaState.pendientes_current_page}",
                                size="2",
                                color="#64748b",
                                padding_x="2",
                                flex_shrink=0,
                            ),
                        ),
                        # Última página + "..." si estamos lejos del final
                        rx.cond(
                            (LogisticaState.pendientes_current_page < LogisticaState.pendientes_total_pages - 2) &
                            (LogisticaState.pendientes_total_pages > 4),
                            rx.hstack(
                                rx.text("...", size="2", color="#64748b", padding_x="1"),
                                create_page_button_pendientes(LogisticaState.pendientes_total_pages),
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
                # Botón SIGUIENTE
                rx.button(
                    rx.hstack(
                        rx.icon("chevron-right", size=16),
                        width="100%",
                        spacing="0",
                        justify="end",
                        align="end",
                    ),
                    on_click=LogisticaState.next_page_pendientes,
                    variant="soft",
                    size="2",
                    is_disabled=LogisticaState.pendientes_current_page == LogisticaState.pendientes_total_pages,
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
        
        # Fila de solicitud (MODIFICADA)
        def solicitud_row(solicitud):
            # Verificar si está completamente aprobada
            is_completely_approved = (
                (solicitud.get("aprobado_tecnica") == True) & 
                (solicitud.get("aprobado_admin") == True) & 
                (solicitud.get("aprobado_logistica") == True)
            )
            
            # Función para mostrar fechas formateadas
            fecha_tecnica = rx.cond(
                (solicitud.get("fecha_aprobacion_tecnica") != None) & (solicitud.get("fecha_aprobacion_tecnica") != ""),
                rx.text(solicitud.get("fecha_aprobacion_tecnica"), color="#070E0C"),
                rx.text("-", color="#94a3b8", font_style="italic")
            )
            
            fecha_admin = rx.cond(
                (solicitud.get("fecha_aprobacion_admin") != None) & (solicitud.get("fecha_aprobacion_admin") != ""),
                rx.text(solicitud.get("fecha_aprobacion_admin"), color="#070E0C"),
                rx.text("-", color="#94a3b8", font_style="italic")
            )
            
            num_recursos = solicitud.get("num_recursos", 0)
            
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
                    rx.text(solicitud.get("Orden trabajo", "-"), color="#070E0C"),
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                # Celda de productos
                rx.table.cell(
                    rx.hstack(
                        rx.badge(
                            rx.cond(
                                num_recursos == 1,
                                "1 producto",
                                num_recursos.to(str) + " productos"
                            ),
                            color_scheme="blue",
                            variant="soft",
                            size="1"
                        ),
                        rx.button(
                            "👁️ Ver",
                            on_click=lambda: LogisticaState.open_detalle_dialog(solicitud),
                            size="1",
                            variant="ghost",
                            style={
                                        "padding": "2px 5px",
                                        "font_size": "11px",
                                        "height": "15px",
                                        "min_width": "70px",
                                        "width": "auto",
                                        "flex_shrink": "0",  # evitar que se estire
                                    }
                        ),
                        spacing="3",
                        justify="start"
                    ),
                    style={"padding": "8px 4px", "min_width": "150px"}
                ),
                rx.table.cell(
                    fecha_tecnica,
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                rx.table.cell(
                    fecha_admin,
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                rx.table.cell(
                    estado_badge_rm(solicitud.get("estado", "aprobado_admin")),
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                rx.table.cell(
                    rx.box(
                        rx.vstack(
                            rx.button(
                                "✅ Aprobar",
                                on_click=lambda: LogisticaState.open_aprobar_dialog(solicitud),
                                color_scheme="green",
                                size="1",
                                variant="solid",
                                width="100%"
                            ),
                            rx.button(
                                "❌ Rechazar",
                                on_click=lambda: LogisticaState.open_rechazar_dialog(solicitud),
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
            "background": "#2563eb",
            "color": "white",
            "font_weight": "600",
            "padding": "12px 4px",
            "text_align": "left",
            "white_space": "nowrap"
        }
        
        return rx.cond(
            LogisticaState.solicitudes_pendientes.length() == 0,
            rx.center(
                rx.vstack(
                    rx.icon("file_text", size=32, color="#cbd5e1"),
                    rx.text("No hay solicitudes pendientes de logística", size="3", color="#64748b"),
                    spacing="2",
                    align="center"
                ),
                padding="3rem",
                width="100%"
            ),
            rx.vstack(
                # Tabla con scroll horizontal
                rx.box(
                    rx.scroll_area(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("ID", style=header_style),
                                    rx.table.column_header_cell("Centro Costo", style=header_style),
                                    rx.table.column_header_cell("Orden Trabajo", style=header_style),
                                    rx.table.column_header_cell("Productos", style=header_style),  # Nueva columna
                                    rx.table.column_header_cell("Aprob. Técnica", style=header_style),
                                    rx.table.column_header_cell("Aprob. Admin", style=header_style),
                                    rx.table.column_header_cell("Estado", style=header_style),
                                    rx.table.column_header_cell("Acciones", style=header_style),
                                )
                            ),
                            rx.table.body(
                                rx.foreach(
                                    LogisticaState.pendientes_paginated,
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
                # Controles de paginación
                rx.cond(
                    LogisticaState.solicitudes_pendientes.length() > LogisticaState.pendientes_items_per_page,
                    rx.box(
                        rx.hstack(
                            # Texto de resultados
                            rx.text(
                                rx.cond(
                                    LogisticaState.solicitudes_pendientes.length() > 0,
                                    rx.cond(
                                        LogisticaState.pendientes_current_page == 1,
                                        "Mostrando 1 a " + rx.cond(
                                            LogisticaState.pendientes_items_per_page > LogisticaState.solicitudes_pendientes.length(),
                                            LogisticaState.solicitudes_pendientes.length().to(str),
                                            LogisticaState.pendientes_items_per_page.to(str)
                                        ) + " de " + LogisticaState.solicitudes_pendientes.length().to(str) + " resultados",
                                        "Mostrando " + ((LogisticaState.pendientes_current_page - 1) * LogisticaState.pendientes_items_per_page + 1).to(str) + " a " + rx.cond(
                                            LogisticaState.pendientes_current_page * LogisticaState.pendientes_items_per_page > LogisticaState.solicitudes_pendientes.length(),
                                            LogisticaState.solicitudes_pendientes.length().to(str),
                                            (LogisticaState.pendientes_current_page * LogisticaState.pendientes_items_per_page).to(str)
                                        ) + " de " + LogisticaState.solicitudes_pendientes.length().to(str) + " resultados"
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
                                render_pagination_pendientes(),
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
                    rx.box(height="1rem")  # Espacio cuando no hay paginación
                ),
                spacing="0",
                width="100%"
            )
        )
    
    # ==================== TABLA DE COMPLETADAS (sin cambios) ====================
    def completadas_table() -> rx.Component:
        """Tabla de solicitudes RM completadas (aprobadas por logística)"""
        
        def solicitud_row_completada(solicitud):
            # Simplificado - mostrar fecha ya formateada del backend
            return rx.table.row(
                rx.table.cell(
                    rx.text(solicitud["id"], font_weight="600", color="#212121"),
                    style={"padding": "8px 4px"}
                ),
                rx.table.cell(
                    rx.text(solicitud.get("Centro costo", "-"), color="#212121"),
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                rx.table.cell(
                    rx.text(solicitud.get("Orden trabajo", "-"), color="#212121"),
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                rx.table.cell(
                    rx.text(
                        solicitud.get("Descripcion", "-"),
                        color="#212121",
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
                    rx.hstack(
                        rx.text(solicitud.get('Cantidad', '-'), color="#212121"),
                        rx.text(" "),
                        rx.text(solicitud.get('UM', ''), color="#212121"),
                        spacing="0",
                        wrap="wrap"
                    ),
                    style={"padding": "8px 4px", "min_width": "100px"}
                ),
                rx.table.cell(
                    # Mostrar fecha ya formateada del backend
                    rx.text(solicitud.get("fecha_aprobacion_logistica", "-"), color="#212121"),
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                rx.table.cell(
                    rx.badge("COMPLETADA", color_scheme="purple", variant="soft"),
                    style={"padding": "8px 4px", "min_width": "120px"}
                ),
                rx.table.cell(
                    rx.button(
                        "📄 Generar Documento",
                        on_click=lambda: LogisticaState.open_generar_dialog(solicitud),
                        color_scheme="purple",
                        size="1",
                        variant="solid",
                        width="100%"
                    ),
                    style={"padding": "8px 4px", "min_width": "150px"}
                ),
            )
        
        header_style = {
            "background": "#8b5cf6",
            "color": "white",
            "font_weight": "600",
            "padding": "12px 4px",
            "text_align": "left",
            "white_space": "nowrap"
        }
        
        return rx.cond(
            LogisticaState.solicitudes_completadas.length() == 0,
            rx.center(
                rx.vstack(
                    rx.icon("check_circle", size=32, color="#cbd5e1"),
                    rx.text("No hay solicitudes completadas", size="3", color="#64748b"),
                    rx.button(
                        "🔄 Cargar Completadas",
                        on_click=LogisticaState.load_completadas,
                        loading=LogisticaState.loading_completadas,
                        variant="soft",
                        margin_top="1rem"
                    ),
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
                                rx.table.column_header_cell("Orden Trabajo", style=header_style),
                                rx.table.column_header_cell("Descripción", style=header_style),
                                rx.table.column_header_cell("Cantidad", style=header_style),
                                rx.table.column_header_cell("Fecha Aprob. Logística", style=header_style),
                                rx.table.column_header_cell("Estado", style=header_style),
                                rx.table.column_header_cell("Acción", style=header_style),
                            )
                        ),
                        rx.table.body(
                            rx.foreach(
                                LogisticaState.solicitudes_completadas,
                                solicitud_row_completada
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
    
    # ==================== NUEVO: Diálogo de detalles de productos ====================
    def detalle_dialog():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title(
                    rx.hstack(
                        rx.icon("package", size=20, color="#2563eb"),
                        rx.text(f"Productos de Solicitud #{LogisticaState.solicitud_detalle.get('id', '')}"),
                        spacing="2",
                        align="center"
                    ),
                    color="#212121"
                ),
                rx.dialog.description(
                    rx.cond(
                        LogisticaState.solicitud_detalle.get("id") != "",
                        rx.vstack(
                            rx.hstack(
                                rx.text("Centro de costo:", size="2", color="#64748b", width="100px"),
                                rx.text(LogisticaState.solicitud_detalle.get("Centro costo", "-"), size="2", color="#1e293b", font_weight="500"),
                                spacing="3",
                                align="center"
                            ),
                            rx.hstack(
                                rx.text("Orden trabajo:", size="2", color="#64748b", width="100px"),
                                rx.text(LogisticaState.solicitud_detalle.get("Orden trabajo", "-"), size="2", color="#1e293b", font_weight="500"),
                                spacing="3",
                                align="center"
                            ),
                            rx.divider(),
                            rx.heading("Recursos solicitados:", size="3", color="#1e293b"),
                            rx.cond(
                                LogisticaState.recursos_detalle.length() > 0,
                                rx.vstack(
                                    rx.foreach(
                                        LogisticaState.recursos_detalle,
                                        lambda recurso, idx: rx.box(
                                            rx.hstack(
                                                rx.badge(idx + 1, color_scheme="blue", size="1"),
                                                rx.vstack(
                                                    rx.text(recurso.get("descripcion", "-"), size="2", font_weight="500"),
                                                    rx.hstack(
                                                        rx.text(f"Cantidad: {recurso.get('cantidad', '-')}", size="1", color="#64748b"),
                                                        rx.text(f"UM: {recurso.get('unidad_medida', '-')}", size="1", color="#64748b"),
                                                        rx.cond(
                                                            recurso.get("observaciones"),
                                                            rx.text(f"Obs: {recurso.get('observaciones')}", size="1", color="#64748b"),
                                                            rx.text("")
                                                        ),
                                                        spacing="2",
                                                        wrap="wrap"
                                                    ),
                                                    spacing="0",
                                                    align="start"
                                                ),
                                                spacing="3",
                                                align="start"
                                            ),
                                            padding="0.5rem",
                                            border_radius="6px",
                                            background=rx.cond(
                                                idx % 2 == 0,
                                                "#f9fafb",
                                                "white"
                                            ),
                                            width="100%"
                                        )
                                    ),
                                    spacing="1",
                                    width="100%"
                                ),
                                rx.text("No hay recursos disponibles", size="2", color="#64748b", font_style="italic")
                            ),
                            spacing="3",
                            align="start",
                            width="100%"
                        ),
                        rx.text("No hay solicitud seleccionada")
                    ),
                    color="#212121"
                ),
                rx.dialog.close(
                    rx.button(
                        "Cerrar",
                        on_click=LogisticaState.close_detalle_dialog,
                        variant="soft",
                        size="2"
                    ),
                    margin_top="1rem"
                ),
                max_width="600px",
                style={
                    "background": "white",
                    "border_radius": "12px",
                    "box_shadow": "0 20px 25px -5px rgba(0, 0, 0, 0.1)"
                }
            ),
            open=LogisticaState.show_detalle_dialog,
            on_open_change=LogisticaState.set_show_detalle_dialog,
        )
    
    # ==================== GESTIÓN DE PRECIOS (sin cambios) ====================
    def gestion_precios_tab() -> rx.Component:
        """Tab para gestionar precios de productos"""
        
        def precios_table() -> rx.Component:
            """Tabla de precios con paginación compacta: flechas + números (máx 4)."""
            
            # --- Botón de página individual (reutilizable) ---
            def create_page_button_precios(page_num: int):
                return rx.button(
                    rx.text(page_num, size="2", font_weight="500"),
                    on_click=lambda: LogisticaState.go_to_page_precios(page_num),
                    variant="soft",
                    size="2",
                    style=rx.cond(
                        LogisticaState.current_page_precios == page_num,
                        {
                            "background": "#f59e0b",
                            "color": "white",
                            "border": "1px solid #f59e0b",
                            "_hover": {"background": "#d97706"},
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
            
            # --- Controles de paginación: siempre horizontales, con flechas ---
            def render_pagination_precios():
                return rx.hstack(
                    # Botón ANTERIOR (icono)
                    rx.button(
                        rx.icon("chevron-left", size=16),
                        on_click=LogisticaState.previous_page_precios,
                        variant="soft",
                        size="2",
                        is_disabled=LogisticaState.current_page_precios == 1,
                        style={
                            "background": "white",
                            "border": "1px solid #e2e8f0",
                            "color": "#1e293b",
                            "flex_shrink": 0,
                            "min_width": "32px",
                            "padding": "0 8px",
                        }
                    ),
                    # Contenedor de números (con scroll horizontal solo si es necesario)
                    rx.box(
                        rx.hstack(
                            # Primera página + "..." si estamos lejos del inicio
                            rx.cond(
                                (LogisticaState.current_page_precios > 3) &
                                (LogisticaState.total_pages_precios > 4),
                                rx.hstack(
                                    create_page_button_precios(1),
                                    rx.text("...", size="2", color="#64748b", padding_x="1"),
                                    spacing="1",
                                    flex_shrink=0,
                                ),
                            ),
                            # Páginas del rango calculado (máximo 4 números)
                            rx.cond(
                                LogisticaState.page_numbers_precios.length() > 0,
                                rx.hstack(
                                    rx.foreach(
                                        LogisticaState.page_numbers_precios,
                                        create_page_button_precios
                                    ),
                                    spacing="1",
                                    wrap="nowrap",
                                    flex_shrink=0,
                                ),
                                # Fallback: mostrar texto con página actual (nunca debería ocurrir)
                                rx.text(
                                    f"Pág. {LogisticaState.current_page_precios}",
                                    size="2",
                                    color="#64748b",
                                    padding_x="2",
                                    flex_shrink=0,
                                ),
                            ),
                            # Última página + "..." si estamos lejos del final
                            rx.cond(
                                (LogisticaState.current_page_precios < LogisticaState.total_pages_precios - 2) &
                                (LogisticaState.total_pages_precios > 4),
                                rx.hstack(
                                    rx.text("...", size="2", color="#64748b", padding_x="1"),
                                    create_page_button_precios(LogisticaState.total_pages_precios),
                                    spacing="1",
                                    flex_shrink=0,
                                ),
                            ),
                            spacing="1",
                            wrap="nowrap",      # ← NUNCA se apilan
                            align="center",
                        ),
                        overflow_x="auto",      # ← Scroll horizontal solo si hay demasiados elementos
                        flex_grow=0,           # No se expande
                        flex_shrink=1,         # Puede encogerse si falta espacio
                        max_width="100%",      # Respeta el ancho del padre
                    ),
                    # Botón SIGUIENTE (icono)
                    rx.button(
                        rx.hstack(
                            rx.icon("chevron-right", size=16),
                            width="100%",
                            spacing="0",
                            justify="end",
                            align="end",
                        ),
                        on_click=LogisticaState.next_page_precios,
                        variant="soft",
                        size="2",
                        is_disabled=LogisticaState.current_page_precios == LogisticaState.total_pages_precios,
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
                    wrap="nowrap",            # ← Todo el conjunto en una sola línea
                    align="center",
                    justify="end",
                    width="100%",
                )
            
            # --- Fila de precio (igual que antes) ---
            def precio_row(precio):
                return rx.table.row(
                    rx.table.cell(
                        rx.text(precio["id"], font_weight="600", color="#1F1F1F"),
                        style={"padding": "8px 4px"}
                    ),
                    rx.table.cell(
                        rx.text(precio.get("Tipo", "-"), color="#1F1F1F"),
                        style={"padding": "8px 4px", "min_width": "150px"}
                    ),
                    rx.table.cell(
                        rx.text(
                            precio.get("Descripcion", "-"),
                            color="#1F1F1F",
                            style={
                                "max_width": "200px",
                                "overflow": "hidden",
                                "text_overflow": "ellipsis",
                                "white_space": "nowrap"
                            }
                        ),
                        style={"padding": "8px 4px", "min_width": "200px"}
                    ),
                    rx.table.cell(
                        rx.text(f"${precio.get('Precio', 0):.2f}", color="#1F1F1F"),
                        style={"padding": "8px 4px", "min_width": "100px"}
                    ),
                    rx.table.cell(
                        rx.box(
                            rx.hstack(
                                rx.button(
                                    "✏️",
                                    on_click=lambda: LogisticaState.open_editar_precio_dialog(precio),
                                    color_scheme="blue",
                                    size="1",
                                    variant="ghost",
                                    style={
                                        "padding": "2px 8px",
                                        "font_size": "11px",
                                        "height": "28px",
                                        "min_width": "70px",
                                        "width": "auto",
                                        "flex_shrink": "0",  # evitar que se estire
                                    }
                                ),
                                rx.button(
                                    "🗑️",
                                    on_click=lambda: LogisticaState.open_eliminar_precio_dialog(precio),
                                    color_scheme="red",
                                    size="1",
                                    variant="ghost",
                                    style={
                                        "padding": "2px 8px",
                                        "font_size": "11px",
                                        "height": "28px",
                                        "min_width": "70px",
                                        "width": "auto",
                                        "flex_shrink": "0",  # evitar que se estire
                                    }

                                ),
                                spacing="1"
                            ),
                            style={"min_width": "100px"}
                        ),
                        style={"padding": "8px 4px"}
                    ),
                )
            
            # --- Estilo del encabezado ---
            header_style = {
                "background": "#f59e0b",
                "color": "white",
                "font_weight": "600",
                "padding": "12px 4px",
                "text_align": "left",
                "white_space": "nowrap"
            }
            
            # --- Renderizado final ---
            return rx.cond(
                LogisticaState.loading_precios,
                rx.center(rx.spinner(size="3"), padding="3rem"),
                rx.cond(
                    LogisticaState.precios.length() == 0,
                    rx.center(
                        rx.vstack(
                            rx.icon("package", size=32, color="#cbd5e1"),
                            rx.text("No hay precios registrados", size="3", color="#64748b"),
                            spacing="2",
                            align="center"
                        ),
                        padding="3rem",
                        width="100%"
                    ),
                    rx.vstack(
                        # Tabla con scroll horizontal (igual que antes)
                        rx.box(
                            rx.scroll_area(
                                rx.table.root(
                                    rx.table.header(
                                        rx.table.row(
                                            rx.table.column_header_cell("ID", style=header_style),
                                            rx.table.column_header_cell("Tipo", style=header_style),
                                            rx.table.column_header_cell("Descripción", style=header_style),
                                            rx.table.column_header_cell("Precio", style=header_style),
                                            rx.table.column_header_cell("Acciones", style=header_style),
                                        )
                                    ),
                                    rx.table.body(
                                        rx.foreach(
                                            LogisticaState.precios_paginated,
                                            precio_row
                                        )
                                    ),
                                    style={
                                        "width": "100%",
                                        "min_width": "800px",
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
                        ),
                        # --- PAGINACIÓN ---
                        rx.cond(
                            LogisticaState.precios.length() > LogisticaState.items_per_page_precios,
                            rx.box(
                                rx.hstack(
                                    # Texto de resultados (siempre a la izquierda)
                                    rx.text(
                                        rx.cond(
                                            LogisticaState.precios.length() > 0,
                                            rx.cond(
                                                LogisticaState.current_page_precios == 1,
                                                "Mostrando 1 a " + rx.cond(
                                                    LogisticaState.items_per_page_precios > LogisticaState.precios.length(),
                                                    LogisticaState.precios.length().to(str),
                                                    LogisticaState.items_per_page_precios.to(str)
                                                ) + " de " + LogisticaState.precios.length().to(str) + " resultados",
                                                "Mostrando " + ((LogisticaState.current_page_precios - 1) * LogisticaState.items_per_page_precios + 1).to(str) + " a " + rx.cond(
                                                    LogisticaState.current_page_precios * LogisticaState.items_per_page_precios > LogisticaState.precios.length(),
                                                    LogisticaState.precios.length().to(str),
                                                    (LogisticaState.current_page_precios * LogisticaState.items_per_page_precios).to(str)
                                                ) + " de " + LogisticaState.precios.length().to(str) + " resultados"
                                            ),
                                            "Mostrando 0 a 0 de 0 resultados"
                                        ),
                                        size="2",
                                        color="#64748b",
                                        font_weight="500",
                                        flex_shrink=0,
                                    ),
                                    rx.spacer(),
                                    rx.box(
                                        render_pagination_precios(),
                                        margin_left="10rem",   # ← SEPARACIÓN ADICIONAL hacia la derecha
                                        flex_shrink=0,
                                    ),   # ← Siempre horizontal, compacta, con flechas
                                    width="100%",
                                    align="center",
                                    spacing="4",
                                    wrap="wrap",          # ← Permite que el texto se mueva arriba si es necesario
                                ),
                                padding="1.5rem 1rem",
                                border_top="1px solid #e2e8f0",
                                background="#f8fafc",
                            ),
                            rx.box(height="1rem")  # Espacio cuando no hay paginación
                        ),
                        spacing="0",
                        width="100%",
                    )
                )
            )
        
        def form_agregar_precio():
            """Formulario para agregar nuevo precio"""
            return rx.box(
                rx.vstack(
                    rx.heading("➕ Agregar Nuevo Producto/Precio", size="4", color="#1F1F1F"),
                    rx.hstack(
                        rx.vstack(
                            rx.text("Tipo *", size="2", color="#1F1F1F"),
                            rx.input(
                                placeholder="Ej: Electricidad, Plomeria, etc.",
                                value=LogisticaState.nuevo_tipo,
                                on_change=LogisticaState.set_nuevo_tipo,
                                width="100%",
                                background="gray"
                            ),
                            spacing="1",
                            align="start",
                            width="100%"
                        ),
                        rx.vstack(
                            rx.text("Descripción *", size="2", color="#1F1F1F"),
                            rx.input(
                                placeholder="Ej: Cable 2.5mm",
                                value=LogisticaState.nueva_descripcion,
                                on_change=LogisticaState.set_nueva_descripcion,
                                width="100%",
                                background="gray"
                            ),
                            spacing="1",
                            align="start",
                            width="100%"
                        ),
                        rx.vstack(
                            rx.text("Precio *", size="2", color="#1F1F1F"),
                            rx.input(
                                placeholder="Ej: 150.00",
                                type="number",
                                min="0",
                                step="0.01",
                                value=LogisticaState.nuevo_precio,
                                on_change=LogisticaState.set_nuevo_precio,
                                width="100%",
                                background="gray"
                            ),
                            spacing="1",
                            align="start",
                            width="100%"
                        ),
                        spacing="3",
                        width="100%",
                        wrap="wrap"
                    ),
                    rx.button(
                        "➕ Agregar Producto",
                        on_click=LogisticaState.agregar_precio,
                        loading=LogisticaState.loading_precios,
                        variant="outline",
                        width="100%",
                        color_scheme="orange"
                    ),
                    spacing="3",
                ),
                width="100%",
                padding="1rem",
                border="2px dashed #fbbf24",
                border_radius="8px",
                margin_bottom="1rem"
            )
        
        def editar_precio_dialog():
            return rx.dialog.root(
                rx.dialog.content(
                    rx.dialog.title("Editar Producto", color="#212121"),
                    rx.dialog.description(
                        rx.hstack(
                            rx.text("Editando producto #"),
                            rx.text(LogisticaState.selected_precio.get("id", ""), font_weight="600"),
                            spacing="1"
                        ),
                        color="#212121"
                    ),
                    rx.vstack(
                        rx.vstack(
                            rx.text("Tipo *", size="2", color="#1F1F1F"),
                            rx.input(
                                value=LogisticaState.precio_editado_tipo,
                                on_change=LogisticaState.set_precio_editado_tipo,
                                width="100%",
                                background="gray"
                            ),
                            spacing="1",
                            align="start",
                            width="100%"
                        ),
                        rx.vstack(
                            rx.text("Descripción *", size="2", color="#1F1F1F"),
                            rx.input(
                                value=LogisticaState.precio_editado_descripcion,
                                on_change=LogisticaState.set_precio_editado_descripcion,
                                width="100%",
                                background="gray"
                            ),
                            spacing="1",
                            align="start",
                            width="100%"
                        ),
                        rx.vstack(
                            rx.text("Precio *", size="2", color="#1F1F1F"),
                            rx.input(
                                type="number",
                                min="0",
                                step="0.01",
                                value=LogisticaState.precio_editado_precio,
                                on_change=LogisticaState.set_precio_editado_precio,
                                width="100%",
                                background="gray"
                            ),
                            spacing="1",
                            align="start",
                            width="100%"
                        ),
                        spacing="3",
                        width="100%",
                        margin_y="1rem"
                    ),
                    rx.vstack(
                        rx.dialog.close(
                            rx.button("Cancelar", variant="soft", size="2"),
                        ),
                        rx.button(
                            "💾 Guardar Cambios",
                            on_click=LogisticaState.actualizar_precio,
                            loading=LogisticaState.loading_precios,
                            color_scheme="orange",
                            size="2",
                            variant="solid"
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
                open=LogisticaState.show_editar_precio_dialog,
                on_open_change=LogisticaState.set_show_editar_precio_dialog,
            )
        
        def eliminar_precio_dialog():
            return rx.dialog.root(
                rx.dialog.content(
                    rx.dialog.title("Eliminar Producto", color="#212121"),
                    rx.dialog.description(
                        rx.hstack(
                            rx.text("¿Eliminar producto #"),
                            rx.text(LogisticaState.selected_precio.get("id", ""), font_weight="600"),
                            rx.text("?"),
                            spacing="1"
                        ),
                        color="#212121"
                    ),
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text("Tipo:", size="2", color="#64748b", width="80px"),
                                rx.text(LogisticaState.selected_precio.get("Tipo", "-"), size="2", color="#1e293b"),
                                spacing="3",
                                align="center"
                            ),
                            rx.hstack(
                                rx.text("Descripción:", size="2", color="#64748b", width="80px"),
                                rx.text(LogisticaState.selected_precio.get("Descripcion", "-"), size="2", color="#1e293b"),
                                spacing="3",
                                align="center"
                            ),
                            rx.hstack(
                                rx.text("Precio:", size="2", color="#64748b", width="80px"),
                                rx.text(f"${LogisticaState.selected_precio.get('Precio', 0):.2f}", size="2", color="#1e293b"),
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
                        width="100%",
                        margin_y="1rem"
                    ),
                    rx.hstack(
                        rx.dialog.close(
                            rx.button("Cancelar", variant="soft", size="2"),
                        ),
                        rx.button(
                            "🗑️ Eliminar",
                            on_click=LogisticaState.eliminar_precio,
                            loading=LogisticaState.loading_precios,
                            color_scheme="red",
                            size="2",
                            variant="solid"
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
                open=LogisticaState.show_eliminar_precio_dialog,
                on_open_change=LogisticaState.set_show_eliminar_precio_dialog,
            )
        
        return rx.vstack(
            rx.heading("💰 Gestión de Precios de Productos", size="5", color="#1F1F1F"),
            rx.text(
                "Agrega y edita los precios de los productos para financiamiento",
                size="2",
                color="#64748b",
                margin_bottom="1rem"
            ),
            
            rx.hstack(
                rx.button(
                    "🔄 Cargar Precios",
                    on_click=LogisticaState.load_precios,
                    loading=LogisticaState.loading_precios,
                    variant="soft",
                    size="2"
                ),
                rx.badge(
                    rx.cond(
                        LogisticaState.precios_count == 1,
                        rx.text("1 producto"),
                        rx.text(LogisticaState.precios_count.to(str) + " productos")
                    ),
                    color_scheme="orange",
                    variant="soft",
                    size="2"
                ),
                spacing="3",
                width="100%",
                wrap="wrap"
            ),
            
            form_agregar_precio(),
            
            rx.cond(
                LogisticaState.loading_precios,
                rx.center(rx.spinner(size="3"), padding="3rem"),
                precios_table()
            ),
            
            # Diálogos para editar/eliminar
            editar_precio_dialog(),
            eliminar_precio_dialog(),
            
            spacing="4",
            width="100%",
        )
    
    # ==================== DIÁLOGOS (sin cambios) ====================
    def aprobar_dialog():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Aprobar Solicitud", color="#212121"),
                rx.dialog.description(
                    rx.cond(
                        LogisticaState.selected_solicitud["id"] != "",
                        rx.hstack(
                            rx.text("¿Aprobar solicitud #"),
                            rx.text(LogisticaState.selected_solicitud["id"], font_weight="600"),
                            rx.text("?"),
                            spacing="1"
                        ),
                        rx.text("¿Aprobar solicitud?")
                    ),
                    color="#212121"
                ),
                rx.cond(
                    (LogisticaState.selected_solicitud["id"] != "") & (LogisticaState.selected_solicitud["id"] != None),
                    rx.vstack(
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("Solicitante:", size="2", color="#64748b", width="100px"),
                                    rx.cond(
                                        LogisticaState.selected_solicitud.get("solicitante_id") != "",
                                        rx.hstack(
                                            rx.text("ID: ", size="2", color="#1e293b"),
                                            rx.text(LogisticaState.selected_solicitud.get("solicitante_id"), size="2", color="#1e293b"),
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
                                        LogisticaState.selected_solicitud.get("Descripcion", "Sin descripción"),
                                        size="2", 
                                        color="#1e293b",
                                        font_weight="500"
                                    ),
                                    spacing="3",
                                    align="center"
                                ),
                                rx.hstack(
                                    rx.text("Última aprobación:", size="2", color="#64748b", width="100px"),
                                    rx.text(
                                        "Administración (Maikel)", 
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
                        "✅ Aprobar Final",
                        on_click=LogisticaState.aprobar_solicitud,
                        color_scheme="green",
                        size="2",
                        variant="solid",
                        style={
                            "background": "linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)"
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
            open=LogisticaState.show_aprobar_dialog,
            on_open_change=LogisticaState.set_show_aprobar_dialog,
        )
    
    def rechazar_dialog():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Rechazar Solicitud", color="#212121"),
                rx.dialog.description(
                    rx.cond(
                        LogisticaState.selected_solicitud["id"] != "",
                        rx.hstack(
                            rx.text("¿Rechazar solicitud #"),
                            rx.text(LogisticaState.selected_solicitud["id"], font_weight="600"),
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
                        value=LogisticaState.motivo_rechazo,
                        on_change=LogisticaState.set_motivo_rechazo,
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
                        on_click=LogisticaState.rechazar_solicitud,
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
            open=LogisticaState.show_rechazar_dialog,
            on_open_change=LogisticaState.set_show_rechazar_dialog,
        )
    
    def generar_dialog():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Generar Documento", color="#212121"),
                rx.dialog.description(
                    rx.cond(
                        LogisticaState.selected_solicitud["id"] != "",
                        rx.hstack(
                            rx.text("¿Generar documento para solicitud #"),
                            rx.text(LogisticaState.selected_solicitud["id"], font_weight="600"),
                            rx.text("?"),
                            spacing="1"
                        ),
                        rx.text("¿Generar documento?")
                    ),
                    color="#212121"
                ),
                rx.cond(
                    (LogisticaState.selected_solicitud["id"] != "") & (LogisticaState.selected_solicitud["id"] != None),
                    rx.vstack(
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("check", size=16, color="#10b981"),
                                    rx.text("✓ Aprobado por Área Técnica", size="2", color="#1e293b"),
                                    spacing="2"
                                ),
                                rx.hstack(
                                    rx.icon("check", size=16, color="#10b981"),
                                    rx.text("✓ Aprobado por Administración", size="2", color="#1e293b"),
                                    spacing="2"
                                ),
                                rx.hstack(
                                    rx.icon("check", size=16, color="#10b981"),
                                    rx.text("✓ Aprobado por Logística", size="2", color="#1e293b"),
                                    spacing="2"
                                ),
                                spacing="2",
                                align="start",
                                padding="1rem",
                                border_radius="md",
                                background="#f0fdfa",
                                border="1px solid #a7f3d0",
                            ),
                            width="100%"
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("El documento incluirá:", size="2", color="#64748b"),
                                rx.text("• Datos completos de la solicitud", size="2", color="#1e293b"),
                                rx.text("• Firmas digitalizadas", size="2", color="#1e293b"),
                                rx.text("• Fecha de generación", size="2", color="#1e293b"),
                                spacing="1",
                                align="start"
                            ),
                            width="100%",
                            padding="1rem",
                            background="#eff6ff",
                            border_radius="md"
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
                        on_click=LogisticaState.generar_documento,
                        color_scheme="purple",
                        size="2",
                        variant="solid",
                        style={
                            "background": "linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)"
                        }
                    ),
                    spacing="1",
                    justify="end",
                ),
                max_width="500px",
                style={
                    "background": "white",
                    "border_radius": "12px",
                    "box_shadow": "0 20px 25px -5px rgba(0, 0, 0, 0.1)"
                }
            ),
            open=LogisticaState.show_generar_dialog,
            on_open_change=LogisticaState.set_show_generar_dialog,
        )
    
    # ==================== CONTENIDO PRINCIPAL ====================
    def dashboard_content():
        return rx.box(
            navbar("Panel de Logística"),
            rx.vstack(
                # Encabezado responsivo
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.vstack(
                                rx.heading(
                                    "🚚 Panel de Logística",
                                    size="7",
                                    color="#1e293b",
                                    style={
                                        "background": "linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)",
                                        "background_clip": "text",
                                        "webkit_background_clip": "text",
                                        "color": "transparent",
                                        "font_weight": "800",
                                    }
                                ),
                                rx.text(
                                    "Aprobación final y generación de documentos",
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
                                f"Pendientes: {LogisticaState.solicitudes_pendientes_count}",
                                color_scheme="blue",
                                variant="soft",
                                size="2"
                            ),
                            rx.badge(
                                f"Completadas: {LogisticaState.solicitudes_completadas_count}",
                                color_scheme="purple",
                                variant="soft",
                                size="2"
                            ),
                            rx.button(
                                "🔄 Actualizar Todo",
                                on_click=[
                                    LogisticaState.load_data,
                                    LogisticaState.load_completadas,
                                    LogisticaState.load_precios
                                ],
                                loading=LogisticaState.loading,
                                variant="soft",
                                size="2"
                            ),
                            rx.button(
                                "🚪 Cerrar Sesión",
                                on_click=LogisticaState.sign_out,
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
                
                # Tabs responsivos
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger("⏳ Pendientes", value="pendientes", color="#1F1F1F"),
                        rx.tabs.trigger("✅ Completadas", value="completadas", color="#1F1F1F"),
                        rx.tabs.trigger("💰 Gestión de Precios", value="precios", color="#1F1F1F"),
                        width="100%",
                        wrap="wrap"
                    ),
                    
                    rx.tabs.content(
                        rx.vstack(
                            # Búsqueda solo para pendientes
                            rx.box(
                                rx.hstack(
                                    rx.input(
                                        placeholder="Buscar solicitudes...",
                                        on_change=LogisticaState.filter_solicitudes,
                                        width=["100%", "100%", "400px", "400px"],
                                        size="3",
                                        background="gray"
                                    ),
                                    spacing="2",
                                    width="100%",
                                    justify="end"
                                ),
                                width="100%",
                                padding_bottom="1.5rem"
                            ),
                            
                            # Tabla de pendientes
                            rx.cond(
                                LogisticaState.loading,
                                rx.center(
                                    rx.vstack(
                                        rx.spinner(size="3", color="#2563eb"),
                                        rx.text("Cargando solicitudes pendientes...", margin_top="1rem", color="#64748b"),
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
                                LogisticaState.search_value != "",
                                rx.box(
                                    rx.hstack(
                                        rx.icon("search", size=16, color="#2563eb"),
                                        rx.text(
                                            rx.hstack(
                                                rx.text("Filtrando por: '"),
                                                rx.text(LogisticaState.search_value),
                                                rx.text("'"),
                                                spacing="0"
                                            ),
                                            size="2",
                                            color="#64748b"
                                        ),
                                        rx.button(
                                            "Limpiar filtro",
                                            on_click=lambda: LogisticaState.filter_solicitudes(""),
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
                                    background="#eff6ff",
                                    border="1px solid #dbeafe",
                                    margin_top="1rem",
                                ),
                            ),
                            
                            spacing="4",
                            width="100%",
                        ),
                        value="pendientes",
                        style={"padding": "1.5rem 0"}
                    ),
                    
                    rx.tabs.content(
                        rx.vstack(
                            # Botón para cargar completadas
                            rx.hstack(
                                rx.button(
                                    "🔄 Cargar Completadas",
                                    on_click=LogisticaState.load_completadas,
                                    loading=LogisticaState.loading_completadas,
                                    variant="soft",
                                    size="2"
                                ),
                                rx.text(
                                    "Solicitudes aprobadas completamente",
                                    size="2",
                                    color="#64748b"
                                ),
                                spacing="3",
                                width="100%",
                                wrap="wrap"
                            ),
                            
                            # Tabla de completadas
                            rx.cond(
                                LogisticaState.loading_completadas,
                                rx.center(rx.spinner(size="3"), padding="3rem"),
                                completadas_table()
                            ),
                            
                            spacing="4",
                            width="100%",
                        ),
                        value="completadas",
                        style={"padding": "1.5rem 0"}
                    ),
                    
                    rx.tabs.content(
                        gestion_precios_tab(),
                        value="precios",
                        style={"padding": "1.5rem 0"}
                    ),
                    
                    default_value="pendientes",
                    width="100%",
                ),
                
                # Diálogos
                aprobar_dialog(),
                rechazar_dialog(),
                generar_dialog(),
                detalle_dialog(),  # <-- Nuevo diálogo agregado
                
                # Pie de página responsivo
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.text("© 2026 Sistema de Gestión de Recursos", 
                                   size="1", 
                                   color="#64748b"),
                            rx.spacer(),
                            rx.text(
                                f"Jefe de Logística - {LogisticaState.admin_name}",
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
        LogisticaState.is_authenticated,
        dashboard_content(),
        rx.center(
            rx.vstack(
                rx.spinner(size="3", color="#2563eb"),
                rx.text("Redirigiendo al login...", margin_top="1rem", color="#64748b"),
                rx.button(
                    "Ir al Login", 
                    on_click=lambda: rx.redirect(Route.LOGISTICA_LOGIN.value), 
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