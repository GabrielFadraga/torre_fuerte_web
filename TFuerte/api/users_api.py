import os
import dotenv
from supabase import create_client
from typing import List, Dict, Any

# NO cargar dotenv aquí de nuevo - Usamos el cliente de supabase_auth.py
# Solo necesitamos importar el cliente ya existente
from TFuerte.api.supabase_auth import supabase_client  # ← Importamos el MISMO cliente

class UsersAPI:
    """API para operaciones CRUD en la tabla users"""
    
    @staticmethod
    def get_all_users() -> List[Dict[str, Any]]:
        """
        Obtiene todos los usuarios de la tabla users
        """
        try:
            if supabase_client is None:
                print("❌ Cliente de Supabase no disponible (importado de supabase_auth)")
                return []
            
            print("🔍 Consultando tabla 'users'...")
            
            # IMPORTANTE: Verificar que hay sesión activa
            try:
                session = supabase_client.auth.get_session()
                if session and session.session:
                    print(f"✅ Usuario autenticado para consulta: {session.session.user.email}")
                else:
                    print("⚠️  No hay sesión activa - La consulta podría fallar por políticas RLS")
            except Exception as auth_error:
                print(f"⚠️  Error verificando sesión: {auth_error}")
            
            # Hacer la consulta usando el MISMO cliente (que ya tiene el token)
            response = supabase_client.table("users").select("*").execute()
            
            print(f"✅ Respuesta recibida de Supabase")
            
            if response.data:
                print(f"✅ {len(response.data)} usuarios obtenidos")
                for user in response.data[:3]:  # Mostrar primeros 3
                    print(f"   - ID: {user.get('id')}, Nombre: {user.get('name')}")
                return response.data
            else:
                print("⚠️  No hay datos en la respuesta")
                return []
                
        except Exception as e:
            print(f"❌ Error al obtener usuarios: {e}")
            # Imprimir detalles completos del error
            import traceback
            traceback.print_exc()
            return []
    
    @staticmethod
    def insert_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inserta un nuevo usuario en la tabla
        """
        try:
            if supabase_client is None:
                print("❌ Cliente de Supabase no disponible")
                return None
            
            print(f"📝 Intentando insertar usuario: {user_data}")
            
            # Validar datos
            if "name" not in user_data or not user_data["name"]:
                print("❌ Nombre es requerido")
                return None
            
            if "password" not in user_data or not user_data["password"]:
                print("❌ Contraseña es requerida")
                return None
            
            # Verificar autenticación antes de insertar
            try:
                session = supabase_client.auth.get_session()
                if not session or not session.session:
                    print("❌ ERROR: No hay sesión activa. Usuario no autenticado.")
                    print("   Las políticas RLS bloquearán esta operación.")
                    return None
                else:
                    print(f"✅ Insertando como usuario autenticado: {session.session.user.email}")
            except Exception as auth_error:
                print(f"⚠️  Error verificando autenticación: {auth_error}")
            
            # Insertar usando el MISMO cliente (con token incluido)
            response = supabase_client.table("users").insert(user_data).execute()
            
            if response.data and len(response.data) > 0:
                print(f"✅ Usuario insertado correctamente: {response.data[0]['name']}")
                return response.data[0]
            else:
                print("⚠️  No se recibieron datos en la respuesta")
                return None
                
        except Exception as e:
            print(f"❌ Error al insertar usuario: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def update_user(user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza un usuario existente
        """
        try:
            if supabase_client is None:
                print("❌ Cliente de Supabase no disponible")
                return None
            
            print(f"📝 Actualizando usuario ID: {user_id}...")
            
            # No permitir actualizar el ID
            if "id" in user_data:
                del user_data["id"]
            
            # Actualizar usando el MISMO cliente
            response = supabase_client.table("users").update(user_data).eq("id", user_id).execute()
            
            if response.data and len(response.data) > 0:
                print(f"✅ Usuario actualizado correctamente: ID {user_id}")
                return response.data[0]
            else:
                print("⚠️  No se recibieron datos en la respuesta")
                return None
                
        except Exception as e:
            print(f"❌ Error al actualizar usuario: {e}")
            return None
    
    @staticmethod
    def delete_users(user_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Elimina usuarios
        """
        try:
            if supabase_client is None:
                print("❌ Cliente de Supabase no disponible")
                return []
            
            if not user_ids:
                print("⚠️  No hay IDs para eliminar")
                return []
            
            print(f"🗑️  Eliminando usuarios con IDs: {user_ids}...")
            
            # Eliminar usando el MISMO cliente
            response = supabase_client.table("users").delete().in_("id", user_ids).execute()
            
            if response.data:
                print(f"✅ Usuarios eliminados correctamente: {len(response.data)} registros")
                return response.data
            else:
                print("⚠️  No se recibieron datos en la respuesta")
                return []
                
        except Exception as e:
            print(f"❌ Error al eliminar usuarios: {e}")
            return []