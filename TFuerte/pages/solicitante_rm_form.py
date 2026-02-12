import reflex as rx
from TFuerte.state.solicitante_rm_state import SolicitanteRMState
from TFuerte.components.navbar import navbar
from TFuerte.routes import Route

@rx.page(
    route=Route.SOLICITANTE_RM_FORM.value,
    title="Solicitud de Recursos - Solicitante",
    on_load=SolicitanteRMState.load_mis_solicitudes_rm
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
    
    # Tabla de historial de Recursos RM
    def historial_solicitudes():
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
                    rx.box(
                        rx.scroll_area(
                            rx.table.root(
                                rx.table.header(
                                    rx.table.row(
                                        rx.table.column_header_cell("ID", color="#1F1F1F"),
                                        rx.table.column_header_cell("Centro Costo", color="#1F1F1F"),
                                        rx.table.column_header_cell("Fecha", color="#1F1F1F"),
                                        rx.table.column_header_cell("Orden Trabajo", color="#1F1F1F"),
                                        rx.table.column_header_cell("Recursos", color="#1F1F1F"),
                                        rx.table.column_header_cell("Estado", color="#1F1F1F"),
                                        rx.table.column_header_cell("Fecha Creación", color="#1F1F1F"),
                                    )
                                ),
                                rx.table.body(
                                    rx.foreach(
                                        SolicitanteRMState.mis_solicitudes_rm,
                                        lambda solicitud: rx.table.row(
                                            rx.table.cell(
                                                rx.text(solicitud["id"]),
                                                color="#1F1F1F"
                                            ),
                                            rx.table.cell(
                                                rx.text(
                                                    rx.cond(
                                                        solicitud["centro_costo"] != "",
                                                        solicitud["centro_costo"],
                                                        "-"
                                                    )
                                                ), 
                                                color="#1F1F1F"
                                            ),
                                            rx.table.cell(
                                                rx.text(
                                                    rx.cond(
                                                        solicitud["fecha"] != "",
                                                        solicitud["fecha"],
                                                        "-"
                                                    )
                                                ), 
                                                color="#1F1F1F"
                                            ),
                                            rx.table.cell(
                                                rx.text(
                                                    rx.cond(
                                                        solicitud["orden_trabajo"] != "",
                                                        solicitud["orden_trabajo"],
                                                        "-"
                                                    )
                                                ), 
                                                color="#1F1F1F"
                                            ),
                                            rx.table.cell(
                                                rx.text(
                                                    rx.cond(
                                                        solicitud["num_recursos"] != 0,
                                                        rx.text(solicitud["num_recursos"], " recursos"),
                                                        "-"
                                                    )
                                                ),
                                                color="#1F1F1F"
                                            ),
                                            rx.table.cell(estado_badge(solicitud["estado"]), color="#1F1F1F"),
                                            rx.table.cell(
                                                rx.text(
                                                    rx.cond(
                                                        solicitud["fecha_creacion_display"] != "",
                                                        solicitud["fecha_creacion_display"],
                                                        "-"
                                                    )
                                                ), 
                                                color="#1F1F1F"
                                            ),
                                        )
                                    )
                                ),
                                variant="surface",
                                size="3"
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
                    )
                )
            ),
            spacing="4",
            width="100%",
        )
    
    # FUNCIONES PARA FINANCIAMIENTO (corregidas también)
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
            rx.heading("💰 Nueva Solicitud de Financiamiento", size="4", color="#1F1F1F"),
            
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
                                                rx.table.cell(
                                                    rx.text(
                                                        rx.cond(
                                                            recurso["cantidad"] != "",
                                                            str(recurso["cantidad"]),
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

    def historial_financiamiento():
        """Tabla de historial de financiamiento"""
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
                    rx.box(
                        rx.scroll_area(
                            rx.table.root(
                                rx.table.header(
                                    rx.table.row(
                                        rx.table.column_header_cell("N° Solicitud", color="#1F1F1F"),
                                        rx.table.column_header_cell("Área", color="#1F1F1F"),
                                        rx.table.column_header_cell("Fecha", color="#1F1F1F"),
                                        rx.table.column_header_cell("Total", color="#1F1F1F"),
                                        rx.table.column_header_cell("Estado", color="#1F1F1F"),
                                    )
                                ),
                                rx.table.body(
                                    rx.foreach(
                                        SolicitanteRMState.mis_solicitudes_fin,
                                        lambda solicitud: rx.table.row(
                                            rx.table.cell(
                                                rx.text(
                                                    rx.cond(
                                                        solicitud["numero_solicitud"] != "",
                                                        solicitud["numero_solicitud"],
                                                        "-"
                                                    )
                                                ),
                                                color="#1F1F1F"
                                            ),
                                            rx.table.cell(
                                                rx.text(
                                                    rx.cond(
                                                        solicitud["Area solicitante"] != "",
                                                        solicitud["Area solicitante"],
                                                        "-"
                                                    )
                                                ), 
                                                color="#1F1F1F"
                                            ),
                                            rx.table.cell(
                                                rx.text(
                                                    rx.cond(
                                                        solicitud["Fecha"] != "",
                                                        solicitud["Fecha"],
                                                        "-"
                                                    )
                                                ), 
                                                color="#1F1F1F"
                                            ),
                                            rx.table.cell(
                                                rx.text(f"${solicitud['Total']:.2f}"), 
                                                color="#1F1F1F"
                                            ),
                                            rx.table.cell(estado_badge_fin(solicitud["estado"]), color="#1F1F1F"),
                                        )
                                    )
                                ),
                                variant="surface",
                                size="3"
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
                    )
                )
            ),
            spacing="4",
            width="100%",
        )

    def financiamiento_tab():
        """Pestaña completa de financiamiento con subtabs"""
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
                                
                                rx.cond(
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
                                        rx.box(
                                            rx.scroll_area(
                                                rx.table.root(
                                                    rx.table.header(
                                                        rx.table.row(
                                                            rx.table.column_header_cell("Tipo", color="#1F1F1F"),
                                                            rx.table.column_header_cell("Descripción", color="#1F1F1F"),
                                                            rx.table.column_header_cell("Precio Base", color="#1F1F1F"),
                                                            rx.table.column_header_cell("Precio Final", color="#1F1F1F"),
                                                        )
                                                    ),
                                                    rx.table.body(
                                                        rx.foreach(
                                                            SolicitanteRMState.precios_disponibles,
                                                            lambda precio: rx.table.row(
                                                                rx.table.cell(
                                                                    rx.text(
                                                                        rx.cond(
                                                                            precio["Tipo"] != "",
                                                                            precio["Tipo"],
                                                                            "-"
                                                                        )
                                                                    ),
                                                                    color="#1F1F1F"
                                                                ),
                                                                rx.table.cell(
                                                                    rx.text(
                                                                        rx.cond(
                                                                            precio["Descripcion"] != "",
                                                                            precio["Descripcion"],
                                                                            "-"
                                                                        )
                                                                    ), 
                                                                    color="#1F1F1F"
                                                                ),
                                                                rx.table.cell(
                                                                    rx.text(f"${precio['Precio_str']}"), 
                                                                    color="#1F1F1F"
                                                                ),
                                                                rx.table.cell(
                                                                    rx.text(f"${precio['Precio_final_str']}"), 
                                                                    color="#1F1F1F",
                                                                    font_weight="600"
                                                                ),
                                                            )
                                                        )
                                                    ),
                                                    variant="surface",
                                                    size="3"
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
                                        )
                                    )
                                ),
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