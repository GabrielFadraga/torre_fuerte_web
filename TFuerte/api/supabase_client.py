# TFuerte/api/supabase_client.py
import os
import dotenv
from supabase import create_client

# Cargar variables de entorno
dotenv.load_dotenv()

# Obtener credenciales
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Variable global para el cliente
_supabase_instance = None

def get_supabase_client():
    """Obtener la instancia única del cliente Supabase"""
    global _supabase_instance
    
    if _supabase_instance is None:
        try:
            _supabase_instance = create_client(SUPABASE_URL, SUPABASE_KEY)
            # IMPORTANTE: Habilitar persistencia de sesión
            _supabase_instance.auth._persist_session = True
            print("✅ Cliente Supabase único creado exitosamente")
        except Exception as e:
            print(f"❌ Error al crear cliente de Supabase: {e}")
            raise
    
    return _supabase_instance