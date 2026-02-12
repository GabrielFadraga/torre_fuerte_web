import reflex as rx
from TFuerte.state.almacen_view_state import AlmacenViewState

def almacen_readonly_table() -> rx.Component:
    """Tabla de solo lectura para los productos en almacén"""
    
    # Estilos para la tabla
    header_style = {
        "background": "linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)",
        "color": "white",
        "font_weight": "600",
        "padding": "12px 6px",
        "text_align": "center",
        "border": "none",
        "font_size": "12px",
        "text_transform": "uppercase",
        "letter_spacing": "0.5px",
    }
    
    cell_style = {
        "padding": "8px 4px",
        "border_bottom": "1px solid #e2e8f0",
        "vertical_align": "middle",
        "font_size": "12px",
        "color": "#475569",
        "text_align": "center",
        "overflow": "hidden",
        "box_sizing": "border-box",
    }
    
    def table_header():
        return rx.table.row(
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
    
    def table_row(item):
        return rx.table.row(
            rx.table.cell(
                rx.badge(
                    item.get("Numero", ""),
                    variant="solid",
                    color_scheme="blue",
                    size="1"
                ),
                style=cell_style
            ),
            rx.table.cell(
                rx.text(
                    item.get("Codigo", ""),
                    style={
                        "font_family": "monospace",
                        "font_weight": "500"
                    }
                ),
                style=cell_style
            ),
            rx.table.cell(
                rx.text(
                    item.get("Descripcion del producto", ""),
                    style={
                        "white_space": "nowrap",
                        "overflow": "hidden",
                        "text_overflow": "ellipsis",
                    }
                ),
                style={**cell_style, "text_align": "left"}
            ),
            rx.table.cell(
                rx.text(item.get("Tipo de producto", "")),
                style=cell_style
            ),
            rx.table.cell(
                rx.badge(
                    item.get("UM", ""),
                    variant="outline",
                    color_scheme="gray",
                    size="1"
                ),
                style=cell_style
            ),
            rx.table.cell(
                rx.text(item.get("Fecha de entrada", "")),
                style=cell_style
            ),
            rx.table.cell(
                rx.badge(
                    item.get("Cantidad E", 0),
                    variant="soft",
                    color_scheme="green",
                    size="1"
                ),
                style=cell_style
            ),
            rx.table.cell(
                rx.cond(
                    item.get("Fecha de salida"),
                    rx.text(item.get("Fecha de salida", "")),
                    rx.text("-", color="#94a3b8", font_style="italic")
                ),
                style=cell_style
            ),
            rx.table.cell(
                rx.cond(
                    item.get("Cantidad S", 0) != 0,
                    rx.badge(
                        item.get("Cantidad S", 0),
                        variant="soft",
                        color_scheme="red",
                        size="1"
                    ),
                    rx.text("-", color="#94a3b8", font_style="italic")
                ),
                style=cell_style
            ),
            rx.table.cell(
                rx.badge(
                    item.get("Saldo", 0),
                    variant="solid",
                    color_scheme="blue",
                    size="1"
                ),
                style=cell_style
            ),
            rx.table.cell(
                rx.text(
                    f"${item.get('Precio', 0):.2f}",
                    style={
                        "font_weight": "600",
                        "color": "#059669"
                    }
                ),
                style=cell_style
            ),
            rx.table.cell(
                rx.text(
                    f"${item.get('Importe', 0):.2f}",
                    style={
                        "font_weight": "600",
                        "color": "#2563eb"
                    }
                ),
                style=cell_style
            ),
        )
    
    return rx.vstack(
        # Estadísticas
        rx.box(
            rx.hstack(
                rx.box(
                    rx.vstack(
                        rx.text("Total Productos", size="1", color="#64748b"),
                        rx.badge(
                            AlmacenViewState.total_productos,
                            variant="solid",
                            color_scheme="green",
                            size="2"
                        ),
                        align="center",
                        spacing="1"
                    ),
                    flex="1"
                ),
                rx.box(
                    rx.vstack(
                        rx.text("Valor Total", size="1", color="#64748b"),
                        rx.text(
                            rx.cond(
                                AlmacenViewState.valor_total > 0,
                                f"${AlmacenViewState.valor_total:,.2f}",
                                "$0.00"
                            ),
                            size="3",
                            font_weight="700",
                            color="#2563eb"
                        ),
                        align="center",
                        spacing="1"
                    ),
                    flex="1"
                ),
                spacing="4",
                width="100%",
                justify="center"
            ),
            width="100%",
            padding="1rem",
            border_radius="8px",
            background="#f8fafc",
            border="1px solid #e2e8f0",
            margin_bottom="1rem"
        ),
        
        # Controles de búsqueda
        rx.hstack(
            rx.input(
                placeholder="Buscar por descripción...",
                on_change=AlmacenViewState.filter_values,
                width=["100%", "300px", "300px", "300px"],
                size="2"
            ),
            rx.select(
                ["Numero", "Codigo", "Descripcion del producto", "Tipo de producto", "Precio"],
                placeholder="Ordenar por...",
                on_change=AlmacenViewState.sort_values,
                width=["100%", "200px", "200px", "200px"],
                size="2"
            ),
            rx.button(
                "🔄 Actualizar",
                on_click=AlmacenViewState.load_data,
                loading=AlmacenViewState.loading,
                variant="soft",
                size="2"
            ),
            spacing="2",
            width="100%",
            wrap="wrap",
            justify="center",
            margin_bottom="1rem"
        ),
        
        # Tabla de datos
        rx.cond(
            AlmacenViewState.loading,
            rx.center(
                rx.vstack(
                    rx.spinner(size="3"),
                    rx.text("Cargando productos...", size="2", color="#64748b"),
                    spacing="2"
                ),
                padding="2rem"
            ),
            rx.cond(
                AlmacenViewState.filtered_data.length() > 0,
                rx.scroll_area(
                    rx.table.root(
                        rx.table.header(table_header()),
                        rx.table.body(
                            rx.foreach(
                                AlmacenViewState.filtered_data,
                                table_row
                            )
                        ),
                        style={
                            "width": "100%",
                            "min_width": "1400px",
                            "table_layout": "fixed",
                        }
                    ),
                    type="always",
                    scrollbars="horizontal",
                    style={
                        "width": "100%",
                        "height": "500px",
                        "overflow_y": "auto",
                        "border": "1px solid #e2e8f0",
                        "border_radius": "8px",
                        "box_shadow": "0 2px 4px rgba(0, 0, 0, 0.05)",
                    }
                ),
                rx.center(
                    rx.vstack(
                        rx.icon("package", size=32, color="#cbd5e1"),
                        rx.text("No se encontraron productos", size="3", color="#64748b"),
                        rx.cond(
                            AlmacenViewState.search_value != "",
                            rx.text(
                                f"La búsqueda '{AlmacenViewState.search_value}' no devolvió resultados",
                                size="2",
                                color="#94a3b8"
                            ),
                        ),
                        spacing="2",
                        align="center"
                    ),
                    padding="3rem"
                )
            )
        ),
        
        # Información de filtrado
        rx.cond(
            AlmacenViewState.search_value != "",
            rx.box(
                rx.hstack(
                    rx.icon("search", size=14, color="#4f46e5"),
                    rx.text(
                        f"Mostrando {AlmacenViewState.filtered_data.length()} de {AlmacenViewState.almacen_data.length()} productos",
                        size="1",
                        color="#64748b"
                    ),
                    rx.button(
                        "Limpiar filtro",
                        on_click=lambda: AlmacenViewState.filter_values(""),
                        size="1",
                        variant="ghost"
                    ),
                    spacing="2",
                    align="center",
                    width="100%",
                    justify="between"
                ),
                width="100%",
                padding="0.5rem 0.75rem",
                border_radius="6px",
                background="#f5f3ff",
                border="1px solid #ddd6fe",
                margin_top="1rem"
            ),
        ),
        
        spacing="3",
        width="100%",
        align="start"
    )