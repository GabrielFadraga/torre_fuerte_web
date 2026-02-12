# TFuerte/api/admin_rm_api.py
import os
import dotenv
from supabase import create_client
from typing import Dict, Any, List

dotenv.load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

try:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente de Supabase para AdminRM creado exitosamente")
except Exception as e:
    print(f"❌ Error al crear cliente de Supabase: {e}")
    supabase_client = None

class AdminRMApi:
    """API para autenticación de administradores de recursos y materiales"""
    
    @staticmethod
    def sign_in(user: str, password: str):
        """Verifica credenciales en tabla Admin"""
        try:
            if supabase_client is None:
                return {"success": False, "error": "Cliente no disponible"}
            
            print(f"🔑 Verificando admin RM: {user}")
            
            response = supabase_client.table("Admin")\
                .select("*")\
                .eq("usuario", user)\
                .eq("password", password)\
                .execute()
            
            if response.data and len(response.data) > 0:
                print(f"✅ Admin RM autenticado: {user}")
                return {
                    "success": True,
                    "user": response.data[0],
                    "error": None
                }
            else:
                print("❌ Credenciales incorrectas")
                return {
                    "success": False,
                    "user": None,
                    "error": "Usuario o contraseña incorrectos"
                }
                
        except Exception as e:
            print(f"❌ Error en autenticación admin RM: {e}")
            return {"success": False, "user": None, "error": str(e)}
    
    @staticmethod
    def get_admin_by_rol(rol: str) -> Dict[str, Any]:
        """Obtiene admin por rol (tecnica, admin, logistica)"""
        try:
            if supabase_client is None:
                return {}
            
            response = supabase_client.table("Admin")\
                .select("*")\
                .eq("rol", rol)\
                .execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            print(f"❌ Error obteniendo admin por rol {rol}: {e}")
            return {}
    
    @staticmethod
    def get_all_admins() -> List[Dict[str, Any]]:
        """Obtiene todos los administradores"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("Admin").select("*").execute()
            return response.data
        except Exception as e:
            print(f"❌ Error obteniendo admins: {e}")
            return []