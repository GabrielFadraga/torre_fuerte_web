# TFuerte/api/registrotf_api.py
import os
import dotenv
from supabase import create_client
from typing import Dict, Any
from TFuerte.api.solicitudes_api import SolicitudesAPI

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

    def load_data(self):
        self.loading = True
        yield

        # Cargar RegistroTF
        registro = RegistroTFAPI.get_all_registros()
        # Asegurar que siempre sea una lista
        self.registro_data = registro if isinstance(registro, list) else []
        self.registro_filtered = self.registro_data.copy()  # copia explícita

        # Cargar Solicitudes
        solicitudes = SolicitudesAPI.get_all_solicitudes()
        self.solicitudes_data = solicitudes if isinstance(solicitudes, list) else []
        self.solicitudes_pendientes = [
            s for s in self.solicitudes_data
            if s.get("estado") == "pendiente"
        ]
        self.calculate_solicitudes_pagination()

        self.loading = False
    
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
        try:
            if supabase_client is None:
                print("❌ RegistroTFAPI: cliente no disponible")
                return []
            response = supabase_client.table("RegistroTF").select("*").order("id", desc=True).execute()
            print(f"✅ RegistroTFAPI: {len(response.data)} registros obtenidos")
            return response.data
        except Exception as e:
            print(f"❌ RegistroTFAPI: error obteniendo registros - {e}")
            import traceback
            traceback.print_exc()
            return []