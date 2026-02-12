import os
import dotenv
from supabase import create_client
from typing import List, Dict, Any
from datetime import datetime

# Cargar variables de entorno
dotenv.load_dotenv()

# Obtener credenciales
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Crear cliente de Supabase
try:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente de Supabase para Solicitudes creado exitosamente")
except Exception as e:
    print(f"❌ Error al crear cliente de Supabase: {e}")
    supabase_client = None

class SolicitudesAPI:
    """API para operaciones en la tabla Solicitudes"""
    
    @staticmethod
    def get_all_solicitudes() -> List[Dict[str, Any]]:
        """Obtiene todas las solicitudes"""
        try:
            if supabase_client is None:
                print("❌ Cliente de Supabase no disponible")
                return []
            
            print("🔍 Obteniendo todas las solicitudes...")
            response = supabase_client.table("Solicitudes").select("*").order("fecha_solicitud", desc=True).execute()
            print(f"✅ {len(response.data)} solicitudes obtenidas")
            return response.data
        except Exception as e:
            print(f"❌ Error obteniendo solicitudes: {e}")
            return []
    
    @staticmethod
    def get_solicitudes_by_solicitante(solicitante_id: int) -> List[Dict[str, Any]]:
        """Obtiene solicitudes de un solicitante específico usando custom_id"""
        try:
            if supabase_client is None:
                print("❌ Cliente de Supabase no disponible")
                return []
            
            print(f"🔍 BUSCANDO SOLICITUDES PARA CUSTOM_ID: {solicitante_id}")
            
            # Consulta usando el campo custom que guarda el id_custom del solicitante
            response = supabase_client.table("Solicitudes")\
                .select("*")\
                .eq("custom", solicitante_id)\
                .order("fecha_solicitud", desc=True)\
                .execute()
            
            print(f"📡 ENCONTRADAS {len(response.data)} SOLICITUDES PARA CUSTOM_ID {solicitante_id}")
            
            # Debug: mostrar las primeras 3 solicitudes
            for i, solicitud in enumerate(response.data[:3]):
                print(f"  📄 {i+1}. ID: {solicitud.get('id')}, Descripción: {solicitud.get('Descripcion')[:30]}...")
            
            return response.data
            
        except Exception as e:
            print(f"❌ ERROR en get_solicitudes_by_solicitante para custom_id {solicitante_id}: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    @staticmethod
    def get_pendientes() -> List[Dict[str, Any]]:
        """Obtiene solo las solicitudes pendientes"""
        try:
            if supabase_client is None:
                print("❌ Cliente de Supabase no disponible")
                return []
            
            response = supabase_client.table("Solicitudes")\
                .select("*")\
                .eq("estado", "pendiente")\
                .order("fecha_solicitud", desc=True)\
                .execute()
            return response.data
        except Exception as e:
            print(f"❌ Error obteniendo solicitudes pendientes: {e}")
            return []
    
    @staticmethod
    def create_solicitud(solicitud_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una nueva solicitud"""
        try:
            if supabase_client is None:
                print("❌ Cliente de Supabase no disponible")
                return None
            
            print(f"📝 Creando solicitud con datos: {solicitud_data}")
            
            # Validar datos críticos
            required_fields = ["Descripcion", "Cantidad", "Destino", "custom"]
            for field in required_fields:
                if field not in solicitud_data:
                    print(f"❌ Campo requerido faltante: {field}")
                    return None
            
            # Asegurar tipos de datos
            if "Cantidad" in solicitud_data:
                try:
                    solicitud_data["Cantidad"] = int(solicitud_data["Cantidad"])
                except:
                    print(f"❌ Cantidad inválida: {solicitud_data['Cantidad']}")
                    return None
            
            # Agregar fecha si no está presente
            if "fecha_solicitud" not in solicitud_data:
                solicitud_data["fecha_solicitud"] = datetime.now().isoformat()
            
            # Asegurar estado
            if "estado" not in solicitud_data:
                solicitud_data["estado"] = "pendiente"
            
            print(f"📦 Insertando en Supabase: {solicitud_data}")
            
            response = supabase_client.table("Solicitudes").insert(solicitud_data).execute()
            
            if response.data and len(response.data) > 0:
                print(f"✅ Solicitud creada con ID: {response.data[0].get('id')}")
                return response.data[0]
            else:
                print("❌ No se recibió respuesta de Supabase")
                return None
                
        except Exception as e:
            print(f"❌ ERROR en create_solicitud: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def aprobar_solicitud(solicitud_id: int, admin_user: str, producto_id: int = None) -> Dict[str, Any]:
        """Aprueba una solicitud pendiente"""
        try:
            if supabase_client is None:
                return None
            
            updates = {
                "estado": "aprobada",
                "aprobado_por": admin_user,  # <-- CAMBIO IMPORTANTE: usar aprobado_por
                "fecha_resolucion": datetime.now().isoformat()
            }
            
            if producto_id:
                updates["producto_id"] = producto_id
            
            print(f"✅ Aprobando solicitud {solicitud_id} por {admin_user}")
            
            response = supabase_client.table("Solicitudes")\
                .update(updates)\
                .eq("id", solicitud_id)\
                .execute()
            
            if response.data:
                print(f"✅ Solicitud {solicitud_id} aprobada por {admin_user}")
                return response.data[0]
            else:
                print("⚠️ No se recibieron datos en la respuesta")
                return None
        except Exception as e:
            print(f"❌ Error aprobando solicitud: {e}")
            return None
    
    @staticmethod
    def rechazar_solicitud(solicitud_id: int, admin_user: str) -> Dict[str, Any]:
        """Rechaza una solicitud pendiente"""
        try:
            if supabase_client is None:
                return None
            
            updates = {
                "estado": "rechazada",
                "admin_responsable": admin_user,
                "fecha_resolucion": datetime.now().isoformat()
            }
            
            print(f"❌ Rechazando solicitud {solicitud_id} por {admin_user}")
            
            response = supabase_client.table("Solicitudes")\
                .update(updates)\
                .eq("id", solicitud_id)\
                .execute()
            
            if response.data:
                print(f"✅ Solicitud {solicitud_id} rechazada")
                return response.data[0]
            else:
                print("⚠️ No se recibieron datos en la respuesta")
                return None
        except Exception as e:
            print(f"❌ Error rechazando solicitud: {e}")
            return None
    
    @staticmethod
    def completar_solicitud(solicitud_id: int) -> Dict[str, Any]:
        """Marca una solicitud como completada (salida realizada)"""
        try:
            if supabase_client is None:
                return None
            
            updates = {
                "estado": "completada",
                "fecha_salida_realizada": datetime.now().isoformat()
            }
            
            response = supabase_client.table("Solicitudes")\
                .update(updates)\
                .eq("id", solicitud_id)\
                .execute()
            
            if response.data:
                print(f"✅ Solicitud {solicitud_id} marcada como completada")
                return response.data[0]
            else:
                print("⚠️ No se recibieron datos en la respuesta")
                return None
        except Exception as e:
            print(f"❌ Error marcando solicitud como completada: {e}")
            return None
    
    # TFuerte/api/solicitudes_api.py - Agregar este método

    @staticmethod
    def get_aprobado_por_solicitud(solicitud_id: int) -> str:
        """Obtiene el administrador que aprobó una solicitud"""
        try:
            if supabase_client is None:
                return ""
            
            response = supabase_client.table("Solicitudes")\
                .select("aprobado_por")\
                .eq("id", solicitud_id)\
                .execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0].get("aprobado_por", "")
            else:
                return ""
                
        except Exception as e:
            print(f"❌ Error obteniendo aprobado_por: {e}")
            return ""