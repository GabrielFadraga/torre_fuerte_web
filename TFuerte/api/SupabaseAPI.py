import os
import dotenv
from supabase import create_client
from typing import List

# Cargar variables de entorno
dotenv.load_dotenv()

# Obtener credenciales
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Crear cliente de Supabase
try:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente de Supabase creado exitosamente")
except Exception as e:
    print(f"❌ Error al crear cliente de Supabase: {e}")
    supabase_client = None

def get_test_data():
    """
    Obtiene todos los datos de la tabla 'testing' de Supabase
    
    Returns:
        list: Lista de diccionarios con los datos de la tabla
    """
    try:
        if supabase_client is None:
            print("❌ Cliente de Supabase no disponible")
            return []
        
        print("🔍 Consultando datos de Supabase...")
        response = supabase_client.table("testing").select("*").execute()
        data = response.data
        
        return data
    except Exception as e:
        print(f"❌ Error al obtener datos: {e}")
        return []

def insert_test_data(user_data: dict):
    """
    Inserta un nuevo registro en la tabla 'testing' de Supabase
    
    Args:
        user_data (dict): Diccionario con los datos del usuario
                          Debe contener: name, surname, email, phone, init_date
    
    Returns:
        dict: Respuesta de Supabase con el registro insertado
    """
    try:
        if supabase_client is None:
            print("❌ Cliente de Supabase no disponible")
            return None
        
        print("📝 Insertando datos en Supabase...")
        
        # Asegurarse de que el teléfono sea string
        if 'phone' in user_data and user_data['phone'] is not None:
            user_data['phone'] = str(user_data['phone'])
        
        # Insertar el registro en Supabase
        response = supabase_client.table("testing").insert(user_data).execute()
        
        if response.data:
            print(f"✅ Datos insertados correctamente: {response.data}")
        else:
            print("⚠️  No se recibieron datos en la respuesta")
        
        return response.data
    except Exception as e:
        print(f"❌ Error al insertar datos: {e}")
        return None

def update_test_data(user_id: int, user_data: dict):
    """
    Actualiza un registro en la tabla 'testing' de Supabase
    
    Args:
        user_id (int): ID del usuario a actualizar
        user_data (dict): Diccionario con los datos a actualizar
    
    Returns:
        dict: Respuesta de Supabase con el registro actualizado
    """
    try:
        if supabase_client is None:
            print("❌ Cliente de Supabase no disponible")
            return None
        
        print(f"📝 Actualizando datos del usuario ID: {user_id}...")
        
        # Asegurarse de que el teléfono sea string si está presente
        if 'phone' in user_data and user_data['phone'] is not None:
            user_data['phone'] = str(user_data['phone'])
        
        # Actualizar el registro en Supabase
        response = supabase_client.table("testing").update(user_data).eq("id", user_id).execute()
        
        if response.data:
            print(f"✅ Datos actualizados correctamente: {response.data}")
        else:
            print("⚠️  No se recibieron datos en la respuesta")
        
        return response.data
    except Exception as e:
        print(f"❌ Error al actualizar datos: {e}")
        return None

def delete_test_data(user_ids: List[int]):
    """
    Elimina registros de la tabla 'testing' de Supabase
    
    Args:
        user_ids (List[int]): Lista de IDs de usuarios a eliminar
    
    Returns:
        dict: Respuesta de Supabase con los registros eliminados
    """
    try:
        if supabase_client is None:
            print("❌ Cliente de Supabase no disponible")
            return None
        
        if not user_ids:
            print("⚠️  No hay IDs para eliminar")
            return None
        
        print(f"🗑️  Eliminando usuarios con IDs: {user_ids}...")
        
        # Para eliminar múltiples registros, necesitamos usar 'in_' (en lugar de 'eq' para uno)
        response = supabase_client.table("testing").delete().in_("id", user_ids).execute()
        
        if response.data:
            print(f"✅ Datos eliminados correctamente: {len(response.data)} registros")
        else:
            print("⚠️  No se recibieron datos en la respuesta")
        
        return response.data
    except Exception as e:
        print(f"❌ Error al eliminar datos: {e}")
        return None