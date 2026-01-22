# TFuerte/api/admin_auth_api.py
import os
import dotenv
from supabase import create_client

# Cargar variables de entorno
dotenv.load_dotenv()

# Obtener credenciales
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Crear cliente de Supabase
try:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente de Supabase para AdminAuth creado exitosamente")
except Exception as e:
    print(f"❌ Error al crear cliente de Supabase: {e}")
    supabase_client = None

class AdminAuthAPI:
    """API para autenticación de administradores contra tabla Autorizacion"""
    
    @staticmethod
    def sign_in(user: str, password: str):
        """Verifica credenciales en tabla Autorizacion"""
        try:
            if supabase_client is None:
                return {"success": False, "error": "Cliente no disponible"}
            
            print(f"🔑 Verificando admin: {user}")
            
            response = supabase_client.table("Autorizacion")\
                .select("*")\
                .eq("user", user)\
                .eq("password", password)\
                .execute()
            
            if response.data and len(response.data) > 0:
                print(f"✅ Admin autenticado: {user}")
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
            print(f"❌ Error en autenticación admin: {e}")
            return {"success": False, "user": None, "error": str(e)}