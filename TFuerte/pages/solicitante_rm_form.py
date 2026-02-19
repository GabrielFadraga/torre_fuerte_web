import reflex as rx
from TFuerte.state.solicitante_rm_state import SolicitanteRMState
from TFuerte.components.navbar import navbar
from TFuerte.routes import Route

@rx.page(
    route=Route.SOLICITANTE_RM_FORM.value,
    title="Solicitud de Recursos - Solicitante",
    on_load=[SolicitanteRMState.reset_loading_states, SolicitanteRMState.load_mis_solicitudes_rm]
)
def solicitante_rm_form() -> rx.Component:
    """Página para crear solicitudes de recursos"""
    
    # Función auxiliar para mostrar estado de recursos RM
    def estado_badge(estado):
        """Muestra un badge para el estado de la solicitud de recursos"""
        return rx.match(
            estado,
            ("pendiente", rx.badge("PENDIENTE TÉCNICA", color_scheme="amber", variant="soft")),
            ("aprobado_tecnica", rx.badge("APROBADO TÉCNICA", color_scheme="blue", variant="soft")),
            ("aprobado_admin", rx.badge("APROBADO ADMIN", color_scheme="green", variant="soft")),
            ("completada", rx.badge("COMPLETADA", color_scheme="purple", variant="soft")),
            rx.badge("RECHAZADA", color_scheme="red", variant="soft")
        )
    
    # Componente para la tabla de recursos agregados
    def recursos_table():
        return rx.cond(
            SolicitanteRMState.total_recursos > 0,
            rx.box(
                rx.vstack(
                    rx.heading("📋 Recursos Agregados", size="4", color="#1F1F1F"),
                    rx.box(
                        rx.scroll_area(
                            rx.table.root(
                                rx.table.header(
                                    rx.table.row(
                                        rx.table.column_header_cell("No.", color="#1F1F1F"),
                                        rx.table.column_header_cell("Descripción", color="#1F1F1F"),
                                        rx.table.column_header_cell("U/M", color="#1F1F1F"),
                                        rx.table.column_header_cell("Cantidad", color="#1F1F1F"),
                                        rx.table.column_header_cell("Observaciones", color="#1F1F1F"),
                                        rx.table.column_header_cell("Acción", color="#1F1F1F"),
                                    )
                                ),
                                rx.table.body(
                                    rx.foreach(
                                        SolicitanteRMState.recursos,
                                        lambda recurso, idx: rx.table.row(
                                            rx.table.cell(rx.text(idx + 1), color="#1F1F1F"),
                                            rx.table.cell(
                                                rx.text(
                                                    recurso["descripcion"],
                                                    style={
                                                        "max_width": "200px",
                                                        "overflow": "hidden",
                                                        "text_overflow": "ellipsis",
                                                        "white_space": "nowrap"
                                                    }
                                                ), 
                                                color="#1F1F1F"
                                            ),
                                            rx.table.cell(
                                                rx.text(
                                                    rx.cond(
                                                        recurso["unidad_medida"] != "",
                                                        recurso["unidad_medida"],
                                                        "-"
                                                    )
                                                ), 
                                                color="#1F1F1F"
                                            ),
                                            rx.table.cell(
                                                rx.text(
                                                    recurso["cantidad"]
                                                ), 
                                                color="#1F1F1F"
                                            ),
                                            rx.table.cell(
                                                rx.text(
                                                    rx.cond(
                                                        recurso["observaciones"] != "",
                                                        recurso["observaciones"],
                                                        "-"
                                                    ),
                                                    style={
                                                        "max_width": "200px",
                                                        "overflow": "hidden",
                                                        "text_overflow": "ellipsis",
                                                        "white_space": "nowrap"
                                                    }
                                                ), 
                                                color="#1F1F1F"
                                            ),
                                            rx.table.cell(
                                                rx.button(
                                                    "❌",
                                                    on_click=lambda idx=idx: SolicitanteRMState.eliminar_recurso(idx),
                                                    color_scheme="red",
                                                    size="1",
                                                    variant="ghost"
                                                ),
                                                color="#1F1F1F"
                                            ),
                                        )
                                    )
                                ),
                                variant="surface",
                            ),
                            type="always",
                            scrollbars="horizontal",
                            style={
                                "width": "100%",
                                "border": "1px solid #e2e8f0",
                                "border_radius": "8px"
                            }
                        ),
                        width="100%",
                        overflow_x="auto"
                    ),
                    spacing="2",
                ),
                width="100%",
                padding="1rem",
                border="1px solid #e2e8f0",
                border_radius="8px",
                margin_bottom="1rem"
            ),
            rx.box(
                rx.text("No hay recursos agregados aún", color="#64748b"),
                padding="1rem",
                border="1px dashed #cbd5e1",
                border_radius="8px",
                text_align="center"
            )
        )
    
    # Formulario para agregar un recurso
    def formulario_recurso():
        return rx.box(
            rx.vstack(
                rx.heading("➕ Agregar Nuevo Recurso", size="4", color="#1F1F1F"),
                rx.hstack(
                    rx.vstack(
                        rx.text("Descripción *", size="2", color="#1F1F1F"),
                        rx.input(
                            placeholder="Ej: Batería 90A 12V",
                            value=SolicitanteRMState.recurso_descripcion,
                            on_change=SolicitanteRMState.set_recurso_descripcion,
                            width="100%"
                        ),
                        spacing="1",
                        align="start",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Unidad de Medida", size="2", color="#1F1F1F"),
                        rx.input(
                            placeholder="Ej: 2m, Lt, Kg, Unidad",
                            value=SolicitanteRMState.recurso_unidad_medida,
                            on_change=SolicitanteRMState.set_recurso_unidad_medida,
                            width="100%"
                        ),
                        spacing="1",
                        align="start",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Cantidad *", size="2", color="#1F1F1F"),
                        rx.input(
                            placeholder="Ej: 10",
                            type="number",
                            min="0",
                            step="0.01",
                            value=SolicitanteRMState.recurso_cantidad,
                            on_change=SolicitanteRMState.set_recurso_cantidad,
                            width="100%"
                        ),
                        spacing="1",
                        align="start",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%",
                    wrap="wrap"
                ),
                rx.vstack(
                    rx.text("Observaciones", size="2", color="#1F1F1F"),
                    rx.input(
                        placeholder="Observaciones adicionales...",
                        value=SolicitanteRMState.recurso_observaciones,
                        on_change=SolicitanteRMState.set_recurso_observaciones,
                        width="100%"
                    ),
                    spacing="1",
                    align="start",
                    width="100%"
                ),
                rx.button(
                    "➕ Agregar Recurso a la Lista",
                    on_click=SolicitanteRMState.agregar_recurso,
                    variant="outline",
                    width="100%",
                    color_scheme="blue"
                ),
                spacing="3",
            ),
            width="100%",
            padding="1rem",
            border="2px dashed #cbd5e1",
            border_radius="8px",
            margin_bottom="1rem"
        )
    
    # Formulario principal
    def formulario_principal():
        return rx.form(
            rx.vstack(
                rx.heading("📋 Datos Generales de la Solicitud", size="4", color="#1F1F1F"),
                rx.hstack(
                    rx.vstack(
                        rx.text("Centro de costo *", size="2", color="#1F1F1F"),
                        rx.input(
                            placeholder="Ej: Obra #123",
                            name="centro_costo",
                            required=True,
                            value=SolicitanteRMState.centro_costo,
                            on_change=SolicitanteRMState.set_centro_costo,
                            width="100%"
                        ),
                        spacing="1",
                        align="start",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Fecha *", size="2", color="#1F1F1F"),
                        rx.input(
                            type="date",
                            name="fecha",
                            required=True,
                            value=SolicitanteRMState.fecha,
                            on_change=SolicitanteRMState.set_fecha,
                            width="100%"
                        ),
                        spacing="1",
                        align="start",
                        width="100%"
                    ),
                    rx.vstack(
                        rx.text("Orden de trabajo *", size="2", color="#1F1F1F"),
                        rx.input(
                            placeholder="Ej: OT-2024-001",
                            name="orden_trabajo",
                            required=True,
                            value=SolicitanteRMState.orden_trabajo,
                            on_change=SolicitanteRMState.set_orden_trabajo,
                            width="100%"
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
                    "📤 Enviar Solicitud Completa",
                    type="submit",
                    variant="solid",
                    width="100%",
                    loading=SolicitanteRMState.loading_form_rm,
                    size="3",
                    disabled=SolicitanteRMState.total_recursos == 0,
                    style={
                        "background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
                        "color": "white",
                        "font_weight": "600",
                        "margin_top": "1rem"
                    }
                ),
                spacing="3",
            ),
            on_submit=SolicitanteRMState.crear_solicitud_rm,
            reset_on_submit=True
        )
    
    # Tabla de historial de Recursos RM (con paginación)
    def historial_solicitudes():
        """Tabla de historial de solicitudes RM con paginación."""
        
        # Botón de página individual
        def create_page_button_rm(page_num: int):
            return rx.button(
                rx.text(page_num, size="2", font_weight="500"),
                on_click=lambda: SolicitanteRMState.go_to_page_rm(page_num),
                variant="soft",
                size="2",
                style=rx.cond(
                    SolicitanteRMState.rm_current_page == page_num,
                    {
                        "background": "#3b82f6",
                        "color": "white",
                        "border": "1px solid #3b82f6",
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
        def render_pagination_rm():
            return rx.hstack(
                # Botón anterior
                rx.button(
                    rx.icon("chevron-left", size=16),
                    on_click=SolicitanteRMState.previous_page_rm,
                    variant="soft",
                    size="2",
                    is_disabled=SolicitanteRMState.rm_current_page == 1,
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
                        rx.cond(
                            (SolicitanteRMState.rm_current_page > 3) & (SolicitanteRMState.rm_total_pages > 4),
                            rx.hstack(
                                create_page_button_rm(1),
                                rx.text("...", size="2", color="#64748b", padding_x="1"),
                                spacing="1",
                                flex_shrink=0,
                            ),
                        ),
                        rx.cond(
                            SolicitanteRMState.rm_page_numbers.length() > 0,
                            rx.hstack(
                                rx.foreach(
                                    SolicitanteRMState.rm_page_numbers,
                                    create_page_button_rm
                                ),
                                spacing="1",
                                wrap="nowrap",
                                flex_shrink=0,
                            ),
                            rx.text(
                                f"Pág. {SolicitanteRMState.rm_current_page}",
                                size="2",
                                color="#64748b",
                                padding_x="2",
                                flex_shrink=0,
                            ),
                        ),
                        rx.cond(
                            (SolicitanteRMState.rm_current_page < SolicitanteRMState.rm_total_pages - 2) & (SolicitanteRMState.rm_total_pages > 4),
                            rx.hstack(
                                rx.text("...", size="2", color="#64748b", padding_x="1"),
                                create_page_button_rm(SolicitanteRMState.rm_total_pages),
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
                    on_click=SolicitanteRMState.next_page_rm,
                    variant="soft",
                    size="2",
                    is_disabled=SolicitanteRMState.rm_current_page == SolicitanteRMState.rm_total_pages,
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
        
        # Fila de solicitud RM
        def solicitud_row_rm(solicitud):
            return rx.table.row(
                rx.table.cell(
                    rx.text(solicitud["id"], color="#1F1F1F"),
                    style={"padding": "8px 4px"}
                ),
                rx.table.cell(
                    rx.text(
                        rx.cond(solicitud["centro_costo"] != "", solicitud["centro_costo"], "-"),
                        color="#1F1F1F"
                    ),
                    style={"padding": "8px 4px"}
                ),
                rx.table.cell(
                    rx.text(
                        rx.cond(solicitud["fecha"] != "", solicitud["fecha"], "-"),
                        color="#1F1F1F"
                    ),
                    style={"padding": "8px 4px"}
                ),
                rx.table.cell(
                    rx.text(
                        rx.cond(solicitud["orden_trabajo"] != "", solicitud["orden_trabajo"], "-"),
                        color="#1F1F1F"
                    ),
                    style={"padding": "8px 4px"}
                ),
                rx.table.cell(
                    rx.text(
                        rx.cond(solicitud["num_recursos"] != 0, f"{solicitud['num_recursos']} recursos", "-"),
                        color="#1F1F1F"
                    ),
                    style={"padding": "8px 4px"}
                ),
                rx.table.cell(
                    estado_badge(solicitud["estado"]),
                    style={"padding": "8px 4px"}
                ),
                rx.table.cell(
                    rx.text(
                        rx.cond(solicitud["fecha_creacion_display"] != "", solicitud["fecha_creacion_display"], "-"),
                        color="#1F1F1F"
                    ),
                    style={"padding": "8px 4px"}
                ),
            )
        
        header_style = {
            "background": "#3b82f6",
            "color": "white",
            "font_weight": "600",
            "padding": "12px 4px",
            "text_align": "left",
            "white_space": "nowrap"
        }
        
        return rx.vstack(
            rx.hstack(
                rx.button(
                    "🔄 Actualizar",
                    on_click=SolicitanteRMState.load_mis_solicitudes_rm,
                    loading=SolicitanteRMState.loading_historial_rm,
                    variant="soft",
                ),
                rx.badge(
                    rx.text(f"{SolicitanteRMState.total_solicitudes} solicitudes"),
                    color_scheme="blue",
                    variant="soft",
                ),
                spacing="3",
                width="100%",
                wrap="wrap"
            ),
            
            rx.cond(
                SolicitanteRMState.loading_historial_rm,
                rx.center(rx.spinner(size="3"), padding="3rem"),
                rx.cond(
                    SolicitanteRMState.total_solicitudes == 0,
                    rx.center(
                        rx.vstack(
                            rx.icon("file_text", size=32, color="#cbd5e1"),
                            rx.text("No tienes solicitudes de recursos", size="3", color="#64748b"),
                            spacing="2",
                        ),
                        padding="3rem",
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
                                            rx.table.column_header_cell("Fecha", style=header_style),
                                            rx.table.column_header_cell("Orden Trabajo", style=header_style),
                                            rx.table.column_header_cell("Recursos", style=header_style),
                                            rx.table.column_header_cell("Estado", style=header_style),
                                            rx.table.column_header_cell("Fecha Creación", style=header_style),
                                        )
                                    ),
                                    rx.table.body(
                                        rx.foreach(
                                            SolicitanteRMState.rm_solicitudes_paginated,
                                            solicitud_row_rm
                                        )
                                    ),
                                    variant="surface",
                                    size="3",
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
                                    "max_height": "600px",
                                    "height": "auto",
                                    "overflow_y": "auto",
                                    "border": "1px solid #e2e8f0",
                                    "border_radius": "8px"
                                }
                            ),
                            width="100%"
                        ),
                        # Controles de paginación
                        rx.cond(
                            SolicitanteRMState.total_solicitudes > SolicitanteRMState.rm_items_per_page,
                            rx.box(
                                rx.hstack(
                                    rx.text(
                                        rx.cond(
                                            SolicitanteRMState.total_solicitudes > 0,
                                            rx.cond(
                                                SolicitanteRMState.rm_current_page == 1,
                                                "Mostrando 1 a " + rx.cond(
                                                    SolicitanteRMState.rm_items_per_page > SolicitanteRMState.total_solicitudes,
                                                    SolicitanteRMState.total_solicitudes.to(str),
                                                    SolicitanteRMState.rm_items_per_page.to(str)
                                                ) + " de " + SolicitanteRMState.total_solicitudes.to(str) + " resultados",
                                                "Mostrando " + ((SolicitanteRMState.rm_current_page - 1) * SolicitanteRMState.rm_items_per_page + 1).to(str) + " a " + rx.cond(
                                                    SolicitanteRMState.rm_current_page * SolicitanteRMState.rm_items_per_page > SolicitanteRMState.total_solicitudes,
                                                    SolicitanteRMState.total_solicitudes.to(str),
                                                    (SolicitanteRMState.rm_current_page * SolicitanteRMState.rm_items_per_page).to(str)
                                                ) + " de " + SolicitanteRMState.total_solicitudes.to(str) + " resultados"
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
                                        render_pagination_rm(),
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
            ),
            spacing="4",
            width="100%",
        )
    
    # FUNCIONES PARA FINANCIAMIENTO
    def estado_badge_fin(estado):
        """Muestra un badge para el estado de la solicitud de financiamiento"""
        return rx.match(
            estado,
            ("pendiente_revfin", rx.badge("PENDIENTE REV. FIN", color_scheme="amber", variant="soft")),
            ("aprobado_revfin", rx.badge("APROBADO REV. FIN", color_scheme="blue", variant="soft")),
            ("completada", rx.badge("COMPLETADA", color_scheme="purple", variant="soft")),
            rx.badge("RECHAZADA", color_scheme="red", variant="soft")
        )
    
    def formulario_financiamiento():
        """Formulario para solicitud de financiamiento con múltiples recursos"""
        return rx.vstack(
            rx.heading("    Complete el formulario", size="4", color="#1F1F1F"),
            
            # Datos de cabecera
            rx.box(
                rx.vstack(
                    rx.heading("📋 Datos de la Solicitud", size="5", color="#1F1F1F"),
                    rx.hstack(
                        rx.vstack(
                            rx.text("Área solicitante *", size="2", color="#1F1F1F"),
                            rx.input(
                                placeholder="Ej: Taller Mecánico",
                                value=SolicitanteRMState.area_solicitante_fin,
                                on_change=SolicitanteRMState.set_area_solicitante_fin,
                                width="100%"
                            ),
                            spacing="1",
                            align="start",
                            width="100%"
                        ),
                        rx.vstack(
                            rx.text("Fecha *", size="2", color="#1F1F1F"),
                            rx.input(
                                type="date",
                                value=SolicitanteRMState.fecha_fin,
                                on_change=SolicitanteRMState.set_fecha_fin,
                                width="100%"
                            ),
                            spacing="1",
                            align="start",
                            width="100%"
                        ),
                        spacing="3",
                        width="100%",
                        wrap="wrap"
                    ),
                    
                    rx.hstack(
                        rx.vstack(
                            rx.text("Número contrato/suplemento", size="2", color="#1F1F1F"),
                            rx.input(
                                placeholder="Ej: CT-2024-001",
                                value=SolicitanteRMState.numero_contrato_fin,
                                on_change=SolicitanteRMState.set_numero_contrato_fin,
                                width="100%"
                            ),
                            spacing="1",
                            align="start",
                            width="100%"
                        ),
                        rx.vstack(
                            rx.text("Orden de trabajo *", size="2", color="#1F1F1F"),
                            rx.input(
                                placeholder="Ej: OT-2024-001",
                                value=SolicitanteRMState.orden_trabajo_fin,
                                on_change=SolicitanteRMState.set_orden_trabajo_fin,
                                width="100%"
                            ),
                            spacing="1",
                            align="start",
                            width="100%"
                        ),
                        spacing="3",
                        width="100%",
                        wrap="wrap"
                    ),
                    spacing="3",
                ),
                width="100%",
                padding="1rem",
                border="1px solid #e2e8f0",
                border_radius="8px",
                margin_bottom="1rem"
            ),
            
            # Agregar productos
            rx.box(
                rx.vstack(
                    rx.heading("➕ Agregar Productos", size="5", color="#1F1F1F"),
                    rx.hstack(
                        rx.vstack(
                            rx.text("Servicio/Tipo *", size="2", color="#1F1F1F"),
                            rx.select(
                                SolicitanteRMState.tipos_productos,
                                placeholder="Seleccione un tipo...",
                                value=SolicitanteRMState.recurso_fin_servicio,
                                on_change=SolicitanteRMState.set_recurso_fin_servicio,
                                width="100%"
                            ),
                            spacing="1",
                            align="start",
                            width="100%"
                        ),
                        rx.vstack(
                            rx.text("Descripción *", size="2", color="#1F1F1F"),
                            rx.input(
                                placeholder="Ej: Cable eléctrico 2.5mm",
                                value=SolicitanteRMState.recurso_fin_descripcion,
                                on_change=SolicitanteRMState.set_recurso_fin_descripcion,
                                width="100%"
                            ),
                            spacing="1",
                            align="start",
                            width="100%"
                        ),
                        rx.vstack(
                            rx.text("Cantidad *", size="2", color="#1F1F1F"),
                            rx.input(
                                placeholder="Ej: 10",
                                type="number",
                                min="1",
                                step="1",
                                value=SolicitanteRMState.recurso_fin_cantidad,
                                on_change=SolicitanteRMState.set_recurso_fin_cantidad,
                                width="100%"
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
                        "➕ Agregar Producto a la Lista",
                        on_click=SolicitanteRMState.agregar_recurso_fin,
                        variant="outline",
                        width="100%",
                        color_scheme="green"
                    ),
                    spacing="3",
                ),
                width="100%",
                padding="1rem",
                border="2px dashed #cbd5e1",
                border_radius="8px",
                margin_bottom="1rem"
            ),
            
            # Lista de productos agregados
            rx.cond(
                SolicitanteRMState.total_recursos_fin > 0,
                rx.box(
                    rx.vstack(
                        rx.heading("📋 Productos Agregados", size="4", color="#1F1F1F"),
                        rx.box(
                            rx.scroll_area(
                                rx.table.root(
                                    rx.table.header(
                                        rx.table.row(
                                            rx.table.column_header_cell("No.", color="#1F1F1F"),
                                            rx.table.column_header_cell("Servicio/Tipo", color="#1F1F1F"),
                                            rx.table.column_header_cell("Descripción", color="#1F1F1F"),
                                            rx.table.column_header_cell("Cantidad", color="#1F1F1F"),
                                            rx.table.column_header_cell("Acción", color="#1F1F1F"),
                                        )
                                    ),
                                    rx.table.body(
                                        rx.foreach(
                                            SolicitanteRMState.recursos_fin,
                                            lambda recurso, idx: rx.table.row(
                                                rx.table.cell(
                                                    rx.text(idx + 1), 
                                                    color="#1F1F1F"
                                                ),
                                                rx.table.cell(
                                                    rx.text(
                                                        rx.cond(
                                                            recurso["servicio"] != "",
                                                            recurso["servicio"],
                                                            "-"
                                                        )
                                                    ), 
                                                    color="#1F1F1F"
                                                ),
                                                rx.table.cell(
                                                    rx.text(
                                                        rx.cond(
                                                            recurso["descripcion"] != "",
                                                            recurso["descripcion"],
                                                            "-"
                                                        ),
                                                        style={
                                                            "max_width": "200px",
                                                            "overflow": "hidden",
                                                            "text_overflow": "ellipsis",
                                                            "white_space": "nowrap"
                                                        }
                                                    ), 
                                                    color="#1F1F1F"
                                                ),
                                                # CELDA DE CANTIDAD CORREGIDA
                                                rx.table.cell(
                                                    rx.text(
                                                        rx.cond(
                                                            recurso["cantidad"] != "",
                                                            recurso["cantidad"].to(str),  # <--- CORRECCIÓN AQUÍ
                                                            "-"
                                                        )
                                                    ), 
                                                    color="#1F1F1F"
                                                ),
                                                rx.table.cell(
                                                    rx.button(
                                                        "❌",
                                                        on_click=lambda idx=idx: SolicitanteRMState.eliminar_recurso_fin(idx),
                                                        color_scheme="red",
                                                        size="1",
                                                        variant="ghost"
                                                    ),
                                                    color="#1F1F1F"
                                                ),
                                            )
                                        )
                                    ),
                                    variant="surface",
                                ),
                                type="always",
                                scrollbars="horizontal",
                                style={
                                    "width": "100%",
                                    "border": "1px solid #e2e8f0",
                                    "border_radius": "8px"
                                }
                            ),
                            width="100%",
                            overflow_x="auto"
                        ),
                        spacing="2",
                    ),
                    width="100%",
                    padding="1rem",
                    border="1px solid #e2e8f0",
                    border_radius="8px",
                    margin_bottom="1rem"
                ),
                rx.box(
                    rx.text("No hay productos agregados aún", color="#64748b"),
                    padding="1rem",
                    border="1px dashed #cbd5e1",
                    border_radius="8px",
                    text_align="center"
                )
            ),
            
            # Botón para enviar
            rx.form(
                rx.button(
                    "💰 Enviar Solicitud de Financiamiento",
                    type="submit",
                    variant="solid",
                    width="100%",
                    loading=SolicitanteRMState.loading_fin,
                    size="3",
                    disabled=SolicitanteRMState.total_recursos_fin == 0,
                    style={
                        "background": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
                        "color": "white",
                        "font_weight": "600"
                    }
                ),
                on_submit=SolicitanteRMState.crear_solicitud_fin,
                reset_on_submit=True
            ),
            
            rx.text(
                "💰 Los precios se calcularán automáticamente (precio base + 25%)",
                size="1",
                color="#64748b",
                margin_top="0.5rem"
            ),
            spacing="3",
            width="100%",
        )

    # Tabla de historial de financiamiento (con paginación)
    def historial_financiamiento():
        """Tabla de historial de financiamiento con paginación."""
        
        # Botón de página individual
        def create_page_button_fin(page_num: int):
            return rx.button(
                rx.text(page_num, size="2", font_weight="500"),
                on_click=lambda: SolicitanteRMState.go_to_page_fin(page_num),
                variant="soft",
                size="2",
                style=rx.cond(
                    SolicitanteRMState.fin_current_page == page_num,
                    {
                        "background": "#10b981",
                        "color": "white",
                        "border": "1px solid #10b981",
                        "_hover": {"background": "#059669"},
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
        def render_pagination_fin():
            return rx.hstack(
                # Botón anterior
                rx.button(
                    rx.icon("chevron-left", size=16),
                    on_click=SolicitanteRMState.previous_page_fin,
                    variant="soft",
                    size="2",
                    is_disabled=SolicitanteRMState.fin_current_page == 1,
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
                        rx.cond(
                            (SolicitanteRMState.fin_current_page > 3) & (SolicitanteRMState.fin_total_pages > 4),
                            rx.hstack(
                                create_page_button_fin(1),
                                rx.text("...", size="2", color="#64748b", padding_x="1"),
                                spacing="1",
                                flex_shrink=0,
                            ),
                        ),
                        rx.cond(
                            SolicitanteRMState.fin_page_numbers.length() > 0,
                            rx.hstack(
                                rx.foreach(
                                    SolicitanteRMState.fin_page_numbers,
                                    create_page_button_fin
                                ),
                                spacing="1",
                                wrap="nowrap",
                                flex_shrink=0,
                            ),
                            rx.text(
                                f"Pág. {SolicitanteRMState.fin_current_page}",
                                size="2",
                                color="#64748b",
                                padding_x="2",
                                flex_shrink=0,
                            ),
                        ),
                        rx.cond(
                            (SolicitanteRMState.fin_current_page < SolicitanteRMState.fin_total_pages - 2) & (SolicitanteRMState.fin_total_pages > 4),
                            rx.hstack(
                                rx.text("...", size="2", color="#64748b", padding_x="1"),
                                create_page_button_fin(SolicitanteRMState.fin_total_pages),
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
                    on_click=SolicitanteRMState.next_page_fin,
                    variant="soft",
                    size="2",
                    is_disabled=SolicitanteRMState.fin_current_page == SolicitanteRMState.fin_total_pages,
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
        
        # Fila de solicitud de financiamiento
        def solicitud_row_fin(solicitud):
            return rx.table.row(
                rx.table.cell(
                    rx.text(
                        rx.cond(solicitud["numero_solicitud"] != "", solicitud["numero_solicitud"], "-"),
                        color="#1F1F1F"
                    ),
                    style={"padding": "8px 4px"}
                ),
                rx.table.cell(
                    rx.text(
                        rx.cond(solicitud["Area solicitante"] != "", solicitud["Area solicitante"], "-"),
                        color="#1F1F1F"
                    ),
                    style={"padding": "8px 4px"}
                ),
                rx.table.cell(
                    rx.text(
                        rx.cond(solicitud["Fecha"] != "", solicitud["Fecha"], "-"),
                        color="#1F1F1F"
                    ),
                    style={"padding": "8px 4px"}
                ),
                rx.table.cell(
                    rx.text(f"${solicitud['Total']:.2f}", color="#1F1F1F"),
                    style={"padding": "8px 4px"}
                ),
                rx.table.cell(
                    estado_badge_fin(solicitud["estado"]),
                    style={"padding": "8px 4px"}
                ),
            )
        
        header_style = {
            "background": "#10b981",
            "color": "white",
            "font_weight": "600",
            "padding": "12px 4px",
            "text_align": "left",
            "white_space": "nowrap"
        }
        
        return rx.vstack(
            rx.hstack(
                rx.button(
                    "🔄 Actualizar",
                    on_click=SolicitanteRMState.load_mis_solicitudes_fin,
                    loading=SolicitanteRMState.loading_fin,
                    variant="soft",
                ),
                rx.badge(
                    rx.text(f"{SolicitanteRMState.total_solicitudes_fin} solicitudes"),
                    color_scheme="green",
                    variant="soft",
                ),
                spacing="3",
                width="100%",
                wrap="wrap"
            ),
            
            rx.cond(
                SolicitanteRMState.loading_fin,
                rx.center(rx.spinner(size="3"), padding="3rem"),
                rx.cond(
                    SolicitanteRMState.total_solicitudes_fin == 0,
                    rx.center(
                        rx.vstack(
                            rx.icon("dollar_sign", size=32, color="#cbd5e1"),
                            rx.text("No tienes solicitudes de financiamiento", size="3", color="#64748b"),
                            spacing="2",
                        ),
                        padding="3rem",
                    ),
                    rx.vstack(
                        # Tabla con scroll horizontal
                        rx.box(
                            rx.scroll_area(
                                rx.table.root(
                                    rx.table.header(
                                        rx.table.row(
                                            rx.table.column_header_cell("N° Solicitud", style=header_style),
                                            rx.table.column_header_cell("Área", style=header_style),
                                            rx.table.column_header_cell("Fecha", style=header_style),
                                            rx.table.column_header_cell("Total", style=header_style),
                                            rx.table.column_header_cell("Estado", style=header_style),
                                        )
                                    ),
                                    rx.table.body(
                                        rx.foreach(
                                            SolicitanteRMState.fin_solicitudes_paginated,
                                            solicitud_row_fin
                                        )
                                    ),
                                    variant="surface",
                                    size="3",
                                    style={
                                        "width": "100%",
                                        "min_width": "600px",
                                        "table_layout": "auto"
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
                                    "border_radius": "8px"
                                }
                            ),
                            width="100%"
                        ),
                        # Controles de paginación
                        rx.cond(
                            SolicitanteRMState.total_solicitudes_fin > SolicitanteRMState.fin_items_per_page,
                            rx.box(
                                rx.hstack(
                                    rx.text(
                                        rx.cond(
                                            SolicitanteRMState.total_solicitudes_fin > 0,
                                            rx.cond(
                                                SolicitanteRMState.fin_current_page == 1,
                                                "Mostrando 1 a " + rx.cond(
                                                    SolicitanteRMState.fin_items_per_page > SolicitanteRMState.total_solicitudes_fin,
                                                    SolicitanteRMState.total_solicitudes_fin.to(str),
                                                    SolicitanteRMState.fin_items_per_page.to(str)
                                                ) + " de " + SolicitanteRMState.total_solicitudes_fin.to(str) + " resultados",
                                                "Mostrando " + ((SolicitanteRMState.fin_current_page - 1) * SolicitanteRMState.fin_items_per_page + 1).to(str) + " a " + rx.cond(
                                                    SolicitanteRMState.fin_current_page * SolicitanteRMState.fin_items_per_page > SolicitanteRMState.total_solicitudes_fin,
                                                    SolicitanteRMState.total_solicitudes_fin.to(str),
                                                    (SolicitanteRMState.fin_current_page * SolicitanteRMState.fin_items_per_page).to(str)
                                                ) + " de " + SolicitanteRMState.total_solicitudes_fin.to(str) + " resultados"
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
            ),
            spacing="4",
            width="100%",
        )

    # Pestaña de financiamiento completa
    def financiamiento_tab():
        """Pestaña completa de financiamiento con subtabs"""
        
        # --- Helper interno para la tabla de precios con paginación (estilo logística) ---
        def precios_table() -> rx.Component:
            """Tabla de precios con paginación estilo logística."""
            
            # Botón de página individual
            def create_page_button_precios(page_num: int):
                return rx.button(
                    rx.text(page_num, size="2", font_weight="500"),
                    on_click=lambda: SolicitanteRMState.go_to_page_precios(page_num),
                    variant="soft",
                    size="2",
                    style=rx.cond(
                        SolicitanteRMState.current_page_precios == page_num,
                        {
                            "background": "#10b981",
                            "color": "white",
                            "border": "1px solid #10b981",
                            "_hover": {"background": "#059669"},
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
            def render_pagination_precios():
                return rx.hstack(
                    # Botón anterior
                    rx.button(
                        rx.icon("chevron-left", size=16),
                        on_click=SolicitanteRMState.previous_page_precios,
                        variant="soft",
                        size="2",
                        is_disabled=SolicitanteRMState.current_page_precios == 1,
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
                            rx.cond(
                                (SolicitanteRMState.current_page_precios > 3) & (SolicitanteRMState.total_pages_precios > 4),
                                rx.hstack(
                                    create_page_button_precios(1),
                                    rx.text("...", size="2", color="#64748b", padding_x="1"),
                                    spacing="1",
                                    flex_shrink=0,
                                ),
                            ),
                            rx.cond(
                                SolicitanteRMState.page_numbers_precios.length() > 0,
                                rx.hstack(
                                    rx.foreach(
                                        SolicitanteRMState.page_numbers_precios,
                                        create_page_button_precios
                                    ),
                                    spacing="1",
                                    wrap="nowrap",
                                    flex_shrink=0,
                                ),
                                rx.text(
                                    f"Pág. {SolicitanteRMState.current_page_precios}",
                                    size="2",
                                    color="#64748b",
                                    padding_x="2",
                                    flex_shrink=0,
                                ),
                            ),
                            rx.cond(
                                (SolicitanteRMState.current_page_precios < SolicitanteRMState.total_pages_precios - 2) & (SolicitanteRMState.total_pages_precios > 4),
                                rx.hstack(
                                    rx.text("...", size="2", color="#64748b", padding_x="1"),
                                    create_page_button_precios(SolicitanteRMState.total_pages_precios),
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
                        on_click=SolicitanteRMState.next_page_precios,
                        variant="soft",
                        size="2",
                        is_disabled=SolicitanteRMState.current_page_precios == SolicitanteRMState.total_pages_precios,
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
            
            # Fila de precio
            def precio_row(precio):
                return rx.table.row(
                    rx.table.cell(
                        rx.text(precio.get("Tipo", "-"), color="#1F1F1F"),
                        style={"padding": "8px 4px"}
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
                        rx.text(f"${precio.get('Precio_str', '0.00')}", color="#1F1F1F"),
                        style={"padding": "8px 4px", "min_width": "100px"}
                    ),
                    rx.table.cell(
                        rx.text(f"${precio.get('Precio_final_str', '0.00')}", color="#1F1F1F", font_weight="600"),
                        style={"padding": "8px 4px", "min_width": "100px"}
                    ),
                )
            
            header_style = {
                "background": "#10b981",
                "color": "white",
                "font_weight": "600",
                "padding": "12px 4px",
                "text_align": "left",
                "white_space": "nowrap"
            }
            
            return rx.cond(
                SolicitanteRMState.precios_loading,
                rx.center(rx.spinner(size="3"), padding="3rem"),
                rx.cond(
                    SolicitanteRMState.precios_disponibles.length() == 0,
                    rx.center(
                        rx.vstack(
                            rx.icon("package", size=32, color="#cbd5e1"),
                            rx.text("No hay productos disponibles", size="3", color="#64748b"),
                            spacing="2",
                        ),
                        padding="3rem",
                    ),
                    rx.vstack(
                        # Tabla con scroll horizontal
                        rx.box(
                            rx.scroll_area(
                                rx.table.root(
                                    rx.table.header(
                                        rx.table.row(
                                            rx.table.column_header_cell("Tipo", style=header_style),
                                            rx.table.column_header_cell("Descripción", style=header_style),
                                            rx.table.column_header_cell("Precio Base", style=header_style),
                                            rx.table.column_header_cell("Precio Final", style=header_style),
                                        )
                                    ),
                                    rx.table.body(
                                        rx.foreach(
                                            SolicitanteRMState.precios_paginated,
                                            precio_row
                                        )
                                    ),
                                    style={
                                        "width": "100%",
                                        "min_width": "600px",
                                        "table_layout": "auto"
                                    }
                                ),
                                type="always",
                                scrollbars="horizontal",
                                style={
                                    "width": "100%",
                                    "height": "400px",
                                    "border": "1px solid #e2e8f0",
                                    "border_radius": "8px"
                                }
                            ),
                            width="100%",
                            overflow_x="auto"
                        ),
                        # Paginación
                        rx.cond(
                            SolicitanteRMState.precios_disponibles.length() > SolicitanteRMState.items_per_page_precios,
                            rx.box(
                                rx.hstack(
                                    rx.text(
                                        rx.cond(
                                            SolicitanteRMState.precios_disponibles.length() > 0,
                                            rx.cond(
                                                SolicitanteRMState.current_page_precios == 1,
                                                "Mostrando 1 a " + rx.cond(
                                                    SolicitanteRMState.items_per_page_precios > SolicitanteRMState.precios_disponibles.length(),
                                                    SolicitanteRMState.precios_disponibles.length().to(str),
                                                    SolicitanteRMState.items_per_page_precios.to(str)
                                                ) + " de " + SolicitanteRMState.precios_disponibles.length().to(str) + " resultados",
                                                "Mostrando " + ((SolicitanteRMState.current_page_precios - 1) * SolicitanteRMState.items_per_page_precios + 1).to(str) + " a " + rx.cond(
                                                    SolicitanteRMState.current_page_precios * SolicitanteRMState.items_per_page_precios > SolicitanteRMState.precios_disponibles.length(),
                                                    SolicitanteRMState.precios_disponibles.length().to(str),
                                                    (SolicitanteRMState.current_page_precios * SolicitanteRMState.items_per_page_precios).to(str)
                                                ) + " de " + SolicitanteRMState.precios_disponibles.length().to(str) + " resultados"
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
                                        render_pagination_precios(),
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
                        width="100%",
                    )
                )
            )
        
        # --- Estructura de la pestaña con subtabs ---
        return rx.vstack(
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("➕ Nueva Solicitud", value="nueva_fin", color="#1F1F1F"),
                    rx.tabs.trigger("📋 Historial Financiamiento", value="historial_fin", color="#1F1F1F"),
                    rx.tabs.trigger("💰 Productos Disponibles", value="precios_fin", color="#1F1F1F"),
                ),
                
                rx.tabs.content(
                    rx.vstack(
                        rx.card(
                            rx.vstack(
                                rx.heading("💰 Nueva Solicitud de Financiamiento", size="5", color="#1F1F1F"),
                                rx.text(
                                    "Completa los datos para solicitar financiamiento de materiales",
                                    size="2",
                                    color="#64748b",
                                    margin_bottom="1rem"
                                ),
                                formulario_financiamiento(),
                                spacing="3",
                            ),
                            width="100%"
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    value="nueva_fin",
                    style={"padding": "1.5rem 0"}
                ),
                
                rx.tabs.content(
                    rx.vstack(
                        rx.card(
                            rx.vstack(
                                rx.heading("📋 Historial de Solicitudes de Financiamiento", size="5", color="#1F1F1F"),
                                historial_financiamiento(),
                                spacing="3",
                            ),
                            width="100%"
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    value="historial_fin",
                    style={"padding": "1.5rem 0"}
                ),

                rx.tabs.content(
                    rx.vstack(
                        rx.card(
                            rx.vstack(
                                rx.heading("💰 Productos y Precios Disponibles", size="5", color="#1F1F1F"),
                                rx.text(
                                    "Consulta los productos disponibles con sus precios base",
                                    size="2",
                                    color="#64748b",
                                    margin_bottom="1rem"
                                ),
                                rx.hstack(
                                    rx.button(
                                        "🔄 Cargar Productos",
                                        on_click=SolicitanteRMState.load_precios_disponibles,
                                        loading=SolicitanteRMState.precios_loading,
                                        variant="soft",
                                        size="2"
                                    ),
                                    rx.text(
                                        "Nota: El precio final incluye un 25% adicional al precio base",
                                        size="1",
                                        color="#64748b",
                                        font_style="italic"
                                    ),
                                    spacing="3",
                                    wrap="wrap",
                                    width="100%"
                                ),
                                
                                precios_table(),
                                
                                spacing="3",
                            ),
                            width="100%"
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    value="precios_fin",
                    style={"padding": "1.5rem 0"}
                ),
                
                default_value="nueva_fin",
                width="100%",
            ),
            spacing="4",
            width="100%",
        )
    
    # Diálogo de éxito
    def success_dialog():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("✅ Solicitud Creada", color="#212121"),
                rx.dialog.description(
                    "Tu solicitud de recursos ha sido creada exitosamente y será revisada por el Jefe de Área Técnica.",
                    color="#212121",
                ),
                rx.dialog.close(
                    rx.button(
                        "Aceptar",
                        on_click=SolicitanteRMState.close_success_dialog,
                        variant="solid",
                        size="2"
                    ),
                ),
                max_width="500px",
                style={
                    "background": "white",
                    "border_radius": "12px",
                    "box_shadow": "0 20px 25px -5px rgba(0, 0, 0, 0.1)"
                }
            ),
            open=SolicitanteRMState.show_success,
        )
    
    def success_dialog_fin():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("✅ Solicitud de Financiamiento Creada", color="#212121"),
                rx.dialog.description(
                    "Tu solicitud de financiamiento ha sido creada exitosamente y será revisada por el Revisor Financiero.",
                    color="#212121",
                ),
                rx.dialog.close(
                    rx.button(
                        "Aceptar",
                        on_click=SolicitanteRMState.close_success_dialog_fin,
                        variant="solid",
                        size="2"
                    ),
                ),
                max_width="500px",
                style={
                    "background": "white",
                    "border_radius": "12px",
                    "box_shadow": "0 20px 25px -5px rgba(0, 0, 0, 0.1)"
                }
            ),
            open=SolicitanteRMState.show_success_fin,
        )
    
    def dashboard_content():
        return rx.box(
            navbar("Solicitud de Recursos y Materiales"),
            rx.vstack(
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.vstack(
                                rx.heading("📦 Solicitud de Recursos", size="7", color="#1F1F1F"),
                                rx.text(
                                    rx.cond(
                                        SolicitanteRMState.is_authenticated_rm,
                                        rx.hstack(
                                            rx.text("Solicitante: "),
                                            rx.text(SolicitanteRMState.current_solicitante_rm["usuario"]),
                                            spacing="1"
                                        ),
                                        rx.text("Usuario: No disponible")
                                    ),
                                    size="4",
                                    color="#64748b"
                                ),
                                align="start",
                                spacing="1"
                            ),
                            rx.spacer(),
                            width="100%"
                        ),
                        rx.hstack(
                            rx.badge(
                                rx.cond(
                                    SolicitanteRMState.total_recursos == 1,
                                    rx.text("1 recurso"),
                                    rx.text(f"{SolicitanteRMState.total_recursos} recursos")
                                ),
                                color_scheme="blue",
                                variant="soft",
                                size="2"
                            ),
                            rx.button(
                                "📋 Mis Solicitudes",
                                on_click=lambda: rx.redirect(Route.SOLICITANTE_RM_FORM.value),
                                variant="soft",
                                size="2"
                            ),
                            rx.button(
                                "🚪 Cerrar Sesión",
                                on_click=SolicitanteRMState.sign_out_rm,
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
                    ),
                    width="100%",
                    padding_bottom="1.5rem",
                    border_bottom="1px solid #e2e8f0"
                ),
                
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger("➕ Nueva Solicitud", value="nueva", color="#1F1F1F"),
                        rx.tabs.trigger("📋 Mis Solicitudes RM", value="historial", color="#1F1F1F"),
                        rx.tabs.trigger("💰 Financiamiento", value="financiamiento", color="#1F1F1F"),
                    ),
                    
                    rx.tabs.content(
                        rx.vstack(
                            rx.card(
                                rx.vstack(
                                    rx.heading("📋 Nueva Solicitud de Recursos", size="5", color="#1F1F1F"),
                                    rx.text(
                                        "Agrega todos los recursos que necesitas en esta solicitud",
                                        size="2",
                                        color="#64748b",
                                        margin_bottom="1rem"
                                    ),
                                    recursos_table(),
                                    formulario_recurso(),
                                    formulario_principal(),
                                    spacing="3",
                                ),
                                width="100%"
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        value="nueva",
                        style={"padding": "1.5rem 0"}
                    ),
                    
                    rx.tabs.content(
                        rx.vstack(
                            rx.card(
                                rx.vstack(
                                    rx.heading("📋 Historial de Solicitudes", size="5", color="#1F1F1F"),
                                    historial_solicitudes(),
                                    spacing="3",
                                ),
                                width="100%"
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        value="historial",
                        style={"padding": "1.5rem 0"}
                    ),
                    
                    rx.tabs.content(
                        financiamiento_tab(),
                        value="financiamiento",
                        style={"padding": "1.5rem 0"}
                    ),
                    
                    default_value="nueva",
                    width="100%",
                ),
                
                success_dialog(),
                success_dialog_fin(),
                
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
        SolicitanteRMState.is_authenticated_rm,
        dashboard_content(),
        rx.center(
            rx.vstack(
                rx.spinner(size="3"),
                rx.text("Redirigiendo al login...", margin_top="1rem"),
                rx.button("Ir al Login", on_click=lambda: rx.redirect(Route.SOLICITANTERM_LOGIN.value)),
                spacing="3",
                align="center",
                max_width="400px",
                padding="2rem",
            ),
            height="100vh",
            width="100%",
        )
    )