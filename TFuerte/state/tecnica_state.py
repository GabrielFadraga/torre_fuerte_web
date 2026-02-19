import reflex as rx
from typing import List
from TFuerte.api.solicitudes_rm_api import SolicitudesRMApi
from TFuerte.api.admin_rm_api import AdminRMApi
from TFuerte.routes import Route

class TecnicaState(rx.State):
    """Estado para el dashboard de Jefe de Área Técnica (Alexander)"""
    
    # Datos (AHORA CON RECURSOS)
    solicitudes_pendientes: List[dict] = []  # Cada dict tiene campo 'recursos'
    solicitudes_aprobadas: List[dict] = []   # Cada dict tiene campo 'recursos'
    
    # Estados de UI (SIN CAMBIOS)
    loading: bool = False
    show_aprobar_dialog: bool = False
    show_rechazar_dialog: bool = False
    selected_solicitud: dict = {}
    search_value: str = ""
    
    # Usuario actual (SIN CAMBIOS)
    current_admin: dict = {}
    is_authenticated: bool = False
    
    # Credenciales para login (SIN CAMBIOS)
    username: str = ""
    password: str = ""
    error_message: str = ""
    
    # ==================================================
    # PAGINACIÓN
    # ==================================================
    solicitudes_paginated: List[dict] = []
    current_page: int = 1
    items_per_page: int = 10
    total_pages: int = 1
    page_numbers: List[int] = []

    # Setters (SIN CAMBIOS)
    def set_username(self, username: str):
        self.username = username
    
    def set_password(self, password: str):
        self.password = password
    
    @rx.event
    def sign_in(self):
        """Inicia sesión como Jefe de Área Técnica (SIN CAMBIOS)"""
        self.loading = True
        self.error_message = ""
        yield
        
        if not self.username or not self.password:
            self.error_message = "Usuario y contraseña son requeridos"
            self.loading = False
            return
        
        response = AdminRMApi.sign_in(self.username, self.password)
        
        if response["success"]:
            user = response["user"]
            if user.get("rol") == "tecnica":
                self.is_authenticated = True
                self.current_admin = user
                
                self.username = ""
                self.password = ""
                
                yield rx.toast.success(
                    "✅ Inicio de sesión exitoso",
                    position="top-right",
                    duration=3000
                )
                
                yield rx.redirect(Route.TECNICA_DASHBOARD.value)
            else:
                self.error_message = "No tienes permisos para acceder a este panel"
                yield rx.toast.error(
                    "❌ No tienes permisos para acceder a este panel",
                    position="top-right",
                    duration=4000
                )
        else:
            self.error_message = response["error"] or "Error al iniciar sesión"
            yield rx.toast.error(
                self.error_message,
                position="top-right",
                duration=4000
            )
        
        self.loading = False
    
    @rx.event
    def load_data(self):
        """Carga las solicitudes pendientes (¡AHORA CON RECURSOS!)"""
        self.loading = True
        yield
        
        # ¡IMPORTANTE! get_solicitudes_rm_pendientes_tecnica() AHORA devuelve
        # solicitudes CON el campo 'recursos'
        solicitudes = SolicitudesRMApi.get_solicitudes_rm_pendientes_tecnica()
        
        # Formatear fechas y extraer primer recurso
        solicitudes_procesadas = []
        for solicitud in solicitudes:
            # Crear una copia para no modificar el original
            solicitud_procesada = solicitud.copy()
            
            # Formatear fechas
            if "fecha_creacion" in solicitud_procesada and solicitud_procesada["fecha_creacion"]:
                fecha = solicitud_procesada["fecha_creacion"]
                if isinstance(fecha, str) and len(fecha) >= 10:
                    solicitud_procesada["fecha_creacion"] = fecha[:10]
            
            if "Fecha" in solicitud_procesada and solicitud_procesada["Fecha"]:
                fecha = solicitud_procesada["Fecha"]
                if isinstance(fecha, str) and len(fecha) >= 10:
                    solicitud_procesada["Fecha"] = fecha[:10]
            
            # Extraer datos del primer recurso para facilitar el acceso
            recursos = solicitud_procesada.get("recursos", [])
            if recursos and len(recursos) > 0:
                primer_recurso = recursos[0]
                solicitud_procesada["Descripcion"] = primer_recurso.get("descripcion", "-")
                solicitud_procesada["Cantidad"] = primer_recurso.get("cantidad", "-")
                solicitud_procesada["UM"] = primer_recurso.get("unidad_medida", "-")
            else:
                solicitud_procesada["Descripcion"] = "-"
                solicitud_procesada["Cantidad"] = "-"
                solicitud_procesada["UM"] = "-"
            
            solicitudes_procesadas.append(solicitud_procesada)
        
        self.solicitudes_pendientes = solicitudes_procesadas
        self.reset_pagination()  # <-- Añadido
        self.loading = False
    
    def filter_solicitudes(self, search_value: str):
        """Filtra las solicitudes (¡AHORA BUSCA EN RECURSOS!)"""
        self.search_value = search_value
        
        if not search_value:
            return self.load_data()
        
        # Filtrar localmente - ¡AHORA TAMBIÉN BUSCA EN DESCRIPCIONES DE RECURSOS!
        search_term = search_value.lower()
        filtered = []
        for s in self.solicitudes_pendientes:
            # Buscar en campos principales
            match = False
            if (search_term in s.get("Centro costo", "").lower() or
                search_term in s.get("Orden trabajo", "").lower() or
                search_term in s.get("Descripcion", "").lower()):  # Ahora busca en Descripcion que viene del recurso
                match = True
            
            if match:
                filtered.append(s)
        
        self.solicitudes_pendientes = filtered
        self.reset_pagination()  # <-- Añadido
    
    # Diálogos (SIN CAMBIOS)
    def open_aprobar_dialog(self, solicitud: dict):
        self.selected_solicitud = solicitud
        self.show_aprobar_dialog = True
    
    def close_aprobar_dialog(self):
        self.show_aprobar_dialog = False
        self.selected_solicitud = {}
    
    def open_rechazar_dialog(self, solicitud: dict):
        self.selected_solicitud = solicitud
        self.show_rechazar_dialog = True
    
    def close_rechazar_dialog(self):
        self.show_rechazar_dialog = False
        self.selected_solicitud = {}
    
    def set_show_aprobar_dialog(self, show: bool):
        self.show_aprobar_dialog = show
    
    def set_show_rechazar_dialog(self, show: bool):
        self.show_rechazar_dialog = show
    
    # Métodos de aprobación (SIN CAMBIOS)
    @rx.event
    def aprobar_solicitud(self):
        if not self.selected_solicitud:
            yield rx.toast.error(
                "❌ No hay solicitud seleccionada",
                position="top-right",
                duration=4000
            )
            return

        solicitud_id = self.selected_solicitud.get("id")
        admin_usuario = self.current_admin.get("usuario", "Alexander")

        # Mostrar carga
        self.loading = True
        yield

        try:
            result = SolicitudesRMApi.aprobar_por_tecnica(solicitud_id, admin_usuario)

            if result:
                self.close_aprobar_dialog()
                
                # ✅ CORREGIDO: usar yield from para ejecutar el generador load_data
                yield from self.load_data()

                yield rx.toast.success(
                    "✅ Solicitud aprobada por Área Técnica",
                    position="top-right",
                    duration=3000
                )
            else:
                yield rx.toast.error(
                    "❌ Error al aprobar la solicitud",
                    position="top-right",
                    duration=4000
                )
        except Exception as e:
            print(f"❌ Error en aprobar_solicitud: {e}")
            yield rx.toast.error(
                f"❌ Error interno: {str(e)}",
                position="top-right",
                duration=4000
            )
        finally:
            self.loading = False
            yield
    
    @rx.event
    def rechazar_solicitud(self):
        if not self.selected_solicitud:
            yield rx.toast.error(
                "❌ No hay solicitud seleccionada",
                position="top-right",
                duration=4000
            )
            return

        solicitud_id = self.selected_solicitud.get("id")

        self.loading = True
        yield

        try:
            result = SolicitudesRMApi.rechazar_solicitud_rm(
                solicitud_id,
                "Rechazado por Área Técnica"
            )

            if result:
                self.close_rechazar_dialog()
                
                # ✅ CORREGIDO: usar yield from
                yield from self.load_data()

                yield rx.toast.success(
                    "✅ Solicitud rechazada",
                    position="top-right",
                    duration=3000
                )
            else:
                yield rx.toast.error(
                    "❌ Error al rechazar la solicitud",
                    position="top-right",
                    duration=4000
                )
        except Exception as e:
            print(f"❌ Error en rechazar_solicitud: {e}")
            yield rx.toast.error(
                f"❌ Error interno: {str(e)}",
                position="top-right",
                duration=4000
            )
        finally:
            self.loading = False
            yield
    
    @rx.event
    def sign_out(self):
        self.is_authenticated = False
        self.current_admin = {}
        
        yield rx.toast.success(
            "✅ Sesión cerrada exitosamente",
            position="top-right",
            duration=3000
        )
        
        yield rx.redirect(Route.TECNICA_LOGIN.value)
    
    # Variables computadas
    @rx.var
    def solicitudes_count(self) -> int:
        return len(self.solicitudes_pendientes)
    
    @rx.var
    def total_recursos_pendientes(self) -> int:
        total = 0
        for solicitud in self.solicitudes_pendientes:
            total += len(solicitud.get("recursos", []))
        return total
    
    def reset_loading(self):
        """Resetea el estado de carga al cargar la página"""
        self.loading = False

    # ==================================================
    # MÉTODOS DE PAGINACIÓN
    # ==================================================
    
    def calculate_pagination(self):
        """Calcula la paginación para la tabla de solicitudes pendientes."""
        total_items = len(self.solicitudes_pendientes)

        if total_items == 0:
            self.total_pages = 1
            self.solicitudes_paginated = []
        else:
            self.total_pages = max(1, (total_items + self.items_per_page - 1) // self.items_per_page)

        # Asegurar que la página actual esté dentro de los límites
        if self.current_page > self.total_pages:
            self.current_page = max(1, self.total_pages)

        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, total_items)

        if total_items > 0:
            self.solicitudes_paginated = self.solicitudes_pendientes[start_idx:end_idx]
        else:
            self.solicitudes_paginated = []

        self.calculate_page_numbers()

    def calculate_page_numbers(self):
        """Calcula los números de página a mostrar (máximo 4)."""
        max_pages_to_show = 4
        current = self.current_page
        total = self.total_pages

        if total <= max_pages_to_show:
            self.page_numbers = list(range(1, total + 1))
            return

        start = max(1, current - 1)
        end = min(total, start + max_pages_to_show - 1)

        if end - start + 1 < max_pages_to_show:
            start = max(1, end - max_pages_to_show + 1)

        self.page_numbers = list(range(start, end + 1))

    def go_to_page(self, page_number: int):
        """Navega a una página específica."""
        if 1 <= page_number <= self.total_pages:
            self.current_page = page_number
            self.calculate_pagination()

    def next_page(self):
        """Página siguiente."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.calculate_pagination()

    def previous_page(self):
        """Página anterior."""
        if self.current_page > 1:
            self.current_page -= 1
            self.calculate_pagination()

    def reset_pagination(self):
        """Resetea la paginación a la primera página."""
        self.current_page = 1
        self.calculate_pagination()