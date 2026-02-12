# TFuerte/pages/solicitante_dashboard.py
import reflex as rx
from TFuerte.state.solicitante_dashboard_state import SolicitanteDashboardState
from TFuerte.state.almacen_state import AlmacenState
from TFuerte.components.navbar import navbar
from TFuerte.state.solicitante_auth_state import SolicitanteAuthState

@rx.page(
    route="/solicitante-dashboard",
    title="Dashboard - Solicitante",
    on_load=[SolicitanteDashboardState.on_load, AlmacenState.load_data]
)
def solicitante_dashboard() -> rx.Component:
    """Dashboard para solicitantes"""
    
    def nueva_solicitud_form():
        """Formulario para crear una nueva solicitud múltiple"""
        
        def recurso_form_row(recurso, index):
            """Fila individual para un recurso en el formulario"""
            return rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.heading(f"Recurso #{index + 1}", size="3", color="#1e293b"),
                        rx.spacer(),
                        rx.button(
                            "🗑️",
                            on_click=lambda: SolicitanteDashboardState.eliminar_recurso_form(index),
                            size="1",
                            color_scheme="red",
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
                        width="100%",
                        align="center"
                    ),
                    
                    rx.vstack(
                        rx.vstack(
                            rx.text("Descripción:", size="2", color="#64748b"),
                            rx.input(
                                placeholder="Descripción del recurso...",
                                value=recurso.get("descripcion", ""),
                                on_change=lambda value: SolicitanteDashboardState.set_recurso_field(index, "descripcion", value),
                                size="2",
                                width="100%"
                            ),
                            align="start",
                            spacing="1",
                            width="100%"
                        ),
                        
                        rx.vstack(
                            rx.text("Cantidad:", size="2", color="#64748b"),
                            rx.input(
                                type="number",
                                placeholder="Cantidad...",
                                value=recurso.get("cantidad", ""),
                                on_change=lambda value: SolicitanteDashboardState.set_recurso_field(index, "cantidad", value),
                                size="2",
                                width="100%",
                                min="1"
                            ),
                            align="start",
                            spacing="1",
                            width="100%"
                        ),
                        
                        rx.vstack(
                            rx.text("Observación:", size="2", color="#64748b"),
                            rx.input(
                                placeholder="Observación opcional...",
                                value=recurso.get("observacion", ""),
                                on_change=lambda value: SolicitanteDashboardState.set_recurso_field(index, "observacion", value),
                                size="2",
                                width="100%"
                            ),
                            align="start",
                            spacing="1",
                            width="100%"
                        ),
                        
                        spacing="3",
                        width="100%"
                    ),
                    
                    spacing="3",
                    width="100%"
                ),
                width="100%",
                padding="1rem",
                border_radius="md",
                border="1px solid #e2e8f0",
                background="#f8fafc"
            )
        
        return rx.box(
            rx.vstack(
                rx.box(
                    rx.hstack(
                        rx.vstack(
                            rx.heading("📝 Nueva Solicitud", size="5", color="#1e293b"),
                            rx.text(
                                "Complete los datos para solicitar recursos",
                                size="2",
                                color="#64748b"
                            ),
                            align="start",
                            spacing="1"
                        ),
                        rx.spacer(),
                        rx.cond(
                            SolicitanteDashboardState.tiene_recursos_en_formulario,
                            rx.badge(
                                f"{SolicitanteDashboardState.recursos_form.length()} recursos",
                                color_scheme="green",
                                variant="soft",
                                size="2"
                            ),
                            rx.badge(
                                "Sin recursos",
                                color_scheme="gray",
                                variant="soft",
                                size="2"
                            )
                        ),
                        width="100%",
                        align="center",
                        wrap="wrap"
                    ),
                    width="100%",
                    padding_bottom="1.5rem",
                    border_bottom="1px solid #e2e8f0"
                ),
                
                rx.box(
                    rx.vstack(
                        rx.vstack(
                            rx.text("Destino:", size="2", font_weight="500", color="#1e293b"),
                            rx.input(
                                placeholder="Ej: Departamento de Producción",
                                value=SolicitanteDashboardState.destino,
                                on_change=SolicitanteDashboardState.set_destino,
                                size="2",
                                width="100%"
                            ),
                            align="start",
                            spacing="1",
                            width="100%"
                        ),
                        
                        rx.box(
                            rx.button(
                                "➕ Agregar Recurso",
                                on_click=SolicitanteDashboardState.agregar_recurso_form,
                                variant="soft",
                                size="2",
                                width="100%"
                            ),
                            width="100%",
                            padding_y="1rem"
                        ),
                        
                        rx.cond(
                            SolicitanteDashboardState.tiene_recursos_en_formulario,
                            rx.vstack(
                                rx.heading("Recursos Solicitados", size="4", color="#1e293b"),
                                rx.foreach(
                                    SolicitanteDashboardState.recursos_form,
                                    lambda recurso, idx: recurso_form_row(recurso, idx)
                                ),
                                spacing="3",
                                width="100%"
                            ),
                            rx.center(
                                rx.vstack(
                                    rx.icon("package", size=32, color="#cbd5e1"),
                                    rx.text(
                                        "No hay recursos agregados",
                                        size="3",
                                        color="#64748b",
                                        text_align="center"
                                    ),
                                    rx.text(
                                        "Haz clic en 'Agregar Recurso' para comenzar",
                                        size="2",
                                        color="#94a3b8",
                                        text_align="center"
                                    ),
                                    spacing="2",
                                    align="center"
                                ),
                                width="100%",
                                padding="2rem"
                            )
                        ),
                        
                        rx.box(
                            rx.vstack(
                                rx.button(
                                    "🗑️ Limpiar Todo",
                                    on_click=SolicitanteDashboardState.limpiar_recursos_form,
                                    variant="soft",
                                    color_scheme="red",
                                    size="2",
                                    width="100%",
                                ),
                                rx.button(
                                    "📤 Enviar Solicitud",
                                    on_click=SolicitanteDashboardState.crear_solicitud_multiple,
                                    color_scheme="green",
                                    size="2",
                                    variant="solid",
                                    loading=SolicitanteDashboardState.loading,
                                    width="100%"
                                ),
                                spacing="2",
                                width="100%"
                            ),
                            width="100%",
                            padding_top="1.5rem",
                            border_top="1px solid #e2e8f0"
                        ),
                        
                        spacing="4",
                        width="100%"
                    ),
                    width="100%",
                    padding="1.5rem",
                    border_radius="md",
                    border="1px solid #e2e8f0",
                    background="white"
                ),
                
                spacing="4",
                width="100%"
            ),
            width="100%"
        )
    
    def mis_solicitudes_section():
        """Sección de mis solicitudes"""
        
        def grupo_solicitud_card(grupo):
            """Tarjeta para mostrar un grupo de solicitudes"""
            estado_raw = grupo.get("estado", "pendiente")  # Esto está bien porque es Python puro
            estado_str = str(estado_raw)
            
            estado_color = {
                "pendiente": "amber",
                "aprobada": "green",
                "rechazada": "red"
            }.get(estado_str, "gray")
            
            grupo_id = grupo["grupo_id"]  # <--- CAMBIO CLAVE: usar índice directo
            
            return rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                f"Solicitud #{grupo_id}",  # <--- ahora es el valor real
                                size="3",
                                font_weight="600",
                                color="#1e293b"
                            ),
                            rx.text(
                                f"Destino: {grupo['destino']}",  # <--- índice directo
                                size="2",
                                color="#64748b"
                            ),
                            align="start",
                            spacing="1"
                        ),
                        rx.spacer(),
                        rx.badge(
                            estado_str.upper(),
                            color_scheme=estado_color,
                            size="2"
                        ),
                        width="100%",
                        align="center"
                    ),
                    
                    rx.hstack(
                        rx.vstack(
                            rx.hstack(
                                rx.icon("calendar", size=14, color="#64748b"),
                                rx.text(
                                    f"Fecha: {grupo['fecha_formateada']}",  # <--- índice directo
                                    size="2",
                                    color="#64748b"
                                ),
                                spacing="2",
                                align="center"
                            ),
                            rx.hstack(
                                rx.icon("package", size=14, color="#64748b"),
                                rx.text(
                                    f"Recursos: {grupo['num_recursos']}",  # <--- índice directo
                                    size="2",
                                    color="#64748b"
                                ),
                                spacing="2",
                                align="center"
                            ),
                            spacing="1"
                        ),
                        rx.spacer(),
                        rx.button(
                            "Ver Detalles",
                            on_click=lambda: SolicitanteDashboardState.ver_detalle_grupo(grupo_id),  # <--- ahora pasa el string real
                            size="1",
                            variant="soft",
                            style={
                                "padding": "2px 8px",
                                "font_size": "11px",
                                "height": "28px",
                                "min_width": "70px",
                                "width": "auto",
                                "flex_shrink": "0",  # evitar que se estire
                            }
                        ),
                        width="100%",
                        align="center"
                    ),
                    
                    spacing="3",
                    align="start"
                ),
                width="100%",
                variant="surface"
            )
        
        return rx.box(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.heading("📋 Mis Solicitudes", size="5", color="#1e293b"),
                        rx.text(
                            "Historial de solicitudes enviadas",
                            size="2",
                            color="#64748b"
                        ),
                        align="start",
                        spacing="1"
                    ),
                    rx.spacer(),
                    rx.badge(
                        f"{SolicitanteDashboardState.computed_total_solicitudes} solicitudes",
                        color_scheme="blue",
                        variant="soft",
                        size="2"
                    ),
                    width="100%",
                    align="center"
                ),
                
                rx.cond(
                    SolicitanteDashboardState.loading,
                    rx.center(
                        rx.vstack(
                            rx.spinner(size="3", color="#0f766e"),
                            rx.text("Cargando solicitudes...", margin_top="1rem", color="#64748b"),
                            spacing="3",
                            align="center"
                        ),
                        height="200px",
                        width="100%"
                    ),
                    rx.cond(
                        SolicitanteDashboardState.mis_solicitudes.length() > 0,
                        rx.vstack(
                            rx.foreach(
                                SolicitanteDashboardState.mis_solicitudes,
                                lambda grupo: grupo_solicitud_card(grupo)
                            ),
                            spacing="3",
                            width="100%"
                        ),
                        rx.center(
                            rx.vstack(
                                rx.icon("file_text", size=32, color="#cbd5e1"),
                                rx.text(
                                    "No hay solicitudes registradas",
                                    size="3",
                                    color="#64748b",
                                    text_align="center"
                                ),
                                rx.text(
                                    "Comienza creando una nueva solicitud arriba",
                                    size="2",
                                    color="#94a3b8",
                                    text_align="center"
                                ),
                                spacing="2",
                                align="center"
                            ),
                            width="100%",
                            padding="3rem"
                        )
                    )
                ),
                
                spacing="4",
                width="100%"
            ),
            width="100%",
            padding="1.5rem",
            border_radius="md",
            border="1px solid #e2e8f0",
            background="white",
            margin_top="1.5rem"
        )
    
    def productos_almacen_section():
        """Sección de productos en almacén (solo lectura para solicitantes)"""
        
        def producto_row(item):
            return rx.table.row(
                # Número
                rx.table.cell(
                    rx.text(
                        item["Numero"],
                        color="#1e293b"
                    )
                ),
                # Código
                rx.table.cell(
                    rx.text(
                        item["Codigo"],
                        color="#1e293b"
                    )
                ),
                # Descripción
                rx.table.cell(
                    rx.text(
                        item["Descripcion del producto"],
                        color="#1e293b",
                        style={
                            "white_space": "nowrap",
                            "overflow": "hidden",
                            "text_overflow": "ellipsis"
                        }
                    )
                ),
                # Unidad de medida
                rx.table.cell(
                    rx.text(
                        item["UM"],
                        color="#1e293b"
                    )
                ),
                # Saldo
                rx.table.cell(
                    rx.text(
                        item["Saldo"],
                        color="#1e293b"
                    )
                ),
                # Precio formateado
                rx.table.cell(
                    rx.text(
                        f"${item['Precio']:.2f}",
                        color="#1e293b"
                    )
                ),
            )
        
        return rx.box(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.heading("📦 Productos en Almacén", size="5", color="#1e293b"),
                        rx.text(
                            "Visualización de productos disponibles (solo lectura)",
                            size="2",
                            color="#64748b"
                        ),
                        align="start",
                        spacing="1"
                    ),
                    rx.spacer(),
                    rx.badge(
                        f"{AlmacenState.filtered_data.length()} productos",
                        color_scheme="blue",
                        variant="soft",
                        size="2"
                    ),
                    width="100%",
                    align="center"
                ),
                
                # Controles de búsqueda - RESPONSIVE
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.input(
                                placeholder="Buscar productos...",
                                on_change=AlmacenState.filter_values,
                                size="2",
                                width="100%"
                            ),
                            rx.select(
                                ["Numero", "Codigo", "Descripcion del producto", "Precio"],
                                placeholder="Ordenar por...",
                                on_change=AlmacenState.sort_values,
                                size="2",
                                width="100%"
                            ),
                            spacing="3",
                            width="100%",
                            wrap="wrap"
                        ),
                        spacing="2"
                    ),
                    width="100%",
                    padding_bottom="1.5rem"
                ),
                
                # Tabla de productos
                rx.box(
                    rx.cond(
                        AlmacenState.filtered_data.length() == 0,
                        rx.center(
                            rx.vstack(
                                rx.icon("package", size=32, color="#cbd5e1"),
                                rx.text("No hay productos disponibles", size="3", color="#64748b"),
                                spacing="2",
                            ),
                            padding="3rem",
                        ),
                        rx.scroll_area(
                            rx.table.root(
                                rx.table.header(
                                    rx.table.row(
                                        rx.table.column_header_cell("Número", style={"color": "#1e293b"}),
                                        rx.table.column_header_cell("Código", style={"color": "#1e293b"}),
                                        rx.table.column_header_cell("Descripción", style={"color": "#1e293b"}),
                                        rx.table.column_header_cell("UM", style={"color": "#1e293b"}),
                                        rx.table.column_header_cell("Saldo", style={"color": "#1e293b"}),
                                        rx.table.column_header_cell("Precio", style={"color": "#1e293b"}),
                                    )
                                ),
                                rx.table.body(
                                    rx.foreach(
                                        AlmacenState.filtered_data,
                                        producto_row
                                    )
                                ),
                                variant="surface",
                                size="3"
                            ),
                            type="always",
                            scrollbars="horizontal",
                            style={
                                "width": "100%",
                                "max_width": "100%",
                                "overflow_x": "auto"
                            }
                        )
                    ),
                    width="100%"
                ),
                
                spacing="3",
                width="100%"
            ),
            width="100%",
            padding="1.5rem",
            border_radius="md",
            border="1px solid #e2e8f0",
            background="white",
            margin_top="1.5rem"
        )
    
    def main_content():
        return rx.vstack(
            # Encabezado principal
            rx.box(
                rx.hstack(
                    rx.vstack(
                        rx.heading(
                            "👤 Panel del Solicitante",
                            size="7",
                            color="#1e293b"
                        ),
                        rx.text(
                            "Gestión de solicitudes de recursos y visualización de productos",
                            size="4",
                            color="#64748b"
                        ),
                        align="start",
                        spacing="1"
                    ),
                    rx.spacer(),
                    rx.hstack(
                        rx.button(
                            "🔄 Actualizar",
                            on_click=[SolicitanteDashboardState.load_mis_solicitudes, AlmacenState.load_data],
                            loading=SolicitanteDashboardState.loading | AlmacenState.loading,  # <-- expresión directa
                            variant="soft",
                            size="2",
                            #width="auto"
                        ),
                        rx.button(
                                "🚪 Cerrar Sesión",
                                on_click=SolicitanteAuthState.sign_out,  # <-- BOTÓN DE LOGOUT
                                variant="soft",
                                color_scheme="red",
                                size="2",
                            ),
                        spacing="2",
                        wrap="wrap",
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
            
            # Contenido principal - RESPONSIVE
            rx.vstack(
                # Nueva Solicitud
                rx.box(
                    nueva_solicitud_form(),
                    width="100%"
                ),
                
                # Productos en Almacén
                rx.box(
                    productos_almacen_section(),
                    width="100%"
                ),
                
                # Mis Solicitudes
                rx.box(
                    mis_solicitudes_section(),
                    width="100%"
                ),
                
                spacing="4",
                width="100%"
            ),
            
            # Estadísticas
            rx.box(
                rx.hstack(
                    rx.card(
                        rx.vstack(
                            rx.text("Solicitudes Totales", size="2", color="#64748b"),
                            rx.text(
                                SolicitanteDashboardState.computed_total_solicitudes,
                                size="4",
                                font_weight="700",
                                color="#0f766e"
                            ),
                            spacing="1",
                            align="center"
                        ),
                        variant="surface",
                        width="100%"
                    ),
                    rx.card(
                        rx.vstack(
                            rx.text("Recursos Totales", size="2", color="#64748b"),
                            rx.text(
                                SolicitanteDashboardState.computed_total_recursos,
                                size="4",
                                font_weight="700",
                                color="#2563eb"
                            ),
                            spacing="1",
                            align="center"
                        ),
                        variant="surface",
                        width="100%"
                    ),
                    rx.card(
                        rx.vstack(
                            rx.text("Productos Disponibles", size="2", color="#64748b"),
                            rx.text(
                                AlmacenState.filtered_data.length(),
                                size="4",
                                font_weight="700",
                                color="#7c3aed"
                            ),
                            spacing="1",
                            align="center"
                        ),
                        variant="surface",
                        width="100%"
                    ),
                    spacing="3",
                    width="100%",
                    wrap="wrap"
                ),
                width="100%",
                padding_top="1.5rem",
                border_top="1px solid #e2e8f0",
                margin_top="1.5rem"
            ),
            
            spacing="4",
            padding=["1rem", "1.5rem", "2rem", "3rem"],
            width="100%",
            max_width="1400px",
            margin="0 auto",
            align="start"
        )
    
    return rx.box(
        navbar("Panel del Solicitante"),
        main_content(),
        width="100%",
        min_height="100vh",
        background="linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
    )