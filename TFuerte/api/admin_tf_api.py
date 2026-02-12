import os
import dotenv
from supabase import create_client
from typing import Dict, Any

dotenv.load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

try:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente de Supabase para AdminTF creado exitosamente")
except Exception as e:
    print(f"❌ Error al crear cliente de Supabase: {e}")
    supabase_client = None

class AdminTFApi:
    """API para autenticación de administradores del sistema de almacén"""
    
    @staticmethod
    def sign_in(user: str, password: str):
        """Verifica credenciales en tabla AdminTF"""
        try:
            if supabase_client is None:
                return {"success": False, "error": "Cliente no disponible"}
            
            print(f"🔑 Verificando admin TF: {user}")
            
            response = supabase_client.table("AdminTF")\
                .select("*")\
                .eq("usuario", user)\
                .eq("clave", password)\
                .execute()
            
            if response.data and len(response.data) > 0:
                print(f"✅ Admin TF autenticado: {user}")
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
            print(f"❌ Error en autenticación admin TF: {e}")
            return {"success": False, "user": None, "error": str(e)}
    
    @staticmethod
    def get_all_admins() -> list:
        """Obtiene todos los administradores"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("AdminTF").select("*").execute()
            return response.data
        except Exception as e:
            print(f"❌ Error obteniendo admins TF: {e}")
            return []