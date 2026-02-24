import reflex as rx
from typing import List
from TFuerte.api.financiamiento_api import FinanciamientoApi
from TFuerte.api.revfin_auth_api import RevFinAuthAPI
from TFuerte.routes import Route

class FinanciamientoState(rx.State):
    """Estado para las solicitudes de financiamiento"""
    
    # Datos para RevFin
    solicitudes_pendientes_revfin: List[dict] = []
    
    # Estados de UI para RevFin
    loading_revfin: bool = False
    show_aprobar_dialog_revfin: bool = False
    show_rechazar_dialog_revfin: bool = False
    selected_solicitud_revfin: dict = {}
    search_value_revfin: str = ""
    motivo_rechazo_revfin: str = ""
    
    # ==================================================
    # NUEVO: Diálogo de detalles de financiamiento
    # ==================================================
    show_detalle_dialog_revfin: bool = False
    solicitud_detalle_revfin: dict = {}
    recursos_detalle_revfin: List[dict] = []
    
    # Usuario actual de RevFin
    current_revfin: dict = {}
    is_authenticated_revfin: bool = False
    
    # Credenciales para login de RevFin
    username_revfin: str = ""
    password_revfin: str = ""
    error_message_revfin: str = ""
    
    # ==================================================
    # PAGINACIÓN PARA REVFIN
    # ==================================================
    solicitudes_revfin_paginated: List[dict] = []
    revfin_current_page: int = 1
    revfin_items_per_page: int = 10
    revfin_total_pages: int = 1
    revfin_page_numbers: List[int] = []
    
    # Setters para RevFin
    def set_username_revfin(self, username: str):
        self.username_revfin = username
    
    def set_password_revfin(self, password: str):
        self.password_revfin = password
    
    def set_motivo_rechazo_revfin(self, motivo: str):
        self.motivo_rechazo_revfin = motivo
    
    # Métodos de autenticación para RevFin
    @rx.event
    def sign_in_revfin(self):
        """Inicia sesión como Revisor Financiero"""
        self.loading_revfin = True
        self.error_message_revfin = ""
        yield
        
        if not self.username_revfin or not self.password_revfin:
            self.error_message_revfin = "Usuario y contraseña son requeridos"
            self.loading_revfin = False
            return
        
        response = RevFinAuthAPI.sign_in(self.username_revfin, self.password_revfin)
        
        if response["success"]:
            self.is_authenticated_revfin = True
            self.current_revfin = response["user"]
            
            self.username_revfin = ""
            self.password_revfin = ""
            
            yield rx.toast.success(
                "✅ Inicio de sesión exitoso",
                position="top-right",
                duration=3000
            )
            
            yield rx.redirect(Route.REVFIN_DASHBOARD.value)
        else:
            self.error_message_revfin = response["error"] or "Error al iniciar sesión"
            yield rx.toast.error(
                self.error_message_revfin,
                position="top-right",
                duration=4000
            )
        
        self.loading_revfin = False
    
    # Cargar datos para RevFin (MODIFICADO: agrupar por número de solicitud)
    @rx.event
    def load_data_revfin(self):
        """Carga las solicitudes pendientes para revisión financiera y las agrupa por número de solicitud"""
        self.loading_revfin = True
        yield
        
        solicitudes_pendientes = FinanciamientoApi.get_solicitudes_fin_pendientes_revfin()
        
        # Agrupar por número de solicitud
        solicitudes_agrupadas = {}
        for solicitud in solicitudes_pendientes:
            numero_solicitud = solicitud.get("numero_solicitud")
            if not numero_solicitud:
                # Si no tiene número de solicitud (caso raro), se asigna uno basado en ID
                numero_solicitud = f"FIN-{solicitud.get('id')}"
            
            # Formatear fechas (para la cabecera del grupo)
            fecha = solicitud.get("Fecha", "")
            if isinstance(fecha, str) and len(fecha) >= 10:
                fecha = fecha[:10]
            
            if numero_solicitud not in solicitudes_agrupadas:
                solicitudes_agrupadas[numero_solicitud] = {
                    "id": solicitud.get("id"),  # ID del primer recurso (puede no ser necesario)
                    "numero_solicitud": numero_solicitud,
                    "Area solicitante": solicitud.get("Area solicitante"),
                    "Fecha": fecha,
                    "Orden de trabajo": solicitud.get("Orden de trabajo"),
                    "Total": solicitud.get("Total", 0),
                    "estado": solicitud.get("estado", "pendiente_revfin"),
                    "num_recursos": 1,
                    "recursos": [solicitud]
                }
            else:
                solicitudes_agrupadas[numero_solicitud]["num_recursos"] += 1
                solicitudes_agrupadas[numero_solicitud]["recursos"].append(solicitud)
                # Actualizar el total (ya está calculado por el trigger, pero por si acaso)
                solicitudes_agrupadas[numero_solicitud]["Total"] = max(
                    solicitudes_agrupadas[numero_solicitud]["Total"],
                    solicitud.get("Total", 0)
                )
        
        self.solicitudes_pendientes_revfin = list(solicitudes_agrupadas.values())
        self.reset_revfin_pagination()
        self.loading_revfin = False
    
    # Filtrar solicitudes para RevFin (ahora sobre los grupos)
    def filter_solicitudes_revfin(self, search_value: str):
        """Filtra las solicitudes por término de búsqueda (sobre los grupos)"""
        self.search_value_revfin = search_value
        
        if not search_value:
            return self.load_data_revfin()
        
        search_term = search_value.lower()
        filtered = []
        for s in self.solicitudes_pendientes_revfin:
            if (search_term in s.get("Area solicitante", "").lower() or
                search_term in s.get("Orden de trabajo", "").lower() or
                search_term in str(s.get("Total", "")).lower()):
                filtered.append(s)
        
        self.solicitudes_pendientes_revfin = filtered
        self.reset_revfin_pagination()
    
    # Diálogos para RevFin
    def open_aprobar_dialog_revfin(self, solicitud: dict):
        self.selected_solicitud_revfin = solicitud
        self.show_aprobar_dialog_revfin = True
    
    def close_aprobar_dialog_revfin(self):
        self.show_aprobar_dialog_revfin = False
        self.selected_solicitud_revfin = {}
    
    def open_rechazar_dialog_revfin(self, solicitud: dict):
        self.selected_solicitud_revfin = solicitud
        self.show_rechazar_dialog_revfin = True
        self.motivo_rechazo_revfin = ""
    
    def close_rechazar_dialog_revfin(self):
        self.show_rechazar_dialog_revfin = False
        self.selected_solicitud_revfin = {}
        self.motivo_rechazo_revfin = ""
    
    def set_show_aprobar_dialog_revfin(self, show: bool):
        self.show_aprobar_dialog_revfin = show
        if not show:
            self.selected_solicitud_revfin = {}
    
    def set_show_rechazar_dialog_revfin(self, show: bool):
        self.show_rechazar_dialog_revfin = show
        if not show:
            self.selected_solicitud_revfin = {}
            self.motivo_rechazo_revfin = ""
    
    # ==================================================
    # NUEVO: Métodos para diálogo de detalles
    # ==================================================
    def open_detalle_dialog_revfin(self, solicitud: dict):
        self.solicitud_detalle_revfin = solicitud
        self.recursos_detalle_revfin = solicitud.get("recursos", [])
        self.show_detalle_dialog_revfin = True
    
    def close_detalle_dialog_revfin(self):
        self.show_detalle_dialog_revfin = False
        self.solicitud_detalle_revfin = {}
        self.recursos_detalle_revfin = []
    
    def set_show_detalle_dialog_revfin(self, show: bool):
        self.show_detalle_dialog_revfin = show
        if not show:
            self.solicitud_detalle_revfin = {}
            self.recursos_detalle_revfin = []
    
    # Métodos de aprobación/rechazo para RevFin (ahora sobre el grupo)
    @rx.event
    def aprobar_solicitud_revfin(self):
        if not self.selected_solicitud_revfin:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return

        numero_solicitud = self.selected_solicitud_revfin.get("numero_solicitud")
        recursos = self.selected_solicitud_revfin.get("recursos", [])

        if not recursos:
            yield rx.toast.error("❌ No se encontraron recursos para esta solicitud")
            return

        revfin_usuario = self.current_revfin.get("usuario", "Revisor Financiero")

        self.loading_revfin = True
        yield

        try:
            exito = True
            for recurso in recursos:
                result = FinanciamientoApi.aprobar_por_revfin(recurso["id"], revfin_usuario)
                if not result:
                    exito = False
                    yield rx.toast.error(f"❌ Error al aprobar recurso {recurso['id']}")
                    break

            if exito:
                self.close_aprobar_dialog_revfin()
                yield from self.load_data_revfin()
                yield rx.toast.success("✅ Solicitud de financiamiento aprobada")
            else:
                yield rx.toast.error("❌ Error al aprobar la solicitud")
        except Exception as e:
            print(f"❌ Error en aprobar_solicitud_revfin: {e}")
            yield rx.toast.error(f"❌ Error interno: {str(e)}")
        finally:
            self.loading_revfin = False
            yield
    
    @rx.event
    def rechazar_solicitud_revfin(self):
        if not self.selected_solicitud_revfin:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return

        numero_solicitud = self.selected_solicitud_revfin.get("numero_solicitud")
        recursos = self.selected_solicitud_revfin.get("recursos", [])
        motivo = self.motivo_rechazo_revfin if self.motivo_rechazo_revfin else "Rechazado por Revisor Financiero"

        if not recursos:
            yield rx.toast.error("❌ No se encontraron recursos para esta solicitud")
            return

        self.loading_revfin = True
        yield

        try:
            exito = True
            for recurso in recursos:
                result = FinanciamientoApi.rechazar_solicitud_fin(recurso["id"], motivo)
                if not result:
                    exito = False
                    yield rx.toast.error(f"❌ Error al rechazar recurso {recurso['id']}")
                    break

            if exito:
                self.close_rechazar_dialog_revfin()
                yield from self.load_data_revfin()
                yield rx.toast.success("✅ Solicitud de financiamiento rechazada")
            else:
                yield rx.toast.error("❌ Error al rechazar la solicitud")
        except Exception as e:
            print(f"❌ Error en rechazar_solicitud_revfin: {e}")
            yield rx.toast.error(f"❌ Error interno: {str(e)}")
        finally:
            self.loading_revfin = False
            yield
    
    # Cerrar sesión RevFin
    @rx.event
    def sign_out_revfin(self):
        self.is_authenticated_revfin = False
        self.current_revfin = {}
        
        yield rx.toast.success(
            "✅ Sesión cerrada exitosamente",
            position="top-right",
            duration=3000
        )
        
        yield rx.redirect(Route.REVFIN_LOGIN.value)
    
    # Variables computadas
    @rx.var
    def solicitudes_count_revfin(self) -> int:
        return len(self.solicitudes_pendientes_revfin)
    
    @rx.var
    def revfin_name(self) -> str:
        return self.current_revfin.get("usuario", "Revisor Financiero")
    
    def reset_loading_revfin(self):
        """Resetea el estado de carga al cargar la página"""
        self.loading_revfin = False

    # ==================================================
    # MÉTODOS DE PAGINACIÓN PARA REVFIN
    # ==================================================
    
    def calculate_revfin_pagination(self):
        """Calcula la paginación para la tabla de solicitudes de financiamiento."""
        total_items = len(self.solicitudes_pendientes_revfin)

        if total_items == 0:
            self.revfin_total_pages = 1
            self.solicitudes_revfin_paginated = []
        else:
            self.revfin_total_pages = max(1, (total_items + self.revfin_items_per_page - 1) // self.revfin_items_per_page)

        if self.revfin_current_page > self.revfin_total_pages:
            self.revfin_current_page = max(1, self.revfin_total_pages)

        start_idx = (self.revfin_current_page - 1) * self.revfin_items_per_page
        end_idx = min(start_idx + self.revfin_items_per_page, total_items)

        if total_items > 0:
            self.solicitudes_revfin_paginated = self.solicitudes_pendientes_revfin[start_idx:end_idx]
        else:
            self.solicitudes_revfin_paginated = []

        self.calculate_revfin_page_numbers()

    def calculate_revfin_page_numbers(self):
        max_pages_to_show = 4
        current = self.revfin_current_page
        total = self.revfin_total_pages

        if total <= max_pages_to_show:
            self.revfin_page_numbers = list(range(1, total + 1))
            return

        start = max(1, current - 1)
        end = min(total, start + max_pages_to_show - 1)

        if end - start + 1 < max_pages_to_show:
            start = max(1, end - max_pages_to_show + 1)

        self.revfin_page_numbers = list(range(start, end + 1))

    def go_to_page_revfin(self, page_number: int):
        if 1 <= page_number <= self.revfin_total_pages:
            self.revfin_current_page = page_number
            self.calculate_revfin_pagination()

    def next_page_revfin(self):
        if self.revfin_current_page < self.revfin_total_pages:
            self.revfin_current_page += 1
            self.calculate_revfin_pagination()

    def previous_page_revfin(self):
        if self.revfin_current_page > 1:
            self.revfin_current_page -= 1
            self.calculate_revfin_pagination()

    def reset_revfin_pagination(self):
        self.revfin_current_page = 1
        self.calculate_revfin_pagination()