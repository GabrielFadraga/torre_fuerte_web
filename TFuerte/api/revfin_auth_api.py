# TFuerte/api/revfin_auth_api.py
import os
import dotenv
from supabase import create_client

dotenv.load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

try:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente de Supabase para RevFin creado exitosamente")
except Exception as e:
    print(f"❌ Error al crear cliente de Supabase: {e}")
    supabase_client = None

class RevFinAuthAPI:
    """API para autenticación de revisores de financiamiento"""
    
    @staticmethod
    def sign_in(user: str, password: str):
        """Verifica credenciales en tabla RevFin"""
        try:
            if supabase_client is None:
                return {"success": False, "error": "Cliente no disponible"}
            
            print(f"🔑 Verificando revisor financiero: {user}")
            
            response = supabase_client.table("RevFin")\
                .select("*")\
                .eq("usuario", user)\
                .eq("clave", password)\
                .execute()
            
            if response.data and len(response.data) > 0:
                print(f"✅ Revisor financiero autenticado: {user}")
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
            print(f"❌ Error en autenticación revisor financiero: {e}")
            return {"success": False, "user": None, "error": str(e)}