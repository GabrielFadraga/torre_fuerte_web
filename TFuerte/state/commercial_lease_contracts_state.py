import reflex as rx
import csv
import io
from datetime import datetime, timedelta
from typing import List, Optional
from TFuerte.api.commercial_api import LeaseContractsAPI, LeasingSuppliersAPI

class CommercialLeaseContractsState(rx.State):
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

    # Autocompletado de proveedores de arrendamiento
    leasing_suppliers_list: List[dict] = []
    supplier_search_text: str = ""
    filtered_suppliers: List[dict] = []

    def load_data(self):
        self.loading = True
        yield

        data = LeaseContractsAPI.get_all()
        if data:
            self.contracts_data = data
        else:
            self.contracts_data = []

        suppliers = LeasingSuppliersAPI.get_all()
        self.leasing_suppliers_list = suppliers if suppliers else []

        self.apply_filters()
        self.loading = False
        yield rx.toast.success(f"Contratos de arrendamiento cargados: {len(data)}", position="top-right")

    def apply_filters(self):
        result = self.contracts_data.copy()
        if self.search_value:
            search = self.search_value.lower()
            result = [c for c in result if search in c.get("proveedor", "").lower()]
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
        proveedor = self.add_form_data.get("proveedor")
        if not proveedor:
            yield rx.toast.error("Debe seleccionar o escribir un proveedor", position="top-right")
            return

        valor = form_data.get("valor", "0")
        if valor == "":
            valor = "0"
        try:
            valor = float(valor)
        except:
            valor = 0

        insert_data = {
            "proveedor": proveedor,
            "tipo_contrato": form_data.get("tipo_contrato"),
            "valor": valor,
            "vigencia": form_data.get("vigencia"),
            "fecha_inicio": form_data.get("fecha_inicio"),
            "observacion": form_data.get("observacion"),
        }

        result = LeaseContractsAPI.insert(insert_data)
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
            self.supplier_search_text = contract.get("proveedor", "")
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

        proveedor = self.edit_form_data.get("proveedor")
        if not proveedor:
            yield rx.toast.error("El proveedor no puede estar vacío", position="top-right")
            return

        valor = form_data.get("valor", "0")
        if valor == "":
            valor = "0"
        try:
            valor = float(valor)
        except:
            valor = 0

        update_data = {
            "proveedor": proveedor,
            "tipo_contrato": form_data.get("tipo_contrato"),
            "valor": valor,
            "vigencia": form_data.get("vigencia"),
            "fecha_inicio": form_data.get("fecha_inicio"),
            "observacion": form_data.get("observacion"),
        }

        result = LeaseContractsAPI.update(contract_id, update_data)
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
        success = LeaseContractsAPI.delete(self.selected_items)
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
        fieldnames = ["id", "proveedor", "tipo_contrato", "valor", "vigencia", "fecha_inicio", "fecha_terminacion", "observacion"]
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for row in self.filtered_data:
            row_copy = {k: row.get(k, "") for k in fieldnames}
            writer.writerow(row_copy)
        csv_data = output.getvalue()
        output.close()
        return rx.download(data=csv_data, filename="contratos_arrendamiento.csv")

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
        if self.show_add_dialog:
            self.add_form_data["proveedor"] = text
            self.add_form_data = self.add_form_data.copy()
        elif self.show_edit_dialog:
            self.edit_form_data["proveedor"] = text
            self.edit_form_data = self.edit_form_data.copy()
        if text:
            lower = text.lower()
            self.filtered_suppliers = [
                s for s in self.leasing_suppliers_list
                if lower in s.get("nombre_proveedor", "").lower()
            ][:10]
        else:
            self.filtered_suppliers = []

    def select_supplier(self, supplier_data: dict):
        supplier_name = supplier_data.get("nombre_proveedor", "")
        if self.show_edit_dialog:
            self.edit_form_data["proveedor"] = supplier_name
            self.edit_form_data = self.edit_form_data.copy()
        elif self.show_add_dialog:
            self.add_form_data["proveedor"] = supplier_name
            self.add_form_data = self.add_form_data.copy()
        self.supplier_search_text = supplier_name
        self.filtered_suppliers = []
        yield rx.toast.success(f"Proveedor seleccionado: {supplier_name}", position="top-right")