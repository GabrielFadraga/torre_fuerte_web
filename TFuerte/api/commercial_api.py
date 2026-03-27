import os
import dotenv
from supabase import create_client
from typing import List, Dict, Any, Optional

dotenv.load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente Supabase (commercial) creado")
except Exception as e:
    print(f"❌ Error creando cliente Supabase: {e}")
    supabase = None

# -------------------------------------------------------------------
# Usuarios comerciales (login)
# -------------------------------------------------------------------
class CommercialUserAPI:
    @staticmethod
    def authenticate(username: str, password: str) -> Optional[Dict[str, Any]]:
        if not supabase:
            return None
        try:
            response = supabase.table("commercial_users").select("*").eq("username", username).eq("password", password).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error en autenticación: {e}")
            return None

# -------------------------------------------------------------------
# Clientes
# -------------------------------------------------------------------
class ClientsAPI:
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        if not supabase: return []
        try:
            return supabase.table("clients").select("*").order("id").execute().data
        except Exception as e:
            print(f"Error obteniendo clientes: {e}")
            return []

    @staticmethod
    def insert(client_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase: return None
        try:
            client_data.pop("id", None)
            response = supabase.table("clients").insert(client_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error insertando cliente: {e}")
            return None

    @staticmethod
    def update(client_id: int, client_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase: return None
        try:
            client_data.pop("id", None)
            response = supabase.table("clients").update(client_data).eq("id", client_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando cliente: {e}")
            return None

    @staticmethod
    def delete(client_ids: List[int]) -> bool:
        if not supabase: return False
        try:
            supabase.table("clients").delete().in_("id", client_ids).execute()
            return True
        except Exception as e:
            print(f"Error eliminando clientes: {e}")
            return False

# -------------------------------------------------------------------
# Contratos con Clientes
# -------------------------------------------------------------------
class ContractsAPI:
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        if not supabase: return []
        try:
            return supabase.table("contracts").select("*").order("id").execute().data
        except Exception as e:
            print(f"Error obteniendo contratos: {e}")
            return []

    @staticmethod
    def get_with_client_names() -> List[Dict[str, Any]]:
        if not supabase: return []
        try:
            response = supabase.table("contracts").select("*, clients(nombre_cliente)").execute()
            data = response.data
            for item in data:
                if item.get("clients"):
                    item["cliente_nombre"] = item["clients"]["nombre_cliente"]
                else:
                    item["cliente_nombre"] = ""
                item.pop("clients", None)
            return data
        except Exception as e:
            print(f"Error obteniendo contratos con clientes: {e}")
            return []

    @staticmethod
    def insert(contract_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase: return None
        try:
            contract_data.pop("id", None)
            response = supabase.table("contracts").insert(contract_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error insertando contrato: {e}")
            return None

    @staticmethod
    def update(contract_id: int, contract_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase: return None
        try:
            contract_data.pop("id", None)
            response = supabase.table("contracts").update(contract_data).eq("id", contract_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando contrato: {e}")
            return None

    @staticmethod
    def delete(contract_ids: List[int]) -> bool:
        if not supabase: return False
        try:
            supabase.table("contracts").delete().in_("id", contract_ids).execute()
            return True
        except Exception as e:
            print(f"Error eliminando contratos: {e}")
            return False

# -------------------------------------------------------------------
# Contratos con Proveedores
# -------------------------------------------------------------------
class SupplierContractsAPI:
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        if not supabase: return []
        try:
            return supabase.table("supplier_contracts").select("*").order("id").execute().data
        except Exception as e:
            print(f"Error obteniendo contratos de proveedores: {e}")
            return []

    @staticmethod
    def insert(contract_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase: return None
        try:
            contract_data.pop("id", None)
            response = supabase.table("supplier_contracts").insert(contract_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error insertando contrato de proveedor: {e}")
            return None

    @staticmethod
    def update(contract_id: int, contract_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase: return None
        try:
            contract_data.pop("id", None)
            response = supabase.table("supplier_contracts").update(contract_data).eq("id", contract_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando contrato de proveedor: {e}")
            return None

    @staticmethod
    def delete(contract_ids: List[int]) -> bool:
        if not supabase: return False
        try:
            supabase.table("supplier_contracts").delete().in_("id", contract_ids).execute()
            return True
        except Exception as e:
            print(f"Error eliminando contratos de proveedores: {e}")
            return False

# -------------------------------------------------------------------
# Proveedores (nuevo)
# -------------------------------------------------------------------
class SuppliersAPI:
    @staticmethod
    def get_all() -> Optional[List[Dict[str, Any]]]:
        if not supabase: return None
        try:
            return supabase.table("suppliers").select("*").order("id").execute().data
        except Exception as e:
            print(f"Error obteniendo proveedores: {e}")
            return None

    @staticmethod
    def insert(supplier_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase: return None
        try:
            supplier_data.pop("id", None)
            response = supabase.table("suppliers").insert(supplier_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error insertando proveedor: {e}")
            return None

    @staticmethod
    def update(supplier_id: int, supplier_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase: return None
        try:
            supplier_data.pop("id", None)
            response = supabase.table("suppliers").update(supplier_data).eq("id", supplier_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando proveedor: {e}")
            return None

    @staticmethod
    def delete(supplier_ids: List[int]) -> bool:
        if not supabase: return False
        try:
            supabase.table("suppliers").delete().in_("id", supplier_ids).execute()
            return True
        except Exception as e:
            print(f"Error eliminando proveedores: {e}")
            return False

# -------------------------------------------------------------------
# Contratos de Arrendamiento
# -------------------------------------------------------------------
class LeaseContractsAPI:
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        if not supabase: return []
        try:
            return supabase.table("lease_contracts").select("*").order("id").execute().data
        except Exception as e:
            print(f"Error obteniendo contratos de arrendamiento: {e}")
            return []

    @staticmethod
    def insert(contract_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase: return None
        try:
            contract_data.pop("id", None)
            response = supabase.table("lease_contracts").insert(contract_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error insertando contrato de arrendamiento: {e}")
            return None

    @staticmethod
    def update(contract_id: int, contract_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase: return None
        try:
            contract_data.pop("id", None)
            response = supabase.table("lease_contracts").update(contract_data).eq("id", contract_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando contrato de arrendamiento: {e}")
            return None

    @staticmethod
    def delete(contract_ids: List[int]) -> bool:
        if not supabase: return False
        try:
            supabase.table("lease_contracts").delete().in_("id", contract_ids).execute()
            return True
        except Exception as e:
            print(f"Error eliminando contratos de arrendamiento: {e}")
            return False

# -------------------------------------------------------------------
# Contratos de Adhesión
# -------------------------------------------------------------------
class AdhesionContractsAPI:
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        if not supabase: return []
        try:
            return supabase.table("adhesion_contracts").select("*").order("id").execute().data
        except Exception as e:
            print(f"Error obteniendo contratos de adhesión: {e}")
            return []

    @staticmethod
    def insert(contract_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase: return None
        try:
            contract_data.pop("id", None)
            response = supabase.table("adhesion_contracts").insert(contract_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error insertando contrato de adhesión: {e}")
            return None

    @staticmethod
    def update(contract_id: int, contract_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase: return None
        try:
            contract_data.pop("id", None)
            response = supabase.table("adhesion_contracts").update(contract_data).eq("id", contract_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando contrato de adhesión: {e}")
            return None

    @staticmethod
    def delete(contract_ids: List[int]) -> bool:
        if not supabase: return False
        try:
            supabase.table("adhesion_contracts").delete().in_("id", contract_ids).execute()
            return True
        except Exception as e:
            print(f"Error eliminando contratos de adhesión: {e}")
            return False

# -------------------------------------------------------------------
# Proveedores de Arrendamiento
# -------------------------------------------------------------------
class LeasingSuppliersAPI:
    @staticmethod
    def get_all() -> Optional[List[Dict[str, Any]]]:
        if not supabase: return None
        try:
            return supabase.table("leasing_suppliers").select("*").order("id").execute().data
        except Exception as e:
            print(f"Error obteniendo proveedores de arrendamiento: {e}")
            return None

    @staticmethod
    def insert(supplier_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase: return None
        try:
            supplier_data.pop("id", None)
            response = supabase.table("leasing_suppliers").insert(supplier_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error insertando proveedor de arrendamiento: {e}")
            return None

    @staticmethod
    def update(supplier_id: int, supplier_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase: return None
        try:
            supplier_data.pop("id", None)
            response = supabase.table("leasing_suppliers").update(supplier_data).eq("id", supplier_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando proveedor de arrendamiento: {e}")
            return None

    @staticmethod
    def delete(supplier_ids: List[int]) -> bool:
        if not supabase: return False
        try:
            supabase.table("leasing_suppliers").delete().in_("id", supplier_ids).execute()
            return True
        except Exception as e:
            print(f"Error eliminando proveedores de arrendamiento: {e}")
            return False

# -------------------------------------------------------------------
# Proveedores de Adhesión
# -------------------------------------------------------------------
class AdhesionSuppliersAPI:
    @staticmethod
    def get_all() -> Optional[List[Dict[str, Any]]]:
        if not supabase: return None
        try:
            return supabase.table("adhesion_suppliers").select("*").order("id").execute().data
        except Exception as e:
            print(f"Error obteniendo proveedores de adhesión: {e}")
            return None

    @staticmethod
    def insert(supplier_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase: return None
        try:
            supplier_data.pop("id", None)
            response = supabase.table("adhesion_suppliers").insert(supplier_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error insertando proveedor de adhesión: {e}")
            return None

    @staticmethod
    def update(supplier_id: int, supplier_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not supabase: return None
        try:
            supplier_data.pop("id", None)
            response = supabase.table("adhesion_suppliers").update(supplier_data).eq("id", supplier_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error actualizando proveedor de adhesión: {e}")
            return None

    @staticmethod
    def delete(supplier_ids: List[int]) -> bool:
        if not supabase: return False
        try:
            supabase.table("adhesion_suppliers").delete().in_("id", supplier_ids).execute()
            return True
        except Exception as e:
            print(f"Error eliminando proveedores de adhesión: {e}")
            return False
        
# -------------------------------------------------------------------
# Usuarios administradores del área comercial
# -------------------------------------------------------------------
class CommercialAdminUserAPI:
    @staticmethod
    def authenticate(username: str, password: str) -> Optional[Dict[str, Any]]:
        if not supabase:
            return None
        try:
            response = supabase.table("commercial_admin_users").select("*").eq("username", username).eq("password", password).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error en autenticación de admin comercial: {e}")
            return None