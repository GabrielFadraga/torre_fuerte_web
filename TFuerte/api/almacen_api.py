# TFuerte/api/almacen_api.py
import os
import dotenv
from supabase import create_client
from typing import List, Dict, Any

# Cargar variables de entorno
dotenv.load_dotenv()

# Obtener credenciales
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Crear cliente de Supabase
try:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente de Supabase para Almacen creado exitosamente")
except Exception as e:
    print(f"❌ Error al crear cliente de Supabase: {e}")
    supabase_client = None

class AlmacenAPI:
    """API para operaciones CRUD en la tabla Almacen"""
    
    @staticmethod
    def get_all_items() -> List[Dict[str, Any]]:
        """Obtiene todos los registros de la tabla 'Almacen'"""
        try:
            if supabase_client is None:
                return []
            
            response = supabase_client.table("Almacen").select("*").execute()
            data = response.data
            
            if data:
                print(f"✅ {len(data)} registros obtenidos")
            
            return data
        except Exception as e:
            print(f"❌ Error al obtener datos: {e}")
            return []
    
    @staticmethod
    def insert_item(item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Inserta un nuevo registro en la tabla 'Almacen'"""
        try:
            if supabase_client is None:
                return None
            
            print(f"📝 Insertando datos en Almacen...")
            
            # Convertir tipos básicos
            if "Numero" in item_data:
                try:
                    item_data["Numero"] = int(item_data["Numero"])
                except:
                    item_data["Numero"] = 0
            
            if "Cantidad E" in item_data:
                try:
                    item_data["Cantidad E"] = int(item_data["Cantidad E"])
                except:
                    item_data["Cantidad E"] = 0
            
            if "Cantidad S" in item_data and item_data["Cantidad S"]:
                try:
                    item_data["Cantidad S"] = int(item_data["Cantidad S"])
                except:
                    item_data["Cantidad S"] = 0
            elif "Cantidad S" in item_data:
                # Si está vacío o None, no lo incluyas
                del item_data["Cantidad S"]
            
            if "Precio" in item_data:
                try:
                    item_data["Precio"] = float(item_data["Precio"])
                except:
                    item_data["Precio"] = 0.0
            
            # NOTA: NO calculamos Saldo ni Importe - Supabase lo hará automáticamente
            # Eliminar Saldo e Importe si están presentes
            if "Saldo" in item_data:
                del item_data["Saldo"]
            if "Importe" in item_data:
                del item_data["Importe"]
            
            print(f"📦 Datos a insertar: {item_data}")
            
            response = supabase_client.table("Almacen").insert(item_data).execute()
            
            if response.data:
                print(f"✅ Datos insertados correctamente")
                return response.data[0]
            else:
                print("⚠️  No se recibieron datos en la respuesta")
                return None
        except Exception as e:
            print(f"❌ Error al insertar datos: {e}")
            return None
    
    # En TFuerte/api/almacen_api.py, método update_item:

    @staticmethod
    def update_item(numero: int, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza un registro en la tabla 'Almacen' usando Numero como identificador"""
        try:
            if supabase_client is None:
                return None
            
            print(f"📝 Actualizando producto Numero: {numero}...")
            
            # No incluir "Numero" en los datos a actualizar
            if "Numero" in item_data:
                del item_data["Numero"]
            
            # Convertir tipos básicos
            if "Cantidad E" in item_data:
                try:
                    item_data["Cantidad E"] = int(item_data["Cantidad E"])
                except:
                    item_data["Cantidad E"] = 0
            
            if "Cantidad S" in item_data:
                try:
                    item_data["Cantidad S"] = int(item_data["Cantidad S"])
                except:
                    item_data["Cantidad S"] = 0
            
            if "Precio" in item_data:
                try:
                    item_data["Precio"] = float(item_data["Precio"])
                except:
                    item_data["Precio"] = 0.0
            
            # Manejar fechas nulas
            if "Fecha de entrada" in item_data and item_data["Fecha de entrada"] is None:
                # Establecer como nulo explícitamente
                item_data["Fecha de entrada"] = None
            
            if "Fecha de salida" in item_data:
                if item_data["Fecha de salida"] is None:
                    # Establecer como nulo explícitamente
                    item_data["Fecha de salida"] = None
                # Si la columna en Supabase tiene espacio doble, usar el nombre correcto
                # Cambiar "Fecha de salida" a "Fecha de salida" (con el nombre correcto)
                pass  # Ya está en el nombre correcto
            
            # NOTA: NO calculamos el Saldo ni el Importe aquí - Supabase lo hace automáticamente
            # Eliminar Saldo e Importe si están presentes, para que Supabase los calcule
            if "Saldo" in item_data:
                del item_data["Saldo"]
            if "Importe" in item_data:
                del item_data["Importe"]
            
            print(f"📦 Datos para actualizar: {item_data}")
            
            # Usar eq con el nuevo nombre "Numero"
            response = supabase_client.table("Almacen").update(item_data).eq("Numero", numero).execute()
            
            if response.data:
                print(f"✅ Datos actualizados correctamente")
                return response.data[0]
            else:
                print("⚠️  No se recibieron datos en la respuesta")
                return None
        except Exception as e:
            print(f"❌ Error al actualizar datos: {e}")
            return None
    
    @staticmethod
    def delete_items(numeros: List[int]) -> List[Dict[str, Any]]:
        """Elimina registros de la tabla 'Almacen' usando Numero como identificador"""
        try:
            if supabase_client is None:
                return []
            
            if not numeros:
                return []
            
            print(f"🗑️  Eliminando productos con Numeros: {numeros}...")
            
            # Eliminar múltiples registros usando in_
            response = supabase_client.table("Almacen").delete().in_("Numero", numeros).execute()
            
            if response.data:
                print(f"✅ Datos eliminados correctamente: {len(response.data)} registros")
            else:
                print("⚠️  No se recibieron datos en la respuesta")
            
            return response.data
        except Exception as e:
            print(f"❌ Error al eliminar datos: {e}")
            return []