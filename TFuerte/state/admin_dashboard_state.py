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
    
    def load_data(self):
        """Carga todos los datos necesarios"""
        self.loading = True
        yield
        
        # Cargar RegistroTF
        registro = RegistroTFAPI.get_all_registros()
        if registro:
            self.registro_data = registro
            self.registro_filtered = registro
        
        # Cargar Solicitudes
        solicitudes = SolicitudesAPI.get_all_solicitudes()
        if solicitudes:
            self.solicitudes_data = solicitudes
            # Filtrar solo las pendientes
            self.solicitudes_pendientes = [
                s for s in solicitudes 
                if s.get("estado") == "pendiente"
            ]
            # Calcular paginación inicial
            self.calculate_solicitudes_pagination()
        
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
        """Filtra los datos de RegistroTF"""
        self.search_registro = search_value
        
        if not search_value:
            self.registro_filtered = self.registro_data
            return
        
        search_term = search_value.lower()
        filtered = []
        for item in self.registro_data:
            if (search_term in item.get("Producto", "").lower() or
                search_term in item.get("Destino", "").lower() or
                search_term in item.get("Recibe", "").lower() or
                search_term in item.get("Cliente", "").lower()):
                filtered.append(item)
        
        self.registro_filtered = filtered
    
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
        """Aprueba la solicitud seleccionada - SIN DAR SALIDA AUTOMÁTICA"""
        if not self.selected_solicitud:
            yield rx.toast.error(
                "❌ No hay solicitud seleccionada",
                position="top-right",
                duration=4000
            )
            return
        
        solicitud_id = self.selected_solicitud.get("id")
        descripcion = self.selected_solicitud.get("Descripcion", "")
        cantidad_solicitada = self.selected_solicitud.get("Cantidad", 0)
        
        # Validar que haya cantidad
        if cantidad_solicitada <= 0:
            yield rx.toast.error(
                "❌ La cantidad debe ser mayor a 0",
                position="top-right",
                duration=4000
            )
            return
        
        # 1. Verificar productos disponibles
        productos = AlmacenAPI.get_all_items()
        producto_disponible = None
        
        for p in productos:
            if (descripcion.lower() in p.get("Descripcion del producto", "").lower() and
                p.get("Saldo", 0) >= cantidad_solicitada):
                producto_disponible = p
                break
        
        if not producto_disponible:
            yield rx.toast.error(
                f"❌ No se encontró producto con suficiente saldo: {descripcion}",
                position="top-right",
                duration=4000
            )
            return
        
        # 2. Usar el nombre de usuario almacenado en este estado
        admin_user = self.admin_username
        
        # 3. Solo actualizar estado de la solicitud a "aprobada" (NO dar salida)
        result = SolicitudesAPI.aprobar_solicitud(
            solicitud_id, 
            admin_user, 
            producto_disponible.get("Numero", 0)
        )
        
        if not result:
            yield rx.toast.error(
                "❌ Error al aprobar la solicitud",
                position="top-right",
                duration=4000
            )
            return
        
        # 4. Recargar datos
        self.close_aprobar_dialog()
        self.loading = True
        yield
        
        yield self.load_data()
        
        self.loading = False
        
        yield rx.toast.success(
            f"✅ Solicitud aprobada. El producto {descripcion} está listo para salida.",
            position="top-right",
            duration=4000
        )
    
    def rechazar_solicitud(self):
        """Rechaza la solicitud seleccionada"""
        if not self.selected_solicitud:
            yield rx.toast.error(
                "❌ No hay solicitud seleccionada",
                position="top-right",
                duration=4000
            )
            return
        
        solicitud_id = self.selected_solicitud.get("id")
        
        # Usar el nombre de usuario almacenado en este estado
        admin_user = self.admin_username
        
        SolicitudesAPI.rechazar_solicitud(solicitud_id, admin_user)
        
        # Recargar datos
        self.close_rechazar_dialog()
        self.loading = True
        yield
        
        yield self.load_data()
        
        self.loading = False
        
        yield rx.toast.success(
            "✅ Solicitud rechazada",
            position="top-right",
            duration=3000
        )
    
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