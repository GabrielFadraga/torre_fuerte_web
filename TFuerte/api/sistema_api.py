# TFuerte/api/sistema_api.py
import os
import dotenv
from supabase import create_client
from typing import Dict, Any, List

dotenv.load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

try:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente de Supabase para Sistema creado exitosamente")
except Exception as e:
    print(f"❌ Error al crear cliente de Supabase: {e}")
    supabase_client = None

class SistemaAPI:
    """API para comunicación entre diferentes sistemas"""
    
    @staticmethod
    def get_producto_por_descripcion(descripcion: str) -> List[Dict[str, Any]]:
        """Busca productos en el almacén por descripción"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("Almacen").select("*").ilike("Descripcion del producto", f"%{descripcion}%").execute()
            return response.data
        except Exception as e:
            print(f"❌ Error al buscar producto: {e}")
            return []
    
    @staticmethod
    def get_producto_por_codigo(codigo: str) -> List[Dict[str, Any]]:
        """Busca productos en el almacén por código"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("Almacen").select("*").eq("Codigo", codigo).execute()
            return response.data
        except Exception as e:
            print(f"❌ Error al buscar producto por código: {e}")
            return []
    
    @staticmethod
    def actualizar_solicitud_aprobada(solicitud_id: int, datos_aprobacion: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza una solicitud como aprobada"""
        try:
            if supabase_client is None:
                return None
            
            datos_aprobacion["estado"] = "aprobada"
            datos_aprobacion["fecha_aprobacion"] = "now()"
            
            response = supabase_client.table("Solicitudes").update(datos_aprobacion).eq("id", solicitud_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"❌ Error al aprobar solicitud: {e}")
            return None
    
    @staticmethod
    def rechazar_solicitud(solicitud_id: int, motivo: str = None) -> bool:
        """Marca una solicitud como rechazada"""
        try:
            if supabase_client is None:
                return False
            
            datos = {"estado": "rechazada"}
            if motivo:
                datos["observacion"] = f"RECHAZADA: {motivo}"
            
            response = supabase_client.table("Solicitudes").update(datos).eq("id", solicitud_id).execute()
            return True if response.data else False
        except Exception as e:
            print(f"❌ Error al rechazar solicitud: {e}")
            return False
    
    @staticmethod
    def get_solicitudes_pendientes() -> List[Dict[str, Any]]:
        """Obtiene todas las solicitudes pendientes"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("Solicitudes").select("*").eq("estado", "pendiente").order("id", desc=True).execute()
            return response.data
        except Exception as e:
            print(f"❌ Error al obtener solicitudes pendientes: {e}")
            return []
    
    @staticmethod
    def get_solicitudes_aprobadas() -> List[Dict[str, Any]]:
        """Obtiene todas las solicitudes aprobadas"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("Solicitudes").select("*").eq("estado", "aprobada").order("fecha_aprobacion", desc=True).execute()
            return response.data
        except Exception as e:
            print(f"❌ Error al obtener solicitudes aprobadas: {e}")
            return []