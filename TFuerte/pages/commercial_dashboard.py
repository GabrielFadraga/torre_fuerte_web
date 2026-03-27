import reflex as rx
from TFuerte.state.commercial_auth_state import CommercialAuthState
from TFuerte.state.commercial_clients_state import CommercialClientsState
from TFuerte.state.commercial_contracts_state import CommercialContractsState
from TFuerte.state.commercial_suppliers_state import CommercialSuppliersState
from TFuerte.state.commercial_supplier_contracts_state import CommercialSupplierContractsState
from TFuerte.state.commercial_leasing_suppliers_state import CommercialLeasingSuppliersState
from TFuerte.state.commercial_lease_contracts_state import CommercialLeaseContractsState
from TFuerte.state.commercial_adhesion_suppliers_state import CommercialAdhesionSuppliersState
from TFuerte.state.commercial_adhesion_contracts_state import CommercialAdhesionContractsState
from TFuerte.components.navbar import navbar
from TFuerte.routes import Route

class CommercialDashboardState(rx.State):
    active_section: str = "clients"
    sidebar_collapsed: bool = False

    def set_active_section(self, section: str):
        self.active_section = section

    def toggle_sidebar(self):
        self.sidebar_collapsed = not self.sidebar_collapsed

@rx.page(
    route=Route.COMMERCIAL_DASHBOARD.value,
    title="Dashboard Comercial",
    on_load=[
        CommercialAuthState.check_auth,
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
def commercial_dashboard() -> rx.Component:
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

    # -------------------- Diálogos para Clientes --------------------
    def add_edit_client_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title(
                    rx.cond(
                        CommercialClientsState.edit_form_data.get("id"),
                        "Editar Cliente",
                        "Nuevo Cliente",
                    ),
                    color="#1e293b",
                ),
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Nombre del Cliente *",
                            name="nombre_cliente",
                            default_value=CommercialClientsState.edit_form_data.get("nombre_cliente", ""),
                            required=True,
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Objeto Social",
                            name="objeto_social",
                            default_value=CommercialClientsState.edit_form_data.get("objeto_social", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Organismo",
                            name="organismo",
                            default_value=CommercialClientsState.edit_form_data.get("organismo", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Código REUP",
                            name="codigo_reup",
                            default_value=CommercialClientsState.edit_form_data.get("codigo_reup", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                            max_length=4,
                        ),
                        rx.input(
                            placeholder="Representante",
                            name="representante",
                            default_value=CommercialClientsState.edit_form_data.get("representante", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Dirección",
                            name="direccion",
                            default_value=CommercialClientsState.edit_form_data.get("direccion", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Teléfono",
                            name="telefono",
                            default_value=CommercialClientsState.edit_form_data.get("telefono", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Correo Electrónico",
                            name="correo_electronico",
                            default_value=CommercialClientsState.edit_form_data.get("correo_electronico", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.vstack(
                            rx.dialog.close(
                                rx.button(
                                    "Cancelar",
                                    type="button",
                                    variant="soft",
                                    color_scheme="gray",
                                    on_click=CommercialClientsState.close_edit_dialog,
                                    style={"background": "#f1f5f9", "color": "#1e293b"},
                                )
                            ),
                            rx.button(
                                "Guardar",
                                type="submit",
                                color_scheme="green",
                                style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                            ),
                            spacing="3",
                            justify="end",
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    on_submit=CommercialClientsState.submit_client,
                    reset_on_submit=True,
                ),
                max_width="500px",
                style={"background": "white", "color": "#1e293b"},
            ),
            open=rx.cond(
                CommercialClientsState.show_edit_dialog,
                True,
                rx.cond(CommercialClientsState.show_add_dialog, True, False),
            ),
            on_open_change=CommercialClientsState.on_dialog_open_change,
            background="black",
        )

    def delete_client_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title("Confirmar Eliminación", color="#1e293b"),
                rx.dialog.description(
                    "¿Estás seguro de que deseas eliminar los clientes seleccionados?",
                    color="#475569",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            type="button",
                            variant="soft",
                            color_scheme="gray",
                            on_click=CommercialClientsState.close_delete_dialog,
                            style={"background": "#f1f5f9", "color": "#1e293b"},
                        )
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Eliminar",
                            type="button",
                            color_scheme="red",
                            on_click=CommercialClientsState.delete_selected,
                            style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
                        )
                    ),
                    spacing="3",
                    justify="end",
                ),
                max_width="400px",
                style={"background": "white"},
            ),
            open=CommercialClientsState.show_delete_dialog,
            on_open_change=CommercialClientsState.set_show_delete_dialog,
        )

    # -------------------- Diálogos para Contratos con Clientes --------------------
    def add_edit_contract_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title(
                    rx.cond(
                        CommercialContractsState.edit_form_data.get("id"),
                        "Editar Contrato",
                        "Nuevo Contrato",
                    ),
                    color="#1e293b",
                ),
                rx.form(
                    rx.vstack(
                        rx.vstack(
                            rx.text("Cliente *", size="2", color="#1e293b", width="100%"),
                            rx.box(
                                rx.input(
                                    placeholder="Escribe para buscar cliente...",
                                    value=CommercialContractsState.client_search_text,
                                    on_change=CommercialContractsState.update_client_search,
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                    placeholder_color="#94a3b8",
                                ),
                                rx.cond(
                                    (CommercialContractsState.filtered_clients.length() > 0) & (CommercialContractsState.client_search_text != ""),
                                    rx.box(
                                        rx.vstack(
                                            rx.foreach(
                                                CommercialContractsState.filtered_clients,
                                                lambda c: rx.button(
                                                    c.get("nombre_cliente", ""),
                                                    on_click=lambda: CommercialContractsState.select_client(c),
                                                    width="100%",
                                                    justify="start",
                                                    variant="soft",
                                                    size="1",
                                                    style={
                                                        "background": "#f8fafc",
                                                        "color": "#1e293b",
                                                        "_hover": {"background": "#e2e8f0"},
                                                        "border_radius": "0",
                                                        "padding": "0.5rem 1rem",
                                                        "text_align": "left",
                                                    }
                                                )
                                            ),
                                            spacing="0",
                                            width="100%",
                                        ),
                                        position="absolute",
                                        top="100%",
                                        left="0",
                                        right="0",
                                        background="white",
                                        border="1px solid #e2e8f0",
                                        border_radius="0 0 8px 8px",
                                        box_shadow="md",
                                        z_index="1000",
                                        max_height="200px",
                                        overflow_y="auto",
                                        overflow_x="hidden",
                                        width="100%",
                                    ),
                                ),
                                position="relative",
                                width="100%",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Objeto del Contrato *", size="2", color="#1e293b", width="100%"),
                            rx.input(
                                placeholder="Ej: Suministro de materiales",
                                name="objeto",
                                default_value=CommercialContractsState.edit_form_data.get("objeto", ""),
                                required=True,
                                width="100%",
                                background="gray",
                                color="#1e293b",
                                border="1px solid #e2e8f0",
                                placeholder_color="#94a3b8",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Fecha a Firma *", size="2", color="#1e293b", width="100%"),
                            rx.hstack(
                                rx.input(
                                    placeholder="Seleccionar fecha",
                                    name="fecha_a_firma",
                                    type="date",
                                    default_value=CommercialContractsState.edit_form_data.get("fecha_a_firma", ""),
                                    required=True,
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                    placeholder_color="#94a3b8",
                                ),
                                rx.icon("calendar", color="#64748b"),
                                spacing="1",
                                width="100%",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        rx.hstack(
                            rx.vstack(
                                rx.text("Importe CUP", size="2", color="#1e293b", width="100%"),
                                rx.input(
                                    placeholder="0.00",
                                    name="importe_cup",
                                    type="number",
                                    default_value=CommercialContractsState.edit_form_data.get("importe_cup", "0"),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                    placeholder_color="#94a3b8",
                                ),
                                width="100%",
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.text("Importe MLC/USD", size="2", color="#1e293b", width="100%"),
                                rx.input(
                                    placeholder="0.00",
                                    name="importe_mlc",
                                    type="number",
                                    default_value=CommercialContractsState.edit_form_data.get("importe_mlc", "0"),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                    placeholder_color="#94a3b8",
                                ),
                                width="100%",
                                spacing="1",
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        rx.hstack(
                            rx.vstack(
                                rx.text("Ejecución CUP", size="2", color="#1e293b", width="100%"),
                                rx.input(
                                    placeholder="0.00",
                                    name="ejecucion_cup",
                                    type="number",
                                    default_value=CommercialContractsState.edit_form_data.get("ejecucion_cup", "0"),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                    placeholder_color="#94a3b8",
                                ),
                                width="100%",
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.text("Ejecución MLC/USD", size="2", color="#1e293b", width="100%"),
                                rx.input(
                                    placeholder="0.00",
                                    name="ejecucion_mlc",
                                    type="number",
                                    default_value=CommercialContractsState.edit_form_data.get("ejecucion_mlc", "0"),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                    placeholder_color="#94a3b8",
                                ),
                                width="100%",
                                spacing="1",
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        rx.hstack(
                            rx.vstack(
                                rx.text("Promedio Mensual", size="2", color="#1e293b", width="100%"),
                                rx.input(
                                    placeholder="0.00",
                                    name="promedio_mensual",
                                    type="number",
                                    default_value=CommercialContractsState.edit_form_data.get("promedio_mensual", "0"),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                    placeholder_color="#94a3b8",
                                ),
                                width="100%",
                                spacing="1",
                            ),
                            rx.vstack(
                                rx.text("Vigencia (opcional)", size="2", color="#1e293b", width="100%"),
                                rx.input(
                                    placeholder="Ej: 12 meses",
                                    name="vigencia",
                                    default_value=CommercialContractsState.edit_form_data.get("vigencia", ""),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                    placeholder_color="#94a3b8",
                                ),
                                width="100%",
                                spacing="1",
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Fecha Firmado", size="2", color="#1e293b", width="100%"),
                            rx.hstack(
                                rx.input(
                                    placeholder="Seleccionar fecha (opcional)",
                                    name="fecha_firmado",
                                    type="date",
                                    default_value=CommercialContractsState.edit_form_data.get("fecha_firmado", ""),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                    placeholder_color="#94a3b8",
                                ),
                                rx.icon("calendar", color="#64748b"),
                                spacing="1",
                                width="100%",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Observaciones", size="2", color="#1e293b", width="100%"),
                            rx.text_area(
                                placeholder="Notas adicionales (opcional)",
                                name="observaciones",
                                default_value=CommercialContractsState.edit_form_data.get("observaciones", ""),
                                width="100%",
                                background="gray",
                                color="#1e293b",
                                border="1px solid #e2e8f0",
                                placeholder_color="#94a3b8",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        rx.hstack(
                            rx.dialog.close(
                                rx.button(
                                    "Cancelar",
                                    type="button",
                                    variant="soft",
                                    color_scheme="gray",
                                    on_click=CommercialContractsState.close_edit_dialog,
                                    style={"background": "#f1f5f9", "color": "#1e293b"},
                                )
                            ),
                            rx.button(
                                "Guardar",
                                type="submit",
                                color_scheme="green",
                                style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                            ),
                            spacing="3",
                            justify="end",
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    on_submit=CommercialContractsState.submit_contract,
                    reset_on_submit=True,
                ),
                max_width="600px",
                style={"background": "white", "color": "#1e293b"},
            ),
            open=rx.cond(
                CommercialContractsState.show_edit_dialog,
                True,
                rx.cond(CommercialContractsState.show_add_dialog, True, False),
            ),
            on_open_change=CommercialContractsState.on_dialog_open_change,
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

    def delete_contract_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title("Confirmar Eliminación", color="#1e293b"),
                rx.dialog.description(
                    "¿Estás seguro de que deseas eliminar los contratos seleccionados?",
                    color="#475569",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            type="button",
                            variant="soft",
                            color_scheme="gray",
                            on_click=CommercialContractsState.close_delete_dialog,
                            style={"background": "#f1f5f9", "color": "#1e293b"},
                        )
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Eliminar",
                            type="button",
                            color_scheme="red",
                            on_click=CommercialContractsState.delete_selected,
                            style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
                        )
                    ),
                    spacing="3",
                    justify="end",
                ),
                max_width="400px",
                style={"background": "white"},
            ),
            open=CommercialContractsState.show_delete_dialog,
            on_open_change=CommercialContractsState.set_show_delete_dialog,
        )

    def supplement_confirm_dialog():
        return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Confirmar adición de suplemento", color="#1e293b"),
                rx.dialog.description(
                    "¿Estás seguro de que deseas agregar un suplemento a este contrato? "
                    "El número del contrato se actualizará al siguiente consecutivo (ej. 01-1/2026, 01-2/2026...).",
                    color="#475569",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            type="button",
                            variant="soft",
                            color_scheme="gray",
                            on_click=CommercialContractsState.close_supplement_confirm,
                            style={"background": "#f1f5f9", "color": "#1e293b"},
                        )
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Aceptar",
                            type="button",
                            color_scheme="green",
                            on_click=CommercialContractsState.confirm_add_supplement,
                            style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                        )
                    ),
                    spacing="3",
                    justify="end",
                ),
                max_width="400px",
                style={"background": "white"},
            ),
            open=CommercialContractsState.show_supplement_confirm,
            on_open_change=CommercialContractsState.set_show_supplement_confirm,
        )

    # -------------------- Diálogos para Proveedores Generales --------------------
    def add_edit_supplier_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title(
                    rx.cond(
                        CommercialSuppliersState.edit_form_data.get("id"),
                        "Editar Proveedor",
                        "Nuevo Proveedor",
                    ),
                    color="#1e293b",
                ),
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Nombre del Proveedor *",
                            name="nombre_proveedor",
                            default_value=CommercialSuppliersState.edit_form_data.get("nombre_proveedor", ""),
                            required=True,
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Objeto Social",
                            name="objeto_social",
                            default_value=CommercialSuppliersState.edit_form_data.get("objeto_social", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Organismo",
                            name="organismo",
                            default_value=CommercialSuppliersState.edit_form_data.get("organismo", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Código REUP",
                            name="codigo_reup",
                            default_value=CommercialSuppliersState.edit_form_data.get("codigo_reup", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                            max_length=4,
                        ),
                        rx.input(
                            placeholder="Representante",
                            name="representante",
                            default_value=CommercialSuppliersState.edit_form_data.get("representante", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Dirección",
                            name="direccion",
                            default_value=CommercialSuppliersState.edit_form_data.get("direccion", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Teléfono",
                            name="telefono",
                            default_value=CommercialSuppliersState.edit_form_data.get("telefono", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Correo Electrónico",
                            name="correo_electronico",
                            default_value=CommercialSuppliersState.edit_form_data.get("correo_electronico", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.vstack(
                            rx.dialog.close(
                                rx.button(
                                    "Cancelar",
                                    type="button",
                                    variant="soft",
                                    color_scheme="gray",
                                    on_click=CommercialSuppliersState.close_edit_dialog,
                                    style={"background": "#f1f5f9", "color": "#1e293b"},
                                )
                            ),
                            rx.button(
                                "Guardar",
                                type="submit",
                                color_scheme="green",
                                style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                            ),
                            spacing="3",
                            justify="end",
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    on_submit=CommercialSuppliersState.submit_supplier,
                    reset_on_submit=True,
                ),
                max_width="500px",
                style={"background": "white", "color": "#1e293b"},
            ),
            open=rx.cond(
                CommercialSuppliersState.show_edit_dialog,
                True,
                rx.cond(CommercialSuppliersState.show_add_dialog, True, False),
            ),
            on_open_change=CommercialSuppliersState.on_dialog_open_change,
            background="black",
        )

    def delete_supplier_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title("Confirmar Eliminación", color="#1e293b"),
                rx.dialog.description(
                    "¿Estás seguro de que deseas eliminar los proveedores seleccionados?",
                    color="#475569",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            type="button",
                            variant="soft",
                            color_scheme="gray",
                            on_click=CommercialSuppliersState.close_delete_dialog,
                            style={"background": "#f1f5f9", "color": "#1e293b"},
                        )
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Eliminar",
                            type="button",
                            color_scheme="red",
                            on_click=CommercialSuppliersState.delete_selected,
                            style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
                        )
                    ),
                    spacing="3",
                    justify="end",
                ),
                max_width="400px",
                style={"background": "white"},
            ),
            open=CommercialSuppliersState.show_delete_dialog,
            on_open_change=CommercialSuppliersState.set_show_delete_dialog,
        )

    # -------------------- Diálogos para Contratos con Proveedores (con autocompletado) --------------------
    def add_edit_supplier_contract_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title(
                    rx.cond(
                        CommercialSupplierContractsState.edit_form_data.get("id"),
                        "Editar Contrato con Proveedor",
                        "Nuevo Contrato con Proveedor",
                    ),
                    color="#1e293b",
                ),
                rx.form(
                    rx.vstack(
                        # Número de contrato
                        rx.vstack(
                            rx.text("N° Contrato *", size="2", color="#1e293b", width="100%"),
                            rx.input(
                                placeholder="Ej: PROV-2026-001",
                                name="contract_number",
                                default_value=CommercialSupplierContractsState.edit_form_data.get("contract_number", ""),
                                required=True,
                                width="100%",
                                background="gray",
                                color="#1e293b",
                                border="1px solid #e2e8f0",
                                placeholder_color="#94a3b8",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Proveedor con autocompletado
                        rx.vstack(
                            rx.text("Proveedor *", size="2", color="#1e293b", width="100%"),
                            rx.box(
                                rx.input(
                                    placeholder="Escribe para buscar proveedor...",
                                    value=CommercialSupplierContractsState.supplier_search_text,
                                    on_change=CommercialSupplierContractsState.update_supplier_search,
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                    placeholder_color="#94a3b8",
                                ),
                                rx.cond(
                                    (CommercialSupplierContractsState.filtered_suppliers.length() > 0) & (CommercialSupplierContractsState.supplier_search_text != ""),
                                    rx.box(
                                        rx.vstack(
                                            rx.foreach(
                                                CommercialSupplierContractsState.filtered_suppliers,
                                                lambda s: rx.button(
                                                    s.get("nombre_proveedor", ""),
                                                    on_click=lambda: CommercialSupplierContractsState.select_supplier(s),
                                                    width="100%",
                                                    justify="start",
                                                    variant="soft",
                                                    size="1",
                                                    style={
                                                        "background": "#f8fafc",
                                                        "color": "#1e293b",
                                                        "_hover": {"background": "#e2e8f0"},
                                                        "border_radius": "0",
                                                        "padding": "0.5rem 1rem",
                                                        "text_align": "left",
                                                    }
                                                )
                                            ),
                                            spacing="0",
                                            width="100%",
                                        ),
                                        position="absolute",
                                        top="100%",
                                        left="0",
                                        right="0",
                                        background="white",
                                        border="1px solid #e2e8f0",
                                        border_radius="0 0 8px 8px",
                                        box_shadow="md",
                                        z_index="1000",
                                        max_height="200px",
                                        overflow_y="auto",
                                        overflow_x="hidden",
                                        width="100%",
                                    ),
                                ),
                                position="relative",
                                width="100%",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Tipo de Contrato y Objeto
                        rx.vstack(
                            rx.text("Tipo de Contrato y Objeto", size="2", color="#1e293b", width="100%"),
                            rx.input(
                                placeholder="Ej: Suministro de materiales",
                                name="contract_type_object",
                                default_value=CommercialSupplierContractsState.edit_form_data.get("contract_type_object", ""),
                                width="100%",
                                background="gray",
                                color="#1e293b",
                                border="1px solid #e2e8f0",
                                placeholder_color="#94a3b8",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Valor
                        rx.vstack(
                            rx.text("Valor", size="2", color="#1e293b", width="100%"),
                            rx.input(
                                placeholder="0.00",
                                name="value",
                                type="number",
                                default_value=CommercialSupplierContractsState.edit_form_data.get("value", "0"),
                                width="100%",
                                background="gray",
                                color="#1e293b",
                                border="1px solid #e2e8f0",
                                placeholder_color="#94a3b8",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Fecha de inicio
                        rx.vstack(
                            rx.text("Fecha de Inicio", size="2", color="#1e293b", width="100%"),
                            rx.hstack(
                                rx.input(
                                    placeholder="Seleccionar fecha",
                                    name="start_date",
                                    type="date",
                                    default_value=CommercialSupplierContractsState.edit_form_data.get("start_date", ""),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                    placeholder_color="#94a3b8",
                                ),
                                rx.icon("calendar", color="#64748b"),
                                spacing="1",
                                width="100%",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Vigencia
                        rx.vstack(
                            rx.text("Vigencia (opcional)", size="2", color="#1e293b", width="100%"),
                            rx.input(
                                placeholder="Ej: 12 meses",
                                name="validity",
                                default_value=CommercialSupplierContractsState.edit_form_data.get("validity", ""),
                                width="100%",
                                background="gray",
                                color="#1e293b",
                                border="1px solid #e2e8f0",
                                placeholder_color="#94a3b8",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Fecha de terminación (solo lectura)
                        rx.vstack(
                            rx.text("Fecha de Terminación", size="2", color="#1e293b", width="100%"),
                            rx.input(
                                placeholder="Se calculará automáticamente",
                                value=CommercialSupplierContractsState.edit_form_data.get("end_date", ""),
                                disabled=True,
                                width="100%",
                                background="gray",
                                color="#64748b",
                                border="1px solid #e2e8f0",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Observaciones
                        rx.vstack(
                            rx.text("Observaciones", size="2", color="#1e293b", width="100%"),
                            rx.text_area(
                                placeholder="Notas adicionales (opcional)",
                                name="observations",
                                default_value=CommercialSupplierContractsState.edit_form_data.get("observations", ""),
                                width="100%",
                                background="gray",
                                color="#1e293b",
                                border="1px solid #e2e8f0",
                                placeholder_color="#94a3b8",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Botones
                        rx.hstack(
                            rx.dialog.close(
                                rx.button(
                                    "Cancelar",
                                    type="button",
                                    variant="soft",
                                    color_scheme="gray",
                                    on_click=CommercialSupplierContractsState.close_edit_dialog,
                                    style={"background": "#f1f5f9", "color": "#1e293b"},
                                )
                            ),
                            rx.button(
                                "Guardar",
                                type="submit",
                                color_scheme="green",
                                style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                            ),
                            spacing="3",
                            justify="end",
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    on_submit=CommercialSupplierContractsState.submit_contract,
                    reset_on_submit=True,
                ),
                max_width="600px",
                style={"background": "white", "color": "#1e293b"},
            ),
            open=rx.cond(
                CommercialSupplierContractsState.show_edit_dialog,
                True,
                rx.cond(CommercialSupplierContractsState.show_add_dialog, True, False),
            ),
            on_open_change=CommercialSupplierContractsState.on_dialog_open_change,
        )

    def delete_supplier_contract_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title("Confirmar Eliminación", color="#1e293b"),
                rx.dialog.description(
                    "¿Estás seguro de que deseas eliminar los contratos seleccionados?",
                    color="#475569",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            type="button",
                            variant="soft",
                            color_scheme="gray",
                            on_click=CommercialSupplierContractsState.close_delete_dialog,
                            style={"background": "#f1f5f9", "color": "#1e293b"},
                        )
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Eliminar",
                            type="button",
                            color_scheme="red",
                            on_click=CommercialSupplierContractsState.delete_selected,
                            style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
                        )
                    ),
                    spacing="3",
                    justify="end",
                ),
                max_width="400px",
                style={"background": "white"},
            ),
            open=CommercialSupplierContractsState.show_delete_dialog,
            on_open_change=CommercialSupplierContractsState.set_show_delete_dialog,
        )

    # -------------------- Diálogos para Proveedores de Arrendamiento --------------------
    def add_edit_leasing_supplier_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title(
                    rx.cond(
                        CommercialLeasingSuppliersState.edit_form_data.get("id"),
                        "Editar Proveedor de Arrendamiento",
                        "Nuevo Proveedor de Arrendamiento",
                    ),
                    color="#1e293b",
                ),
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Nombre del Proveedor *",
                            name="nombre_proveedor",
                            default_value=CommercialLeasingSuppliersState.edit_form_data.get("nombre_proveedor", ""),
                            required=True,
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Objeto Social",
                            name="objeto_social",
                            default_value=CommercialLeasingSuppliersState.edit_form_data.get("objeto_social", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Organismo",
                            name="organismo",
                            default_value=CommercialLeasingSuppliersState.edit_form_data.get("organismo", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Código REUP",
                            name="codigo_reup",
                            default_value=CommercialLeasingSuppliersState.edit_form_data.get("codigo_reup", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                            max_length=4,
                        ),
                        rx.input(
                            placeholder="Representante",
                            name="representante",
                            default_value=CommercialLeasingSuppliersState.edit_form_data.get("representante", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Dirección",
                            name="direccion",
                            default_value=CommercialLeasingSuppliersState.edit_form_data.get("direccion", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Teléfono",
                            name="telefono",
                            default_value=CommercialLeasingSuppliersState.edit_form_data.get("telefono", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Correo Electrónico",
                            name="correo_electronico",
                            default_value=CommercialLeasingSuppliersState.edit_form_data.get("correo_electronico", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.vstack(
                            rx.dialog.close(
                                rx.button(
                                    "Cancelar",
                                    type="button",
                                    variant="soft",
                                    color_scheme="gray",
                                    on_click=CommercialLeasingSuppliersState.close_edit_dialog,
                                    style={"background": "#f1f5f9", "color": "#1e293b"},
                                )
                            ),
                            rx.button(
                                "Guardar",
                                type="submit",
                                color_scheme="green",
                                style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                            ),
                            spacing="3",
                            justify="end",
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    on_submit=CommercialLeasingSuppliersState.submit_supplier,
                    reset_on_submit=True,
                ),
                max_width="500px",
                style={"background": "white", "color": "#1e293b"},
            ),
            open=rx.cond(
                CommercialLeasingSuppliersState.show_edit_dialog,
                True,
                rx.cond(CommercialLeasingSuppliersState.show_add_dialog, True, False),
            ),
            on_open_change=CommercialLeasingSuppliersState.on_dialog_open_change,
            background="black",
        )

    def delete_leasing_supplier_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title("Confirmar Eliminación", color="#1e293b"),
                rx.dialog.description(
                    "¿Estás seguro de que deseas eliminar los proveedores de arrendamiento seleccionados?",
                    color="#475569",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            type="button",
                            variant="soft",
                            color_scheme="gray",
                            on_click=CommercialLeasingSuppliersState.close_delete_dialog,
                            style={"background": "#f1f5f9", "color": "#1e293b"},
                        )
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Eliminar",
                            type="button",
                            color_scheme="red",
                            on_click=CommercialLeasingSuppliersState.delete_selected,
                            style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
                        )
                    ),
                    spacing="3",
                    justify="end",
                ),
                max_width="400px",
                style={"background": "white"},
            ),
            open=CommercialLeasingSuppliersState.show_delete_dialog,
            on_open_change=CommercialLeasingSuppliersState.set_show_delete_dialog,
        )

    # -------------------- Diálogos para Contratos de Arrendamiento (con autocompletado) --------------------
    def add_edit_lease_contract_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title(
                    rx.cond(
                        CommercialLeaseContractsState.edit_form_data.get("id"),
                        "Editar Contrato de Arrendamiento",
                        "Nuevo Contrato de Arrendamiento",
                    ),
                    color="#1e293b",
                ),
                rx.form(
                    rx.vstack(
                        # Proveedor con autocompletado
                        rx.vstack(
                            rx.text("Proveedor *", size="2", color="#1e293b", width="100%"),
                            rx.box(
                                rx.input(
                                    placeholder="Escribe para buscar proveedor...",
                                    value=CommercialLeaseContractsState.supplier_search_text,
                                    on_change=CommercialLeaseContractsState.update_supplier_search,
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                    placeholder_color="#94a3b8",
                                ),
                                rx.cond(
                                    (CommercialLeaseContractsState.filtered_suppliers.length() > 0) & (CommercialLeaseContractsState.supplier_search_text != ""),
                                    rx.box(
                                        rx.vstack(
                                            rx.foreach(
                                                CommercialLeaseContractsState.filtered_suppliers,
                                                lambda s: rx.button(
                                                    s.get("nombre_proveedor", ""),
                                                    on_click=lambda: CommercialLeaseContractsState.select_supplier(s),
                                                    width="100%",
                                                    justify="start",
                                                    variant="soft",
                                                    size="1",
                                                    style={
                                                        "background": "#f8fafc",
                                                        "color": "#1e293b",
                                                        "_hover": {"background": "#e2e8f0"},
                                                        "border_radius": "0",
                                                        "padding": "0.5rem 1rem",
                                                        "text_align": "left",
                                                    }
                                                )
                                            ),
                                            spacing="0",
                                            width="100%",
                                        ),
                                        position="absolute",
                                        top="100%",
                                        left="0",
                                        right="0",
                                        background="white",
                                        border="1px solid #e2e8f0",
                                        border_radius="0 0 8px 8px",
                                        box_shadow="md",
                                        z_index="1000",
                                        max_height="200px",
                                        overflow_y="auto",
                                        overflow_x="hidden",
                                        width="100%",
                                    ),
                                ),
                                position="relative",
                                width="100%",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Tipo de Contrato
                        rx.vstack(
                            rx.text("Tipo de Contrato", size="2", color="#1e293b", width="100%"),
                            rx.input(
                                placeholder="Ej: Alquiler de local",
                                name="tipo_contrato",
                                default_value=CommercialLeaseContractsState.edit_form_data.get("tipo_contrato", ""),
                                width="100%",
                                background="gray",
                                color="#1e293b",
                                border="1px solid #e2e8f0",
                                placeholder_color="#94a3b8",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Valor
                        rx.vstack(
                            rx.text("Valor", size="2", color="#1e293b", width="100%"),
                            rx.input(
                                placeholder="0.00",
                                name="valor",
                                type="number",
                                default_value=CommercialLeaseContractsState.edit_form_data.get("valor", "0"),
                                width="100%",
                                background="gray",
                                color="#1e293b",
                                border="1px solid #e2e8f0",
                                placeholder_color="#94a3b8",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Vigencia
                        rx.vstack(
                            rx.text("Vigencia", size="2", color="#1e293b", width="100%"),
                            rx.input(
                                placeholder="Ej: 12 meses",
                                name="vigencia",
                                default_value=CommercialLeaseContractsState.edit_form_data.get("vigencia", ""),
                                width="100%",
                                background="gray",
                                color="#1e293b",
                                border="1px solid #e2e8f0",
                                placeholder_color="#94a3b8",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Fecha de inicio
                        rx.vstack(
                            rx.text("Fecha de Inicio", size="2", color="#1e293b", width="100%"),
                            rx.hstack(
                                rx.input(
                                    placeholder="Seleccionar fecha",
                                    name="fecha_inicio",
                                    type="date",
                                    default_value=CommercialLeaseContractsState.edit_form_data.get("fecha_inicio", ""),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                    placeholder_color="#94a3b8",
                                ),
                                rx.icon("calendar", color="#64748b"),
                                spacing="1",
                                width="100%",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Fecha de terminación (solo lectura)
                        rx.vstack(
                            rx.text("Fecha de Terminación", size="2", color="#1e293b", width="100%"),
                            rx.input(
                                placeholder="Se calculará automáticamente",
                                value=CommercialLeaseContractsState.edit_form_data.get("fecha_terminacion", ""),
                                disabled=True,
                                width="100%",
                                background="gray",
                                color="#64748b",
                                border="1px solid #e2e8f0",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Observación
                        rx.vstack(
                            rx.text("Observación", size="2", color="#1e293b", width="100%"),
                            rx.text_area(
                                placeholder="Notas adicionales (opcional)",
                                name="observacion",
                                default_value=CommercialLeaseContractsState.edit_form_data.get("observacion", ""),
                                width="100%",
                                background="gray",
                                color="#1e293b",
                                border="1px solid #e2e8f0",
                                placeholder_color="#94a3b8",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Botones
                        rx.hstack(
                            rx.dialog.close(
                                rx.button(
                                    "Cancelar",
                                    type="button",
                                    variant="soft",
                                    color_scheme="gray",
                                    on_click=CommercialLeaseContractsState.close_edit_dialog,
                                    style={"background": "#f1f5f9", "color": "#1e293b"},
                                )
                            ),
                            rx.button(
                                "Guardar",
                                type="submit",
                                color_scheme="green",
                                style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                            ),
                            spacing="3",
                            justify="end",
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    on_submit=CommercialLeaseContractsState.submit_contract,
                    reset_on_submit=True,
                ),
                max_width="600px",
                style={"background": "white", "color": "#1e293b"},
            ),
            open=rx.cond(
                CommercialLeaseContractsState.show_edit_dialog,
                True,
                rx.cond(CommercialLeaseContractsState.show_add_dialog, True, False),
            ),
            on_open_change=CommercialLeaseContractsState.on_dialog_open_change,
        )

    def delete_lease_contract_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title("Confirmar Eliminación", color="#1e293b"),
                rx.dialog.description(
                    "¿Estás seguro de que deseas eliminar los contratos de arrendamiento seleccionados?",
                    color="#475569",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            type="button",
                            variant="soft",
                            color_scheme="gray",
                            on_click=CommercialLeaseContractsState.close_delete_dialog,
                            style={"background": "#f1f5f9", "color": "#1e293b"},
                        )
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Eliminar",
                            type="button",
                            color_scheme="red",
                            on_click=CommercialLeaseContractsState.delete_selected,
                            style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
                        )
                    ),
                    spacing="3",
                    justify="end",
                ),
                max_width="400px",
                style={"background": "white"},
            ),
            open=CommercialLeaseContractsState.show_delete_dialog,
            on_open_change=CommercialLeaseContractsState.set_show_delete_dialog,
        )

    # -------------------- Diálogos para Proveedores de Adhesión --------------------
    def add_edit_adhesion_supplier_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title(
                    rx.cond(
                        CommercialAdhesionSuppliersState.edit_form_data.get("id"),
                        "Editar Proveedor de Adhesión",
                        "Nuevo Proveedor de Adhesión",
                    ),
                    color="#1e293b",
                ),
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Nombre del Proveedor *",
                            name="nombre_proveedor",
                            default_value=CommercialAdhesionSuppliersState.edit_form_data.get("nombre_proveedor", ""),
                            required=True,
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Objeto Social",
                            name="objeto_social",
                            default_value=CommercialAdhesionSuppliersState.edit_form_data.get("objeto_social", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Organismo",
                            name="organismo",
                            default_value=CommercialAdhesionSuppliersState.edit_form_data.get("organismo", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Código REUP",
                            name="codigo_reup",
                            default_value=CommercialAdhesionSuppliersState.edit_form_data.get("codigo_reup", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                            max_length=4,
                        ),
                        rx.input(
                            placeholder="Representante",
                            name="representante",
                            default_value=CommercialAdhesionSuppliersState.edit_form_data.get("representante", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Dirección",
                            name="direccion",
                            default_value=CommercialAdhesionSuppliersState.edit_form_data.get("direccion", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Teléfono",
                            name="telefono",
                            default_value=CommercialAdhesionSuppliersState.edit_form_data.get("telefono", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.input(
                            placeholder="Correo Electrónico",
                            name="correo_electronico",
                            default_value=CommercialAdhesionSuppliersState.edit_form_data.get("correo_electronico", ""),
                            width="100%",
                            background="gray",
                            color="#1e293b",
                            border="1px solid #e2e8f0",
                            placeholder_color="#94a3b8",
                        ),
                        rx.vstack(
                            rx.dialog.close(
                                rx.button(
                                    "Cancelar",
                                    type="button",
                                    variant="soft",
                                    color_scheme="gray",
                                    on_click=CommercialAdhesionSuppliersState.close_edit_dialog,
                                    style={"background": "#f1f5f9", "color": "#1e293b"},
                                )
                            ),
                            rx.button(
                                "Guardar",
                                type="submit",
                                color_scheme="green",
                                style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                            ),
                            spacing="3",
                            justify="end",
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    on_submit=CommercialAdhesionSuppliersState.submit_supplier,
                    reset_on_submit=True,
                ),
                max_width="500px",
                style={"background": "white", "color": "#1e293b"},
            ),
            open=rx.cond(
                CommercialAdhesionSuppliersState.show_edit_dialog,
                True,
                rx.cond(CommercialAdhesionSuppliersState.show_add_dialog, True, False),
            ),
            on_open_change=CommercialAdhesionSuppliersState.on_dialog_open_change,
            background="black",
        )

    def delete_adhesion_supplier_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title("Confirmar Eliminación", color="#1e293b"),
                rx.dialog.description(
                    "¿Estás seguro de que deseas eliminar los proveedores de adhesión seleccionados?",
                    color="#475569",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            type="button",
                            variant="soft",
                            color_scheme="gray",
                            on_click=CommercialAdhesionSuppliersState.close_delete_dialog,
                            style={"background": "#f1f5f9", "color": "#1e293b"},
                        )
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Eliminar",
                            type="button",
                            color_scheme="red",
                            on_click=CommercialAdhesionSuppliersState.delete_selected,
                            style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
                        )
                    ),
                    spacing="3",
                    justify="end",
                ),
                max_width="400px",
                style={"background": "white"},
            ),
            open=CommercialAdhesionSuppliersState.show_delete_dialog,
            on_open_change=CommercialAdhesionSuppliersState.set_show_delete_dialog,
        )

    # -------------------- Diálogos para Contratos de Adhesión (con autocompletado) --------------------
    def add_edit_adhesion_contract_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title(
                    rx.cond(
                        CommercialAdhesionContractsState.edit_form_data.get("id"),
                        "Editar Contrato de Adhesión",
                        "Nuevo Contrato de Adhesión",
                    ),
                    color="#1e293b",
                ),
                rx.form(
                    rx.vstack(
                        # Proveedor con autocompletado
                        rx.vstack(
                            rx.text("Proveedor *", size="2", color="#1e293b", width="100%"),
                            rx.box(
                                rx.input(
                                    placeholder="Escribe para buscar proveedor...",
                                    value=CommercialAdhesionContractsState.supplier_search_text,
                                    on_change=CommercialAdhesionContractsState.update_supplier_search,
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                    placeholder_color="#94a3b8",
                                ),
                                rx.cond(
                                    (CommercialAdhesionContractsState.filtered_suppliers.length() > 0) & (CommercialAdhesionContractsState.supplier_search_text != ""),
                                    rx.box(
                                        rx.vstack(
                                            rx.foreach(
                                                CommercialAdhesionContractsState.filtered_suppliers,
                                                lambda s: rx.button(
                                                    s.get("nombre_proveedor", ""),
                                                    on_click=lambda: CommercialAdhesionContractsState.select_supplier(s),
                                                    width="100%",
                                                    justify="start",
                                                    variant="soft",
                                                    size="1",
                                                    style={
                                                        "background": "#f8fafc",
                                                        "color": "#1e293b",
                                                        "_hover": {"background": "#e2e8f0"},
                                                        "border_radius": "0",
                                                        "padding": "0.5rem 1rem",
                                                        "text_align": "left",
                                                    }
                                                )
                                            ),
                                            spacing="0",
                                            width="100%",
                                        ),
                                        position="absolute",
                                        top="100%",
                                        left="0",
                                        right="0",
                                        background="white",
                                        border="1px solid #e2e8f0",
                                        border_radius="0 0 8px 8px",
                                        box_shadow="md",
                                        z_index="1000",
                                        max_height="200px",
                                        overflow_y="auto",
                                        overflow_x="hidden",
                                        width="100%",
                                    ),
                                ),
                                position="relative",
                                width="100%",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Tipo de Contrato
                        rx.vstack(
                            rx.text("Tipo de Contrato", size="2", color="#1e293b", width="100%"),
                            rx.input(
                                placeholder="Ej: Contrato de adhesión a servicios",
                                name="tipo_contrato",
                                default_value=CommercialAdhesionContractsState.edit_form_data.get("tipo_contrato", ""),
                                width="100%",
                                background="gray",
                                color="#1e293b",
                                border="1px solid #e2e8f0",
                                placeholder_color="#94a3b8",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Valor
                        rx.vstack(
                            rx.text("Valor", size="2", color="#1e293b", width="100%"),
                            rx.input(
                                placeholder="0.00",
                                name="valor",
                                type="number",
                                default_value=CommercialAdhesionContractsState.edit_form_data.get("valor", "0"),
                                width="100%",
                                background="gray",
                                color="#1e293b",
                                border="1px solid #e2e8f0",
                                placeholder_color="#94a3b8",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Vigencia
                        rx.vstack(
                            rx.text("Vigencia", size="2", color="#1e293b", width="100%"),
                            rx.input(
                                placeholder="Ej: 12 meses",
                                name="vigencia",
                                default_value=CommercialAdhesionContractsState.edit_form_data.get("vigencia", ""),
                                width="100%",
                                background="gray",
                                color="#1e293b",
                                border="1px solid #e2e8f0",
                                placeholder_color="#94a3b8",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Fecha de inicio
                        rx.vstack(
                            rx.text("Fecha de Inicio", size="2", color="#1e293b", width="100%"),
                            rx.hstack(
                                rx.input(
                                    placeholder="Seleccionar fecha",
                                    name="fecha_inicio",
                                    type="date",
                                    default_value=CommercialAdhesionContractsState.edit_form_data.get("fecha_inicio", ""),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                    placeholder_color="#94a3b8",
                                ),
                                rx.icon("calendar", color="#64748b"),
                                spacing="1",
                                width="100%",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Fecha de terminación (solo lectura)
                        rx.vstack(
                            rx.text("Fecha de Terminación", size="2", color="#1e293b", width="100%"),
                            rx.input(
                                placeholder="Se calculará automáticamente",
                                value=CommercialAdhesionContractsState.edit_form_data.get("fecha_terminacion", ""),
                                disabled=True,
                                width="100%",
                                background="gray",
                                color="#64748b",
                                border="1px solid #e2e8f0",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Observación
                        rx.vstack(
                            rx.text("Observación", size="2", color="#1e293b", width="100%"),
                            rx.text_area(
                                placeholder="Notas adicionales (opcional)",
                                name="observacion",
                                default_value=CommercialAdhesionContractsState.edit_form_data.get("observacion", ""),
                                width="100%",
                                background="gray",
                                color="#1e293b",
                                border="1px solid #e2e8f0",
                                placeholder_color="#94a3b8",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        # Botones
                        rx.hstack(
                            rx.dialog.close(
                                rx.button(
                                    "Cancelar",
                                    type="button",
                                    variant="soft",
                                    color_scheme="gray",
                                    on_click=CommercialAdhesionContractsState.close_edit_dialog,
                                    style={"background": "#f1f5f9", "color": "#1e293b"},
                                )
                            ),
                            rx.button(
                                "Guardar",
                                type="submit",
                                color_scheme="green",
                                style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                            ),
                            spacing="3",
                            justify="end",
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    on_submit=CommercialAdhesionContractsState.submit_contract,
                    reset_on_submit=True,
                ),
                max_width="600px",
                style={"background": "white", "color": "#1e293b"},
            ),
            open=rx.cond(
                CommercialAdhesionContractsState.show_edit_dialog,
                True,
                rx.cond(CommercialAdhesionContractsState.show_add_dialog, True, False),
            ),
            on_open_change=CommercialAdhesionContractsState.on_dialog_open_change,
        )

    def delete_adhesion_contract_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title("Confirmar Eliminación", color="#1e293b"),
                rx.dialog.description(
                    "¿Estás seguro de que deseas eliminar los contratos de adhesión seleccionados?",
                    color="#475569",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            type="button",
                            variant="soft",
                            color_scheme="gray",
                            on_click=CommercialAdhesionContractsState.close_delete_dialog,
                            style={"background": "#f1f5f9", "color": "#1e293b"},
                        )
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Eliminar",
                            type="button",
                            color_scheme="red",
                            on_click=CommercialAdhesionContractsState.delete_selected,
                            style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
                        )
                    ),
                    spacing="3",
                    justify="end",
                ),
                max_width="400px",
                style={"background": "white"},
            ),
            open=CommercialAdhesionContractsState.show_delete_dialog,
            on_open_change=CommercialAdhesionContractsState.set_show_delete_dialog,
        )

    # -------------------- Funciones de las pestañas (tabs) --------------------
    def clients_tab() -> rx.Component:
        def client_row(client):
            return rx.table.row(
                rx.table.cell(
                    rx.checkbox(
                        checked=CommercialClientsState.selected_items.contains(client.get("id")),
                        on_change=lambda: CommercialClientsState.toggle_selection(client.get("id")),
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
                rx.table.cell(client.get("id", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(client.get("nombre_cliente", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(client.get("organismo", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(client.get("codigo_reup", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(client.get("telefono", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(
                    rx.button(
                        "✏️",
                        size="1",
                        on_click=lambda: CommercialClientsState.open_edit_dialog(client.get("id")),
                        style={"background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)", "color": "white"},
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
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
                    "➕ Agregar",
                    on_click=CommercialClientsState.open_add_dialog,
                    style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                ),
                rx.button(
                    "🗑️ Eliminar",
                    on_click=CommercialClientsState.open_delete_dialog,
                    disabled=CommercialClientsState.selected_items.length() == 0,
                    style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
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
                                rx.table.column_header_cell("Sel", width="50px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("ID", width="50px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Nombre", width="200px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Organismo", width="150px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("REUP", width="100px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Teléfono", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Acciones", width="80px", style={"background": "#f1f5f9", "color": "#1e293b"}),
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
            show_supplement = contract.get("fecha_firmado") is not None
            return rx.table.row(
                rx.table.cell(
                    rx.checkbox(
                        checked=CommercialContractsState.selected_items.contains(contract.get("id")),
                        on_change=lambda: CommercialContractsState.toggle_selection(contract.get("id")),
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
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
                        "➕ Suplemento",
                        size="1",
                        on_click=lambda: CommercialContractsState.open_supplement_confirm(contract.get("id")),
                        is_disabled=not show_supplement,
                        style={
                            "background": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
                            "color": "white",
                            "padding": "2px 8px",
                            "font_size": "12px"
                        }
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
                rx.table.cell(
                    rx.button(
                        "👁️ Ver",
                        size="1",
                        on_click=lambda: CommercialContractsState.open_details_dialog(contract.get("id")),
                        style={"background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)", "color": "white"},
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
                rx.table.cell(
                    rx.button(
                        "✏️",
                        size="1",
                        on_click=lambda: CommercialContractsState.open_edit_dialog(contract.get("id")),
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
                    "➕ Agregar",
                    on_click=CommercialContractsState.open_add_dialog,
                    style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                ),
                rx.button(
                    "🗑️ Eliminar",
                    on_click=CommercialContractsState.open_delete_dialog,
                    disabled=CommercialContractsState.selected_items.length() == 0,
                    style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
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
                                rx.table.column_header_cell("Sel", width="50px", style={"background": "#f1f5f9", "color": "#1e293b"}),
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
                                rx.table.column_header_cell("Suplemento", width="100px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Detalles", width="70px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Acciones", width="70px", style={"background": "#f1f5f9", "color": "#1e293b"}),
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
            width="100%",
            spacing="4",
        )

    def suppliers_tab() -> rx.Component:
        def supplier_row(supplier):
            return rx.table.row(
                rx.table.cell(
                    rx.checkbox(
                        checked=CommercialSuppliersState.selected_items.contains(supplier.get("id")),
                        on_change=lambda: CommercialSuppliersState.toggle_selection(supplier.get("id")),
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
                rx.table.cell(supplier.get("id", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("nombre_proveedor", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("organismo", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("codigo_reup", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("telefono", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(
                    rx.button(
                        "✏️",
                        size="1",
                        on_click=lambda: CommercialSuppliersState.open_edit_dialog(supplier.get("id")),
                        style={"background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)", "color": "white"},
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
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
                    "➕ Agregar",
                    on_click=CommercialSuppliersState.open_add_dialog,
                    style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                ),
                rx.button(
                    "🗑️ Eliminar",
                    on_click=CommercialSuppliersState.open_delete_dialog,
                    disabled=CommercialSuppliersState.selected_items.length() == 0,
                    style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
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
                                rx.table.column_header_cell("Sel", width="50px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("ID", width="50px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Nombre", width="200px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Organismo", width="150px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("REUP", width="100px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Teléfono", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Acciones", width="80px", style={"background": "#f1f5f9", "color": "#1e293b"}),
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
                rx.table.cell(
                    rx.checkbox(
                        checked=CommercialSupplierContractsState.selected_items.contains(contract.get("id")),
                        on_change=lambda: CommercialSupplierContractsState.toggle_selection(contract.get("id")),
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
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
                rx.table.cell(
                    rx.button(
                        "✏️",
                        size="1",
                        on_click=lambda: CommercialSupplierContractsState.open_edit_dialog(contract.get("id")),
                        style={"background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)", "color": "white"},
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
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
                    "➕ Agregar",
                    on_click=CommercialSupplierContractsState.open_add_dialog,
                    style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                ),
                rx.button(
                    "🗑️ Eliminar",
                    on_click=CommercialSupplierContractsState.open_delete_dialog,
                    disabled=CommercialSupplierContractsState.selected_items.length() == 0,
                    style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
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
                                rx.table.column_header_cell("Sel", width="50px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("N° Contrato", width="150px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Proveedor", width="200px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Tipo y Objeto", width="200px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Valor", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Fecha Inicio", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Fecha Terminación", width="140px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Vigencia", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Acciones", width="80px", style={"background": "#f1f5f9", "color": "#1e293b"}),
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
                rx.table.cell(
                    rx.checkbox(
                        checked=CommercialLeasingSuppliersState.selected_items.contains(supplier.get("id")),
                        on_change=lambda: CommercialLeasingSuppliersState.toggle_selection(supplier.get("id")),
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
                rx.table.cell(supplier.get("id", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("nombre_proveedor", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("organismo", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("codigo_reup", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("telefono", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(
                    rx.button(
                        "✏️",
                        size="1",
                        on_click=lambda: CommercialLeasingSuppliersState.open_edit_dialog(supplier.get("id")),
                        style={"background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)", "color": "white"},
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
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
                    "➕ Agregar",
                    on_click=CommercialLeasingSuppliersState.open_add_dialog,
                    style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                ),
                rx.button(
                    "🗑️ Eliminar",
                    on_click=CommercialLeasingSuppliersState.open_delete_dialog,
                    disabled=CommercialLeasingSuppliersState.selected_items.length() == 0,
                    style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
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
                                rx.table.column_header_cell("Sel", width="50px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("ID", width="50px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Nombre", width="200px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Organismo", width="150px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("REUP", width="100px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Teléfono", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Acciones", width="80px", style={"background": "#f1f5f9", "color": "#1e293b"}),
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
                rx.table.cell(
                    rx.checkbox(
                        checked=CommercialLeaseContractsState.selected_items.contains(contract.get("id")),
                        on_change=lambda: CommercialLeaseContractsState.toggle_selection(contract.get("id")),
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
                rx.table.cell(contract.get("proveedor", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("tipo_contrato", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(f"${contract.get('valor', 0):,.2f}", style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("vigencia", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("fecha_inicio", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("fecha_terminacion", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(
                    rx.button(
                        "✏️",
                        size="1",
                        on_click=lambda: CommercialLeaseContractsState.open_edit_dialog(contract.get("id")),
                        style={"background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)", "color": "white"},
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
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
                    "➕ Agregar",
                    on_click=CommercialLeaseContractsState.open_add_dialog,
                    style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                ),
                rx.button(
                    "🗑️ Eliminar",
                    on_click=CommercialLeaseContractsState.open_delete_dialog,
                    disabled=CommercialLeaseContractsState.selected_items.length() == 0,
                    style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
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
                                rx.table.column_header_cell("Sel", width="50px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Proveedor", width="200px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Tipo Contrato", width="150px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Valor", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Vigencia", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Fecha Inicio", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Fecha Terminación", width="140px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Acciones", width="80px", style={"background": "#f1f5f9", "color": "#1e293b"}),
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
                rx.table.cell(
                    rx.checkbox(
                        checked=CommercialAdhesionSuppliersState.selected_items.contains(supplier.get("id")),
                        on_change=lambda: CommercialAdhesionSuppliersState.toggle_selection(supplier.get("id")),
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
                rx.table.cell(supplier.get("id", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("nombre_proveedor", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("organismo", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("codigo_reup", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(supplier.get("telefono", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(
                    rx.button(
                        "✏️",
                        size="1",
                        on_click=lambda: CommercialAdhesionSuppliersState.open_edit_dialog(supplier.get("id")),
                        style={"background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)", "color": "white"},
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
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
                    "➕ Agregar",
                    on_click=CommercialAdhesionSuppliersState.open_add_dialog,
                    style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                ),
                rx.button(
                    "🗑️ Eliminar",
                    on_click=CommercialAdhesionSuppliersState.open_delete_dialog,
                    disabled=CommercialAdhesionSuppliersState.selected_items.length() == 0,
                    style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
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
                                rx.table.column_header_cell("Sel", width="50px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("ID", width="50px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Nombre", width="200px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Organismo", width="150px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("REUP", width="100px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Teléfono", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Acciones", width="80px", style={"background": "#f1f5f9", "color": "#1e293b"}),
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
                rx.table.cell(
                    rx.checkbox(
                        checked=CommercialAdhesionContractsState.selected_items.contains(contract.get("id")),
                        on_change=lambda: CommercialAdhesionContractsState.toggle_selection(contract.get("id")),
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
                rx.table.cell(contract.get("proveedor", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("tipo_contrato", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(f"${contract.get('valor', 0):,.2f}", style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("vigencia", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("fecha_inicio", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(contract.get("fecha_terminacion", ""), style={"padding": "12px 4px", "color": "#1e293b"}),
                rx.table.cell(
                    rx.button(
                        "✏️",
                        size="1",
                        on_click=lambda: CommercialAdhesionContractsState.open_edit_dialog(contract.get("id")),
                        style={"background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)", "color": "white"},
                    ),
                    style={"padding": "12px 4px", "text_align": "center"},
                ),
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
                    "➕ Agregar",
                    on_click=CommercialAdhesionContractsState.open_add_dialog,
                    style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                ),
                rx.button(
                    "🗑️ Eliminar",
                    on_click=CommercialAdhesionContractsState.open_delete_dialog,
                    disabled=CommercialAdhesionContractsState.selected_items.length() == 0,
                    style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
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
                                rx.table.column_header_cell("Sel", width="50px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Proveedor", width="200px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Tipo Contrato", width="150px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Valor", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Vigencia", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Fecha Inicio", width="120px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Fecha Terminación", width="140px", style={"background": "#f1f5f9", "color": "#1e293b"}),
                                rx.table.column_header_cell("Acciones", width="80px", style={"background": "#f1f5f9", "color": "#1e293b"}),
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
                            rx.text("Usuario del Área Comercial", size="4", font_weight="700", color="#1e293b"),
                            rx.text(
                                rx.cond(
                                    CommercialAuthState.current_user,
                                    f"Usuario: {CommercialAuthState.current_user.get('username', 'No disponible')}",
                                    "Usuario: No disponible"
                                ),
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
                        rx.text("📋 Permisos:", size="3", font_weight="600", color="#1e293b"),
                        rx.list(
                            rx.list.item("✓ Gestión de clientes"),
                            rx.list.item("✓ Gestión de proveedores"),
                            rx.list.item("✓ Gestión de contratos con clientes"),
                            rx.list.item("✓ Gestión de contratos con proveedores"),
                            rx.list.item("✓ Gestión de proveedores de arrendamiento"),
                            rx.list.item("✓ Gestión de contratos de arrendamiento"),
                            rx.list.item("✓ Gestión de proveedores de adhesión"),
                            rx.list.item("✓ Gestión de contratos de adhesión"),
                            rx.list.item("✓ Agregar suplementos a contratos con clientes"),
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
                            on_click=CommercialAuthState.logout,
                            color_scheme="red",
                            variant="solid",
                            size="2",
                            style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)"}
                        ),
                        rx.button(
                            "🔄 Recargar Datos",
                            on_click=lambda: [
                                CommercialClientsState.load_data(),
                                CommercialContractsState.load_data(),
                                CommercialSuppliersState.load_data(),
                                CommercialSupplierContractsState.load_data(),
                                CommercialLeasingSuppliersState.load_data(),
                                CommercialLeaseContractsState.load_data(),
                                CommercialAdhesionSuppliersState.load_data(),
                                CommercialAdhesionContractsState.load_data(),
                            ],
                            variant="soft",
                            size="2"
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
            is_active = CommercialDashboardState.active_section == section
            return rx.link(
                rx.hstack(
                    rx.icon(icon, size=20),
                    rx.cond(
                        ~CommercialDashboardState.sidebar_collapsed,
                        rx.text(label, weight="medium"),
                    ),
                    spacing="3",
                    align="center",
                ),
                on_click=lambda: CommercialDashboardState.set_active_section(section),
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
                        CommercialDashboardState.sidebar_collapsed,
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
                        ~CommercialDashboardState.sidebar_collapsed,
                        rx.heading("Área Comercial", size="5", color="#1e293b"),
                    ),
                    rx.button(
                        rx.icon("menu", size=20, color="#3D3A3D"),
                        on_click=CommercialDashboardState.toggle_sidebar,
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
                CommercialDashboardState.sidebar_collapsed,
                "80px",
                "310px"
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
                                    CommercialDashboardState.active_section == "clients", "Clientes",
                                    rx.cond(
                                        CommercialDashboardState.active_section == "contracts", "Contratos con Clientes",
                                        rx.cond(
                                            CommercialDashboardState.active_section == "suppliers", "Proveedores",
                                            rx.cond(
                                                CommercialDashboardState.active_section == "supplier_contracts", "Contratos con Proveedores",
                                                rx.cond(
                                                    CommercialDashboardState.active_section == "leasing_suppliers", "Proveedores de Arrendamiento",
                                                    rx.cond(
                                                        CommercialDashboardState.active_section == "lease_contracts", "Contratos de Arrendamiento",
                                                        rx.cond(
                                                            CommercialDashboardState.active_section == "adhesion_suppliers", "Proveedores de Adhesión",
                                                            rx.cond(
                                                                CommercialDashboardState.active_section == "adhesion_contracts", "Contratos de Adhesión",
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
                            width="100%",
                        ),
                        rx.spacer(),
                        rx.button(
                            "Cerrar Sesión",
                            on_click=CommercialAuthState.logout,
                            color_scheme="red",
                            variant="soft",
                            size="1",
                            width="25%"
                        ),
                        width="100%",
                        align="center",
                    ),
                    padding="1rem 2rem",
                    border_bottom="1px solid #e2e8f0",
                    background="white",
                    width="100%"
                ),
                rx.box(
                    rx.cond(
                        CommercialDashboardState.active_section == "clients", clients_tab(),
                        rx.cond(
                            CommercialDashboardState.active_section == "contracts", contracts_tab(),
                            rx.cond(
                                CommercialDashboardState.active_section == "suppliers", suppliers_tab(),
                                rx.cond(
                                    CommercialDashboardState.active_section == "supplier_contracts", supplier_contracts_tab(),
                                    rx.cond(
                                        CommercialDashboardState.active_section == "leasing_suppliers", leasing_suppliers_tab(),
                                        rx.cond(
                                            CommercialDashboardState.active_section == "lease_contracts", lease_contracts_tab(),
                                            rx.cond(
                                                CommercialDashboardState.active_section == "adhesion_suppliers", adhesion_suppliers_tab(),
                                                rx.cond(
                                                    CommercialDashboardState.active_section == "adhesion_contracts", adhesion_contracts_tab(),
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
                CommercialDashboardState.sidebar_collapsed,
                "80px",
                "280px"
            ),
            width=rx.cond(
                CommercialDashboardState.sidebar_collapsed,
                "calc(100% - 80px)",
                "calc(100% - 280px)"
            ),
            transition="margin-left 0.3s ease, width 0.3s ease",
        )

    # -------------------- Render final --------------------
    return rx.cond(
        CommercialAuthState.is_authenticated,
        rx.box(
            sidebar(),
            main_content(),
            # Diálogos
            add_edit_client_dialog(),
            delete_client_dialog(),
            add_edit_contract_dialog(),
            contract_details_dialog(),
            delete_contract_dialog(),
            supplement_confirm_dialog(),
            add_edit_supplier_dialog(),
            delete_supplier_dialog(),
            add_edit_supplier_contract_dialog(),
            delete_supplier_contract_dialog(),
            add_edit_leasing_supplier_dialog(),
            delete_leasing_supplier_dialog(),
            add_edit_lease_contract_dialog(),
            delete_lease_contract_dialog(),
            add_edit_adhesion_supplier_dialog(),
            delete_adhesion_supplier_dialog(),
            add_edit_adhesion_contract_dialog(),
            delete_adhesion_contract_dialog(),
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