# TFuerte/api/solicitudes_rm_api.py
import os
import dotenv
from supabase import create_client
from typing import List, Dict, Any
from datetime import datetime

dotenv.load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

try:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente de Supabase para SolicitudesRM creado exitosamente")
except Exception as e:
    print(f"❌ Error al crear cliente de Supabase: {e}")
    supabase_client = None

class SolicitudesRMApi:
    @staticmethod
    def create_solicitud_rm(solicitud_data: Dict[str, Any], recursos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Crea una solicitud RM con múltiples recursos.
        
        Args:
            solicitud_data: Datos generales (Centro costo, Fecha, Orden trabajo, solicitante_id)
            recursos: Lista de recursos [{"descripcion": "...", "unidad_medida": "...", "cantidad": 1, "observaciones": "..."}]
        """
        try:
            if supabase_client is None:
                return None
            
            print(f"📝 Creando solicitud RM con {len(recursos)} recursos")
            
            # Validar campos requeridos de la solicitud principal
            required_fields = ["Centro costo", "Fecha", "Orden trabajo", "solicitante_id"]
            for field in required_fields:
                if field not in solicitud_data:
                    print(f"❌ Campo requerido faltante: {field}")
                    return None
            
            # Validar que haya al menos un recurso
            if not recursos:
                print(f"❌ Debe haber al menos un recurso")
                return None
            
            # Validar cada recurso
            for i, recurso in enumerate(recursos):
                if "descripcion" not in recurso or "cantidad" not in recurso:
                    print(f"❌ Recurso {i+1}: Faltan campos requeridos")
                    return None
                try:
                    # Convertir cantidad a float (permite decimales)
                    recursos[i]["cantidad"] = float(recurso["cantidad"])
                except:
                    print(f"❌ Recurso {i+1}: Cantidad inválida: {recurso['cantidad']}")
                    return None
            
            # Datos de la solicitud principal (sin campos de recursos)
            solicitud_principal = {
                "Centro costo": solicitud_data["Centro costo"],
                "Fecha": solicitud_data["Fecha"],
                "Orden trabajo": solicitud_data["Orden trabajo"],
                "solicitante_id": solicitud_data["solicitante_id"],
                "fecha_creacion": datetime.now().isoformat(),
                "estado": "pendiente",
                "aprobado_tecnica": False,
                "aprobado_admin": False,
                "aprobado_logistica": False
            }
            
            # Insertar solicitud principal
            response = supabase_client.table("SolicitudesRM").insert(solicitud_principal).execute()
            
            if not response.data:
                print("❌ No se pudo crear la solicitud principal")
                return None
            
            solicitud_id = response.data[0]["id"]
            print(f"✅ Solicitud principal creada con ID: {solicitud_id}")
            
            # Insertar recursos
            recursos_insertados = []
            for i, recurso in enumerate(recursos, 1):
                recurso_data = {
                    "solicitud_id": solicitud_id,
                    "numero_item": i,
                    "descripcion": recurso["descripcion"],
                    "unidad_medida": recurso.get("unidad_medida", ""),
                    "cantidad": recurso["cantidad"],
                    "observaciones": recurso.get("observaciones", "")
                }
                
                recurso_response = supabase_client.table("RecursosSolicitados").insert(recurso_data).execute()
                
                if recurso_response.data:
                    recursos_insertados.append(recurso_response.data[0])
                    print(f"  ✅ Recurso {i}: {recurso['descripcion']}")
                else:
                    print(f"  ❌ Error al insertar recurso {i}")
            
            # Combinar datos de respuesta
            resultado = response.data[0]
            resultado["recursos"] = recursos_insertados
            
            return resultado
                
        except Exception as e:
            print(f"❌ ERROR en create_solicitud_rm: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def get_solicitudes_rm_by_solicitante(solicitante_id: int) -> List[Dict[str, Any]]:
        """Obtiene todas las solicitudes de un solicitante con sus recursos"""
        try:
            if supabase_client is None:
                return []
            
            # Obtener solicitudes principales
            response = supabase_client.table("SolicitudesRM")\
                .select("*")\
                .eq("solicitante_id", solicitante_id)\
                .order("fecha_creacion", desc=True)\
                .execute()
            
            # Para cada solicitud, obtener sus recursos
            solicitudes_con_recursos = []
            for solicitud in response.data:
                recursos = SolicitudesRMApi.get_recursos_por_solicitud(solicitud["id"])
                solicitud["recursos"] = recursos
                solicitudes_con_recursos.append(solicitud)
            
            return solicitudes_con_recursos
        except Exception as e:
            print(f"❌ Error al obtener solicitudes RM: {e}")
            return []
    
    @staticmethod
    def get_solicitudes_rm_pendientes_tecnica() -> List[Dict[str, Any]]:
        """Obtiene solicitudes pendientes de aprobación técnica con sus recursos"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("SolicitudesRM")\
                .select("*")\
                .eq("estado", "pendiente")\
                .order("fecha_creacion", desc=True)\
                .execute()
            
            # Obtener recursos para cada solicitud
            solicitudes_con_recursos = []
            for solicitud in response.data:
                recursos = SolicitudesRMApi.get_recursos_por_solicitud(solicitud["id"])
                solicitud["recursos"] = recursos
                solicitudes_con_recursos.append(solicitud)
            
            return solicitudes_con_recursos
        except Exception as e:
            print(f"❌ Error al obtener solicitudes RM pendientes: {e}")
            return []
    
    @staticmethod
    def get_solicitudes_rm_pendientes_admin() -> List[Dict[str, Any]]:
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("SolicitudesRM")\
                .select("*")\
                .eq("aprobado_tecnica", True)\
                .eq("aprobado_admin", False)\
                .eq("estado", "aprobado_tecnica")\
                .order("fecha_aprobacion_tecnica", desc=True)\
                .execute()
            
            # Obtener recursos para cada solicitud
            solicitudes_con_recursos = []
            for solicitud in response.data:
                recursos = SolicitudesRMApi.get_recursos_por_solicitud(solicitud["id"])
                solicitud["recursos"] = recursos
                solicitudes_con_recursos.append(solicitud)
            
            return solicitudes_con_recursos
        except Exception as e:
            print(f"❌ Error al obtener solicitudes RM pendientes admin: {e}")
            return []
    
    @staticmethod
    def get_solicitudes_rm_pendientes_logistica() -> List[Dict[str, Any]]:
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("SolicitudesRM")\
                .select("*")\
                .eq("aprobado_tecnica", True)\
                .eq("aprobado_admin", True)\
                .eq("aprobado_logistica", False)\
                .eq("estado", "aprobado_admin")\
                .order("fecha_aprobacion_admin", desc=True)\
                .execute()
            
            # Obtener recursos para cada solicitud
            solicitudes_con_recursos = []
            for solicitud in response.data:
                recursos = SolicitudesRMApi.get_recursos_por_solicitud(solicitud["id"])
                solicitud["recursos"] = recursos
                solicitudes_con_recursos.append(solicitud)
            
            return solicitudes_con_recursos
        except Exception as e:
            print(f"❌ Error al obtener solicitudes RM pendientes logística: {e}")
            return []
    
    @staticmethod
    def get_solicitudes_rm_completadas() -> List[Dict[str, Any]]:
        """Obtiene todas las solicitudes completadas con sus recursos"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("SolicitudesRM")\
                .select("*")\
                .eq("aprobado_logistica", True)\
                .eq("estado", "completada")\
                .order("fecha_aprobacion_logistica", desc=True)\
                .execute()
            
            # Obtener recursos para cada solicitud
            solicitudes_con_recursos = []
            for solicitud in response.data:
                recursos = SolicitudesRMApi.get_recursos_por_solicitud(solicitud["id"])
                solicitud["recursos"] = recursos
                solicitudes_con_recursos.append(solicitud)
            
            return solicitudes_con_recursos
        except Exception as e:
            print(f"❌ Error al obtener solicitudes RM completadas: {e}")
            return []
    
    @staticmethod
    def get_recursos_por_solicitud(solicitud_id: int) -> List[Dict[str, Any]]:
        """Obtiene todos los recursos de una solicitud específica"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("RecursosSolicitados")\
                .select("*")\
                .eq("solicitud_id", solicitud_id)\
                .order("numero_item")\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"❌ Error al obtener recursos por solicitud: {e}")
            return []
    
    @staticmethod
    def get_solicitud_rm_by_id(solicitud_id: int) -> Dict[str, Any]:
        """Obtiene una solicitud específica con todos sus recursos"""
        try:
            if supabase_client is None:
                return {}
            
            # Obtener solicitud principal
            response = supabase_client.table("SolicitudesRM")\
                .select("*")\
                .eq("id", solicitud_id)\
                .execute()
            
            if not response.data:
                return {}
            
            solicitud = response.data[0]
            
            # Obtener recursos
            recursos = SolicitudesRMApi.get_recursos_por_solicitud(solicitud_id)
            solicitud["recursos"] = recursos
            
            return solicitud
        except Exception as e:
            print(f"❌ Error al obtener solicitud RM por ID: {e}")
            return {}
    
    # Los métodos de aprobación no cambian, siguen trabajando con SolicitudesRM
    @staticmethod
    def aprobar_por_tecnica(solicitud_id: int, admin_usuario: str) -> Dict[str, Any]:
        try:
            if supabase_client is None:
                return None
            
            updates = {
                "aprobado_tecnica": True,
                "fecha_aprobacion_tecnica": datetime.now().isoformat(),
                "estado": "aprobado_tecnica"
            }
            
            response = supabase_client.table("SolicitudesRM")\
                .update(updates)\
                .eq("id", solicitud_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"❌ Error al aprobar por técnica: {e}")
            return None
    
    @staticmethod
    def aprobar_por_admin(solicitud_id: int, admin_usuario: str) -> Dict[str, Any]:
        try:
            if supabase_client is None:
                return None
            
            updates = {
                "aprobado_admin": True,
                "fecha_aprobacion_admin": datetime.now().isoformat(),
                "estado": "aprobado_admin"
            }
            
            response = supabase_client.table("SolicitudesRM")\
                .update(updates)\
                .eq("id", solicitud_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"❌ Error al aprobar por admin: {e}")
            return None
    
    @staticmethod
    def aprobar_por_logistica(solicitud_id: int, admin_usuario: str) -> Dict[str, Any]:
        try:
            if supabase_client is None:
                return None
            
            updates = {
                "aprobado_logistica": True,
                "fecha_aprobacion_logistica": datetime.now().isoformat(),
                "estado": "completada"
            }
            
            response = supabase_client.table("SolicitudesRM")\
                .update(updates)\
                .eq("id", solicitud_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"❌ Error al aprobar por logística: {e}")
            return None
    
    @staticmethod
    def rechazar_solicitud_rm(solicitud_id: int, motivo: str = None) -> bool:
        try:
            if supabase_client is None:
                return False
            
            updates = {"estado": "rechazada"}
            if motivo:
                updates["Observaciones"] = f"RECHAZADA: {motivo}"
            
            response = supabase_client.table("SolicitudesRM")\
                .update(updates)\
                .eq("id", solicitud_id)\
                .execute()
            return True if response.data else False
        except Exception as e:
            print(f"❌ Error al rechazar solicitud RM: {e}")
            return False