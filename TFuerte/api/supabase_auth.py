import os
import dotenv
from supabase import create_client, Client
from typing import Dict, Any

# Cargar variables de entorno - MISMO FORMATO QUE TU CÓDIGO FUNCIONAL
dotenv.load_dotenv()

# Obtener credenciales - USA SUPABASE_KEY COMO EN TU CÓDIGO
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")  # Nota: tu .env debe tener SUPABASE_KEY

# Crear cliente de Supabase - GLOBAL Y ÚNICO
try:
    # Este es el cliente GLOBAL que usaremos en TODA la aplicación
    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # CRUCIAL: Habilitar persistencia de sesión para guardar el token
    supabase_client.auth._persist_session = True
    
    print("✅ Cliente de Supabase creado exitosamente")
    print(f"   URL: {SUPABASE_URL}")
    print(f"   Key: {'*' * 20}...{SUPABASE_KEY[-5:] if SUPABASE_KEY and len(SUPABASE_KEY) > 5 else '***'}")
    
except Exception as e:
    print(f"❌ Error al crear cliente de Supabase: {e}")
    supabase_client = None

class SupabaseAuth:
    """Clase para manejar autenticación con Supabase"""
    
    @staticmethod
    def sign_up(email: str, password: str) -> Dict[str, Any]:
        """Registrar nuevo usuario"""
        try:
            if supabase_client is None:
                return {"error": "Cliente de Supabase no disponible", "success": False}
            
            print(f"📝 Registrando usuario: {email}")
            response = supabase_client.auth.sign_up({
                "email": email,
                "password": password,
            })
            
            return {
                "success": True,
                "user": response.user,
                "session": response.session,
                "error": None
            }
            
        except Exception as e:
            print(f"❌ Error al registrar usuario: {e}")
            return {"error": str(e), "success": False}
    
    @staticmethod
    def sign_in(email: str, password: str) -> Dict[str, Any]:
        """Iniciar sesión"""
        try:
            if supabase_client is None:
                return {"error": "Cliente de Supabase no disponible", "success": False}
            
            print(f"🔑 Intentando login: {email}")
            response = supabase_client.auth.sign_in_with_password({
                "email": email,
                "password": password,
            })
            
            print(f"✅ Login exitoso. Usuario: {response.user.email}")
            print(f"✅ Token guardado en: localStorage (persist_session=True)")
            
            return {
                "success": True,
                "user": response.user,
                "session": response.session,
                "error": None
            }
            
        except Exception as e:
            print(f"❌ Error al iniciar sesión: {e}")
            return {"error": str(e), "success": False}
    
    @staticmethod
    def sign_out() -> Dict[str, Any]:
        """Cerrar sesión"""
        try:
            if supabase_client is None:
                return {"error": "Cliente de Supabase no disponible", "success": False}
            
            response = supabase_client.auth.sign_out()
            return {"success": True, "error": None}
            
        except Exception as e:
            print(f"❌ Error al cerrar sesión: {e}")
            return {"error": str(e), "success": False}
    
    @staticmethod
    def get_current_user():
        """Obtiene el usuario actual del token almacenado"""
        try:
            if supabase_client is None:
                print("❌ Cliente de Supabase no disponible")
                return None
            
            # Esta función lee el token del localStorage del navegador
            response = supabase_client.auth.get_user()
            
            if response and hasattr(response, 'user') and response.user:
                print(f"✅ Usuario obtenido de token persistente: {response.user.email}")
                return response.user
            else:
                print("⚠️  No hay usuario en la sesión persistente")
                return None
                
        except Exception as e:
            print(f"❌ Error obteniendo usuario: {e}")
            return None