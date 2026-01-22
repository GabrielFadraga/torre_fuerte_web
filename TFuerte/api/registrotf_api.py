# TFuerte/api/registrotf_api.py
import os
import dotenv
from supabase import create_client
from typing import Dict, Any

# Cargar variables de entorno
dotenv.load_dotenv()

# Obtener credenciales
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Crear cliente de Supabase
try:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente de Supabase para RegistroTF creado exitosamente")
except Exception as e:
    print(f"❌ Error al crear cliente de Supabase para RegistroTF: {e}")
    supabase_client = None

class RegistroTFAPI:
    """API para operaciones en la tabla RegistroTF"""
    
    @staticmethod
    def insert_registro(registro_data: Dict[str, Any]) -> Dict[str, Any]:
        """Inserta un nuevo registro en la tabla 'RegistroTF'"""
        try:
            if supabase_client is None:
                return None
            
            print(f"📝 Insertando datos en RegistroTF...")
            
            # Validar campos requeridos
            if "Producto" not in registro_data or not registro_data["Producto"]:
                print("❌ Error: El campo 'Producto' es requerido para RegistroTF")
                return None
            
            # Asegurar tipos de datos básicos
            if "Cant E" in registro_data and registro_data["Cant E"]:
                try:
                    registro_data["Cant E"] = int(registro_data["Cant E"])
                except:
                    registro_data["Cant E"] = 0
            else:
                registro_data["Cant E"] = 0
            
            if "Cant S" in registro_data and registro_data["Cant S"]:
                try:
                    registro_data["Cant S"] = int(registro_data["Cant S"])
                except:
                    registro_data["Cant S"] = 0
            else:
                registro_data["Cant S"] = 0
            
            # Los demás campos (Recibe, Destino, Cliente) pueden ser texto o None
            print(f"📦 Datos para RegistroTF: {registro_data}")
            
            response = supabase_client.table("RegistroTF").insert(registro_data).execute()
            
            if response.data:
                print(f"✅ RegistroTF insertado correctamente")
                return response.data[0]
            else:
                print("⚠️  No se recibieron datos en la respuesta de RegistroTF")
                return None
        except Exception as e:
            print(f"❌ Error al insertar datos en RegistroTF: {e}")
            return None
    
    @staticmethod
    def get_all_registros() -> list[Dict[str, Any]]:
        """Obtiene todos los registros de la tabla 'RegistroTF'"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("RegistroTF").select("*").order("id", desc=True).execute()
            return response.data
        except Exception as e:
            print(f"❌ Error obteniendo registros: {e}")
            return []