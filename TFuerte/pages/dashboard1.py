# TFuerte/pages/dashboard1.py - VERSIÓN CORREGIDA
import reflex as rx
from TFuerte.state.auth_state import AuthState
from TFuerte.state.almacen_state import AlmacenState
from TFuerte.components.navbar import navbar
from TFuerte.routes import Route

@rx.page(
    route=Route.ADMIN1.value,
    title="Dashboard - Almacén",
    on_load=[AuthState.on_load, AlmacenState.load_data]
)
def admin_dashboard() -> rx.Component:
    """Dashboard protegido"""
    
    # Lista de tipos de producto para la leyenda
    tipos_producto = [
        ("1", "ELECTRICIDAD"),
        ("2", "PLOMERIA BOMBAS"),
        ("3", "INSUMOS DE CORTE Y DESBASTE"),
        ("4", "TORNILLERIA"),
        ("5", "SOLDADURA"),
        ("6", "RODAMIENTOS"),
        ("7", "SERVICIOS"),
        ("8", "MATERIAL DE PINTURA"),
        ("9", "MATERIAL DE OFICINA"),
        ("10", "LUBRICANTES Y LIMPIADORES"),
        ("11", "CERRAGERIA"),
        ("12", "CLIMA"),
        ("13", "LIMPIEZA"),
        ("14", "COMPUTACION"),
        ("15", "ALIMENTACION"),
        ("16", "PIEZAS AUTOS"),
        ("17", "MAQUINADO Y HERRAMIENTAS"),
        ("18", "MEDIOS DE PROTECCIÓN")
    ]
    
    def almacen_table() -> rx.Component:
        table_style = {
            "width": "100%",
            "min_width": "1400px",
            "table_layout": "fixed",
            "border_collapse": "separate",
            "border_spacing": "0",
        }
        
        header_style = {
            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "color": "white",
            "font_weight": "600",
            "padding": "18px 6px",
            "text_align": "center",
            "border": "none",
            "font_size": "14px",
            "text_transform": "uppercase",
            "letter_spacing": "0.5px",
            "position": "sticky",
            "top": "0",
            "z_index": "10",
        }
        
        cell_style = {
            "padding": "12px 4px",
            "border_bottom": "1px solid #f1f5f9",
            "vertical_align": "middle",
            "font_size": "14px",
            "color": "#475569",
            "transition": "all 0.2s ease",
            "text_align": "center",
            "overflow": "hidden",
            "box_sizing": "border-box",
        }
        
        return rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Seleccionar", style={**header_style, "width": "100px"}),
                        rx.table.column_header_cell("Número", style={**header_style, "width": "80px"}),
                        rx.table.column_header_cell("Código", style={**header_style, "width": "120px"}),
                        rx.table.column_header_cell("Descripción", style={**header_style, "width": "250px"}),
                        rx.table.column_header_cell("Tipo", style={**header_style, "width": "150px"}),
                        rx.table.column_header_cell("UM", style={**header_style, "width": "100px"}),
                        rx.table.column_header_cell("Fecha Entrada", style={**header_style, "width": "120px"}),
                        rx.table.column_header_cell("Cant. E", style={**header_style, "width": "100px"}),
                        rx.table.column_header_cell("Fecha Salida", style={**header_style, "width": "120px"}),
                        rx.table.column_header_cell("Cant. S", style={**header_style, "width": "100px"}),
                        rx.table.column_header_cell("Saldo", style={**header_style, "width": "100px"}),
                        rx.table.column_header_cell("Precio", style={**header_style, "width": "120px"}),
                        rx.table.column_header_cell("Importe", style={**header_style, "width": "120px"}),
                    )
                ),
                style=table_style,
            ),
            
            rx.scroll_area(
                rx.table.root(
                    rx.table.body(
                        rx.foreach(
                            AlmacenState.filtered_data,
                            lambda item: rx.table.row(
                                # Checkbox usando Numero como identificador
                                rx.table.cell(
                                    rx.box(
                                        rx.checkbox(
                                            checked=AlmacenState.selected_items.contains(item.get("Numero", 0)),
                                            on_change=lambda checked, item_numero=item.get("Numero", 0): AlmacenState.toggle_item_selection(item_numero),
                                            radius="full",
                                        ),
                                        display="flex",
                                        justify_content="center",
                                        align_items="center",
                                        width="100%",
                                    ),
                                    style={**cell_style, "width": "100px"}
                                ),
                                # NÚMERO
                                rx.table.cell(
                                    rx.box(
                                        rx.badge(
                                            item.get("Numero", "N/A"),
                                            variant="solid",
                                            color_scheme="blue",
                                            style={
                                                "background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
                                                "color": "white",
                                                "padding": "6px 8px",
                                                "border_radius": "20px",
                                                "font_weight": "600",
                                                "box_shadow": "0 2px 4px rgba(59, 130, 246, 0.3)",
                                                "max_width": "60px",
                                            }
                                        ),
                                        display="flex",
                                        justify_content="center",
                                        align_items="center",
                                        width="100%",
                                    ),
                                    style={**cell_style, "width": "80px"}
                                ),
                                # CÓDIGO
                                rx.table.cell(
                                    rx.box(
                                        rx.text(item.get("Codigo", ""), 
                                                style={
                                                    "font_weight": "600", 
                                                    "color": "#1e293b",
                                                    "font_family": "monospace",
                                                    "letter_spacing": "0.5px",
                                                    "text_align": "center",
                                                    "width": "100%",
                                                    "padding": "0 4px",
                                                }),
                                        display="flex",
                                        justify_content="center",
                                        align_items="center",
                                        width="100%",
                                    ),
                                    style={**cell_style, "width": "120px"}
                                ),
                                # DESCRIPCIÓN
                                rx.table.cell(
                                    rx.box(
                                        rx.text(
                                            item.get("Descripcion del producto", ""), 
                                            style={
                                                "color": "#334155",
                                                "white_space": "nowrap",
                                                "overflow": "hidden",
                                                "text_overflow": "ellipsis",
                                                "text_align": "center",
                                                "width": "100%",
                                                "padding": "0 4px",
                                            }
                                        ),
                                        display="flex",
                                        justify_content="center",
                                        align_items="center",
                                        width="100%",
                                    ),
                                    style={**cell_style, "width": "250px"}
                                ),
                                # TIPO
                                rx.table.cell(
                                    rx.box(
                                        rx.badge(
                                            item.get("Tipo de producto", ""),
                                            variant="surface",
                                            color_scheme="gray",
                                            style={
                                                "font_weight": "500",
                                                "white_space": "nowrap",
                                                "overflow": "hidden",
                                                "text_overflow": "ellipsis",
                                                "max_width": "120px",
                                            }
                                        ),
                                        display="flex",
                                        justify_content="center",
                                        align_items="center",
                                        width="100%",
                                    ),
                                    style={**cell_style, "width": "150px"}
                                ),
                                # UM
                                rx.table.cell(
                                    rx.box(
                                        rx.badge(
                                            item.get("UM", ""), 
                                            variant="outline",
                                            color_scheme="gray",
                                            style={
                                                "font_family": "monospace",
                                                "font_weight": "600",
                                                "color": "#64748b",
                                                "max_width": "70px",
                                            }
                                        ),
                                        display="flex",
                                        justify_content="center",
                                        align_items="center",
                                        width="100%",
                                    ),
                                    style={**cell_style, "width": "100px"}
                                ),
                                # FECHA ENTRADA
                                rx.table.cell(
                                    rx.box(
                                        rx.box(
                                            rx.text(item.get("Fecha de entrada", ""), 
                                                    style={"color": "#475569", "font_weight": "500", "text_align": "center"}),
                                            style={
                                                "background": "linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%)",
                                                "padding": "6px 8px",
                                                "border_radius": "8px",
                                                "border": "1px solid #dbeafe",
                                                "max_width": "90px",
                                            }
                                        ),
                                        display="flex",
                                        justify_content="center",
                                        align_items="center",
                                        width="100%",
                                    ),
                                    style={**cell_style, "width": "120px"}
                                ),
                                # CANTIDAD E
                                rx.table.cell(
                                    rx.box(
                                        rx.badge(
                                            item.get("Cantidad E", 0), 
                                            variant="solid", 
                                            color_scheme="green",
                                            style={
                                                "background": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
                                                "font_weight": "600",
                                                "padding": "6px 8px",
                                                "max_width": "70px",
                                            }
                                        ),
                                        display="flex",
                                        justify_content="center",
                                        align_items="center",
                                        width="100%",
                                    ),
                                    style={**cell_style, "width": "100px"}
                                ),
                                # FECHA SALIDA
                                rx.table.cell(
                                    rx.box(
                                        rx.box(
                                            rx.text(
                                                rx.cond(
                                                    item.get("Fecha de salida"),
                                                    item.get("Fecha de salida", ""),
                                                    "-"
                                                ),
                                                style={"color": "#475569", "font_weight": "500", "text_align": "center"}
                                            ),
                                            style={
                                                "background": "linear-gradient(135deg, #fef3c7 0%, #fef9c3 100%)",
                                                "padding": "6px 8px",
                                                "border_radius": "8px",
                                                "border": "1px solid #fde68a",
                                                "max_width": "90px",
                                            }
                                        ),
                                        display="flex",
                                        justify_content="center",
                                        align_items="center",
                                        width="100%",
                                    ),
                                    style={**cell_style, "width": "120px"}
                                ),
                                # CANTIDAD S
                                rx.table.cell(
                                    rx.box(
                                        rx.cond(
                                            item.get("Cantidad S", 0) != 0,
                                            rx.badge(
                                                f"{item.get('Cantidad S', 0)}", 
                                                variant="solid", 
                                                color_scheme="red",
                                                style={
                                                    "background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
                                                    "font_weight": "600",
                                                    "padding": "6px 8px",
                                                    "max_width": "70px",
                                                }
                                            ),
                                            rx.text("-", style={"color": "#cbd5e1", "font_weight": "500", "text_align": "center", "width": "100%"})
                                        ),
                                        display="flex",
                                        justify_content="center",
                                        align_items="center",
                                        width="100%",
                                    ),
                                    style={**cell_style, "width": "100px"}
                                ),
                                # SALDO
                                rx.table.cell(
                                    rx.box(
                                        rx.badge(
                                            item.get("Saldo", 0), 
                                            variant="outline", 
                                            color_scheme="blue",
                                            style={
                                                "font_weight": "700",
                                                "font_size": "14px",
                                                "padding": "6px 8px",
                                                "border_width": "2px",
                                                "border_color": "#3b82f6",
                                                "max_width": "70px",
                                            }
                                        ),
                                        display="flex",
                                        justify_content="center",
                                        align_items="center",
                                        width="100%",
                                    ),
                                    style={**cell_style, "width": "100px"}
                                ),
                                # PRECIO
                                rx.table.cell(
                                    rx.box(
                                        rx.box(
                                            rx.text(
                                                f"${item.get('Precio', 0):.2f}", 
                                                style={
                                                    "font_weight": "700", 
                                                    "color": "#059669",
                                                    "font_size": "14px",
                                                    "text_align": "center",
                                                }
                                            ),
                                            style={
                                                "background": "linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)",
                                                "padding": "6px 8px",
                                                "border_radius": "8px",
                                                "border": "1px solid #a7f3d0",
                                                "max_width": "90px",
                                            }
                                        ),
                                        display="flex",
                                        justify_content="center",
                                        align_items="center",
                                        width="100%",
                                    ),
                                    style={**cell_style, "width": "120px"}
                                ),
                                # IMPORTE
                                rx.table.cell(
                                    rx.box(
                                        rx.box(
                                            rx.text(
                                                f"${item.get('Importe', 0):.2f}", 
                                                style={
                                                    "font_weight": "700", 
                                                    "color": "#2563eb",
                                                    "font_size": "14px",
                                                    "text_align": "center",
                                                }
                                            ),
                                            style={
                                                "background": "linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%)",
                                                "padding": "6px 8px",
                                                "border_radius": "8px",
                                                "border": "1px solid #93c5fd",
                                                "max_width": "90px",
                                            }
                                        ),
                                        display="flex",
                                        justify_content="center",
                                        align_items="center",
                                        width="100%",
                                    ),
                                    style={**cell_style, "width": "120px"}
                                ),
                                _hover={
                                    "background_color": "#f8fafc",
                                    "transform": "translateY(-1px)",
                                    "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                                },
                                style={
                                    "transition": "all 0.2s ease",
                                    "cursor": "pointer",
                                }
                            )
                        )
                    ),
                    style=table_style,
                ),
                type="always",
                scrollbars="horizontal",
                style={
                    "width": "100%",
                    "height": "600px",
                    "overflow_y": "auto",
                    "border": "1px solid #e2e8f0",
                    "border_radius": "12px",
                    "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                }
            ),
            width="100%",
        )
    
    def add_product_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.button("➕ Agregar Producto", variant="solid", color_scheme="green", size="2")),
            rx.dialog.content(
                rx.dialog.title("Agregar Nuevo Producto"),
                rx.dialog.description("Completa el formulario para agregar un nuevo producto al almacén."),
                rx.form(
                    rx.vstack(
                        rx.input(placeholder="Código *", name="codigo", required=True, size="3", margin_bottom="1rem"),
                        rx.input(placeholder="Descripción *", name="descripcion", required=True, size="3", margin_bottom="1rem"),
                        rx.input(placeholder="Tipo *", name="tipo", required=True, size="3", margin_bottom="1rem"),
                        rx.input(placeholder="Unidad de Medida *", name="um", required=True, size="3", margin_bottom="1rem"),
                        rx.hstack(
                            rx.vstack(
                                rx.text("Fecha Entrada:", size="2"),
                                rx.input(type="date", name="fecha_entrada", required=True, size="3"),
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.text("Cantidad Entrada:", size="2"),
                                rx.input(type="number", name="cantidad_e", required=True, size="3", min="0", step="1"),
                                spacing="1",
                            ),
                            spacing="3", width="100%",
                        ),
                        rx.input(placeholder="Precio *", type="number", name="precio", required=True, size="3", 
                                margin_bottom="2rem", min="0", step="0.01"),
                        rx.hstack(
                            rx.dialog.close(rx.button("Cancelar", variant="soft", color_scheme="gray", size="2")),
                            rx.button("Agregar Producto", type="submit", variant="solid", color_scheme="green", size="2"),
                            spacing="3", justify="end", width="100%",
                        ),
                        spacing="1",
                    ),
                    on_submit=AlmacenState.add_item_to_db,
                    reset_on_submit=True,
                ),
                max_width="500px",
            ),
        )
    
    def entrada_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(
                rx.button(
                    "📥 Dar Entrada",
                    on_click=AlmacenState.open_entrada_dialog,
                    variant="solid",
                    color_scheme="green",
                    size="2",
                    is_disabled=AlmacenState.selected_items.length() != 1,
                ),
            ),
            rx.dialog.content(
                rx.dialog.title("Dar Entrada al Producto"),
                rx.dialog.description("Actualiza los datos de entrada del producto seleccionado."),
                rx.form(
                    rx.vstack(
                        # Campos principales (existentes)
                        rx.hstack(
                            rx.vstack(
                                rx.text("Fecha Entrada:", size="2"),
                                rx.input(type="date", name="fecha_entrada", 
                                        default_value=AlmacenState.edit_form_data.get("fecha_entrada", ""),
                                        required=True, size="3"),
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.text("Cantidad Entrada:", size="2"),
                                rx.input(type="number", name="cantidad_e", 
                                        default_value=AlmacenState.edit_form_data.get("cantidad_e", "0"),
                                        required=True, size="3", min="0", step="1"),
                                spacing="1",
                            ),
                            spacing="3", width="100%",
                        ),
                        rx.input(placeholder="Precio *", type="number", name="precio", 
                                default_value=AlmacenState.edit_form_data.get("precio", "0"),
                                required=True, size="3", min="0", step="0.01"),
                        
                        # Botones
                        rx.vstack(
                            rx.dialog.close(
                                rx.button("Cancelar", on_click=AlmacenState.close_entrada_dialog, 
                                         variant="soft", color_scheme="gray", size="2")
                            ),
                            rx.button("Actualizar Entrada", type="submit", variant="solid", color_scheme="green", size="2"),
                            spacing="3", justify="end", width="100%",
                        ),
                        spacing="3",
                    ),
                    on_submit=AlmacenState.update_entrada_in_db,
                    reset_on_submit=False,
                ),
                max_width="500px",
            ),
            open=AlmacenState.show_entrada_dialog,
            on_open_change=AlmacenState.set_show_entrada_dialog,
        )
    
    def salida_dialog():
        """Diálogo para dar salida - solo se habilita si hay solicitudes aprobadas"""
        # Usamos una variable computada en el estado para determinar si está habilitado
        return rx.dialog.root(
            rx.dialog.trigger(
                rx.button(
                    "📤 Dar Salida",
                    on_click=AlmacenState.open_salida_dialog,
                    variant="solid",
                    color_scheme="red",
                    size="2",
                    # Usamos rx.cond para determinar si está deshabilitado
                    # Solo habilitado si hay exactamente un producto seleccionado Y tiene solicitudes aprobadas
                    is_disabled=rx.cond(
                        AlmacenState.selected_items.length() == 1,
                        # Si hay un producto seleccionado, verificar si tiene solicitudes aprobadas
                        rx.cond(
                            AlmacenState.producto_tiene_solicitudes_aprobadas,
                            False,  # Habilitado si tiene solicitudes aprobadas
                            True    # Deshabilitado si no tiene
                        ),
                        True  # Deshabilitado si no hay producto seleccionado
                    ),
                    style={
                        "background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
                        "width": ["100%", "auto", "auto", "auto"],
                    }
                ),
            ),
            rx.dialog.content(
                rx.dialog.title("Dar Salida para Solicitud Aprobada"),
                rx.dialog.description(
                    "Completa los detalles para dar salida a un producto con solicitud aprobada."
                ),
                rx.form(
                    rx.vstack(
                        # Campos del formulario de salida
                        rx.hstack(
                            rx.vstack(
                                rx.text("Fecha Salida:", size="2"),
                                rx.input(type="date", name="fecha_salida", required=True, size="3"),
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.text("Cantidad Salida:", size="2"),
                                rx.input(type="number", name="cantidad_s", required=True, size="3", min="1", step="1"),
                                spacing="1",
                            ),
                            spacing="3", width="100%",
                        ),
                        rx.input(placeholder="Quién recibe *", name="recibe", required=True, size="3"),
                        rx.input(placeholder="Destino *", name="destino", required=True, size="3"),
                        rx.input(placeholder="Cliente/Proyecto *", name="cliente", required=True, size="3"),
                        
                        # Botones
                        rx.vstack(
                            rx.dialog.close(
                                rx.button("Cancelar", variant="soft", color_scheme="gray", size="2")
                            ),
                            rx.button(
                                "Confirmar Salida", 
                                type="submit", 
                                variant="solid", 
                                color_scheme="red", 
                                size="2",
                                style={
                                    "background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)"
                                }
                            ),
                            spacing="3", justify="end", width="100%",
                        ),
                        spacing="3",
                    ),
                    on_submit=AlmacenState.dar_salida_para_solicitud_aprobada,
                    reset_on_submit=False,
                ),
                max_width="500px",
            ),
            open=AlmacenState.show_salida_dialog,
            on_open_change=AlmacenState.set_show_salida_dialog,
        )
    
    def delete_confirm_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(
                rx.button(
                    "🗑️ Eliminar Productos",
                    on_click=AlmacenState.open_delete_dialog,
                    variant="solid",
                    color_scheme="red",
                    size="2",
                    is_disabled=AlmacenState.selected_items.length() == 0,
                ),
            ),
            rx.dialog.content(
                rx.dialog.title("Confirmar Eliminación"),
                rx.dialog.description(
                    rx.cond(
                        AlmacenState.selected_items.length() == 1,
                        "¿Estás seguro de que deseas eliminar el producto seleccionado? Esta acción no se puede deshacer.",
                        f"¿Estás seguro de que deseas eliminar los {AlmacenState.selected_items.length()} productos seleccionados? Esta acción no se puede deshacer.",
                    )
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button("Cancelar", on_click=AlmacenState.close_delete_dialog, variant="soft", color_scheme="gray", size="2"),
                    ),
                    rx.button("Eliminar", on_click=AlmacenState.delete_selected_items, variant="solid", color_scheme="red", size="2"),
                    spacing="3", justify="end",
                ),
                max_width="500px",
            ),
            open=AlmacenState.show_delete_dialog,
            on_open_change=AlmacenState.set_show_delete_dialog,
        )
    
    def leyenda_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(
                rx.button(
                    "📋 Leyenda de Tipos",
                    variant="solid",
                    color_scheme="cyan",
                    size="2",
                    style={
                        "background": "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)",
                        "flex": "1",
                        "min_width": ["100%", "140px", "140px", "140px"],
                    }
                ),
            ),
            rx.dialog.content(
                rx.dialog.title("Leyenda de Tipos de Producto"),
                rx.dialog.description("Número que identifica cada tipo de producto"),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Número", style={"font_weight": "bold", "width": "80px", "text_align": "center"}),
                            rx.table.column_header_cell("Descripción", style={"font_weight": "bold", "text_align": "left"}),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            tipos_producto,
                            lambda tipo: rx.table.row(
                                rx.table.cell(
                                    rx.badge(
                                        tipo[0],
                                        variant="solid",
                                        color_scheme="blue",
                                        style={
                                            "font_weight": "bold",
                                            "font_size": "12px",
                                            "padding": "4px 8px",
                                        }
                                    ),
                                    style={"text_align": "center", "vertical_align": "middle"}
                                ),
                                rx.table.cell(
                                    rx.text(
                                        tipo[1],
                                        style={
                                            "font_size": "12px",
                                            "color": "#d7dfec"
                                        }
                                    ),
                                    style={"text_align": "left", "vertical_align": "middle"}
                                ),
                            )
                        )
                    ),
                    style={
                        "width": "100%",
                        "border_collapse": "separate",
                        "border_spacing": "0 8px",
                    }
                ),
                rx.dialog.close(
                    rx.button("Cerrar", variant="soft", color_scheme="gray", size="2", margin_top="1rem"),
                ),
                max_width="500px",
            ),
        )
    
    def dashboard_content():
        return rx.box(
            navbar("Admin"),
            rx.vstack(
                rx.heading("📦 Gestión de Almacén", 
                          size="8", 
                          margin_bottom="0.5rem", 
                          color="#1e293b",
                          width="100%", 
                          text_align="center",
                          style={
                              "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                              "background_clip": "text",
                              "webkit_background_clip": "text",
                              "color": "transparent",
                              "font_weight": "800",
                              "letter_spacing": "-0.5px",
                          }),
                rx.text("Tabla completa de productos en almacén",
                       size="4", 
                       color="#64748b", 
                       margin_bottom="2rem", 
                       width="100%", 
                       text_align="center",
                       style={"font_weight": "500"}),
                
                # Estadísticas responsivas
                rx.box(
                    rx.hstack(
                        rx.box(
                            rx.vstack(
                                rx.text("Total Productos", size="2", color="#64748b", font_weight="500"),
                                rx.badge(
                                    f"{AlmacenState.total_productos}", 
                                    variant="solid", 
                                    color_scheme="green",
                                    size="3",
                                    style={
                                        "background": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
                                        "font_weight": "700",
                                        "padding": "12px 24px",
                                        "border_radius": "12px",
                                        "min_width": "120px",
                                        "justify_content": "center",
                                    }
                                ),
                                align="center",
                                spacing="1",
                            ),
                            flex="1",
                            min_width=["100%", "auto", "auto", "auto"],
                            margin_bottom=["1rem", "0", "0", "0"],
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("Valor Total", size="2", color="#64748b", font_weight="500"),
                                rx.badge(
                                    f"${AlmacenState.valor_total:,.2f}", 
                                    variant="outline",
                                    size="3",
                                    style={
                                        "font_weight": "700",
                                        "padding": "12px 24px",
                                        "border_radius": "12px",
                                        "border_width": "2px",
                                        "border_color": "#3b82f6",
                                        "color": "#1d4ed8",
                                        "min_width": "150px",
                                        "justify_content": "center",
                                        "background": "white",
                                    }
                                ),
                                align="center",
                                spacing="1",
                            ),
                            flex="1",
                            min_width=["100%", "auto", "auto", "auto"],
                            margin_bottom=["1rem", "0", "0", "0"],
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("Seleccionados", size="2", color="#64748b", font_weight="500"),
                                rx.badge(
                                    rx.text(f"{AlmacenState.selected_items.length()}", color="#E8E8E8"), 
                                    variant="soft", 
                                    color_scheme="blue",
                                    size="3",
                                    style={
                                        "background": "linear-gradient(135deg, #93c5fd 0%, #60a5fa 100%)",
                                        "font_weight": "700",
                                        "padding": "12px 24px",
                                        "border_radius": "12px",
                                        "min_width": "120px",
                                        "justify_content": "center",
                                    }
                                ),
                                align="center",
                                spacing="1",
                            ),
                            flex="1",
                            min_width=["100%", "auto", "auto", "auto"],
                        ),
                        spacing="4",
                        wrap="wrap",
                        justify="center",
                        width="100%",
                        margin_bottom="2rem",
                    ),
                    width="100%",
                    padding="1rem",
                    border_radius="12px",
                    background="linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
                    border="1px solid #e2e8f0",
                ),
                
                # Botones principales responsivos
                rx.box(
                    rx.vstack(
                        # Filtros y búsqueda
                        rx.hstack(
                            rx.input(
                                placeholder="Buscar por descripción...",
                                on_change=AlmacenState.filter_values,
                                width=["100%", "300px", "300px", "300px"],
                                size="3",
                                style={
                                    "background": "black",
                                    "border": "1px solid #e2e8f0",
                                    "border_radius": "8px",
                                }
                            ),
                            # MODIFICADO: Agregada la opción "Descripcion del producto"
                            rx.select(
                                ["Numero", "Codigo", "Descripcion del producto", "Tipo de producto", "UM", "Fecha de entrada", "Precio"],
                                placeholder="Ordenar por...",
                                on_change=AlmacenState.sort_values,
                                width=["100%", "200px", "200px", "200px"],
                                size="3",
                                style={
                                    "background": "white",
                                    "border": "1px solid #e2e8f0",
                                    "border_radius": "8px",
                                }
                            ),
                            spacing="2",
                            width="100%",
                            wrap="wrap",
                            justify="center",
                            margin_bottom="1rem",
                        ),
                        
                        # Primera fila de botones generales
                        rx.hstack(
                            rx.button(
                                "🔄 Actualizar", 
                                on_click=AlmacenState.load_data, 
                                loading=AlmacenState.loading,
                                variant="solid", 
                                color_scheme="cyan", 
                                size="2",
                                style={
                                    "background": "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)",
                                    "flex": "1",
                                    "min_width": ["100%", "120px", "120px", "120px"],
                                }
                            ),
                            rx.button(
                                "📥 CSV", 
                                on_click=AlmacenState.download_csv_data, 
                                variant="solid", 
                                color_scheme="cyan", 
                                size="2",
                                style={
                                    "background": "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)",
                                    "flex": "1",
                                    "min_width": ["100%", "120px", "120px", "120px"],
                                }
                            ),
                            rx.button(
                                "📥 JSON", 
                                on_click=AlmacenState.download_json_data, 
                                variant="solid", 
                                color_scheme="cyan", 
                                size="2",
                                style={
                                    "background": "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)",
                                    "flex": "1",
                                    "min_width": ["100%", "120px", "120px", "120px"],
                                }
                            ),
                            # NUEVO: Botón para leyenda de tipos
                            leyenda_dialog(),
                            spacing="2",
                            width="100%",
                            wrap="wrap",
                            justify="center",
                        ),
                        
                        # Segunda fila: acciones con productos seleccionados
                        rx.cond(
                            AlmacenState.selected_items.length() > 0,
                            rx.vstack(
                                rx.text(
                                    f"{AlmacenState.selected_items.length()} producto(s) seleccionado(s)", 
                                    size="3", 
                                    color="#475569",
                                    font_weight="600",
                                    margin_bottom="1rem",
                                ),
                                rx.hstack(
                                    entrada_dialog(),
                                    salida_dialog(),
                                    rx.button(
                                        "🗑️ Limpiar", 
                                        on_click=AlmacenState.clear_selection,
                                        variant="solid", 
                                        color_scheme="amber", 
                                        size="2",
                                        style={
                                            "background": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
                                            "flex": "1",
                                            "min_width": ["100%", "120px", "120px", "120px"],
                                        }
                                    ),
                                    delete_confirm_dialog(),
                                    spacing="2",
                                    width="100%",
                                    wrap="wrap",
                                    justify="center",
                                ),
                                spacing="2",
                                width="100%",
                                padding="1rem",
                                border_radius="12px",
                                background="linear-gradient(135deg, #fef3c7 0%, #fef9c3 100%)",
                                border="1px solid #fde68a",
                            ),
                        ),
                        
                        # Tercera fila: agregar producto y cerrar sesión
                        rx.vstack(
                            add_product_dialog(),
                            rx.button(
                                "🚪 Cerrar Sesión", 
                                on_click=AuthState.sign_out, 
                                variant="solid", 
                                color_scheme="red", 
                                size="2",
                                style={
                                    "background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
                                    "flex": "1",
                                    "min_width": ["100%", "140px", "140px", "140px"],
                                }
                            ),
                            rx.link(
                            rx.button(
                                "📃 Generar comprobante",
                                variant="solid",  
                                size="2",
                                style={
                                    #"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
                                    "flex": "1",
                                    "min_width": ["100%", "140px", "140px", "140px"],
                                }
                            ),
                            href=Route.GENERAR_COMPROBANTE.value,
                            width="100%",
                            color_scheme="indigo",
                        ),
                            spacing="2",
                            width="100%",
                            wrap="wrap",
                            justify="center",
                        ),
                        
                        spacing="3",
                        align="stretch",
                        width="100%",
                    ),
                    width="100%", 
                    margin_bottom="2rem",
                ),
                
                # Tabla de datos
                rx.cond(
                    AlmacenState.loading,
                    rx.center(
                        rx.vstack(
                            rx.spinner(size="3", color="#3b82f6"),
                            rx.text("Cargando datos...", 
                                   margin_top="1rem", 
                                   color="#475569",
                                   font_weight="500"), 
                            spacing="2"),
                        height="200px", 
                        width="100%",
                    ),
                    rx.cond(
                        AlmacenState.almacen_data.length() > 0,
                        rx.vstack(
                            rx.cond(
                                AlmacenState.filtered_data.length() > 0,
                                rx.vstack(
                                    rx.box(
                                        rx.box(almacen_table(), width="100%", overflow="hidden"),
                                        width="100%",
                                        border_radius="12px",
                                        overflow="hidden",
                                        box_shadow="0 10px 15px -3px rgba(0, 0, 0, 0.1)",
                                    ),
                                    # Información de filtrado
                                    rx.cond(
                                        AlmacenState.search_value != "",
                                        rx.box(
                                            rx.hstack(
                                                rx.icon("search", size=20, color="#3b82f6"),
                                                rx.text(
                                                    f"Mostrando {AlmacenState.filtered_data.length()} de {AlmacenState.almacen_data.length()} productos",
                                                    size="2",
                                                    color="#475569",
                                                    font_weight="500"
                                                ),
                                                spacing="2",
                                                align="center",
                                            ),
                                            width="100%",
                                            padding="0.75rem",
                                            border_radius="8px",
                                            background="linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)",
                                            border="1px solid #bae6fd",
                                            margin_top="1rem",
                                        ),
                                    ),
                                    width="100%",
                                ),
                                rx.center(
                                    rx.vstack(
                                        rx.icon("search", size=48, color="#cbd5e1"),
                                        rx.text("No se encontraron productos", 
                                               size="4", 
                                               color="#64748b",
                                               font_weight="600"),
                                        rx.text(
                                            f"La búsqueda '{AlmacenState.search_value}' no devolvió resultados",
                                            size="2",
                                            color="#94a3b8",
                                            margin_top="0.5rem"
                                        ),
                                        rx.button(
                                            "🔄 Limpiar búsqueda", 
                                            on_click=lambda: AlmacenState.filter_values(""), 
                                            size="2", 
                                            margin_top="1rem",
                                            variant="outline",
                                        ),
                                        spacing="3",
                                        align="center",
                                    ),
                                    height="300px", 
                                    width="100%",
                                )
                            ),
                            # Panel de instrucciones
                            rx.box(
                                rx.vstack(
                                    rx.hstack(
                                        rx.icon("info", size=20, color="#3b82f6"), 
                                        rx.text("💡 Instrucciones de uso:", 
                                               weight="bold", 
                                               size="3", 
                                               color="#1e293b"), 
                                        spacing="2",
                                        align="center",
                                    ),
                                    rx.grid(
                                        rx.box(
                                            rx.vstack(
                                                rx.text("1. Agregar Productos", size="2", font_weight="600", color="#1e293b"),
                                                rx.text("Usa el botón '➕ Agregar Producto' para añadir nuevos productos.", size="2", color="#475569"),
                                                spacing="1",
                                            ),
                                        ),
                                        rx.box(
                                            rx.vstack(
                                                rx.text("2. Filtrar y Ordenar", size="2", font_weight="600", color="#1e293b"),
                                                rx.text("Usa los campos de búsqueda y ordenación para organizar los datos.", size="2", color="#475569"),
                                                spacing="1",
                                            ),
                                        ),
                                        rx.box(
                                            rx.vstack(
                                                rx.text("3. Leyenda de Tipos", size="2", font_weight="600", color="#1e293b"),
                                                rx.text("Usa el botón '📋 Leyenda de Tipos' para ver los números de cada tipo.", size="2", color="#475569"),
                                                spacing="1",
                                            ),
                                        ),
                                        rx.box(
                                            rx.vstack(
                                                rx.text("4. Operaciones", size="2", font_weight="600", color="#1e293b"),
                                                rx.text("Selecciona UN producto para dar entrada o salida.", size="2", color="#475569"),
                                                spacing="1",
                                            ),
                                        ),
                                        columns="2",
                                        spacing="3",
                                        width="100%",
                                    ),
                                    align="start",
                                    spacing="3",
                                ),
                                width="100%", 
                                padding="1.5rem", 
                                border_radius="md", 
                                background="linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)",
                                border="1px solid #dbeafe",
                                margin_top="1.5rem",
                            ),
                            width="100%",
                        ),
                        rx.center(
                            rx.vstack(
                                rx.icon("package", size=48, color="#cbd5e1"),
                                rx.text("No hay productos en el almacén", 
                                       size="4", 
                                       color="#64748b",
                                       font_weight="600"),
                                rx.hstack(
                                    rx.button(
                                        "🔄 Intentar nuevamente", 
                                        on_click=AlmacenState.load_data, 
                                        size="2", 
                                        margin_top="1rem",
                                        variant="outline",
                                    ),
                                    add_product_dialog(),
                                    spacing="2",
                                ),
                                spacing="3",
                                align="center",
                            ),
                            height="300px", 
                            width="100%",
                        )
                    )
                ),
                spacing="4", 
                align="start", 
                padding="2rem", 
                width="100%",
            ),
            width="100%",
            style={
                "background": "linear-gradient(135deg, #f5f7ff 0%, #f0f2ff 100%)",
                "min_height": "100vh",
            }
        )
    
    return rx.cond(
        AuthState.is_authenticated,
        dashboard_content(),
        rx.center(
            rx.vstack(
                rx.spinner(size="3", color="#3b82f6"),
                rx.text("No autenticado. Redirigiendo...", 
                       margin_top="1rem", 
                       color="#475569",
                       text_align="center",
                       font_weight="500"),
                rx.button("Ir al Login", 
                         on_click=lambda: rx.redirect(Route.ADMIN_LOGIN.value), 
                         margin_top="2rem", 
                         width="200px",
                         variant="solid",
                         style={
                             "background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)"
                         }),
                spacing="3", 
                align="center", 
                width="100%", 
                max_width="400px", 
                padding="2rem",
            ),
            height="100vh", 
            width="100%",
            background="linear-gradient(135deg, #f5f7ff 0%, #f0f2ff 100%)",
        )
    )