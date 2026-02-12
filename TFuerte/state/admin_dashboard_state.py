# TFuerte/state/admin_dashboard_state.py
import reflex as rx
from typing import List
from TFuerte.api.registrotf_api import RegistroTFAPI
from TFuerte.api.solicitudes_api import SolicitudesAPI
from TFuerte.api.almacen_api import AlmacenAPI
from datetime import datetime

class AdminDashboardState(rx.State):
    """Estado para el dashboard de administradores"""
    
    # Datos de RegistroTF
    registro_data: List[dict] = []
    registro_filtered: List[dict] = []
    
    # Datos de Solicitudes
    solicitudes_data: List[dict] = []
    solicitudes_pendientes: List[dict] = []
    solicitudes_paginated: List[dict] = []  # Datos para la página actual
    
    # Estados de UI
    loading: bool = False
    search_registro: str = ""
    search_solicitudes: str = ""
    
    # Para aprobar/rechazar
    selected_solicitud: dict = {}
    show_aprobar_dialog: bool = False
    show_rechazar_dialog: bool = False
    producto_seleccionado_id: int = 0
    
    # Variable para almacenar el nombre de usuario del admin
    admin_username: str = "admin"
    
    # Variables para paginación de SOLICITUDES
    current_page_solicitudes: int = 1
    items_per_page_solicitudes: int = 10  # Items por página
    total_pages_solicitudes: int = 1
    page_numbers_solicitudes: List[int] = []  # Lista de números de página a mostrar

    # NUEVO: Para manejar solicitudes múltiples
    solicitud_grupo_actual: dict = {}
    recursos_solicitud_grupo: List[dict] = []
    show_grupo_dialog: bool = False

    registro_paginated: List[dict] = []          # Datos de la página actual
    current_page_registro: int = 1
    items_per_page_registro: int = 10
    total_pages_registro: int = 1
    page_numbers_registro: List[int] = []
    
    def _fetch_all_data(self):
        """Obtiene todos los datos de Supabase (sin eventos, solo lógica)"""
        # Cargar RegistroTF
        registro = RegistroTFAPI.get_all_registros()
        if registro:
            self.registro_data = registro
            self.registro_filtered = registro
        
        # Cargar Solicitudes
        solicitudes = SolicitudesAPI.get_all_solicitudes()
        if solicitudes:
            self.solicitudes_data = solicitudes
            self.solicitudes_pendientes = [
                s for s in solicitudes 
                if s.get("estado") == "pendiente"
            ]
            self.calculate_solicitudes_pagination()

    def load_data(self):
        self.loading = True
        yield

        try:
            # ---- RegistroTF ----
            registro = RegistroTFAPI.get_all_registros()
            self.registro_data = registro if isinstance(registro, list) else []
            self.registro_filtered = self.registro_data.copy()
            self.calculate_registro_pagination()   # <--- NUEVO
            print(f"📊 Registros cargados: {len(self.registro_data)}")

            # ---- Solicitudes ----
            solicitudes = SolicitudesAPI.get_all_solicitudes()
            self.solicitudes_data = solicitudes if isinstance(solicitudes, list) else []
            self.solicitudes_pendientes = [
                s for s in self.solicitudes_data 
                if s.get("estado") == "pendiente"
            ]
            self.calculate_solicitudes_pagination()

        except Exception as e:
            print(f"❌ Error en load_data: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.loading = False
    
    def calculate_solicitudes_pagination(self):
        """Calcula la paginación para las solicitudes"""
        total_items = len(self.solicitudes_pendientes)
        
        # Calcular total de páginas
        if total_items == 0:
            self.total_pages_solicitudes = 1
        else:
            self.total_pages_solicitudes = max(1, (total_items + self.items_per_page_solicitudes - 1) // self.items_per_page_solicitudes)
        
        # Asegurar que current_page_solicitudes esté dentro de los límites
        if self.current_page_solicitudes > self.total_pages_solicitudes:
            self.current_page_solicitudes = max(1, self.total_pages_solicitudes)
        
        # Calcular índices para la página actual
        start_idx = (self.current_page_solicitudes - 1) * self.items_per_page_solicitudes
        end_idx = min(start_idx + self.items_per_page_solicitudes, total_items)
        
        # Obtener los datos para la página actual
        if self.solicitudes_pendientes and total_items > 0:
            self.solicitudes_paginated = self.solicitudes_pendientes[start_idx:end_idx]
        else:
            self.solicitudes_paginated = []
        
        # Calcular números de página a mostrar
        self.calculate_page_numbers()
        
        return start_idx, end_idx
    
    def calculate_page_numbers(self):
        """Calcula los números de página a mostrar en los botones"""
        max_pages_to_show = 4
        current = self.current_page_solicitudes
        total = self.total_pages_solicitudes
        
        if total <= max_pages_to_show:
            # Si hay 4 o menos páginas, mostrar todas
            self.page_numbers_solicitudes = list(range(1, total + 1))
            return
        
        # Calcular rango de páginas a mostrar
        start = max(1, current - 1)
        end = min(total, start + max_pages_to_show - 1)
        
        # Ajustar si estamos cerca del final
        if end - start + 1 < max_pages_to_show:
            start = max(1, end - max_pages_to_show + 1)
        
        self.page_numbers_solicitudes = list(range(start, end + 1))
    
    def filter_registro(self, search_value: str):
        self.search_registro = search_value
        self.current_page_registro = 1   # <--- RESET
        
        if not search_value:
            self.registro_filtered = self.registro_data
        else:
            search_term = search_value.lower()
            filtered = []
            for item in self.registro_data:
                if (search_term in item.get("Producto", "").lower() or
                    search_term in item.get("Destino", "").lower() or
                    search_term in item.get("Recibe", "").lower() or
                    search_term in item.get("Cliente", "").lower()):
                    filtered.append(item)
            self.registro_filtered = filtered
        
        self.calculate_registro_pagination()   # <--- RECALCULAR
    
    def filter_solicitudes(self, search_value: str):
        """Filtra las solicitudes"""
        self.search_solicitudes = search_value
        self.current_page_solicitudes = 1  # Resetear a primera página al filtrar
        
        if not search_value:
            # Recargar todas las pendientes
            self.solicitudes_pendientes = [
                s for s in self.solicitudes_data 
                if s.get("estado") == "pendiente"
            ]
        else:
            search_term = search_value.lower()
            filtered = []
            for s in self.solicitudes_data:
                if (s.get("estado") == "pendiente" and
                    (search_term in s.get("Descripcion", "").lower() or
                     search_term in s.get("Destino", "").lower() or
                     search_term in s.get("Observacion", "").lower())):
                    filtered.append(s)
            
            self.solicitudes_pendientes = filtered
        
        # Recalcular paginación
        self.calculate_solicitudes_pagination()
    
    def go_to_page_solicitudes(self, page_number: int):
        """Navega a una página específica de solicitudes"""
        if 1 <= page_number <= self.total_pages_solicitudes:
            self.current_page_solicitudes = page_number
            self.calculate_solicitudes_pagination()
    
    def next_page_solicitudes(self):
        """Va a la siguiente página de solicitudes"""
        if self.current_page_solicitudes < self.total_pages_solicitudes:
            self.current_page_solicitudes += 1
            self.calculate_solicitudes_pagination()
    
    def previous_page_solicitudes(self):
        """Va a la página anterior de solicitudes"""
        if self.current_page_solicitudes > 1:
            self.current_page_solicitudes -= 1
            self.calculate_solicitudes_pagination()
    
    def open_aprobar_dialog(self, solicitud: dict):
        """Abre diálogo para aprobar solicitud"""
        self.selected_solicitud = solicitud
        self.show_aprobar_dialog = True
        
        # Buscar productos que coincidan con la descripción
        productos = AlmacenAPI.get_all_items()
        productos_coincidentes = [
            p for p in productos 
            if solicitud.get("Descripcion", "").lower() in p.get("Descripcion del producto", "").lower()
            and p.get("Saldo", 0) >= solicitud.get("Cantidad", 0)
        ]
        
        if productos_coincidentes:
            self.producto_seleccionado_id = productos_coincidentes[0].get("Numero", 0)
    
    def close_aprobar_dialog(self):
        """Cierra diálogo de aprobación"""
        self.show_aprobar_dialog = False
        self.selected_solicitud = {}
        self.producto_seleccionado_id = 0
    
    def open_rechazar_dialog(self, solicitud: dict):
        """Abre diálogo para rechazar solicitud"""
        self.selected_solicitud = solicitud
        self.show_rechazar_dialog = True
    
    def close_rechazar_dialog(self):
        """Cierra diálogo de rechazo"""
        self.show_rechazar_dialog = False
        self.selected_solicitud = {}
    
    def aprobar_solicitud(self):
        """Aprueba la solicitud seleccionada"""
        if not self.selected_solicitud:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return

        solicitud_id = self.selected_solicitud.get("id")
        descripcion = self.selected_solicitud.get("Descripcion", "")
        cantidad_solicitada = self.selected_solicitud.get("Cantidad", 0)

        if cantidad_solicitada <= 0:
            yield rx.toast.error("❌ La cantidad debe ser mayor a 0")
            return

        # Verificar productos disponibles
        productos = AlmacenAPI.get_all_items()
        producto_disponible = None
        for p in productos:
            if (descripcion.lower() in p.get("Descripcion del producto", "").lower() and
                p.get("Saldo", 0) >= cantidad_solicitada):
                producto_disponible = p
                break

        if not producto_disponible:
            yield rx.toast.error(f"❌ No hay suficiente saldo para {descripcion}")
            return

        admin_user = self.admin_username

        self.loading = True
        yield

        try:
            result = SolicitudesAPI.aprobar_solicitud(
                solicitud_id,
                admin_user,
                producto_disponible.get("Numero", 0)
            )

            if not result:
                yield rx.toast.error("❌ Error al aprobar la solicitud")
                return

            self.close_aprobar_dialog()
            
            # Recargar datos SIN yield
            self._fetch_all_data()

            yield rx.toast.success(
                f"✅ Solicitud aprobada por {admin_user}. "
                f"El producto {descripcion} está listo para salida."
            )

        except Exception as e:
            print(f"❌ Error en aprobar_solicitud: {e}")
            yield rx.toast.error("❌ Error interno al aprobar")
        finally:
            self.loading = False
    
    def rechazar_solicitud(self):
        if not self.selected_solicitud:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return

        solicitud_id = self.selected_solicitud.get("id")
        admin_user = self.admin_username

        self.loading = True
        yield

        try:
            result = SolicitudesAPI.rechazar_solicitud(solicitud_id, admin_user)
            if not result:
                yield rx.toast.error("❌ Error al rechazar la solicitud")
                return

            self.close_rechazar_dialog()
            self._fetch_all_data()
            yield rx.toast.success("✅ Solicitud rechazada")

        except Exception as e:
            print(f"❌ Error en rechazar_solicitud: {e}")
            yield rx.toast.error("❌ Error interno al rechazar")
        finally:
            self.loading = False
    
    def cargar_admin_username(self):
        """Carga el nombre de usuario del administrador actual"""
        from TFuerte.state.admin_auth_state import AdminAuthState
        
        # Obtener el nombre de usuario de manera segura
        try:
            # Verificar si hay un admin autenticado
            if AdminAuthState.is_authenticated:
                # Obtener el nombre de usuario del admin actual
                if AdminAuthState.current_admin and 'user' in AdminAuthState.current_admin:
                    self.admin_username = AdminAuthState.current_admin['user']
        except Exception as e:
            print(f"⚠️ Error cargando nombre de usuario: {e}")
            self.admin_username = "admin"

    #Esto es codigo nuevo
    def open_grupo_dialog(self, grupo_id: str):
        """Abre el diálogo para ver los recursos de una solicitud grupal"""
        # Obtener todas las solicitudes con el mismo grupo_id
        solicitudes_grupo = []
        for solicitud in self.solicitudes_data:
            if solicitud.get("solicitud_grupo_id") == grupo_id:
                solicitudes_grupo.append(solicitud)
        
        if solicitudes_grupo:
            self.solicitud_grupo_actual = solicitudes_grupo[0]  # Primera para datos generales
            self.recursos_solicitud_grupo = solicitudes_grupo
            self.show_grupo_dialog = True
    
    def close_grupo_dialog(self):
        """Cierra el diálogo de grupo"""
        self.show_grupo_dialog = False
        self.solicitud_grupo_actual = {}
        self.recursos_solicitud_grupo = []
    
    def aprobar_grupo_solicitudes(self):
        if not self.recursos_solicitud_grupo:
            yield rx.toast.error("❌ No hay solicitudes en el grupo")
            return

        admin_user = self.admin_username
        self.loading = True
        yield

        try:
            for solicitud in self.recursos_solicitud_grupo:
                solicitud_id = solicitud.get("id")
                descripcion = solicitud.get("Descripcion", "")
                cantidad = solicitud.get("Cantidad", 0)

                # Buscar producto disponible (puedes optimizar esta parte)
                productos = AlmacenAPI.get_all_items()
                producto_disponible = None
                for p in productos:
                    if (descripcion.lower() in p.get("Descripcion del producto", "").lower() and
                        p.get("Saldo", 0) >= cantidad):
                        producto_disponible = p
                        break

                if producto_disponible:
                    SolicitudesAPI.aprobar_solicitud(
                        solicitud_id,
                        admin_user,
                        producto_disponible.get("Numero", 0)
                    )

            self.close_grupo_dialog()
            self._fetch_all_data()
            yield rx.toast.success(f"✅ Grupo aprobado: {len(self.recursos_solicitud_grupo)} recursos")

        except Exception as e:
            print(f"❌ Error en aprobar_grupo_solicitudes: {e}")
            yield rx.toast.error("❌ Error al aprobar grupo")
        finally:
            self.loading = False
    
    def rechazar_grupo_solicitudes(self):
        if not self.recursos_solicitud_grupo:
            yield rx.toast.error("❌ No hay solicitudes en el grupo")
            return

        admin_user = self.admin_username
        self.loading = True
        yield

        try:
            for solicitud in self.recursos_solicitud_grupo:
                solicitud_id = solicitud.get("id")
                SolicitudesAPI.rechazar_solicitud(solicitud_id, admin_user)

            self.close_grupo_dialog()
            self._fetch_all_data()
            yield rx.toast.success(f"✅ Grupo rechazado: {len(self.recursos_solicitud_grupo)} recursos")

        except Exception as e:
            print(f"❌ Error en rechazar_grupo_solicitudes: {e}")
            yield rx.toast.error("❌ Error al rechazar grupo")
        finally:
            self.loading = False
    
    
    def agrupar_solicitudes_para_vista(self):
        """Agrupa las solicitudes pendientes por grupo_id para la vista"""
        grupos = {}
        
        for solicitud in self.solicitudes_pendientes:
            grupo_id = solicitud.get("solicitud_grupo_id")
            
            if not grupo_id:
                # Si no tiene grupo, usar el ID individual
                grupo_id = f"individual_{solicitud.get('id')}"
            
            if grupo_id not in grupos:
                grupos[grupo_id] = {
                    "grupo_id": grupo_id,
                    "solicitudes": [],
                    "destino": solicitud.get("Destino", ""),
                    "solicitante_id": solicitud.get("solicitante_id", ""),
                    "fecha_solicitud": solicitud.get("fecha_solicitud", "")
                }
            
            grupos[grupo_id]["solicitudes"].append(solicitud)
        
        # Convertir a lista para usar en la vista
        self.solicitudes_agrupadas = list(grupos.values())

    #ESTO ES PARA LA PAGINACION DE LA TABLA DE REGISTROS

    def calculate_registro_pagination(self):
        """Calcula la paginación para los registros de RegistroTF"""
        total_items = len(self.registro_filtered)
        
        if total_items == 0:
            self.total_pages_registro = 1
            self.registro_paginated = []
        else:
            self.total_pages_registro = max(1, (total_items + self.items_per_page_registro - 1) // self.items_per_page_registro)
        
        # Asegurar que current_page esté dentro de límites
        if self.current_page_registro > self.total_pages_registro:
            self.current_page_registro = max(1, self.total_pages_registro)
        
        start_idx = (self.current_page_registro - 1) * self.items_per_page_registro
        end_idx = min(start_idx + self.items_per_page_registro, total_items)
        
        if total_items > 0:
            self.registro_paginated = self.registro_filtered[start_idx:end_idx]
        else:
            self.registro_paginated = []
        
        self.calculate_registro_page_numbers()

    def calculate_registro_page_numbers(self):
        """Calcula los números de página a mostrar en los botones"""
        max_pages_to_show = 4
        current = self.current_page_registro
        total = self.total_pages_registro
        
        if total <= max_pages_to_show:
            self.page_numbers_registro = list(range(1, total + 1))
            return
        
        start = max(1, current - 1)
        end = min(total, start + max_pages_to_show - 1)
        
        if end - start + 1 < max_pages_to_show:
            start = max(1, end - max_pages_to_show + 1)
        
        self.page_numbers_registro = list(range(start, end + 1))

    def go_to_page_registro(self, page_number: int):
        """Navega a una página específica de registros"""
        if 1 <= page_number <= self.total_pages_registro:
            self.current_page_registro = page_number
            self.calculate_registro_pagination()

    def next_page_registro(self):
        """Página siguiente de registros"""
        if self.current_page_registro < self.total_pages_registro:
            self.current_page_registro += 1
            self.calculate_registro_pagination()

    def previous_page_registro(self):
        """Página anterior de registros"""
        if self.current_page_registro > 1:
            self.current_page_registro -= 1
            self.calculate_registro_pagination()