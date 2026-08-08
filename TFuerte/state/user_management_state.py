# TFuerte/state/user_management_state.py
import reflex as rx
from typing import List, Dict, Any
from TFuerte.api.user_management_api import (
    AdminTFAPI, AutorizacionAPI, AdminRecursosAPI, SolicitantesAPI,
    CommercialAdminUsersAPI, CommercialUsersAPI, SuperAdminAPI
)

class UserManagementState(rx.State):
    # Datos para cada tabla
    super_admin_users: List[dict] = []
    admin_tf_users: List[dict] = []
    autorizacion_users: List[dict] = []
    admin_recursos_users: List[dict] = []
    solicitantes_users: List[dict] = []
    commercial_admin_users: List[dict] = []
    commercial_users: List[dict] = []

    # Estado de carga
    loading: bool = False

    # Diálogos y formularios
    show_add_dialog: bool = False
    show_edit_dialog: bool = False
    current_table: str = ""
    current_user_id: int = 0
    edit_form_data: dict = {}
    add_form_data: dict = {}

    # Campos específicos por tabla (diccionario estático)
    table_fields_dict = {
        "super_admin": ["username", "password"],
        "admin_tf": ["usuario", "clave"],
        "autorizacion": ["user", "password"],
        "admin_recursos": ["usuario", "password", "cargo", "rol"],
        "solicitantes": ["usuario", "clave", "cargo"],
        "commercial_admin": ["username", "password"],
        "commercial": ["username", "password"],
    }

    # Descripciones
    table_descriptions = {
        "super_admin": "Superadministradores del sistema (acceso a este panel de gestión de usuarios).",
        "admin_tf": "Usuarios del sistema de gestión empresarial (AdminTF).",
        "autorizacion": "Usuarios que autorizan salidas de productos del almacén.",
        "admin_recursos": "Usuarios del sistema de solicitud de recursos y financiamiento (con cargo y rol).",
        "solicitantes": "Solicitantes de recursos (usuario, clave, cargo).",
        "commercial_admin": "Administradores del panel de gestión comercial (solo lectura).",
        "commercial": "Usuarios del panel de gestión comercial (operadores).",
    }

    # Variable computada para los campos de la tabla actual
    @rx.var
    def current_fields(self) -> List[str]:
        return self.table_fields_dict.get(self.current_table, [])

    # Métodos de carga
    def load_all_data(self):
        self.loading = True
        yield

        data = SuperAdminAPI.get_all()
        self.super_admin_users = data if data is not None else []

        data = AdminTFAPI.get_all()
        self.admin_tf_users = data if data is not None else []

        data = AutorizacionAPI.get_all()
        self.autorizacion_users = data if data is not None else []

        data = AdminRecursosAPI.get_all()
        self.admin_recursos_users = data if data is not None else []

        data = SolicitantesAPI.get_all()
        self.solicitantes_users = data if data is not None else []

        data = CommercialAdminUsersAPI.get_all()
        self.commercial_admin_users = data if data is not None else []

        data = CommercialUsersAPI.get_all()
        self.commercial_users = data if data is not None else []

        self.loading = False

    # Diálogos
    def open_add_dialog(self, table_key: str):
        self.current_table = table_key
        self.add_form_data = {}
        self.show_add_dialog = True

    def close_add_dialog(self):
        self.show_add_dialog = False
        self.add_form_data = {}

    def open_edit_dialog(self, table_key: str, user_id: int, user_data: dict):
        self.current_table = table_key
        self.current_user_id = user_id
        self.edit_form_data = user_data.copy()
        self.show_edit_dialog = True

    def close_edit_dialog(self):
        self.show_edit_dialog = False
        self.edit_form_data = {}

    # Agregar usuario
    def add_user(self, form_data: dict):
        table_key = self.current_table
        if table_key == "super_admin":
            result = SuperAdminAPI.insert(form_data)
        elif table_key == "admin_tf":
            result = AdminTFAPI.insert(form_data)
        elif table_key == "autorizacion":
            result = AutorizacionAPI.insert(form_data)
        elif table_key == "admin_recursos":
            result = AdminRecursosAPI.insert(form_data)
        elif table_key == "solicitantes":
            result = SolicitantesAPI.insert(form_data)
        elif table_key == "commercial_admin":
            result = CommercialAdminUsersAPI.insert(form_data)
        elif table_key == "commercial":
            result = CommercialUsersAPI.insert(form_data)
        else:
            result = None

        if result:
            yield from self.load_all_data()
            self.close_add_dialog()
            yield rx.toast.success("Usuario agregado correctamente", position="top-right")
        else:
            yield rx.toast.error("Error al agregar usuario", position="top-right")

    # Editar usuario
    def update_user(self, form_data: dict):
        table_key = self.current_table
        user_id = self.current_user_id
        if table_key == "super_admin":
            result = SuperAdminAPI.update(user_id, form_data)
        elif table_key == "admin_tf":
            result = AdminTFAPI.update(user_id, form_data)
        elif table_key == "autorizacion":
            result = AutorizacionAPI.update(user_id, form_data)
        elif table_key == "admin_recursos":
            result = AdminRecursosAPI.update(user_id, form_data)
        elif table_key == "solicitantes":
            result = SolicitantesAPI.update(user_id, form_data)
        elif table_key == "commercial_admin":
            result = CommercialAdminUsersAPI.update(user_id, form_data)
        elif table_key == "commercial":
            result = CommercialUsersAPI.update(user_id, form_data)
        else:
            result = None

        if result:
            yield from self.load_all_data()
            self.close_edit_dialog()
            yield rx.toast.success("Usuario actualizado correctamente", position="top-right")
        else:
            yield rx.toast.error("Error al actualizar usuario", position="top-right")

    # Eliminar usuario
    def delete_user(self, table_key: str, user_id: int):
        if table_key == "super_admin":
            success = SuperAdminAPI.delete([user_id])
        elif table_key == "admin_tf":
            success = AdminTFAPI.delete([user_id])
        elif table_key == "autorizacion":
            success = AutorizacionAPI.delete([user_id])
        elif table_key == "admin_recursos":
            success = AdminRecursosAPI.delete([user_id])
        elif table_key == "solicitantes":
            success = SolicitantesAPI.delete([user_id])
        elif table_key == "commercial_admin":
            success = CommercialAdminUsersAPI.delete([user_id])
        elif table_key == "commercial":
            success = CommercialUsersAPI.delete([user_id])
        else:
            success = False

        if success:
            yield from self.load_all_data()
            yield rx.toast.success("Usuario eliminado", position="top-right")
        else:
            yield rx.toast.error("Error al eliminar usuario", position="top-right")

    # Actualizar campo del formulario
    def update_add_form_field(self, field: str, value: str):
        self.add_form_data[field] = value
        self.add_form_data = self.add_form_data.copy()

    def update_edit_form_field(self, field: str, value: str):
        self.edit_form_data[field] = value
        self.edit_form_data = self.edit_form_data.copy()