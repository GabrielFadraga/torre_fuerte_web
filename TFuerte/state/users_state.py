import reflex as rx
from typing import List, Dict, Any
from TFuerte.api.users_api import UsersAPI

class UsersState(rx.State):
    users_data: List[Dict[str, Any]] = []
    loading: bool = False
    
    async def load_users(self):
        """Cargar usuarios desde Supabase"""
        print("🔄 Cargando usuarios desde Supabase...")
        self.loading = True
        yield
        
        try:
            data = UsersAPI.get_all_users()
            print(f"📊 Datos recibidos de API: {data}")
            
            if data:
                self.users_data = sorted(data, key=lambda x: x.get('id', 0))
                print(f"✅ {len(self.users_data)} usuarios cargados")
                
                yield rx.toast.success(
                    f"{len(self.users_data)} usuarios cargados",
                    position="top-right",
                    duration=3000
                )
            else:
                self.users_data = []
                print("⚠️ No se obtuvieron datos")
                
                yield rx.toast.warning(
                    "No hay usuarios en la tabla",
                    position="top-right",
                    duration=3000
                )
        except Exception as e:
            print(f"❌ Error cargando usuarios: {e}")
            self.users_data = []
            
            yield rx.toast.error(
                f"Error: {str(e)}",
                position="top-right",
                duration=5000
            )
        
        self.loading = False