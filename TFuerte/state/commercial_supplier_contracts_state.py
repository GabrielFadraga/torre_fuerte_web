import reflex as rx
import csv
import io
from datetime import datetime, timedelta
from typing import List, Optional
from TFuerte.api.commercial_api import SupplierContractsAPI, SuppliersAPI

class CommercialSupplierContractsState(rx.State):
    # Datos
    contracts_data: List[dict] = []
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

    # Autocompletado de proveedores
    suppliers_list: List[dict] = []
    supplier_search_text: str = ""
    filtered_suppliers: List[dict] = []

    def load_data(self):
        self.loading = True
        yield

        # Cargar contratos
        data = SupplierContractsAPI.get_all()
        if data:
            self.contracts_data = data
        else:
            self.contracts_data = []

        # Cargar proveedores generales
        suppliers = SuppliersAPI.get_all()
        self.suppliers_list = suppliers if suppliers else []

        self.apply_filters()
        self.loading = False
        yield rx.toast.success(f"Contratos cargados: {len(data)}", position="top-right")

    def apply_filters(self):
        result = self.contracts_data.copy()
        if self.search_value:
            search = self.search_value.lower()
            result = [c for c in result if search in c.get("supplier", "").lower() or
                      search in c.get("contract_number", "").lower()]
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

    def toggle_selection(self, contract_id: int):
        if contract_id in self.selected_items:
            self.selected_items.remove(contract_id)
        else:
            self.selected_items.append(contract_id)

    def clear_selection(self):
        self.selected_items = []

    # ----- CRUD -----
    def open_add_dialog(self):
        self.add_form_data = {}
        self.supplier_search_text = ""
        self.filtered_suppliers = []
        self.show_add_dialog = True

    def close_add_dialog(self):
        self.show_add_dialog = False
        self.add_form_data = {}
        self.supplier_search_text = ""
        self.filtered_suppliers = []

    def add_contract(self, form_data: dict):
        # Usar el proveedor guardado en el estado (no del formulario)
        supplier = self.add_form_data.get("supplier")
        if not supplier:
            yield rx.toast.error("Debe seleccionar o escribir un proveedor", position="top-right")
            return

        required = ["contract_number"]
        missing = [f for f in required if not form_data.get(f)]
        if missing:
            yield rx.toast.error(f"Faltan: {', '.join(missing)}", position="top-right")
            return

        value = form_data.get("value", "0")
        if value == "":
            value = "0"
        try:
            value = float(value)
        except:
            value = 0

        insert_data = {
            "contract_number": form_data["contract_number"],
            "supplier": supplier,
            "contract_type_object": form_data.get("contract_type_object"),
            "value": value,
            "start_date": form_data.get("start_date"),
            "validity": form_data.get("validity"),
            "observations": form_data.get("observations"),
        }

        result = SupplierContractsAPI.insert(insert_data)
        if result:
            yield from self.load_data()
            self.close_add_dialog()
            yield rx.toast.success("Contrato agregado", position="top-right")
        else:
            yield rx.toast.error("Error al agregar", position="top-right")

    def open_edit_dialog(self, contract_id: int):
        contract = next((c for c in self.contracts_data if c["id"] == contract_id), None)
        if contract:
            self.edit_form_data = contract.copy()
            self.supplier_search_text = contract.get("supplier", "")
            self.show_edit_dialog = True

    def close_edit_dialog(self):
        self.show_edit_dialog = False
        self.edit_form_data = {}
        self.supplier_search_text = ""
        self.filtered_suppliers = []

    def update_contract(self, form_data: dict):
        contract_id = self.edit_form_data.get("id")
        if not contract_id:
            yield rx.toast.error("Error: ID no encontrado", position="top-right")
            return

        supplier = self.edit_form_data.get("supplier")
        if not supplier:
            yield rx.toast.error("El proveedor no puede estar vacío", position="top-right")
            return

        value = form_data.get("value", "0")
        if value == "":
            value = "0"
        try:
            value = float(value)
        except:
            value = 0

        update_data = {
            "contract_number": form_data.get("contract_number"),
            "supplier": supplier,
            "contract_type_object": form_data.get("contract_type_object"),
            "value": value,
            "start_date": form_data.get("start_date"),
            "validity": form_data.get("validity"),
            "observations": form_data.get("observations"),
        }

        result = SupplierContractsAPI.update(contract_id, update_data)
        if result:
            yield from self.load_data()
            self.close_edit_dialog()
            yield rx.toast.success("Contrato actualizado", position="top-right")
        else:
            yield rx.toast.error("Error al actualizar", position="top-right")

    def open_delete_dialog(self):
        if not self.selected_items:
            return rx.toast.error("Seleccione al menos un contrato", position="top-right")
        self.show_delete_dialog = True

    def close_delete_dialog(self):
        self.show_delete_dialog = False

    def delete_selected(self):
        if not self.selected_items:
            self.show_delete_dialog = False
            return
        success = SupplierContractsAPI.delete(self.selected_items)
        if success:
            self.selected_items = []
            yield from self.load_data()
            self.show_delete_dialog = False
            yield rx.toast.success("Contratos eliminados", position="top-right")
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
        fieldnames = ["id", "contract_number", "supplier", "contract_type_object", "value",
                      "start_date", "end_date", "validity", "observations"]
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for row in self.filtered_data:
            row_copy = {k: row.get(k, "") for k in fieldnames}
            writer.writerow(row_copy)
        csv_data = output.getvalue()
        output.close()
        return rx.download(data=csv_data, filename="contratos_proveedores.csv")

    def submit_contract(self, form_data: dict):
        if self.edit_form_data.get("id"):
            return self.update_contract(form_data)
        else:
            return self.add_contract(form_data)

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

    # ----- Autocompletado -----
    def update_supplier_search(self, text: str):
        self.supplier_search_text = text or ""
        # Actualizar también el proveedor en el estado (para que al escribir manualmente se guarde)
        if self.show_add_dialog:
            self.add_form_data["supplier"] = text
            self.add_form_data = self.add_form_data.copy()
        elif self.show_edit_dialog:
            self.edit_form_data["supplier"] = text
            self.edit_form_data = self.edit_form_data.copy()
        # Filtrar sugerencias
        if text:
            lower = text.lower()
            self.filtered_suppliers = [
                s for s in self.suppliers_list
                if lower in s.get("nombre_proveedor", "").lower()
            ][:10]
        else:
            self.filtered_suppliers = []

    def select_supplier(self, supplier_data: dict):
        supplier_name = supplier_data.get("nombre_proveedor", "")
        if self.show_edit_dialog:
            self.edit_form_data["supplier"] = supplier_name
            self.edit_form_data = self.edit_form_data.copy()
        elif self.show_add_dialog:
            self.add_form_data["supplier"] = supplier_name
            self.add_form_data = self.add_form_data.copy()
        self.supplier_search_text = supplier_name
        self.filtered_suppliers = []
        yield rx.toast.success(f"Proveedor seleccionado: {supplier_name}", position="top-right")