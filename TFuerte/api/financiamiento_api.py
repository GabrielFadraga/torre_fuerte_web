# TFuerte/api/financiamiento_api.py - VERSIÓN CORREGIDA
import os
import dotenv
from supabase import create_client
from typing import List, Dict, Any
from datetime import datetime
import uuid

dotenv.load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

try:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente de Supabase para Financiamiento creado exitosamente")
except Exception as e:
    print(f"❌ Error al crear cliente de Supabase: {e}")
    supabase_client = None

class FinanciamientoApi:
    
    @staticmethod
    def get_precio_producto(tipo: str, descripcion: str) -> float:
        """Obtiene el precio base de un producto"""
        try:
            if supabase_client is None:
                return 0.0
            
            response = supabase_client.table("Precios")\
                .select("Precio")\
                .eq("Tipo", tipo)\
                .eq("Descripcion", descripcion)\
                .limit(1)\
                .execute()
            
            if response.data and len(response.data) > 0:
                return float(response.data[0]["Precio"])
            return 0.0
        except Exception as e:
            print(f"❌ Error obteniendo precio: {e}")
            return 0.0
    
    @staticmethod
    def create_solicitud_fin_multi(solicitudes_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Crea múltiples recursos en una solicitud de financiamiento - CORREGIDO"""
        try:
            if supabase_client is None:
                return []
            
            print(f"📝 Creando {len(solicitudes_data)} recursos de financiamiento")
            
            # Generar número de solicitud único
            numero_solicitud = f"FIN-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"
            
            # Preparar todos los datos para inserción
            datos_insertar = []
            for i, solicitud in enumerate(solicitudes_data):
                # Obtener precio base
                precio_base = FinanciamientoApi.get_precio_producto(
                    solicitud.get("Servicio", ""), 
                    solicitud.get("Descripcion", "")
                )
                
                # Calcular precio unitario (+25%)
                precio_unitario = precio_base * 1.25
                
                # Calcular importe
                cantidad = int(solicitud.get("Cantidad", 0))
                importe = precio_unitario * cantidad
                
                # Preparar datos del recurso
                recurso_data = {
                    "Area solicitante": solicitud.get("Area solicitante"),
                    "Fecha": solicitud.get("Fecha"),
                    "Servicio": solicitud.get("Servicio"),
                    "Numero de contrato/suplemento": solicitud.get("Numero de contrato/suplemento"),
                    "Orden de trabajo": solicitud.get("Orden de trabajo"),
                    "Descripcion": solicitud.get("Descripcion"),
                    "Cantidad": cantidad,
                    "Precio unitario": precio_unitario,
                    "Importe": importe,
                    "Total": importe,  # Temporal, luego se actualizará
                    "solicitante_id": solicitud.get("solicitante_id"),
                    "numero_solicitud": numero_solicitud,
                    "numero_item": i + 1,
                    "estado": "pendiente_revfin",
                    "fecha_creacion": datetime.now().isoformat()
                }
                datos_insertar.append(recurso_data)
            
            # Insertar TODOS los recursos en UNA sola operación
            response = supabase_client.table("Financiamiento").insert(datos_insertar).execute()
            
            if response.data:
                # Calcular y actualizar el total de la solicitud
                total_solicitud = sum([r.get("Importe", 0) for r in response.data])
                
                # Actualizar todos los registros con el total
                supabase_client.table("Financiamiento")\
                    .update({"Total": total_solicitud})\
                    .eq("numero_solicitud", numero_solicitud)\
                    .execute()
                
                print(f"✅ Solicitud {numero_solicitud} creada con {len(response.data)} recursos. Total: ${total_solicitud:.2f}")
                return response.data
            else:
                print("❌ No se pudo crear la solicitud")
                return []
                
        except Exception as e:
            print(f"❌ ERROR en create_solicitud_fin_multi: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    @staticmethod
    def get_solicitudes_fin_by_solicitante(solicitante_id: int) -> List[Dict[str, Any]]:
        """Obtiene todas las solicitudes de financiamiento de un solicitante"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("Financiamiento")\
                .select("*")\
                .eq("solicitante_id", solicitante_id)\
                .order("fecha_creacion", desc=True)\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"❌ Error al obtener solicitudes de financiamiento: {e}")
            return []
    
    @staticmethod
    def get_solicitudes_fin_pendientes_revfin() -> List[Dict[str, Any]]:
        """Obtiene solicitudes pendientes de revisión financiera"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("Financiamiento")\
                .select("*")\
                .eq("estado", "pendiente_revfin")\
                .order("fecha_creacion", desc=True)\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"❌ Error al obtener solicitudes pendientes de revfin: {e}")
            return []
    
    @staticmethod
    def get_solicitudes_fin_pendientes_admin() -> List[Dict[str, Any]]:
        """Obtiene solicitudes aprobadas por revfin y pendientes de admin"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("Financiamiento")\
                .select("*")\
                .eq("estado", "aprobado_revfin")\
                .eq("aprobado_admin", False)\
                .order("fecha_aprobacion_revfin", desc=True)\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"❌ Error al obtener solicitudes pendientes admin: {e}")
            return []
    
    @staticmethod
    def get_solicitud_fin_by_numero(numero_solicitud: str) -> List[Dict[str, Any]]:
        """Obtiene todos los recursos de una solicitud por número de solicitud"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("Financiamiento")\
                .select("*")\
                .eq("numero_solicitud", numero_solicitud)\
                .order("numero_item")\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"❌ Error al obtener solicitud por número: {e}")
            return []
    
    @staticmethod
    def get_total_solicitud_fin(numero_solicitud: str) -> float:
        """Calcula el total de una solicitud sumando todos los Importes"""
        try:
            recursos = FinanciamientoApi.get_solicitud_fin_by_numero(numero_solicitud)
            total = sum([r.get("Importe", 0) for r in recursos])
            return total
        except Exception as e:
            print(f"❌ Error calculando total de solicitud: {e}")
            return 0.0
    
    @staticmethod
    def aprobar_por_revfin(solicitud_id: int, revfin_usuario: str) -> Dict[str, Any]:
        """Aprueba una solicitud por el revisor financiero"""
        try:
            if supabase_client is None:
                return None
            
            updates = {
                "aprobado_revfin": True,
                "fecha_aprobacion_revfin": datetime.now().isoformat(),
                "estado": "aprobado_revfin"
            }
            
            response = supabase_client.table("Financiamiento")\
                .update(updates)\
                .eq("id", solicitud_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"❌ Error al aprobar por revfin: {e}")
            return None
    
    @staticmethod
    def aprobar_por_admin(solicitud_id: int, admin_usuario: str) -> Dict[str, Any]:
        """Aprueba una solicitud por el administrador"""
        try:
            if supabase_client is None:
                return None
            
            updates = {
                "aprobado_admin": True,
                "fecha_aprobacion_admin": datetime.now().isoformat(),
                "estado": "completada"
            }
            
            response = supabase_client.table("Financiamiento")\
                .update(updates)\
                .eq("id", solicitud_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"❌ Error al aprobar por admin: {e}")
            return None
    
    @staticmethod
    def rechazar_solicitud_fin(solicitud_id: int, motivo: str = None) -> bool:
        """Rechaza una solicitud de financiamiento"""
        try:
            if supabase_client is None:
                return False
            
            updates = {"estado": "rechazada"}
            if motivo:
                updates["Observaciones"] = f"RECHAZADA: {motivo}"
            
            response = supabase_client.table("Financiamiento")\
                .update(updates)\
                .eq("id", solicitud_id)\
                .execute()
            return True if response.data else False
        except Exception as e:
            print(f"❌ Error al rechazar solicitud de financiamiento: {e}")
            return False
    
    # ==================== MÉTODOS PARA OBTENER SOLICITUDES COMPLETAS ====================
    
    @staticmethod
    def get_solicitud_completa_by_numero(numero_solicitud: str) -> Dict[str, Any]:
        """Obtiene una solicitud completa con todos sus recursos y total"""
        try:
            recursos = FinanciamientoApi.get_solicitud_fin_by_numero(numero_solicitud)
            if not recursos:
                return {}
            
            primer_recurso = recursos[0]
            total = FinanciamientoApi.get_total_solicitud_fin(numero_solicitud)
            
            return {
                "numero_solicitud": numero_solicitud,
                "Area solicitante": primer_recurso.get("Area solicitante"),
                "Fecha": primer_recurso.get("Fecha"),
                "Orden de trabajo": primer_recurso.get("Orden de trabajo"),
                "Total": total,
                "estado": primer_recurso.get("estado"),
                "num_recursos": len(recursos),
                "recursos": recursos
            }
        except Exception as e:
            print(f"❌ Error obteniendo solicitud completa: {e}")
            return {}
    
    @staticmethod
    def get_all_precios() -> List[Dict[str, Any]]:
        """Obtiene todos los precios de productos"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("Precios")\
                .select("*")\
                .order("Tipo", desc=False)\
                .order("Descripcion", desc=False)\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"❌ Error al obtener precios: {e}")
            return []
    
    @staticmethod
    def create_precio(precio_data: Dict[str, Any]) -> bool:
        """Crea un nuevo precio"""
        try:
            if supabase_client is None:
                return False
            
            response = supabase_client.table("Precios").insert(precio_data).execute()
            return True if response.data else False
        except Exception as e:
            print(f"❌ Error al crear precio: {e}")
            return False
    
    @staticmethod
    def update_precio(precio_id: int, precio_data: Dict[str, Any]) -> bool:
        """Actualiza un precio existente"""
        try:
            if supabase_client is None:
                return False
            
            response = supabase_client.table("Precios")\
                .update(precio_data)\
                .eq("id", precio_id)\
                .execute()
            return True if response.data else False
        except Exception as e:
            print(f"❌ Error al actualizar precio: {e}")
            return False
    
    @staticmethod
    def delete_precio(precio_id: int) -> bool:
        """Elimina un precio"""
        try:
            if supabase_client is None:
                return False
            
            response = supabase_client.table("Precios")\
                .delete()\
                .eq("id", precio_id)\
                .execute()
            return True if response.data else False
        except Exception as e:
            print(f"❌ Error al eliminar precio: {e}")
            return False
        
    @staticmethod
    def get_solicitante_by_id(solicitante_id: int) -> Dict[str, Any]:
        """Obtiene un solicitante por su ID"""
        try:
            if supabase_client is None:
                return {"usuario": "Solicitante", "cargo": "Solicitante"}
            
            response = supabase_client.table("Solicitantes")\
                .select("id, usuario, cargo")\
                .eq("id", solicitante_id)\
                .execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            else:
                return {"usuario": "Solicitante", "cargo": "Solicitante"}
                
        except Exception as e:
            print(f"❌ Error obteniendo solicitante {solicitante_id}: {e}")
            return {"usuario": "Solicitante", "cargo": "Solicitante"}
    
    @staticmethod
    def get_solicitud_fin_con_solicitante(numero_solicitud: str):
        """Obtiene una solicitud de financiamiento con datos del solicitante"""
        try:
            if supabase_client is None:
                return []
            
            # Obtener todos los recursos de la solicitud
            response = supabase_client.table("Financiamiento")\
                .select("*")\
                .eq("numero_solicitud", numero_solicitud)\
                .execute()
            
            recursos = response.data
            
            if recursos:
                # Obtener datos del solicitante (del primer recurso)
                primer_recurso = recursos[0]
                solicitante_id = primer_recurso.get("solicitante_id")
                
                # Obtener solicitante
                solicitante = FinanciamientoApi.get_solicitante_by_id(solicitante_id)
                
                return {
                    "recursos": recursos,
                    "solicitante": solicitante
                }
            
            return {"recursos": [], "solicitante": {}}
            
        except Exception as e:
            print(f"❌ Error obteniendo solicitud {numero_solicitud}: {e}")
            return {"recursos": [], "solicitante": {}}