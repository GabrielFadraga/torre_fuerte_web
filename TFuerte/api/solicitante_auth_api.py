import os
import dotenv
from supabase import create_client
from typing import List, Dict, Any

# Cargar variables de entorno
dotenv.load_dotenv()

# Obtener credenciales
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Crear cliente de Supabase
try:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente de Supabase para Autenticación creado exitosamente")
except Exception as e:
    print(f"❌ Error al crear cliente de Supabase: {e}")
    supabase_client = None

class SolicitanteAuthAPI:
    """API para operaciones de autenticación de solicitantes"""
    
    @staticmethod
    def sign_in(usuario: str, clave: str) -> Dict[str, Any]:
        """Autentica un solicitante y devuelve sus datos incluyendo id_custom"""
        try:
            if supabase_client is None:
                return {"success": False, "error": "Cliente no disponible"}
            
            print(f"🔍 Buscando solicitante: {usuario}")
            
            # IMPORTANTE: Incluir id_custom en la consulta
            response = supabase_client.table("Solicitantes")\
                .select("id, usuario, id_custom")\
                .eq("usuario", usuario)\
                .eq("clave", clave)\
                .execute()
            
            print(f"📡 Respuesta de autenticación: {response.data}")
            
            if response.data and len(response.data) > 0:
                user = response.data[0]
                print(f"✅ Usuario encontrado: {user}")
                return {
                    "success": True,
                    "user": user,
                    "error": None
                }
            else:
                print("❌ Credenciales incorrectas")
                return {
                    "success": False,
                    "user": None,
                    "error": "Credenciales incorrectas"
                }
                
        except Exception as e:
            print(f"❌ Error en sign_in: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_all_solicitantes() -> List[Dict[str, Any]]:
        """Obtiene todos los solicitantes"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("Solicitantes").select("*").execute()
            return response.data
        except Exception as e:
            print(f"❌ Error obteniendo solicitantes: {e}")
            return []