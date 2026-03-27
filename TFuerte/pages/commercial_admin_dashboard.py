# TFuerte/pages/commercial_admin_dashboard.py
import reflex as rx
from TFuerte.state.commercial_admin_auth_state import CommercialAdminAuthState
from TFuerte.state.commercial_clients_state import CommercialClientsState
from TFuerte.state.commercial_contracts_state import CommercialContractsState
from TFuerte.state.commercial_suppliers_state import CommercialSuppliersState
from TFuerte.state.commercial_supplier_contracts_state import CommercialSupplierContractsState
from TFuerte.state.commercial_leasing_suppliers_state import CommercialLeasingSuppliersState
from TFuerte.state.commercial_lease_contracts_state import CommercialLeaseContractsState
from TFuerte.state.commercial_adhesion_suppliers_state import CommercialAdhesionSuppliersState
from TFuerte.state.commercial_adhesion_contracts_state import CommercialAdhesionContractsState
from TFuerte.routes import Route

class CommercialAdminState(rx.State):
    active_section: str = "clients"
    sidebar_collapsed: bool = False

    def set_active_section(self, section: str):
        self.active_section = section

    def toggle_sidebar(self):
        self.sidebar_collapsed = not self.sidebar_collapsed

@rx.page(
    route=Route.COMMERCIAL_ADMIN_DASHBOARD.value,
    title="Panel de Administración - Área Comercial",
    on_load=[
        CommercialAdminAuthState.check_auth,
        CommercialClientsState.load_data,
        CommercialContractsState.load_data,
        CommercialSuppliersState.load_data,
        CommercialSupplierContractsState.load_data,
        CommercialLeasingSuppliersState.load_data,
        CommercialLeaseContractsState.load_data,
        CommercialAdhesionSuppliersState.load_data,
        CommercialAdhesionContractsState.load_data,
    ],
)
def commercial_admin_dashboard() -> rx.Component:
    # -------------------- Componentes reutilizables --------------------
    def summary_cards() -> rx.Component:
        return rx.grid(
            rx.card(
                rx.vstack(
                    rx.text("Total Contratos", size="2", color="#64748b"),
                    rx.heading(CommercialContractsState.total_contracts, size="6", color="#1e293b"),
                    align="center",
                ),
                padding="1rem",
                border_radius="12px",
                box_shadow="sm",
                background="white",
            ),
            rx.card(
                rx.vstack(
                    rx.text("Pendientes Firma", size="2", color="#64748b"),
                    rx.heading(CommercialContractsState.pending_signature, size="6", color="#e67e22"),
                    align="center",
                ),
                padding="1rem",
                border_radius="12px",
                box_shadow="sm",
                background="white",
            ),
            rx.card(
                rx.vstack(
                    rx.text("Firmados", size="2", color="#64748b"),
                    rx.heading(CommercialContractsState.signed, size="6", color="#27ae60"),
                    align="center",
                ),
                padding="1rem",
                border_radius="12px",
                box_shadow="sm",
                background="white",
            ),
            rx.card(
                rx.vstack(
                    rx.text("Vencidos", size="2", color="#64748b"),
                    rx.heading(CommercialContractsState.expired, size="6", color="#c0392b"),
                    align="center",
                ),
                padding="1rem",
                border_radius="12px",
                box_shadow="sm",
                background="white",
            ),
            rx.card(
                rx.vstack(
                    rx.text("Próximos a vencer", size="2", color="#64748b"),
                    rx.heading(CommercialContractsState.near_expiry, size="6", color="#f39c12"),
                    align="center",
                ),
                padding="1rem",
                border_radius="12px",
                box_shadow="sm",
                background="white",
            ),
            columns="5",
            spacing="3",
            width="100%",
            margin_bottom="2rem",
        )

    def create_page_button(page_num: int, state) -> rx.Component:
        return rx.button(
            rx.text(page_num, size="2", font_weight="500"),
            on_click=lambda: state.go_to_page(page_num),
            variant="soft",
            size="2",
            style=rx.cond(
                state.current_page == page_num,
                {
                    "background": "#3b82f6",
                    "color": "white",
                    "border": "1px solid #3b82f6",
                    "_hover": {"background": "#1d4ed8"},
                    "flex_shrink": 0,
                    "width": "36px",
                    "padding": "0",
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
                    "width": "36px",
                    "padding": "0",
                }
            )
        )

    def render_pagination(state) -> rx.Component:
        return rx.hstack(
            rx.button(
                rx.icon("chevron-left", size=16),
                on_click=state.previous_page,
                variant="soft",
                size="2",
                is_disabled=state.current_page == 1,
                style={
                    "background": "white",
                    "border": "1px solid #e2e8f0",
                    "color": "#1e293b",
                    "flex_shrink": 0,
                    "width": "36px",
                    "padding": "0",
                }
            ),
            rx.box(
                rx.hstack(
                    rx.cond(
                        (state.current_page > 3) & (state.total_pages > 4),
                        rx.hstack(
                            create_page_button(1, state),
                            rx.text("...", size="2", color="#64748b", padding_x="1"),
                            spacing="1",
                            flex_shrink=0,
                        ),
                    ),
                    rx.cond(
                        state.page_numbers.length() > 0,
                        rx.hstack(
                            rx.foreach(state.page_numbers, lambda p: create_page_button(p, state)),
                            spacing="1",
                            wrap="nowrap",
                            flex_shrink=0,
                        ),
                        rx.text(f"Pág. {state.current_page}", size="2", color="#64748b", padding_x="2", flex_shrink=0),
                    ),
                    rx.cond(
                        (state.current_page < state.total_pages - 2) & (state.total_pages > 4),
                        rx.hstack(
                            rx.text("...", size="2", color="#64748b", padding_x="1"),
                            create_page_button(state.total_pages, state),
                            spacing="1",
                            flex_shrink=0,
                        ),
                    ),
                    spacing="1",
                    wrap="nowrap",
                    align="center",
                    justify="end",
                ),
                width="220px",
                flex_shrink=0,
                overflow_x="auto",
            ),
            rx.button(
                rx.icon("chevron-right", size=16),
                on_click=state.next_page,
                variant="soft",
                size="2",
                is_disabled=state.current_page == state.total_pages,
                style={
                    "background": "white",
                    "border": "1px solid #e2e8f0",
                    "color": "#1e293b",
                    "flex_shrink": 0,
                    "width": "36px",
                    "padding": "0",
                }
            ),
            spacing="2",
            wrap="nowrap",
            align="center",
            justify="end",
            width="100%",
        )

    # -------------------- Funciones de las pestañas (solo lectura) --------------------
    def clients_tab() -> rx.Component:
        def client_row(client):
            return rx.table.row(
                rx.table.cell(client.get("id", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(client.get("nombre_cliente", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(client.get("organismo", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(client.get("codigo_reup", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(client.get("telefono", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                _hover={"background_color": "#f8fafc"},
                style={"transition": "all 0.2s ease", "cursor": "pointer"},
            )

        return rx.vstack(
            rx.hstack(
                rx.input(
                    placeholder="Buscar por nombre...",
                    on_change=CommercialClientsState.filter_values,
                    width=["100%", "300px"],
                    style={"background": "white", "color": "#1e293b", "border": "1px solid #e2e8f0"},
                    background="gray",
                ),
                rx.select(
                    ["nombre_cliente", "organismo", "codigo_reup"],
                    placeholder="Ordenar por...",
                    on_change=CommercialClientsState.sort_values,
                    width=["100%", "200px"],
                    style={"background": "white", "color": "#1e293b"},
                ),
                rx.button(
                    "📥 CSV",
                    on_click=CommercialClientsState.download_csv,
                    style={"background": "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)", "color": "white"},
                ),
                spacing="2",
                wrap="wrap",
                width="100%",
                margin_bottom="1rem",
            ),
            rx.box(
                rx.scroll_area(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("ID", width="50px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Nombre", width="200px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Organismo", width="150px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("REUP", width="100px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Teléfono", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                            )
                        ),
                        rx.table.body(rx.foreach(CommercialClientsState.paginated_data, client_row)),
                        width="100%",
                    ),
                    type="always",
                    scrollbars="horizontal",
                    style={"max_height": "600px", "border": "1px solid #e2e8f0", "border_radius": "12px"},
                ),
                width="100%",
            ),
            rx.cond(
                CommercialClientsState.filtered_data.length() > CommercialClientsState.items_per_page,
                rx.box(
                    rx.hstack(
                        rx.text(
                            f"Mostrando {CommercialClientsState.current_page} de {CommercialClientsState.total_pages} páginas",
                            size="2",
                            color="#64748b",
                            flex=1,
                        ),
                        render_pagination(CommercialClientsState),
                        width="100%",
                        align="center",
                        justify="between",
                        wrap="wrap",
                    ),
                    padding="1rem",
                    border_top="1px solid #e2e8f0",
                    background="#f8fafc",
                ),
                rx.box(height="1rem"),
            ),
            width="100%",
            spacing="4",
        )

    def contracts_tab() -> rx.Component:
        def contract_row(contract):
            return rx.table.row(
                rx.table.cell(contract.get("contract_number", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("cliente_nombre", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(
                    rx.text(
                        contract.get("objeto", ""),
                        max_width="200px",
                        overflow="hidden",
                        text_overflow="ellipsis",
                        white_space="nowrap",
                        color="#1e293b",
                    ),
                    style={"padding": "12px 4px"},
                ),
                rx.table.cell(f"${contract.get('importe_cup', 0):,.2f}", style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(f"${contract.get('importe_mlc', 0):,.2f}", style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(f"${contract.get('promedio_mensual', 0):,.2f}", style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(f"${contract.get('ejecucion_cup', 0):,.2f}", style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(f"${contract.get('ejecucion_mlc', 0):,.2f}", style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(f"${contract.get('dif_cup', 0):,.2f}", style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(f"${contract.get('dif_mlc', 0):,.2f}", style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(
                    rx.button(
                        "👁️ Ver",
                        size="1",
                        on_click=lambda: CommercialContractsState.open_details_dialog(contract.get("id")),
                        style={"background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)", "color": "white"},
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
                _hover={"background_color": "#f8fafc"},
                style={"transition": "all 0.2s ease", "cursor": "pointer"},
            )

        return rx.vstack(
            summary_cards(),
            rx.hstack(
                rx.input(
                    placeholder="Buscar por cliente o número...",
                    on_change=CommercialContractsState.filter_values,
                    width=["100%", "300px"],
                    style={"background": "white", "color": "#1e293b", "border": "1px solid #e2e8f0"},
                    background="gray",
                ),
                rx.select(
                    ["contract_number", "cliente_nombre", "importe_cup"],
                    placeholder="Ordenar por...",
                    on_change=CommercialContractsState.sort_values,
                    width=["100%", "200px"],
                    style={"background": "white", "color": "#1e293b"},
                ),
                rx.button(
                    "📥 CSV",
                    on_click=CommercialContractsState.download_csv,
                    style={"background": "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)", "color": "white"},
                ),
                spacing="2",
                wrap="wrap",
                width="100%",
                margin_bottom="1rem",
            ),
            rx.box(
                rx.scroll_area(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("N° Contrato", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Cliente", width="150px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Objeto", width="200px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Imp. CUP", width="100px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Imp. MLC", width="100px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Promedio", width="100px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Ejec. CUP", width="100px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Ejec. MLC", width="100px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Dif. CUP", width="100px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Dif. MLC", width="100px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Detalles", width="70px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                            )
                        ),
                        rx.table.body(rx.foreach(CommercialContractsState.paginated_data, contract_row)),
                        width="100%",
                    ),
                    type="always",
                    scrollbars="horizontal",
                    style={"max_height": "500px", "border": "1px solid #e2e8f0", "border_radius": "12px"},
                ),
                width="100%",
            ),
            rx.cond(
                CommercialContractsState.filtered_data.length() > CommercialContractsState.items_per_page,
                rx.box(
                    rx.hstack(
                        rx.text(
                            f"Mostrando {CommercialContractsState.current_page} de {CommercialContractsState.total_pages} páginas",
                            size="2",
                            color="#64748b",
                            flex=1,
                        ),
                        render_pagination(CommercialContractsState),
                        width="100%",
                        align="center",
                        justify="between",
                        wrap="wrap",
                    ),
                    padding="1rem",
                    border_top="1px solid #e2e8f0",
                    background="#f8fafc",
                ),
                rx.box(height="1rem"),
            ),
            # Diálogo de detalles (solo lectura)
            contract_details_dialog(),
            width="100%",
            spacing="4",
        )

    def contract_details_dialog():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title(
                    rx.hstack(
                        rx.icon("file-text", size=20, color="#3b82f6"),
                        rx.text("Detalles del Contrato", font_weight="600"),
                        spacing="2",
                        align="center"
                    ),
                    color="#1e293b"
                ),
                rx.vstack(
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text("Fecha a Firma:", width="140px", size="2", color="#64748b"),
                                rx.text(CommercialContractsState.details_contract.get("fecha_a_firma", "-"), size="2", font_weight="500", color="#1e293b"),
                                spacing="2",
                                align="center"
                            ),
                            rx.hstack(
                                rx.text("Fecha Firmado:", width="140px", size="2", color="#64748b"),
                                rx.text(CommercialContractsState.details_contract.get("fecha_firmado", "-"), size="2", font_weight="500", color="#1e293b"),
                                spacing="2",
                                align="center"
                            ),
                            rx.hstack(
                                rx.text("Fecha Terminación:", width="140px", size="2", color="#64748b"),
                                rx.text(CommercialContractsState.details_contract.get("fecha_terminacion", "-"), size="2", font_weight="500", color="#1e293b"),
                                spacing="2",
                                align="center"
                            ),
                            rx.hstack(
                                rx.text("Vigencia:", width="140px", size="2", color="#64748b"),
                                rx.text(CommercialContractsState.details_contract.get("vigencia", "-"), size="2", font_weight="500", color="#1e293b"),
                                spacing="2",
                                align="center"
                            ),
                            rx.hstack(
                                rx.text("Ejecución CUP:", width="140px", size="2", color="#64748b"),
                                rx.text(f"${CommercialContractsState.details_contract.get('ejecucion_cup', 0):,.2f}", size="2", font_weight="500", color="#1e293b"),
                                spacing="2",
                                align="center"
                            ),
                            rx.hstack(
                                rx.text("Ejecución MLC/USD:", width="140px", size="2", color="#64748b"),
                                rx.text(f"${CommercialContractsState.details_contract.get('ejecucion_mlc', 0):,.2f}", size="2", font_weight="500", color="#1e293b"),
                                spacing="2",
                                align="center"
                            ),
                            rx.hstack(
                                rx.text("Observaciones:", width="140px", size="2", color="#64748b"),
                                rx.text(CommercialContractsState.details_contract.get("observaciones", "-"), size="2", font_weight="500", color="#1e293b"),
                                spacing="2",
                                align="center"
                            ),
                            spacing="3",
                            align="start",
                            padding="1rem",
                            border_radius="8px",
                            background="#f8fafc",
                            border="1px solid #e2e8f0",
                        ),
                        width="100%",
                    ),
                    rx.dialog.close(
                        rx.button("Cerrar", variant="soft", size="2"),
                        margin_top="1rem",
                    ),
                    spacing="3",
                    width="100%",
                ),
                max_width="500px",
                style={"background": "white", "border_radius": "12px"},
            ),
            open=CommercialContractsState.show_details_dialog,
            on_open_change=CommercialContractsState.set_show_details_dialog,
        )

    def suppliers_tab() -> rx.Component:
        def supplier_row(supplier):
            return rx.table.row(
                rx.table.cell(supplier.get("id", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("nombre_proveedor", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("organismo", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("codigo_reup", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("telefono", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                _hover={"background_color": "#f8fafc"},
                style={"transition": "all 0.2s ease", "cursor": "pointer"},
            )

        return rx.vstack(
            rx.hstack(
                rx.input(
                    placeholder="Buscar por nombre...",
                    on_change=CommercialSuppliersState.filter_values,
                    width=["100%", "300px"],
                    style={"background": "white", "color": "#1e293b", "border": "1px solid #e2e8f0"},
                    background="gray",
                ),
                rx.select(
                    ["nombre_proveedor", "organismo", "codigo_reup"],
                    placeholder="Ordenar por...",
                    on_change=CommercialSuppliersState.sort_values,
                    width=["100%", "200px"],
                    style={"background": "white", "color": "#1e293b"},
                ),
                rx.button(
                    "📥 CSV",
                    on_click=CommercialSuppliersState.download_csv,
                    style={"background": "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)", "color": "white"},
                ),
                spacing="2",
                wrap="wrap",
                width="100%",
                margin_bottom="1rem",
            ),
            rx.box(
                rx.scroll_area(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("ID", width="50px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Nombre", width="200px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Organismo", width="150px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("REUP", width="100px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Teléfono", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                            )
                        ),
                        rx.table.body(rx.foreach(CommercialSuppliersState.paginated_data, supplier_row)),
                        width="100%",
                    ),
                    type="always",
                    scrollbars="horizontal",
                    style={"max_height": "500px", "border": "1px solid #e2e8f0", "border_radius": "12px"},
                ),
                width="100%",
            ),
            rx.cond(
                CommercialSuppliersState.filtered_data.length() > CommercialSuppliersState.items_per_page,
                rx.box(
                    rx.hstack(
                        rx.text(
                            f"Mostrando {CommercialSuppliersState.current_page} de {CommercialSuppliersState.total_pages} páginas",
                            size="2",
                            color="#64748b",
                            flex=1,
                        ),
                        render_pagination(CommercialSuppliersState),
                        width="100%",
                        align="center",
                        justify="between",
                        wrap="wrap",
                    ),
                    padding="1rem",
                    border_top="1px solid #e2e8f0",
                    background="#f8fafc",
                ),
                rx.box(height="1rem"),
            ),
            width="100%",
            spacing="4",
        )

    def supplier_contracts_tab() -> rx.Component:
        def contract_row(contract):
            return rx.table.row(
                rx.table.cell(contract.get("contract_number", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("supplier", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(
                    rx.text(
                        contract.get("contract_type_object", ""),
                        max_width="200px",
                        overflow="hidden",
                        text_overflow="ellipsis",
                        white_space="nowrap",
                        color="#1e293b",
                    ),
                    style={"padding": "12px 4px"},
                ),
                rx.table.cell(f"${contract.get('value', 0):,.2f}", style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("start_date", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("end_date", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("validity", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                _hover={"background_color": "#f8fafc"},
                style={"transition": "all 0.2s ease", "cursor": "pointer"},
            )

        return rx.vstack(
            rx.hstack(
                rx.input(
                    placeholder="Buscar por proveedor o número...",
                    on_change=CommercialSupplierContractsState.filter_values,
                    width=["100%", "300px"],
                    style={"background": "white", "color": "#1e293b", "border": "1px solid #e2e8f0"},
                    background="gray",
                ),
                rx.select(
                    ["contract_number", "supplier", "value"],
                    placeholder="Ordenar por...",
                    on_change=CommercialSupplierContractsState.sort_values,
                    width=["100%", "200px"],
                    style={"background": "white", "color": "#1e293b"},
                ),
                rx.button(
                    "📥 CSV",
                    on_click=CommercialSupplierContractsState.download_csv,
                    style={"background": "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)", "color": "white"},
                ),
                spacing="2",
                wrap="wrap",
                width="100%",
                margin_bottom="1rem",
            ),
            rx.box(
                rx.scroll_area(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("N° Contrato", width="150px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Proveedor", width="200px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Tipo y Objeto", width="200px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Valor", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Fecha Inicio", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Fecha Terminación", width="140px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Vigencia", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                            )
                        ),
                        rx.table.body(rx.foreach(CommercialSupplierContractsState.paginated_data, contract_row)),
                        width="100%",
                    ),
                    type="always",
                    scrollbars="horizontal",
                    style={"max_height": "500px", "border": "1px solid #e2e8f0", "border_radius": "12px"},
                ),
                width="100%",
            ),
            rx.cond(
                CommercialSupplierContractsState.filtered_data.length() > CommercialSupplierContractsState.items_per_page,
                rx.box(
                    rx.hstack(
                        rx.text(
                            f"Mostrando {CommercialSupplierContractsState.current_page} de {CommercialSupplierContractsState.total_pages} páginas",
                            size="2",
                            color="#64748b",
                            flex=1,
                        ),
                        render_pagination(CommercialSupplierContractsState),
                        width="100%",
                        align="center",
                        justify="between",
                        wrap="wrap",
                    ),
                    padding="1rem",
                    border_top="1px solid #e2e8f0",
                    background="#f8fafc",
                ),
                rx.box(height="1rem"),
            ),
            width="100%",
            spacing="4",
        )

    def leasing_suppliers_tab() -> rx.Component:
        def supplier_row(supplier):
            return rx.table.row(
                rx.table.cell(supplier.get("id", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("nombre_proveedor", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("organismo", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("codigo_reup", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("telefono", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                _hover={"background_color": "#f8fafc"},
                style={"transition": "all 0.2s ease", "cursor": "pointer"},
            )

        return rx.vstack(
            rx.hstack(
                rx.input(
                    placeholder="Buscar por nombre...",
                    on_change=CommercialLeasingSuppliersState.filter_values,
                    width=["100%", "300px"],
                    style={"background": "white", "color": "#1e293b", "border": "1px solid #e2e8f0"},
                    background="gray",
                ),
                rx.select(
                    ["nombre_proveedor", "organismo", "codigo_reup"],
                    placeholder="Ordenar por...",
                    on_change=CommercialLeasingSuppliersState.sort_values,
                    width=["100%", "200px"],
                    style={"background": "white", "color": "#1e293b"},
                ),
                rx.button(
                    "📥 CSV",
                    on_click=CommercialLeasingSuppliersState.download_csv,
                    style={"background": "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)", "color": "white"},
                ),
                spacing="2",
                wrap="wrap",
                width="100%",
                margin_bottom="1rem",
            ),
            rx.box(
                rx.scroll_area(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("ID", width="50px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Nombre", width="200px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Organismo", width="150px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("REUP", width="100px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Teléfono", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                            )
                        ),
                        rx.table.body(rx.foreach(CommercialLeasingSuppliersState.paginated_data, supplier_row)),
                        width="100%",
                    ),
                    type="always",
                    scrollbars="horizontal",
                    style={"max_height": "500px", "border": "1px solid #e2e8f0", "border_radius": "12px"},
                ),
                width="100%",
            ),
            rx.cond(
                CommercialLeasingSuppliersState.filtered_data.length() > CommercialLeasingSuppliersState.items_per_page,
                rx.box(
                    rx.hstack(
                        rx.text(
                            f"Mostrando {CommercialLeasingSuppliersState.current_page} de {CommercialLeasingSuppliersState.total_pages} páginas",
                            size="2",
                            color="#64748b",
                            flex=1,
                        ),
                        render_pagination(CommercialLeasingSuppliersState),
                        width="100%",
                        align="center",
                        justify="between",
                        wrap="wrap",
                    ),
                    padding="1rem",
                    border_top="1px solid #e2e8f0",
                    background="#f8fafc",
                ),
                rx.box(height="1rem"),
            ),
            width="100%",
            spacing="4",
        )

    def lease_contracts_tab() -> rx.Component:
        def contract_row(contract):
            return rx.table.row(
                rx.table.cell(contract.get("proveedor", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("tipo_contrato", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(f"${contract.get('valor', 0):,.2f}", style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("vigencia", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("fecha_inicio", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("fecha_terminacion", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                _hover={"background_color": "#f8fafc"},
                style={"transition": "all 0.2s ease", "cursor": "pointer"},
            )

        return rx.vstack(
            rx.hstack(
                rx.input(
                    placeholder="Buscar por proveedor...",
                    on_change=CommercialLeaseContractsState.filter_values,
                    width=["100%", "300px"],
                    style={"background": "white", "color": "#1e293b", "border": "1px solid #e2e8f0"},
                    background="gray",
                ),
                rx.select(
                    ["proveedor", "tipo_contrato", "valor"],
                    placeholder="Ordenar por...",
                    on_change=CommercialLeaseContractsState.sort_values,
                    width=["100%", "200px"],
                    style={"background": "white", "color": "#1e293b"},
                ),
                rx.button(
                    "📥 CSV",
                    on_click=CommercialLeaseContractsState.download_csv,
                    style={"background": "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)", "color": "white"},
                ),
                spacing="2",
                wrap="wrap",
                width="100%",
                margin_bottom="1rem",
            ),
            rx.box(
                rx.scroll_area(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Proveedor", width="200px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Tipo Contrato", width="150px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Valor", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Vigencia", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Fecha Inicio", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Fecha Terminación", width="140px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                            )
                        ),
                        rx.table.body(rx.foreach(CommercialLeaseContractsState.paginated_data, contract_row)),
                        width="100%",
                    ),
                    type="always",
                    scrollbars="horizontal",
                    style={"max_height": "500px", "border": "1px solid #e2e8f0", "border_radius": "12px"},
                ),
                width="100%",
            ),
            rx.cond(
                CommercialLeaseContractsState.filtered_data.length() > CommercialLeaseContractsState.items_per_page,
                rx.box(
                    rx.hstack(
                        rx.text(
                            f"Mostrando {CommercialLeaseContractsState.current_page} de {CommercialLeaseContractsState.total_pages} páginas",
                            size="2",
                            color="#64748b",
                            flex=1,
                        ),
                        render_pagination(CommercialLeaseContractsState),
                        width="100%",
                        align="center",
                        justify="between",
                        wrap="wrap",
                    ),
                    padding="1rem",
                    border_top="1px solid #e2e8f0",
                    background="#f8fafc",
                ),
                rx.box(height="1rem"),
            ),
            width="100%",
            spacing="4",
        )

    def adhesion_suppliers_tab() -> rx.Component:
        def supplier_row(supplier):
            return rx.table.row(
                rx.table.cell(supplier.get("id", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("nombre_proveedor", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("organismo", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("codigo_reup", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("telefono", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                _hover={"background_color": "#f8fafc"},
                style={"transition": "all 0.2s ease", "cursor": "pointer"},
            )

        return rx.vstack(
            rx.hstack(
                rx.input(
                    placeholder="Buscar por nombre...",
                    on_change=CommercialAdhesionSuppliersState.filter_values,
                    width=["100%", "300px"],
                    style={"background": "white", "color": "#1e293b", "border": "1px solid #e2e8f0"},
                    background="gray",
                ),
                rx.select(
                    ["nombre_proveedor", "organismo", "codigo_reup"],
                    placeholder="Ordenar por...",
                    on_change=CommercialAdhesionSuppliersState.sort_values,
                    width=["100%", "200px"],
                    style={"background": "white", "color": "#1e293b"},
                ),
                rx.button(
                    "📥 CSV",
                    on_click=CommercialAdhesionSuppliersState.download_csv,
                    style={"background": "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)", "color": "white"},
                ),
                spacing="2",
                wrap="wrap",
                width="100%",
                margin_bottom="1rem",
            ),
            rx.box(
                rx.scroll_area(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("ID", width="50px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Nombre", width="200px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Organismo", width="150px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("REUP", width="100px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Teléfono", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                            )
                        ),
                        rx.table.body(rx.foreach(CommercialAdhesionSuppliersState.paginated_data, supplier_row)),
                        width="100%",
                    ),
                    type="always",
                    scrollbars="horizontal",
                    style={"max_height": "500px", "border": "1px solid #e2e8f0", "border_radius": "12px"},
                ),
                width="100%",
            ),
            rx.cond(
                CommercialAdhesionSuppliersState.filtered_data.length() > CommercialAdhesionSuppliersState.items_per_page,
                rx.box(
                    rx.hstack(
                        rx.text(
                            f"Mostrando {CommercialAdhesionSuppliersState.current_page} de {CommercialAdhesionSuppliersState.total_pages} páginas",
                            size="2",
                            color="#64748b",
                            flex=1,
                        ),
                        render_pagination(CommercialAdhesionSuppliersState),
                        width="100%",
                        align="center",
                        justify="between",
                        wrap="wrap",
                    ),
                    padding="1rem",
                    border_top="1px solid #e2e8f0",
                    background="#f8fafc",
                ),
                rx.box(height="1rem"),
            ),
            width="100%",
            spacing="4",
        )

    def adhesion_contracts_tab() -> rx.Component:
        def contract_row(contract):
            return rx.table.row(
                rx.table.cell(contract.get("proveedor", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("tipo_contrato", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(f"${contract.get('valor', 0):,.2f}", style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("vigencia", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("fecha_inicio", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("fecha_terminacion", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                _hover={"background_color": "#f8fafc"},
                style={"transition": "all 0.2s ease", "cursor": "pointer"},
            )

        return rx.vstack(
            rx.hstack(
                rx.input(
                    placeholder="Buscar por proveedor...",
                    on_change=CommercialAdhesionContractsState.filter_values,
                    width=["100%", "300px"],
                    style={"background": "white", "color": "#1e293b", "border": "1px solid #e2e8f0"},
                    background="gray",
                ),
                rx.select(
                    ["proveedor", "tipo_contrato", "valor"],
                    placeholder="Ordenar por...",
                    on_change=CommercialAdhesionContractsState.sort_values,
                    width=["100%", "200px"],
                    style={"background": "white", "color": "#1e293b"},
                ),
                rx.button(
                    "📥 CSV",
                    on_click=CommercialAdhesionContractsState.download_csv,
                    style={"background": "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)", "color": "white"},
                ),
                spacing="2",
                wrap="wrap",
                width="100%",
                margin_bottom="1rem",
            ),
            rx.box(
                rx.scroll_area(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Proveedor", width="200px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Tipo Contrato", width="150px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Valor", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Vigencia", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Fecha Inicio", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Fecha Terminación", width="140px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                            )
                        ),
                        rx.table.body(rx.foreach(CommercialAdhesionContractsState.paginated_data, contract_row)),
                        width="100%",
                    ),
                    type="always",
                    scrollbars="horizontal",
                    style={"max_height": "500px", "border": "1px solid #e2e8f0", "border_radius": "12px"},
                ),
                width="100%",
            ),
            rx.cond(
                CommercialAdhesionContractsState.filtered_data.length() > CommercialAdhesionContractsState.items_per_page,
                rx.box(
                    rx.hstack(
                        rx.text(
                            f"Mostrando {CommercialAdhesionContractsState.current_page} de {CommercialAdhesionContractsState.total_pages} páginas",
                            size="2",
                            color="#64748b",
                            flex=1,
                        ),
                        render_pagination(CommercialAdhesionContractsState),
                        width="100%",
                        align="center",
                        justify="between",
                        wrap="wrap",
                    ),
                    padding="1rem",
                    border_top="1px solid #e2e8f0",
                    background="#f8fafc",
                ),
                rx.box(height="1rem"),
            ),
            width="100%",
            spacing="4",
        )

    def profile_tab() -> rx.Component:
        return rx.vstack(
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.icon("user", size=24, color="#3b82f6"),
                        rx.vstack(
                            rx.text("Usuario Administrador", size="4", font_weight="700", color="#1e293b"),
                            rx.text(
                                "Panel de solo lectura - Área Comercial",
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
                        rx.text("📋 Información:", size="3", font_weight="600", color="#1e293b"),
                        rx.list(
                            rx.list.item("✓ Visualización de todos los registros"),
                            rx.list.item("✓ Filtros y ordenamiento"),
                            rx.list.item("✓ Descarga de datos en CSV"),
                            rx.list.item("✓ Vista de detalles de contratos"),
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
                            on_click=CommercialAdminAuthState.logout,
                            color_scheme="red",
                            variant="solid",
                            size="2",
                            style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)"}
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
                                rx.text("Total Clientes", size="2", color="#64748b"),
                                rx.text(CommercialClientsState.clients_data.length(), size="4", font_weight="700", color="#3b82f6"),
                                spacing="1",
                                align="center"
                            ),
                            style={"background": "#eff6ff", "padding": "1rem", "border_radius": "8px", "border": "1px solid #dbeafe", "text_align": "center"}
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("Total Proveedores", size="2", color="#64748b"),
                                rx.text(CommercialSuppliersState.suppliers_data.length(), size="4", font_weight="700", color="#8b5cf6"),
                                spacing="1",
                                align="center"
                            ),
                            style={"background": "#f5f3ff", "padding": "1rem", "border_radius": "8px", "border": "1px solid #c4b5fd", "text_align": "center"}
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("Contratos con Clientes", size="2", color="#64748b"),
                                rx.text(CommercialContractsState.contracts_data.length(), size="4", font_weight="700", color="#059669"),
                                spacing="1",
                                align="center"
                            ),
                            style={"background": "#f0fdfa", "padding": "1rem", "border_radius": "8px", "border": "1px solid #a7f3d0", "text_align": "center"}
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text("Contratos con Proveedores", size="2", color="#64748b"),
                                rx.text(CommercialSupplierContractsState.contracts_data.length(), size="4", font_weight="700", color="#f97316"),
                                spacing="1",
                                align="center"
                            ),
                            style={"background": "#fff7ed", "padding": "1rem", "border_radius": "8px", "border": "1px solid #fed7aa", "text_align": "center"}
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
        )

    # -------------------- Barra lateral colapsable --------------------
    def sidebar():
        def menu_item(icon: str, label: str, section: str):
            is_active = CommercialAdminState.active_section == section
            return rx.link(
                rx.hstack(
                    rx.icon(icon, size=20),
                    rx.cond(
                        ~CommercialAdminState.sidebar_collapsed,
                        rx.text(label, weight="medium"),
                    ),
                    spacing="3",
                    align="center",
                ),
                on_click=lambda: CommercialAdminState.set_active_section(section),
                style={
                    "display": "flex",
                    "align_items": "center",
                    "gap": "12px",
                    "padding": "0.75rem 1rem",
                    "border_radius": "8px",
                    "color": "#1e293b",
                    "transition": "all 0.2s",
                    "white_space": "nowrap",
                    "background": rx.cond(is_active, "#eef2ff", "transparent"),
                    "color": rx.cond(is_active, "#3b82f6", "#1e293b"),
                    "justify_content": rx.cond(
                        CommercialAdminState.sidebar_collapsed,
                        "center",
                        "flex-start"
                    ),
                },
                href="#",
            )

        return rx.box(
            rx.vstack(
                rx.hstack(
                    rx.cond(
                        ~CommercialAdminState.sidebar_collapsed,
                        rx.heading("Área Comercial", size="5", color="#1e293b"),
                    ),
                    rx.button(
                        rx.icon("menu", size=20, color="#3D3A3D"),
                        on_click=CommercialAdminState.toggle_sidebar,
                        variant="ghost",
                        color_scheme="gray",
                        style={"margin_left": "auto", "padding": "0.5rem"},
                    ),
                    justify="between",
                    width="100%",
                    padding="0.5rem 1rem",
                ),
                rx.divider(margin_y="0.5rem"),
                rx.vstack(
                    menu_item("users", "Clientes", "clients"),
                    menu_item("file-text", "Contratos con Clientes", "contracts"),
                    menu_item("building", "Proveedores", "suppliers"),
                    menu_item("file-text", "Contratos con Proveedores", "supplier_contracts"),
                    menu_item("home", "Proveedores de Arrendamiento", "leasing_suppliers"),
                    menu_item("file-text", "Contratos de Arrendamiento", "lease_contracts"),
                    menu_item("file", "Proveedores de Adhesión", "adhesion_suppliers"),
                    menu_item("file-text", "Contratos de Adhesión", "adhesion_contracts"),
                    menu_item("user", "Mi Perfil", "profile"),
                    spacing="1",
                    width="100%",
                ),
                spacing="4",
                align="start",
                width="100%",
                padding="0.5rem 0",
            ),
            width=rx.cond(
                CommercialAdminState.sidebar_collapsed,
                "80px",
                "280px"
            ),
            height="100vh",
            position="fixed",
            left="0",
            top="0",
            background="white",
            border_right="1px solid #e2e8f0",
            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.05)",
            overflow_y="auto",
            transition="width 0.3s ease",
            z_index="1000",
        )

    # -------------------- Contenido principal --------------------
    def main_content():
        return rx.box(
            rx.vstack(
                rx.box(
                    rx.hstack(
                        rx.hstack(
                            rx.heading(
                                rx.cond(
                                    CommercialAdminState.active_section == "clients", "Clientes",
                                    rx.cond(
                                        CommercialAdminState.active_section == "contracts", "Contratos con Clientes",
                                        rx.cond(
                                            CommercialAdminState.active_section == "suppliers", "Proveedores",
                                            rx.cond(
                                                CommercialAdminState.active_section == "supplier_contracts", "Contratos con Proveedores",
                                                rx.cond(
                                                    CommercialAdminState.active_section == "leasing_suppliers", "Proveedores de Arrendamiento",
                                                    rx.cond(
                                                        CommercialAdminState.active_section == "lease_contracts", "Contratos de Arrendamiento",
                                                        rx.cond(
                                                            CommercialAdminState.active_section == "adhesion_suppliers", "Proveedores de Adhesión",
                                                            rx.cond(
                                                                CommercialAdminState.active_section == "adhesion_contracts", "Contratos de Adhesión",
                                                                "Mi Perfil"
                                                            )
                                                        )
                                                    )
                                                )
                                            )
                                        )
                                    )
                                ),
                                size="5",
                                color="#1e293b",
                            ),
                            spacing="3",
                            align="center",
                        ),
                        rx.spacer(),
                        rx.button(
                            "Cerrar Sesión",
                            on_click=CommercialAdminAuthState.logout,
                            color_scheme="red",
                            variant="soft",
                            size="2",
                        ),
                        width="100%",
                        align="center",
                    ),
                    padding="1rem 2rem",
                    border_bottom="1px solid #e2e8f0",
                    background="white",
                ),
                rx.box(
                    rx.cond(
                        CommercialAdminState.active_section == "clients", clients_tab(),
                        rx.cond(
                            CommercialAdminState.active_section == "contracts", contracts_tab(),
                            rx.cond(
                                CommercialAdminState.active_section == "suppliers", suppliers_tab(),
                                rx.cond(
                                    CommercialAdminState.active_section == "supplier_contracts", supplier_contracts_tab(),
                                    rx.cond(
                                        CommercialAdminState.active_section == "leasing_suppliers", leasing_suppliers_tab(),
                                        rx.cond(
                                            CommercialAdminState.active_section == "lease_contracts", lease_contracts_tab(),
                                            rx.cond(
                                                CommercialAdminState.active_section == "adhesion_suppliers", adhesion_suppliers_tab(),
                                                rx.cond(
                                                    CommercialAdminState.active_section == "adhesion_contracts", adhesion_contracts_tab(),
                                                    profile_tab()
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    padding="2rem",
                    width="100%",
                ),
                spacing="0",
                width="100%",
                min_height="100vh",
            ),
            margin_left=rx.cond(
                CommercialAdminState.sidebar_collapsed,
                "80px",
                "280px"
            ),
            width=rx.cond(
                CommercialAdminState.sidebar_collapsed,
                "calc(100% - 80px)",
                "calc(100% - 280px)"
            ),
            transition="margin-left 0.3s ease, width 0.3s ease",
        )

    # -------------------- Render final --------------------
    return rx.cond(
        CommercialAdminAuthState.is_authenticated,  # Opcional: si quieres que solo admins vean
        rx.box(
            sidebar(),
            main_content(),
            width="100%",
            min_height="100vh",
            background="#f8fafc",
        ),
        rx.center(
            rx.vstack(
                rx.spinner(size="3"),
                rx.text("No autenticado. Redirigiendo...", color="#1e293b"),
                rx.button(
                    "Ir al Login",
                    on_click=lambda: rx.redirect(Route.COMMERCIAL_LOGIN.value),
                    style={"background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)", "color": "white"},
                ),
                spacing="3",
                align="center",
            ),
            height="100vh",
        ),
    )