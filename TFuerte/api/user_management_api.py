# TFuerte/api/user_management_api.py
import os
import dotenv
from supabase import create_client
from typing import List, Dict, Any, Optional

dotenv.load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente Supabase (user_management) creado")
except Exception as e:
    print(f"❌ Error creando cliente Supabase: {e}")
    supabase = None

# -------------------------------------------------------------------
# Super Administradores (para login de este panel)
# -------------------------------------------------------------------
class SuperAdminAPI:
    @staticmethod
    def authenticate(username: str, password: str) -> Optional[Dict[str, Any]]:
        if not supabase:
            return None
        try:
            response = supabase.table("super_admin_users").select("*").eq("username", username).eq("password", password).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error en autenticación superadmin: {e}")
            return None

    @staticmethod
    def get_all() -> Optional[List[Dict[str, Any]]]:
        if not supabase:
            return None
        try:
            return supabase.table("super_admin_users").select("*").order("id").execute().data
        except Exception as e:
            print(f"Error obteniendo superadmins: {e}")
            return None

    @staticmethod
    def insert(user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase:
            return None
        try:
            user_data.pop("id", None)
            response = supabase.table("super_admin_users").insert(user_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error insertando superadmin: {e}")
            return None

    @staticmethod
    def update(user_id: int, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase:
            return None
        try:
            user_data.pop("id", None)
            response = supabase.table("super_admin_users").update(user_data).eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando superadmin: {e}")
            return None

    @staticmethod
    def delete(user_ids: List[int]) -> bool:
        if not supabase:
            return False
        try:
            supabase.table("super_admin_users").delete().in_("id", user_ids).execute()
            return True
        except Exception as e:
            print(f"Error eliminando superadmins: {e}")
            return False

# -------------------------------------------------------------------
# Tabla AdminTF (sistema de gestión empresarial)
# -------------------------------------------------------------------
class AdminTFAPI:
    @staticmethod
    def get_all() -> Optional[List[Dict[str, Any]]]:
        if not supabase:
            return None
        try:
            return supabase.table("AdminTF").select("*").order("id").execute().data
        except Exception as e:
            print(f"Error obteniendo AdminTF: {e}")
            return None

    @staticmethod
    def insert(user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase:
            return None
        try:
            user_data.pop("id", None)
            response = supabase.table("AdminTF").insert(user_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error insertando en AdminTF: {e}")
            return None

    @staticmethod
    def update(user_id: int, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase:
            return None
        try:
            user_data.pop("id", None)
            response = supabase.table("AdminTF").update(user_data).eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando AdminTF: {e}")
            return None

    @staticmethod
    def delete(user_ids: List[int]) -> bool:
        if not supabase:
            return False
        try:
            supabase.table("AdminTF").delete().in_("id", user_ids).execute()
            return True
        except Exception as e:
            print(f"Error eliminando AdminTF: {e}")
            return False

# -------------------------------------------------------------------
# Tabla Autorización
# -------------------------------------------------------------------
class AutorizacionAPI:
    @staticmethod
    def get_all() -> Optional[List[Dict[str, Any]]]:
        if not supabase:
            return None
        try:
            return supabase.table("Autorizacion").select("*").order("id").execute().data
        except Exception as e:
            print(f"Error obteniendo Autorización: {e}")
            return None

    @staticmethod
    def insert(user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase:
            return None
        try:
            user_data.pop("id", None)
            response = supabase.table("Autorizacion").insert(user_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error insertando en Autorizacion: {e}")
            return None

    @staticmethod
    def update(user_id: int, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase:
            return None
        try:
            user_data.pop("id", None)
            response = supabase.table("Autorizacion").update(user_data).eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando Autorizacion: {e}")
            return None

    @staticmethod
    def delete(user_ids: List[int]) -> bool:
        if not supabase:
            return False
        try:
            supabase.table("Autorizacion").delete().in_("id", user_ids).execute()
            return True
        except Exception as e:
            print(f"Error eliminando Autorizacion: {e}")
            return False

# -------------------------------------------------------------------
# Tabla Admin (solicitud de recursos y financiamiento)
# -------------------------------------------------------------------
class AdminRecursosAPI:
    @staticmethod
    def get_all() -> Optional[List[Dict[str, Any]]]:
        if not supabase:
            return None
        try:
            return supabase.table("Admin").select("*").order("id").execute().data
        except Exception as e:
            print(f"Error obteniendo Admin: {e}")
            return None

    @staticmethod
    def insert(user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase:
            return None
        try:
            user_data.pop("id", None)
            response = supabase.table("Admin").insert(user_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error insertando en Admin: {e}")
            return None

    @staticmethod
    def update(user_id: int, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase:
            return None
        try:
            user_data.pop("id", None)
            response = supabase.table("Admin").update(user_data).eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando Admin: {e}")
            return None

    @staticmethod
    def delete(user_ids: List[int]) -> bool:
        if not supabase:
            return False
        try:
            supabase.table("Admin").delete().in_("id", user_ids).execute()
            return True
        except Exception as e:
            print(f"Error eliminando Admin: {e}")
            return False

# -------------------------------------------------------------------
# Tabla Solicitantes
# -------------------------------------------------------------------
class SolicitantesAPI:
    @staticmethod
    def get_all() -> Optional[List[Dict[str, Any]]]:
        if not supabase:
            return None
        try:
            return supabase.table("Solicitantes").select("*").order("id").execute().data
        except Exception as e:
            print(f"Error obteniendo Solicitantes: {e}")
            return None

    @staticmethod
    def insert(user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase:
            return None
        try:
            user_data.pop("id", None)
            response = supabase.table("Solicitantes").insert(user_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error insertando en Solicitantes: {e}")
            return None

    @staticmethod
    def update(user_id: int, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase:
            return None
        try:
            user_data.pop("id", None)
            response = supabase.table("Solicitantes").update(user_data).eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando Solicitantes: {e}")
            return None

    @staticmethod
    def delete(user_ids: List[int]) -> bool:
        if not supabase:
            return False
        try:
            supabase.table("Solicitantes").delete().in_("id", user_ids).execute()
            return True
        except Exception as e:
            print(f"Error eliminando Solicitantes: {e}")
            return False

# -------------------------------------------------------------------
# Tabla commercial_admin_users
# -------------------------------------------------------------------
class CommercialAdminUsersAPI:
    @staticmethod
    def get_all() -> Optional[List[Dict[str, Any]]]:
        if not supabase:
            return None
        try:
            return supabase.table("commercial_admin_users").select("*").order("id").execute().data
        except Exception as e:
            print(f"Error obteniendo commercial_admin_users: {e}")
            return None

    @staticmethod
    def insert(user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase:
            return None
        try:
            user_data.pop("id", None)
            response = supabase.table("commercial_admin_users").insert(user_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error insertando en commercial_admin_users: {e}")
            return None

    @staticmethod
    def update(user_id: int, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase:
            return None
        try:
            user_data.pop("id", None)
            response = supabase.table("commercial_admin_users").update(user_data).eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando commercial_admin_users: {e}")
            return None

    @staticmethod
    def delete(user_ids: List[int]) -> bool:
        if not supabase:
            return False
        try:
            supabase.table("commercial_admin_users").delete().in_("id", user_ids).execute()
            return True
        except Exception as e:
            print(f"Error eliminando commercial_admin_users: {e}")
            return False

# -------------------------------------------------------------------
# Tabla commercial_users
# -------------------------------------------------------------------
class CommercialUsersAPI:
    @staticmethod
    def get_all() -> Optional[List[Dict[str, Any]]]:
        if not supabase:
            return None
        try:
            return supabase.table("commercial_users").select("*").order("id").execute().data
        except Exception as e:
            print(f"Error obteniendo commercial_users: {e}")
            return None

    @staticmethod
    def insert(user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase:
            return None
        try:
            user_data.pop("id", None)
            response = supabase.table("commercial_users").insert(user_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error insertando en commercial_users: {e}")
            return None

    @staticmethod
    def update(user_id: int, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase:
            return None
        try:
            user_data.pop("id", None)
            response = supabase.table("commercial_users").update(user_data).eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando commercial_users: {e}")
            return None

    @staticmethod
    def delete(user_ids: List[int]) -> bool:
        if not supabase:
            return False
        try:
            supabase.table("commercial_users").delete().in_("id", user_ids).execute()
            return True
        except Exception as e:
            print(f"Error eliminando commercial_users: {e}")
            return False