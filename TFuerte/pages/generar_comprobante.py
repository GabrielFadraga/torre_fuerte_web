# TFuerte/pages/generar_comprobante.py
import reflex as rx
from TFuerte.state.almacen_state import AlmacenState
from TFuerte.state.comprobante_state import ComprobanteState
from TFuerte.components.navbar import navbar
import TFuerte.styles.styles as styles
from TFuerte.routes import Route

@rx.page(
    route=Route.GENERAR_COMPROBANTE.value,
    title="Generar Comprobante",
    on_load=[AlmacenState.load_data, ComprobanteState.on_load_comprobante]
)
def generar_comprobante() -> rx.Component:
    """Página para generar comprobantes de salida"""
    
    def productos_table():
        """Tabla de productos disponibles para el comprobante"""
        
        def producto_row(item):
            return rx.table.row(
                rx.table.cell(
                    rx.button(
                        "➕",
                        on_click=lambda: ComprobanteState.agregar_producto_comprobante(item),
                        size="2",
                        variant="soft",
                        color_scheme="green"
                    )
                ),
                rx.table.cell(rx.text(item["Numero"], color="#1e293b")),
                rx.table.cell(rx.text(item["Codigo"], color="#1e293b")),
                rx.table.cell(
                    rx.text(
                        item["Descripcion del producto"],
                        color="#1e293b",
                        style={"white_space": "nowrap", "overflow": "hidden", "text_overflow": "ellipsis", "max_width": "200px"}
                    )
                ),
                rx.table.cell(rx.text(item["UM"], color="#1e293b")),
                rx.table.cell(rx.text(item["Saldo"], color="#1e293b")),
                rx.table.cell(rx.text(f"${item['Precio']:.2f}", color="#1e293b")),
            )
        
        return rx.box(
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
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Agregar", style={"color": "#1e293b", "padding": "8px"}),
                                rx.table.column_header_cell("Número", style={"color": "#1e293b", "padding": "8px"}),
                                rx.table.column_header_cell("Código", style={"color": "#1e293b", "padding": "8px"}),
                                rx.table.column_header_cell("Descripción", style={"color": "#1e293b", "padding": "8px"}),
                                rx.table.column_header_cell("UM", style={"color": "#1e293b", "padding": "8px"}),
                                rx.table.column_header_cell("Saldo", style={"color": "#1e293b", "padding": "8px"}),
                                rx.table.column_header_cell("Precio", style={"color": "#1e293b", "padding": "8px"}),
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
                    style={
                        "width": "100%",
                        "overflow_x": "auto",
                        "display": "block"
                    }
                )
            ),
            width="100%"
        )
    
    def productos_seleccionados_table():
        """Tabla de productos seleccionados para el comprobante"""
        
        def producto_seleccionado_row(item, index):
            cantidad_default = str(item.get("cantidad_salida", 1))
            saldo_max = str(item.get("saldo_disponible", 100))
            
            return rx.table.row(
                rx.table.cell(rx.text(index + 1, color="#1e293b")),
                rx.table.cell(rx.text(item.get("codigo", ""), color="#1e293b")),
                rx.table.cell(rx.text(item.get("descripcion", ""), color="#1e293b")),
                rx.table.cell(rx.text(item.get("um", ""), color="#1e293b")),
                rx.table.cell(
                    rx.input(
                        type="number",
                        default_value=cantidad_default,
                        on_change=lambda value: ComprobanteState.actualizar_cantidad_producto(index, value),
                        min="1",
                        max=saldo_max,
                        width="80px",
                        size="2"
                    )
                ),
                rx.table.cell(rx.text(f"${item.get('precio', 0):.2f}", color="#1e293b")),
                rx.table.cell(rx.text(f"${item.get('importe', 0):.2f}", color="#1e293b")),
                rx.table.cell(
                    rx.button(
                        "❌",
                        on_click=lambda: ComprobanteState.eliminar_producto_comprobante(index),
                        color_scheme="red",
                        size="2"
                    )
                ),
            )
        
        return rx.box(
            rx.cond(
                ComprobanteState.productos_seleccionados.length() > 0,
                rx.vstack(
                    rx.heading("Productos Seleccionados", size="4", color="#1e293b", width="100%"),
                    rx.box(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("#", style={"color": "#1e293b", "padding": "8px"}),
                                    rx.table.column_header_cell("Código", style={"color": "#1e293b", "padding": "8px"}),
                                    rx.table.column_header_cell("Descripción", style={"color": "#1e293b", "padding": "8px"}),
                                    rx.table.column_header_cell("UM", style={"color": "#1e293b", "padding": "8px"}),
                                    rx.table.column_header_cell("Cantidad", style={"color": "#1e293b", "padding": "8px"}),
                                    rx.table.column_header_cell("Precio", style={"color": "#1e293b", "padding": "8px"}),
                                    rx.table.column_header_cell("Importe", style={"color": "#1e293b", "padding": "8px"}),
                                    rx.table.column_header_cell("Acción", style={"color": "#1e293b", "padding": "8px"}),
                                )
                            ),
                            rx.table.body(
                                rx.foreach(
                                    ComprobanteState.productos_seleccionados,
                                    lambda item, idx: producto_seleccionado_row(item, idx)
                                )
                            ),
                            variant="surface",
                            size="2"
                        ),
                        style={
                            "width": "100%",
                            "overflow_x": "auto",
                            "display": "block"
                        }
                    ),
                    rx.hstack(
                        rx.text("Subtotal:", size="3", font_weight="bold", color="#1e293b"),
                        rx.spacer(),
                        rx.text(
                            rx.text("$", color="#059669"),
                            rx.text(ComprobanteState.subtotal.to_string(), color="#059669"),
                            size="3",
                            font_weight="bold",
                            color="#059669"
                        ),
                        width="100%",
                        justify="between"
                    ),
                    rx.hstack(
                        rx.text("Total:", size="4", font_weight="bold", color="#1e293b"),
                        rx.spacer(),
                        rx.text(
                            rx.text("$", color="#2563eb"),
                            rx.text(ComprobanteState.total.to_string(), color="#2563eb"),
                            size="4",
                            font_weight="bold",
                            color="#2563eb"
                        ),
                        width="100%",
                        justify="between"
                    ),
                    spacing="3",
                    width="100%"
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("shopping_cart", size=32, color="#cbd5e1"),
                        rx.text("No hay productos seleccionados", size="3", color="#64748b"),
                        rx.text("Selecciona productos de la tabla superior", size="2", color="#94a3b8"),
                        spacing="2",
                    ),
                    padding="2rem",
                )
            ),
            width="100%"
        )
    
    def comprobante_dialog():
        """Diálogo para confirmar y generar el comprobante"""
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Generar Comprobante", color="#1e293b"),
                rx.dialog.description(
                    "Complete los datos para generar el comprobante",
                    color="#64748b"
                ),
                
                rx.vstack(
                    # Formulario del comprobante
                    rx.vstack(
                        rx.hstack(
                            rx.vstack(
                                rx.text("Destino:", size="2", font_weight="500", color="#1e293b"),
                                rx.input(
                                    placeholder="Ej: Departamento de Producción",
                                    value=ComprobanteState.destino_comprobante,
                                    on_change=ComprobanteState.set_destino_comprobante,
                                    size="2",
                                    width="100%"
                                ),
                                align="start",
                                spacing="1",
                                width="100%"
                            ),
                            rx.vstack(
                                rx.text("Fecha de Salida:", size="2", font_weight="500", color="#1e293b"),
                                rx.input(
                                    type="date",
                                    value=ComprobanteState.fecha_salida_comprobante,
                                    on_change=ComprobanteState.set_fecha_salida_comprobante,
                                    size="2",
                                    width="100%"
                                ),
                                align="start",
                                spacing="1",
                                width="100%"
                            ),
                            spacing="3",
                            width="100%",
                            wrap="wrap"
                        ),
                        
                        rx.vstack(
                            rx.text("Recibido por:", size="2", font_weight="500", color="#1e293b"),
                            rx.input(
                                placeholder="Nombre del solicitante",
                                value=ComprobanteState.recibido_por,
                                on_change=ComprobanteState.set_recibido_por,
                                size="2",
                                width="100%"
                            ),
                            align="start",
                            spacing="1",
                            width="100%"
                        ),
                        
                        rx.vstack(
                            rx.text("Observaciones:", size="2", font_weight="500", color="#1e293b"),
                            rx.text_area(
                                placeholder="Observaciones adicionales...",
                                value=ComprobanteState.observaciones_comprobante,
                                on_change=ComprobanteState.set_observaciones_comprobante,
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
                    
                    # Totales
                    rx.box(
                        rx.hstack(
                            rx.text("Total a Facturar:", size="3", font_weight="bold", color="#1e293b"),
                            rx.spacer(),
                            rx.text(
                                rx.text("$", color="#2563eb"),
                                rx.text(ComprobanteState.total.to_string(), color="#2563eb"),
                                size="4",
                                font_weight="bold",
                                color="#2563eb"
                            ),
                            width="100%",
                            padding="1rem",
                            border_radius="md",
                            background="#f8fafc",
                            border="1px solid #e2e8f0"
                        ),
                        width="100%"
                    ),
                    
                    # Botones de acción
                    rx.vstack(
                        rx.button(
                            "📝 Generar Comprobante",
                            on_click=ComprobanteState.generar_comprobante,
                            color_scheme="green",
                            size="2",
                            variant="solid",
                            loading=ComprobanteState.loading_comprobante,
                            width="100%"
                        ),
                        rx.button(
                            "📄 Generar Word",
                            on_click=ComprobanteState.generar_comprobante_word,
                            color_scheme="blue",
                            size="2",
                            variant="solid",
                            width="100%"
                        ),
                        rx.dialog.close(
                            rx.button(
                                "Cancelar", 
                                variant="soft", 
                                size="2",
                                width="100%"
                            ),
                        ),
                        spacing="2",
                        width="100%"
                    ),
                    
                    spacing="4",
                    width="100%"
                ),
                
                max_width="600px",
                style={
                    "background": "white",
                    "border_radius": "12px",
                    "box_shadow": "0 20px 25px -5px rgba(0, 0, 0, 0.1)",
                    "max_height": "90vh",
                    "overflow_y": "auto",
                    "width": "90vw"
                }
            ),
            open=ComprobanteState.show_comprobante_dialog,
            on_open_change=ComprobanteState.set_show_comprobante_dialog,
        )
    
    def main_content():
        return rx.vstack(
            # Encabezado
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.heading("📄 Generar Comprobante", size="6", color="#1e293b"),
                            rx.text(
                                "Seleccione los productos para generar el comprobante de salida",
                                size="4",
                                color="#64748b"
                            ),
                            align="start",
                            spacing="1",
                            width="100%"
                        ),
                        rx.spacer(),
                        rx.button(
                            "🔄 Actualizar",
                            on_click=AlmacenState.load_data,
                            loading=AlmacenState.loading,
                            variant="soft",
                            size="2"
                        ),
                        width="100%",
                        align="center",
                        wrap="wrap",
                        spacing="3"
                    ),
                    width="100%"
                ),
                width="100%",
                padding_bottom="1.5rem",
                border_bottom="1px solid #e2e8f0"
            ),
            
            # Controles de búsqueda
            rx.box(
                rx.vstack(
                    rx.input(
                        placeholder="Buscar productos...",
                        on_change=AlmacenState.filter_values,
                        size="2",
                        width="100%"
                    ),
                    rx.hstack(
                        rx.select(
                            ["Numero", "Codigo", "Descripcion del producto", "Precio"],
                            placeholder="Ordenar por...",
                            on_change=AlmacenState.sort_values,
                            size="2",
                            width="100%"
                        ),
                        rx.box(
                            rx.badge(
                                f"{AlmacenState.filtered_data.length()} productos",
                                color_scheme="blue",
                                variant="soft",
                                size="2"
                            ),
                            display="flex",
                            justify_content="center",
                            align_items="center",
                            width="100%"
                        ),
                        spacing="3",
                        width="100%",
                        wrap="wrap"
                    ),
                    spacing="3",
                    width="100%"
                ),
                width="100%",
                padding_bottom="1.5rem"
            ),
            
            # Tabla de productos disponibles
            rx.box(
                rx.vstack(
                    rx.heading("📦 Productos Disponibles", size="5", color="#1e293b"),
                    rx.text(
                        "Seleccione los productos para incluir en el comprobante",
                        size="2",
                        color="#64748b",
                        margin_bottom="1rem"
                    ),
                    productos_table(),
                    spacing="3",
                ),
                width="100%",
                padding="1.5rem",
                border_radius="md",
                border="1px solid #e2e8f0",
                background="white"
            ),
            
            # Productos seleccionados
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.heading("🛒 Productos Seleccionados", size="5", color="#1e293b"),
                        rx.spacer(),
                        rx.button(
                            "📋 Generar Comprobante",
                            on_click=ComprobanteState.abrir_dialogo_comprobante,
                            variant="solid",
                            color_scheme="green",
                            size="2",
                            is_disabled=ComprobanteState.productos_seleccionados.length() == 0
                        ),
                        width="100%",
                        align="center",
                        wrap="wrap"
                    ),
                    productos_seleccionados_table(),
                    spacing="3",
                ),
                width="100%",
                padding="1.5rem",
                border_radius="md",
                border="1px solid #e2e8f0",
                background="white",
                margin_top="1.5rem"
            ),
            
            # Diálogo de comprobante
            comprobante_dialog(),
            padding_y=styles.Spacer.DEFAULT,
            spacing="4",
            width="100%",
            max_width="1400px",  # Cambia de 100% a un valor fijo
            padding_x=["1rem", "2rem", "3rem", "4rem"],  # Padding responsive
            align="start",
            margin="0 auto"  # Centra el contenido
        )
    
    return rx.box(
        navbar("Generar Comprobante"),
        main_content(),
        width="100%",
        min_height="100vh",
        background="linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
    )