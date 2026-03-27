#commercial_clients_state.py
import reflex as rx
import csv
import io
import json
from typing import List
from TFuerte.api.commercial_api import ClientsAPI

class CommercialClientsState(rx.State):
    # Datos
    clients_data: List[dict] = []
    filtered_data: List[dict] = []
    loading: bool = False
    selected_items: List[int] = []
    search_value: str = ""
    sort_value: str = ""

    # Paginación
    current_page: int = 1
    items_per_page: int = 10
    total_pages: int = 1
    page_numbers: List[int] = []
    paginated_data: List[dict] = []

    # Diálogos
    show_delete_dialog: bool = False
    show_edit_dialog: bool = False
    show_add_dialog: bool = False
    edit_form_data: dict = {}
    add_form_data: dict = {}

    def load_data(self):
        """Carga los datos y aplica filtros/ordenamiento."""
        self.loading = True
        yield

        data = ClientsAPI.get_all()
        if data:
            self.clients_data = data
            self.apply_filters()
            yield rx.toast.success(f"Clientes cargados: {len(data)}", position="top-right")
        else:
            self.clients_data = []
            self.filtered_data = []
            yield rx.toast.error("No se pudieron cargar clientes", position="top-right")

        self.loading = False

    def apply_filters(self):
        result = self.clients_data.copy()
        if self.search_value:
            search = self.search_value.lower()
            result = [c for c in result if search in c.get("nombre_cliente", "").lower()]
        if self.sort_value:
            result = sorted(result, key=lambda x: x.get(self.sort_value, ""))
        self.filtered_data = result
        self.reset_pagination()

    def filter_values(self, value: str):
        self.search_value = value
        self.apply_filters()

    def sort_values(self, value: str):
        self.sort_value = value
        self.apply_filters()

    def toggle_selection(self, client_id: int):
        if client_id in self.selected_items:
            self.selected_items.remove(client_id)
        else:
            self.selected_items.append(client_id)

    def clear_selection(self):
        self.selected_items = []

    # ----- CRUD -----
    def open_add_dialog(self):
        self.add_form_data = {}
        self.show_add_dialog = True

    def close_add_dialog(self):
        self.show_add_dialog = False
        self.add_form_data = {}

    def add_client(self, form_data: dict):
        required = ["nombre_cliente"]
        missing = [f for f in required if not form_data.get(f)]
        if missing:
            yield rx.toast.error(f"Faltan: {', '.join(missing)}", position="top-right")
            return

        # Validar código REUP (máximo 4 caracteres)
        codigo = form_data.get("codigo_reup", "").strip()
        if codigo and len(codigo) > 4:
            yield rx.toast.error("El código REUP no puede tener más de 4 caracteres", position="top-right")
            return

        result = ClientsAPI.insert(form_data)
        if result:
            yield from self.load_data()
            self.close_add_dialog()
            yield rx.toast.success("Cliente agregado", position="top-right")
        else:
            yield rx.toast.error("Error al agregar", position="top-right")

    def open_edit_dialog(self, client_id: int):
        client = next((c for c in self.clients_data if c["id"] == client_id), None)
        if client:
            self.edit_form_data = client.copy()
            self.show_edit_dialog = True

    def close_edit_dialog(self):
        self.show_edit_dialog = False
        self.edit_form_data = {}

    def update_client(self, form_data: dict):
        client_id = self.edit_form_data.get("id")
        if not client_id:
            yield rx.toast.error("Error: ID no encontrado", position="top-right")
            return

        # Validar código REUP (máximo 4 caracteres)
        codigo = form_data.get("codigo_reup", "").strip()
        if codigo and len(codigo) > 4:
            yield rx.toast.error("El código REUP no puede tener más de 4 caracteres", position="top-right")
            return

        result = ClientsAPI.update(client_id, form_data)
        if result:
            yield from self.load_data()
            self.close_edit_dialog()
            yield rx.toast.success("Cliente actualizado", position="top-right")
        else:
            yield rx.toast.error("Error al actualizar", position="top-right")

    def open_delete_dialog(self):
        if not self.selected_items:
            return rx.toast.error("Seleccione al menos un cliente", position="top-right")
        self.show_delete_dialog = True

    def close_delete_dialog(self):
        self.show_delete_dialog = False

    def delete_selected(self):
        if not self.selected_items:
            self.show_delete_dialog = False
            return
        success = ClientsAPI.delete(self.selected_items)
        if success:
            self.selected_items = []
            yield from self.load_data()
            self.show_delete_dialog = False
            yield rx.toast.success("Clientes eliminados", position="top-right")
        else:
            self.show_delete_dialog = False
            yield rx.toast.error("Error al eliminar", position="top-right")

    # ----- Paginación -----
    def calculate_pagination(self):
        total = len(self.filtered_data)
        self.total_pages = max(1, (total + self.items_per_page - 1) // self.items_per_page)
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        self.paginated_data = self.filtered_data[start:end]
        self.calculate_page_numbers()

    def calculate_page_numbers(self):
        max_show = 4
        total = self.total_pages
        current = self.current_page
        if total <= max_show:
            self.page_numbers = list(range(1, total + 1))
            return
        start = max(1, current - 1)
        end = min(total, start + max_show - 1)
        if end - start + 1 < max_show:
            start = max(1, end - max_show + 1)
        self.page_numbers = list(range(start, end + 1))

    def go_to_page(self, page: int):
        if 1 <= page <= self.total_pages:
            self.current_page = page
            self.calculate_pagination()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.calculate_pagination()

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.calculate_pagination()

    def reset_pagination(self):
        self.current_page = 1
        self.calculate_pagination()

    # ----- CSV -----
    def download_csv(self):
        if not self.filtered_data:
            return rx.toast.error("No hay datos para descargar", position="top-right")
        fieldnames = ["id", "nombre_cliente", "objeto_social", "organismo", "codigo_reup",
                      "representante", "direccion", "telefono", "correo_electronico"]
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(self.filtered_data)
        csv_data = output.getvalue()
        output.close()
        return rx.download(data=csv_data, filename="clientes.csv")

    def submit_client(self, form_data: dict):
        if self.edit_form_data.get("id"):
            return self.update_client(form_data)
        else:
            return self.add_client(form_data)

    def on_dialog_open_change(self, open: bool):
        if self.show_edit_dialog:
            self.show_edit_dialog = open
        elif self.show_add_dialog:
            self.show_add_dialog = open

    def update_add_form_field(self, field: str, value):
        self.add_form_data[field] = value
        self.add_form_data = self.add_form_data.copy()

    def update_edit_form_field(self, field: str, value):
        self.edit_form_data[field] = value
        self.edit_form_data = self.edit_form_data.copy()

    def set_dialog_open(self, open: bool):
        if self.show_edit_dialog:
            self.show_edit_dialog = open
        elif self.show_add_dialog:
            self.show_add_dialog = open