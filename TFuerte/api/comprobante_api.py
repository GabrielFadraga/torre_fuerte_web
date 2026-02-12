# TFuerte/api/comprobante_api.py
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
    print("✅ Cliente de Supabase para Comprobantes creado exitosamente")
except Exception as e:
    print(f"❌ Error al crear cliente de Supabase para Comprobantes: {e}")
    supabase_client = None

class ComprobanteAPI:
    """API para operaciones en la tabla Comprobantes"""
    
    @staticmethod
    def crear_comprobante(comprobante_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo comprobante"""
        try:
            if supabase_client is None:
                return None
            
            print(f"📝 Creando comprobante con datos: {comprobante_data}")
            
            # Validar campos requeridos
            required_fields = ["solicitud_grupo_id", "destino", "fecha_salida", "total"]
            for field in required_fields:
                if field not in comprobante_data:
                    print(f"❌ Campo requerido faltante: {field}")
                    return None
            
            response = supabase_client.table("Comprobantes").insert(comprobante_data).execute()
            
            if response.data and len(response.data) > 0:
                print(f"✅ Comprobante creado con ID: {response.data[0]['id']}")
                return response.data[0]
            else:
                print("❌ No se recibió respuesta de Supabase")
                return None
                
        except Exception as e:
            print(f"❌ ERROR en crear_comprobante: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def crear_detalle_comprobante(detalle_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un detalle para un comprobante"""
        try:
            if supabase_client is None:
                return None
            
            print(f"📝 Creando detalle de comprobante")
            
            response = supabase_client.table("ComprobanteDetalles").insert(detalle_data).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            else:
                print("❌ No se recibió respuesta de Supabase")
                return None
                
        except Exception as e:
            print(f"❌ ERROR en crear_detalle_comprobante: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def get_comprobante_by_id(comprobante_id: int) -> Dict[str, Any]:
        """Obtiene un comprobante por su ID"""
        try:
            if supabase_client is None:
                return None
            
            response = supabase_client.table("Comprobantes").select("*").eq("id", comprobante_id).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            else:
                return None
                
        except Exception as e:
            print(f"❌ ERROR en get_comprobante_by_id: {e}")
            return None
    
    @staticmethod
    def get_detalles_by_comprobante_id(comprobante_id: int) -> List[Dict[str, Any]]:
        """Obtiene los detalles de un comprobante"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("ComprobanteDetalles").select("*").eq("comprobante_id", comprobante_id).execute()
            
            if response.data:
                return response.data
            else:
                return []
                
        except Exception as e:
            print(f"❌ ERROR en get_detalles_by_comprobante_id: {e}")
            return []
    
    @staticmethod
    def get_all_comprobantes() -> List[Dict[str, Any]]:
        """Obtiene todos los comprobantes"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("Comprobantes").select("*").order("fecha_generacion", desc=True).execute()
            
            if response.data:
                return response.data
            else:
                return []
                
        except Exception as e:
            print(f"❌ ERROR en get_all_comprobantes: {e}")
            return []
    
    @staticmethod
    def get_precio_by_descripcion(descripcion: str) -> float:
        """Obtiene el precio de un producto por su descripción"""
        try:
            if supabase_client is None:
                return 0.0
            
            # Buscar en la tabla Precios
            response = supabase_client.table("Precios").select("Precio").eq("Descripcion", descripcion).execute()
            
            if response.data and len(response.data) > 0:
                return float(response.data[0].get("Precio", 0))
            else:
                return 0.0
                
        except Exception as e:
            print(f"❌ ERROR en get_precio_by_descripcion: {e}")
            return 0.0
    
    @staticmethod
    def get_almacencargo_by_user(user: str) -> Dict[str, Any]:
        """Obtiene los datos del jefe de almacén por su usuario"""
        try:
            if supabase_client is None:
                return {}
            
            response = supabase_client.table("AlmacenCargo").select("*").eq("user", user).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            else:
                return {}
                
        except Exception as e:
            print(f"❌ ERROR en get_almacencargo_by_user: {e}")
            return {}
        
    # En TFuerte/api/comprobante_api.py - Agregar estos métodos

    @staticmethod
    def get_jefe_almacen() -> Dict[str, Any]:
        """Obtiene el jefe de almacén desde la tabla AlmacenCargo"""
        try:
            if supabase_client is None:
                return {}
            
            # Suponiendo que solo hay un jefe de almacén o tomamos el primero
            response = supabase_client.table("AlmacenCargo").select("*").limit(1).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            else:
                return {}
                
        except Exception as e:
            print(f"❌ ERROR en get_jefe_almacen: {e}")
            return {}

    @staticmethod
    def get_administrador() -> Dict[str, Any]:
        """Obtiene el administrador desde la tabla Autorizacion"""
        try:
            if supabase_client is None:
                return {}
            
            # Tomar el primer administrador o filtrar por algún criterio
            response = supabase_client.table("Autorizacion").select("*").limit(1).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            else:
                return {}
                
        except Exception as e:
            print(f"❌ ERROR en get_administrador: {e}")
            return {}

    # Si ya existe get_almacencargo_by_user, podemos modificar o mantener
    @staticmethod
    def get_almacencargo_by_user(user: str) -> Dict[str, Any]:
        """Obtiene los datos del jefe de almacén por su usuario"""
        try:
            if supabase_client is None:
                return {}
            
            response = supabase_client.table("AlmacenCargo").select("*").eq("user", user).execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            else:
                return {}
                
        except Exception as e:
            print(f"❌ ERROR en get_almacencargo_by_user: {e}")
            return {}
        
    @staticmethod
    def get_admin_by_username(username: str) -> Dict[str, Any]:
        """Obtiene un administrador específico por su nombre de usuario"""
        try:
            if supabase_client is None:
                return {}
            
            response = supabase_client.table("Autorizacion")\
                .select("*")\
                .eq("user", username)\
                .execute()
            
            if response.data and len(response.data) > 0:
                return response.data[0]
            else:
                return {}
                
        except Exception as e:
            print(f"❌ ERROR en get_admin_by_username: {e}")
            return {}

    @staticmethod
    def get_admin_que_aprobo_solicitud(descripcion_producto: str) -> Dict[str, Any]:
        """Busca el administrador que aprobó una solicitud para un producto"""
        try:
            if supabase_client is None:
                return {}
            
            # Buscar solicitudes aprobadas que coincidan con la descripción del producto
            from TFuerte.api.solicitudes_api import SolicitudesAPI
            solicitudes = SolicitudesAPI.get_all_solicitudes()
            
            for solicitud in solicitudes:
                if (solicitud.get("estado") == "aprobada" and 
                    solicitud.get("Descripcion", "").lower() in descripcion_producto.lower()):
                    aprobado_por = solicitud.get("aprobado_por")
                    if aprobado_por:
                        # Obtener los datos completos del administrador
                        return ComprobanteAPI.get_admin_by_username(aprobado_por)
            
            return {}  # Si no se encuentra
            
        except Exception as e:
            print(f"❌ ERROR en get_admin_que_aprobo_solicitud: {e}")
            return {}
        
    # TFuerte/api/comprobante_api.py - Agregar este método

    @staticmethod
    def get_admin_que_aprobo_solicitud(descripcion_producto: str) -> Dict[str, Any]:
        """Busca el administrador que aprobó una solicitud para un producto"""
        try:
            if supabase_client is None:
                return {}
            
            # Primero, buscar solicitudes aprobadas que coincidan con la descripción
            response = supabase_client.table("Solicitudes")\
                .select("aprobado_por")\
                .ilike("Descripcion", f"%{descripcion_producto}%")\
                .eq("estado", "aprobada")\
                .limit(1)\
                .execute()
            
            if response.data and len(response.data) > 0:
                admin_user = response.data[0].get("aprobado_por")
                if admin_user:
                    # Obtener los datos completos del administrador
                    return ComprobanteAPI.get_admin_by_username(admin_user)
            
            return {}  # Si no se encuentra
            
        except Exception as e:
            print(f"❌ ERROR en get_admin_que_aprobo_solicitud: {e}")
            return {}