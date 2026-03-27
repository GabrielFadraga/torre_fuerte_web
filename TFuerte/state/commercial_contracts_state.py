#commercial_contracts_state.py
import reflex as rx
import csv
import io
from datetime import datetime, timedelta
from typing import List, Optional
from TFuerte.api.commercial_api import ContractsAPI, ClientsAPI

class CommercialContractsState(rx.State):
    # Datos
    contracts_data: List[dict] = []
    filtered_data: List[dict] = []
    clients_list: List[dict] = []
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
    show_details_dialog: bool = False
    show_supplement_confirm: bool = False
    supplement_target_id: int = 0
    details_contract: dict = {}
    edit_form_data: dict = {}
    add_form_data: dict = {
        "fecha_firmado": "",
        "vigencia": "",
        "fecha_terminacion": "",
        "client_id": None,
        "codigo_cliente": ""
    }
    original_contract_data: dict = {}

    # Autocompletado de cliente
    client_search_text: str = ""
    filtered_clients: List[dict] = []

    # Resumen
    total_contracts: int = 0
    pending_signature: int = 0
    signed: int = 0
    closed: int = 0
    expired: int = 0
    near_expiry: int = 0

    def load_data(self):
        self.loading = True
        yield

        contracts = ContractsAPI.get_with_client_names()
        clients = ClientsAPI.get_all()

        if contracts:
            self.contracts_data = contracts
        else:
            self.contracts_data = []

        self.clients_list = clients
        self.apply_filters()
        self.calculate_summary()

        self.loading = False
        yield rx.toast.success(f"Contratos cargados: {len(contracts)}", position="top-right")

    def apply_filters(self):
        result = self.contracts_data.copy()
        if self.search_value:
            search = self.search_value.lower()
            result = [c for c in result if search in c.get("cliente_nombre", "").lower() or
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

    # ----- Generación de número de contrato -----
    def generate_contract_number(self, client_id: int, year: int, is_supplement: bool,
                                 parent_contract_id: Optional[int] = None,
                                 current_contract_id: Optional[int] = None,
                                 fecha_firmado: Optional[str] = None,
                                 offset: int = 0) -> str:
        """
        Genera número de contrato.
        Para contratos base firmados, usa el código REUP del cliente.
        Para suplementos, obtiene el prefijo base del padre y asigna el siguiente consecutivo.
        """
        is_provisional = not fecha_firmado

        if not is_provisional:
            # Contrato firmado -> número definitivo
            if not is_supplement:
                # Contrato base: usar código REUP del cliente
                if self.show_add_dialog:
                    client_code = self.add_form_data.get("codigo_cliente", "").strip()
                else:
                    client_code = self.edit_form_data.get("codigo_cliente", "").strip()

                if client_code:
                    return f"{client_code}/{year}"
                else:
                    # Fallback: generación automática con consecutivo numérico
                    existing = [c for c in self.contracts_data
                                if c.get("client_id") == client_id
                                and c.get("year") == year
                                and not c.get("is_supplement")
                                and c.get("id") != current_contract_id]
                    max_num = 0
                    for c in existing:
                        num_part = c["contract_number"].split('/')[0]
                        if num_part.isdigit():
                            max_num = max(max_num, int(num_part))
                    next_num = max_num + 1 + offset
                    return f"{next_num:02d}/{year}"
            else:
                # Suplemento
                if not parent_contract_id:
                    return "ERROR: No se ha seleccionado un contrato base."
                parent = next((c for c in self.contracts_data if c["id"] == parent_contract_id), None)
                if not parent:
                    return f"ERROR: No se encontró el contrato base con ID {parent_contract_id}."

                # Extraer el prefijo base (sin guiones)
                parent_num_full = parent["contract_number"].split('/')[0]
                if '-' in parent_num_full:
                    base_prefix = parent_num_full.split('-')[0]
                else:
                    base_prefix = parent_num_full

                # Contar todos los suplementos de la familia (que comiencen con base_prefix-)
                supplements = [c for c in self.contracts_data
                               if c.get("contract_number", "").startswith(f"{base_prefix}-")
                               and c.get("id") != current_contract_id]
                next_supp = len(supplements) + 1 + offset
                return f"{base_prefix}-{next_supp}/{year}"
        else:
            # Provisional: AFXX/año
            provisional_prefix = "AF"
            existing_provisional = [c for c in self.contracts_data
                                    if c.get("client_id") == client_id
                                    and c.get("year") == year
                                    and (not c.get("fecha_firmado"))
                                    and c.get("id") != current_contract_id]
            max_num = 0
            for c in existing_provisional:
                num_part = c["contract_number"].split('/')[0].replace(provisional_prefix, "")
                if num_part.isdigit():
                    max_num = max(max_num, int(num_part))
            next_num = max_num + 1 + offset
            return f"{provisional_prefix}{next_num:02d}/{year}"

    # ----- Método para abrir confirmación de suplemento -----
    def open_supplement_confirm(self, contract_id: int):
        self.supplement_target_id = contract_id
        self.show_supplement_confirm = True

    def close_supplement_confirm(self):
        self.show_supplement_confirm = False
        self.supplement_target_id = 0

    def set_show_supplement_confirm(self, show: bool):
        self.show_supplement_confirm = show

    def confirm_add_supplement(self):
        contract_id = self.supplement_target_id
        self.close_supplement_confirm()

        if not contract_id:
            yield rx.toast.error("No se seleccionó ningún contrato.", position="top-right")
            return

        contract = next((c for c in self.contracts_data if c["id"] == contract_id), None)
        if not contract:
            yield rx.toast.error("Contrato no encontrado", position="top-right")
            return

        if not contract.get("fecha_firmado"):
            yield rx.toast.error("No se puede agregar suplemento a un contrato sin firmar.", position="top-right")
            return

        year = contract.get("year")
        if not year and contract.get("fecha_firmado"):
            try:
                year = datetime.strptime(contract["fecha_firmado"], "%Y-%m-%d").year
            except:
                year = datetime.now().year

        current_number = contract["contract_number"]

        # Extraer prefijo base y número de suplemento actual
        if '-' in current_number:
            # Ya es suplemento: ejemplo "05-1/2026"
            parts = current_number.split('/')[0]  # "05-1"
            base_prefix = parts.split('-')[0]      # "05"
            current_supp = int(parts.split('-')[1]) # 1
            next_supp = current_supp + 1
        else:
            # Es contrato base: ejemplo "05/2026"
            base_prefix = current_number.split('/')[0]  # "05"
            next_supp = 1

        new_number = f"{base_prefix}-{next_supp}/{year}"

        # Verificar unicidad (por si acaso)
        exists = any(c.get("id") != contract_id and c.get("contract_number") == new_number for c in self.contracts_data)
        if exists:
            yield rx.toast.error("El número generado ya existe. Intente más tarde.", position="top-right")
            return

        # Determinar el ID base original (el contrato base raíz)
        original_base_id = contract.get("parent_contract_id") or contract_id

        update_data = {
            "contract_number": new_number,
            "is_supplement": True,
            "parent_contract_id": original_base_id
        }

        try:
            result = ContractsAPI.update(contract_id, update_data)
        except Exception as e:
            yield rx.toast.error(f"Error al actualizar: {e}", position="top-right")
            return

        if result:
            yield from self.load_data()
            yield rx.toast.success(f"Suplemento agregado. Nuevo número: {new_number}", position="top-right")
        else:
            yield rx.toast.error("Error al actualizar el contrato", position="top-right")

    # ----- CRUD -----
    def open_add_dialog(self):
        self.add_form_data = {
            "fecha_firmado": "",
            "vigencia": "",
            "fecha_terminacion": "",
            "client_id": None,
            "codigo_cliente": ""
        }
        self.client_search_text = ""
        self.filtered_clients = []
        self.show_add_dialog = True

    def close_add_dialog(self):
        self.show_add_dialog = False
        self.add_form_data = {}
        self.client_search_text = ""
        self.filtered_clients = []

    def add_contract(self, form_data: dict):
        client_id = self.add_form_data.get("client_id")
        if not client_id:
            yield rx.toast.error("Debe seleccionar un cliente", position="top-right")
            return

        objeto = form_data.get("objeto")
        fecha_a_firma = form_data.get("fecha_a_firma")
        if not objeto or not fecha_a_firma:
            yield rx.toast.error("Faltan: objeto o fecha a firma", position="top-right")
            return

        fecha_firmado = form_data.get("fecha_firmado")
        if fecha_firmado == "":
            fecha_firmado = None

        vigencia = form_data.get("vigencia", "")
        year = datetime.strptime(fecha_a_firma, "%Y-%m-%d").year

        if fecha_firmado:
            client_code = self.add_form_data.get("codigo_cliente", "").strip()
            if not client_code:
                yield rx.toast.error("El cliente debe tener un código REUP para firmar el contrato.", position="top-right")
                return

        yield from self.load_data()

        max_attempts = 5
        contract_number = None
        for attempt in range(max_attempts):
            candidate = self.generate_contract_number(
                client_id, year, is_supplement=False, parent_contract_id=None,
                current_contract_id=None, fecha_firmado=fecha_firmado, offset=attempt
            )
            if candidate.startswith("ERROR"):
                yield rx.toast.error(candidate, position="top-right")
                return
            exists = any(c.get("contract_number") == candidate for c in self.contracts_data)
            if not exists:
                contract_number = candidate
                break
            if attempt == max_attempts - 1:
                yield rx.toast.error("No se pudo generar un número único. Intente más tarde.", position="top-right")
                return

        insert_data = {
            "contract_number": contract_number,
            "client_id": client_id,
            "objeto": objeto,
            "importe_cup": float(form_data.get("importe_cup", 0)),
            "importe_mlc": float(form_data.get("importe_mlc", 0)),
            "ejecucion_cup": float(form_data.get("ejecucion_cup", 0)),
            "ejecucion_mlc": float(form_data.get("ejecucion_mlc", 0)),
            "fecha_a_firma": fecha_a_firma,
            "fecha_firmado": fecha_firmado,
            "fecha_inicio": form_data.get("fecha_inicio") or fecha_a_firma,
            "vigencia": vigencia,
            "observaciones": form_data.get("observaciones"),
            "is_supplement": False,
            "year": year,
        }

        result = ContractsAPI.insert(insert_data)
        if result:
            yield from self.load_data()
            self.close_add_dialog()
            yield rx.toast.success("Contrato agregado", position="top-right")
        else:
            yield rx.toast.error("Error al agregar contrato", position="top-right")

    def open_edit_dialog(self, contract_id: int):
        contract = next((c for c in self.contracts_data if c["id"] == contract_id), None)
        if contract:
            self.original_contract_data = contract.copy()
            self.edit_form_data = contract.copy()
            client_id = contract.get("client_id")
            if client_id:
                client = next((c for c in self.clients_list if c["id"] == client_id), None)
                if client:
                    self.client_search_text = client.get("nombre_cliente", "")
                    self.edit_form_data["codigo_cliente"] = client.get("codigo_reup", "")
                else:
                    self.client_search_text = ""
                    self.edit_form_data["codigo_cliente"] = ""
            else:
                self.client_search_text = ""
                self.edit_form_data["codigo_cliente"] = ""
            self.show_edit_dialog = True
        else:
            self.show_edit_dialog = True

    def close_edit_dialog(self):
        self.show_edit_dialog = False
        self.edit_form_data = {}
        self.original_contract_data = {}
        self.client_search_text = ""
        self.filtered_clients = []

    def update_contract(self, form_data: dict):
        contract_id = self.edit_form_data.get("id")
        if not contract_id:
            yield rx.toast.error("Error: ID no encontrado", position="top-right")
            return

        original = self.original_contract_data
        if not original:
            yield rx.toast.error("No se encontraron datos originales del contrato", position="top-right")
            return

        original_client_id = original.get("client_id")
        original_fecha_firmado = original.get("fecha_firmado")
        original_fecha_a_firma = original.get("fecha_a_firma")

        new_client_id = self.edit_form_data.get("client_id")
        new_fecha_a_firma = form_data.get("fecha_a_firma")
        new_fecha_firmado = form_data.get("fecha_firmado")
        if new_fecha_firmado == "":
            new_fecha_firmado = None
        new_objeto = form_data.get("objeto")
        new_importe_cup = form_data.get("importe_cup")
        new_importe_mlc = form_data.get("importe_mlc")
        new_ejecucion_cup = form_data.get("ejecucion_cup")
        new_ejecucion_mlc = form_data.get("ejecucion_mlc")
        new_vigencia = form_data.get("vigencia")
        new_observaciones = form_data.get("observaciones")

        effective_fecha = new_fecha_a_firma if new_fecha_a_firma else new_fecha_firmado
        new_year = None
        if effective_fecha:
            try:
                new_year = datetime.strptime(effective_fecha, "%Y-%m-%d").year
            except:
                pass
        else:
            if original_fecha_firmado:
                try:
                    new_year = datetime.strptime(original_fecha_firmado, "%Y-%m-%d").year
                except:
                    pass
            elif original_fecha_a_firma:
                try:
                    new_year = datetime.strptime(original_fecha_a_firma, "%Y-%m-%d").year
                except:
                    pass

        regenerate = False
        if new_client_id != original_client_id:
            regenerate = True
        elif new_fecha_firmado != original_fecha_firmado:
            regenerate = True
        else:
            orig_year = None
            if original_fecha_firmado:
                try:
                    orig_year = datetime.strptime(original_fecha_firmado, "%Y-%m-%d").year
                except:
                    pass
            elif original_fecha_a_firma:
                try:
                    orig_year = datetime.strptime(original_fecha_a_firma, "%Y-%m-%d").year
                except:
                    pass
            if new_year and new_year != orig_year:
                regenerate = True

        update_data = {}
        if new_objeto is not None and new_objeto != "":
            update_data["objeto"] = new_objeto
        if new_fecha_a_firma is not None and new_fecha_a_firma != "":
            update_data["fecha_a_firma"] = new_fecha_a_firma
        if new_fecha_firmado is not None:
            update_data["fecha_firmado"] = new_fecha_firmado
        if new_vigencia is not None and new_vigencia != "":
            update_data["vigencia"] = new_vigencia
        if new_observaciones is not None and new_observaciones != "":
            update_data["observaciones"] = new_observaciones

        for field, val in [("importe_cup", new_importe_cup), ("importe_mlc", new_importe_mlc),
                           ("ejecucion_cup", new_ejecucion_cup), ("ejecucion_mlc", new_ejecucion_mlc)]:
            if val is not None and val != "":
                try:
                    update_data[field] = float(val)
                except:
                    pass

        if new_client_id is not None:
            update_data["client_id"] = new_client_id

        if regenerate:
            yield rx.toast.info("Regenerando número de contrato...", position="top-right")
            if new_fecha_firmado:
                client_code = self.edit_form_data.get("codigo_cliente", "").strip()
                if not client_code:
                    yield rx.toast.error("El cliente debe tener un código REUP para firmar el contrato.", position="top-right")
                    return

            yield from self.load_data()

            max_attempts = 5
            new_number = None
            for attempt in range(max_attempts):
                candidate = self.generate_contract_number(
                    client_id=new_client_id,
                    year=new_year,
                    is_supplement=False,
                    parent_contract_id=None,
                    current_contract_id=contract_id,
                    fecha_firmado=new_fecha_firmado,
                    offset=attempt
                )
                if candidate.startswith("ERROR"):
                    yield rx.toast.error(candidate, position="top-right")
                    return
                exists = any(c.get("id") != contract_id and c.get("contract_number") == candidate for c in self.contracts_data)
                if not exists:
                    new_number = candidate
                    break
                if attempt == max_attempts - 1:
                    yield rx.toast.error("No se pudo generar un número único. Intente más tarde.", position="top-right")
                    return
            update_data["contract_number"] = new_number
            if new_year:
                update_data["year"] = new_year
            yield rx.toast.info(f"Nuevo número generado: {new_number}", position="top-right")
        else:
            yield rx.toast.info("No se requiere regeneración de número.", position="top-right")

        if not update_data:
            yield rx.toast.info("No se detectaron cambios", position="top-right")
            return

        try:
            result = ContractsAPI.update(contract_id, update_data)
        except Exception as e:
            error_msg = str(e)
            if "duplicate key value violates unique constraint" in error_msg:
                yield rx.toast.error("Número de contrato ya existe. Intente nuevamente.", position="top-right")
            else:
                yield rx.toast.error(f"Error: {error_msg}", position="top-right")
            return

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
        success = ContractsAPI.delete(self.selected_items)
        if success:
            self.selected_items = []
            yield from self.load_data()
            self.show_delete_dialog = False
            yield rx.toast.success("Contratos eliminados", position="top-right")
        else:
            self.show_delete_dialog = False
            yield rx.toast.error("Error al eliminar", position="top-right")

    def calculate_summary(self):
        today = datetime.now().date()
        self.total_contracts = len(self.contracts_data)
        self.pending_signature = sum(1 for c in self.contracts_data if not c.get("fecha_firmado"))
        self.signed = sum(1 for c in self.contracts_data if c.get("fecha_firmado"))
        self.expired = sum(1 for c in self.contracts_data if c.get("fecha_terminacion") and datetime.strptime(c["fecha_terminacion"], "%Y-%m-%d").date() < today)
        near = 0
        for c in self.contracts_data:
            if c.get("fecha_terminacion"):
                term = datetime.strptime(c["fecha_terminacion"], "%Y-%m-%d").date()
                if today <= term <= (today + timedelta(days=30)):
                    near += 1
        self.near_expiry = near

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
        fieldnames = ["id", "contract_number", "cliente_nombre", "objeto", "importe_cup", "importe_mlc",
                      "promedio_mensual", "ejecucion_cup", "ejecucion_mlc", "dif_cup", "dif_mlc",
                      "fecha_a_firma", "fecha_firmado", "fecha_inicio", "fecha_terminacion", "vigencia",
                      "observaciones"]
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for row in self.filtered_data:
            row_copy = {k: row.get(k, "") for k in fieldnames}
            writer.writerow(row_copy)
        csv_data = output.getvalue()
        output.close()
        return rx.download(data=csv_data, filename="contratos.csv")

    # ----- Autocompletado -----
    def update_client_search(self, text: str):
        self.client_search_text = text or ""
        if text:
            lower = text.lower()
            self.filtered_clients = [
                c for c in self.clients_list
                if lower in (c.get("nombre_cliente", "").lower())
            ][:10]
        else:
            self.filtered_clients = []

    def select_client(self, client_data: dict):
        client_id = client_data.get("id", 0)
        client_name = client_data.get("nombre_cliente", "")
        client_code = client_data.get("codigo_reup", "")
        if self.show_edit_dialog:
            self.edit_form_data["client_id"] = client_id
            self.edit_form_data["codigo_cliente"] = client_code
            self.edit_form_data = self.edit_form_data.copy()
        elif self.show_add_dialog:
            self.add_form_data["client_id"] = client_id
            self.add_form_data["codigo_cliente"] = client_code
            self.add_form_data = self.add_form_data.copy()
        self.client_search_text = client_name
        self.filtered_clients = []
        yield rx.toast.success(f"Cliente seleccionado: {client_name}", position="top-right")

    def open_details_dialog(self, contract_id: int):
        contract = next((c for c in self.contracts_data if c["id"] == contract_id), None)
        if contract:
            self.details_contract = contract
            self.show_details_dialog = True

    def close_details_dialog(self):
        self.show_details_dialog = False
        self.details_contract = {}

    def set_show_details_dialog(self, show: bool):
        self.show_details_dialog = show
        if not show:
            self.details_contract = {}

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
        if field in ["client_id", "parent_contract_id"]:
            try:
                value = int(value) if value else None
            except:
                value = None
        else:
            self.add_form_data[field] = value
        self.add_form_data = self.add_form_data.copy()

    def update_edit_form_field(self, field: str, value):
        if field in ["client_id", "parent_contract_id"]:
            try:
                value = int(value) if value else None
            except:
                value = None
        else:
            self.edit_form_data[field] = value
        self.edit_form_data = self.edit_form_data.copy()

    def set_dialog_open(self, open: bool):
        if self.show_edit_dialog:
            self.show_edit_dialog = open
        elif self.show_add_dialog:
            self.show_add_dialog = open

    @rx.var
    def client_options(self) -> list[tuple[str, str]]:
        return [(str(c["id"]), c["nombre_cliente"]) for c in self.clients_list]

    @rx.var
    def contract_options(self) -> list[tuple[str, str]]:
        return [(str(c["id"]), c["contract_number"]) for c in self.contracts_data]

    @rx.var
    def base_contracts_options(self) -> list[tuple[str, str]]:
        # Ya no se usa, pero se mantiene por si acaso
        return []