# TFuerte/utilss/precios_api.py
import os
import dotenv
from supabase import create_client
from typing import List, Dict, Any

dotenv.load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

try:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente de Supabase para Precios creado exitosamente")
except Exception as e:
    print(f"❌ Error al crear cliente de Supabase: {e}")
    supabase_client = None

class PreciosApi:
    """API para manejar operaciones de precios"""
    
    @staticmethod
    def get_precio_by_tipo_descripcion(tipo: str, descripcion: str) -> Dict[str, Any]:
        """Obtiene un precio específico por tipo y descripción"""
        try:
            if supabase_client is None:
                return {}
            
            response = supabase_client.table("Precios")\
                .select("*")\
                .eq("Tipo", tipo)\
                .eq("Descripcion", descripcion)\
                .limit(1)\
                .execute()
            
            return response.data[0] if response.data else {}
        except Exception as e:
            print(f"❌ Error obteniendo precio: {e}")
            return {}
    
    @staticmethod
    def buscar_productos_por_palabra(clave: str) -> List[Dict[str, Any]]:
        """Busca productos por palabra clave en Tipo o Descripción"""
        try:
            if supabase_client is None:
                return []
            
            # Búsqueda en Tipo
            response_tipo = supabase_client.table("Precios")\
                .select("*")\
                .ilike("Tipo", f"%{clave}%")\
                .execute()
            
            # Búsqueda en Descripción
            response_desc = supabase_client.table("Precios")\
                .select("*")\
                .ilike("Descripcion", f"%{clave}%")\
                .execute()
            
            # Combinar y eliminar duplicados
            resultados = {}
            for item in response_tipo.data + response_desc.data:
                if item["id"] not in resultados:
                    resultados[item["id"]] = item
            
            return list(resultados.values())
        except Exception as e:
            print(f"❌ Error buscando productos: {e}")
            return []
    
    @staticmethod
    def calcular_importe(tipo: str, descripcion: str, cantidad: int) -> Dict[str, Any]:
        """Calcula precio unitario e importe para un producto"""
        try:
            # Buscar precio base
            precio_base = PreciosApi.get_precio_by_tipo_descripcion(tipo, descripcion)
            
            if not precio_base:
                return {
                    "precio_unitario": 0,
                    "importe": 0,
                    "precio_base": 0,
                    "encontrado": False
                }
            
            precio_base_valor = precio_base.get("Precio", 0)
            precio_unitario = precio_base_valor * 1.25  # +25%
            importe = precio_unitario * cantidad
            
            return {
                "precio_unitario": round(precio_unitario, 2),
                "importe": round(importe, 2),
                "precio_base": precio_base_valor,
                "encontrado": True,
                "producto": precio_base
            }
        except Exception as e:
            print(f"❌ Error calculando importe: {e}")
            return {
                "precio_unitario": 0,
                "importe": 0,
                "precio_base": 0,
                "encontrado": False
            }