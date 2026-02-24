import reflex as rx
from typing import List
from TFuerte.api.solicitudes_rm_api import SolicitudesRMApi
from TFuerte.api.admin_rm_api import AdminRMApi
from TFuerte.api.financiamiento_api import FinanciamientoApi
from TFuerte.utilss.word_generator_fin import generar_word_solicitud_fin
from TFuerte.routes import Route
from datetime import datetime

class AdminRMState(rx.State):
    """Estado para el dashboard del Administrador/Presidente (Maikel)"""
    
    # Datos RECURSOS RM
    solicitudes_pendientes: List[dict] = []
    solicitudes_aprobadas: List[dict] = []
    
    # Datos FINANCIAMIENTO
    solicitudes_fin_pendientes: List[dict] = []
    solicitudes_fin_aprobadas: List[dict] = []
    
    # Estados de UI (RECURSOS RM)
    loading: bool = False
    show_aprobar_dialog: bool = False
    show_rechazar_dialog: bool = False
    selected_solicitud: dict = {}
    search_value: str = ""
    
    # Diálogo de detalles de recursos
    show_detalle_dialog_recursos: bool = False
    solicitud_detalle_recursos: dict = {}
    recursos_detalle_recursos: List[dict] = []
    
    # Estados de UI (FINANCIAMIENTO)
    loading_fin: bool = False
    show_aprobar_dialog_fin: bool = False
    show_rechazar_dialog_fin: bool = False
    show_generar_dialog_fin: bool = False
    selected_solicitud_fin: dict = {}
    search_value_fin: str = ""
    
    # ==================================================
    # NUEVO: Diálogo de detalles de financiamiento
    # ==================================================
    show_detalle_dialog_fin: bool = False
    solicitud_detalle_fin: dict = {}
    recursos_detalle_fin: List[dict] = []
    
    # Variable para el motivo del rechazo
    motivo_rechazo: str = ""
    motivo_rechazo_fin: str = ""
    
    # Usuario actual
    current_admin: dict = {}
    is_authenticated: bool = False
    
    # Credenciales para login
    username: str = ""
    password: str = ""
    error_message: str = ""
    
    # ==================================================
    # PAGINACIÓN PARA RECURSOS RM
    # ==================================================
    recursos_paginated: List[dict] = []
    recursos_current_page: int = 1
    recursos_items_per_page: int = 10
    recursos_total_pages: int = 1
    recursos_page_numbers: List[int] = []

    # ==================================================
    # PAGINACIÓN PARA FINANCIAMIENTO
    # ==================================================
    financiamiento_paginated: List[dict] = []
    fin_current_page: int = 1
    fin_items_per_page: int = 10
    fin_total_pages: int = 1
    fin_page_numbers: List[int] = []
    
    # Setters
    def set_username(self, username: str):
        self.username = username
    
    def set_password(self, password: str):
        self.password = password
    
    def set_motivo_rechazo(self, motivo: str):
        self.motivo_rechazo = motivo
    
    def set_motivo_rechazo_fin(self, motivo: str):
        self.motivo_rechazo_fin = motivo
    
    # ==================== MÉTODOS FINANCIAMIENTO ====================
    
    @rx.event
    def load_data_fin(self):
        """Carga las solicitudes de financiamiento pendientes para admin"""
        self.loading_fin = True
        yield
        
        solicitudes_pendientes = FinanciamientoApi.get_solicitudes_fin_pendientes_admin()
        
        # Agrupar por número de solicitud
        solicitudes_agrupadas = {}
        for solicitud in solicitudes_pendientes:
            numero_solicitud = solicitud.get("numero_solicitud")
            if not numero_solicitud:
                numero_solicitud = f"FIN-{solicitud.get('id')}"
            
            if numero_solicitud not in solicitudes_agrupadas:
                solicitudes_agrupadas[numero_solicitud] = {
                    "id": solicitud.get("id"),
                    "numero_solicitud": numero_solicitud,
                    "Area solicitante": solicitud.get("Area solicitante"),
                    "Fecha": solicitud.get("Fecha"),
                    "Orden de trabajo": solicitud.get("Orden de trabajo"),
                    "Total": solicitud.get("Total", 0),
                    "estado": solicitud.get("estado", "aprobado_revfin"),
                    "num_recursos": 1,
                    "recursos": [solicitud]
                }
            else:
                solicitudes_agrupadas[numero_solicitud]["num_recursos"] += 1
                solicitudes_agrupadas[numero_solicitud]["recursos"].append(solicitud)
                solicitudes_agrupadas[numero_solicitud]["Total"] = max(
                    solicitudes_agrupadas[numero_solicitud]["Total"],
                    solicitud.get("Total", 0)
                )
        
        self.solicitudes_fin_pendientes = list(solicitudes_agrupadas.values())
        self.reset_fin_pagination()
        self.loading_fin = False
    
    def filter_solicitudes_fin(self, search_value: str):
        self.search_value_fin = search_value
        if not search_value:
            return self.load_data_fin()
        
        search_term = search_value.lower()
        filtered = []
        for s in self.solicitudes_fin_pendientes:
            if (search_term in s.get("Area solicitante", "").lower() or
                search_term in s.get("Orden de trabajo", "").lower() or
                search_term in str(s.get("Total", "")).lower()):
                filtered.append(s)
        
        self.solicitudes_fin_pendientes = filtered
        self.reset_fin_pagination()
    
    # Diálogos para financiamiento
    def open_aprobar_dialog_fin(self, solicitud: dict):
        self.selected_solicitud_fin = solicitud
        self.show_aprobar_dialog_fin = True
    
    def close_aprobar_dialog_fin(self):
        self.show_aprobar_dialog_fin = False
        self.selected_solicitud_fin = {}
    
    def open_rechazar_dialog_fin(self, solicitud: dict):
        self.selected_solicitud_fin = solicitud
        self.show_rechazar_dialog_fin = True
        self.motivo_rechazo_fin = ""
    
    def close_rechazar_dialog_fin(self):
        self.show_rechazar_dialog_fin = False
        self.selected_solicitud_fin = {}
        self.motivo_rechazo_fin = ""
    
    def open_generar_dialog_fin(self, solicitud: dict):
        self.selected_solicitud_fin = solicitud
        self.show_generar_dialog_fin = True
    
    def close_generar_dialog_fin(self):
        self.show_generar_dialog_fin = False
        self.selected_solicitud_fin = {}
    
    def set_show_aprobar_dialog_fin(self, show: bool):
        self.show_aprobar_dialog_fin = show
        if not show:
            self.selected_solicitud_fin = {}
    
    def set_show_rechazar_dialog_fin(self, show: bool):
        self.show_rechazar_dialog_fin = show
        if not show:
            self.selected_solicitud_fin = {}
            self.motivo_rechazo_fin = ""
    
    def set_show_generar_dialog_fin(self, show: bool):
        self.show_generar_dialog_fin = show
        if not show:
            self.selected_solicitud_fin = {}
    
    # ==================================================
    # NUEVO: Métodos para diálogo de detalles de financiamiento
    # ==================================================
    def open_detalle_dialog_fin(self, solicitud: dict):
        self.solicitud_detalle_fin = solicitud
        self.recursos_detalle_fin = solicitud.get("recursos", [])
        self.show_detalle_dialog_fin = True
    
    def close_detalle_dialog_fin(self):
        self.show_detalle_dialog_fin = False
        self.solicitud_detalle_fin = {}
        self.recursos_detalle_fin = []
    
    def set_show_detalle_dialog_fin(self, show: bool):
        self.show_detalle_dialog_fin = show
        if not show:
            self.solicitud_detalle_fin = {}
            self.recursos_detalle_fin = []
    
    @rx.event
    def aprobar_solicitud_fin(self):
        if not self.selected_solicitud_fin:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return

        numero_solicitud = self.selected_solicitud_fin.get("numero_solicitud")
        recursos = FinanciamientoApi.get_solicitud_fin_by_numero(numero_solicitud)

        if not recursos:
            yield rx.toast.error("❌ No se encontraron recursos para esta solicitud")
            return

        admin_usuario = self.current_admin.get("usuario", "Maikel")

        self.loading_fin = True
        yield

        try:
            exito = True
            for recurso in recursos:
                result = FinanciamientoApi.aprobar_por_admin(recurso["id"], admin_usuario)
                if not result:
                    exito = False
                    yield rx.toast.error(f"❌ Error al aprobar recurso {recurso['id']}")
                    break

            if exito:
                self.close_aprobar_dialog_fin()
                yield from self.load_data_fin()
                yield rx.toast.success("✅ Solicitud de financiamiento aprobada")
        except Exception as e:
            print(f"❌ Error en aprobar_solicitud_fin: {e}")
            yield rx.toast.error(f"❌ Error interno: {str(e)}")
        finally:
            self.loading_fin = False
            yield
    
    @rx.event
    def rechazar_solicitud_fin(self):
        if not self.selected_solicitud_fin:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return

        numero_solicitud = self.selected_solicitud_fin.get("numero_solicitud")
        recursos = FinanciamientoApi.get_solicitud_fin_by_numero(numero_solicitud)

        if not recursos:
            yield rx.toast.error("❌ No se encontraron recursos para esta solicitud")
            return

        motivo = self.motivo_rechazo_fin if self.motivo_rechazo_fin else "Rechazado por Administración"

        self.loading_fin = True
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
                self.close_rechazar_dialog_fin()
                yield from self.load_data_fin()
                yield rx.toast.success("✅ Solicitud de financiamiento rechazada")
        except Exception as e:
            print(f"❌ Error en rechazar_solicitud_fin: {e}")
            yield rx.toast.error(f"❌ Error interno: {str(e)}")
        finally:
            self.loading_fin = False
            yield
    
    @rx.event
    def generar_documento_fin(self):
        if not self.selected_solicitud_fin:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return
        
        numero_solicitud = self.selected_solicitud_fin.get("numero_solicitud")
        
        self.loading_fin = True
        yield
        
        try:
            from TFuerte.api.financiamiento_api import FinanciamientoApi
            datos_completos = FinanciamientoApi.get_solicitud_fin_con_solicitante(numero_solicitud)
            
            if not datos_completos.get("recursos"):
                yield rx.toast.error("❌ No se encontraron recursos para esta solicitud")
                self.loading_fin = False
                return
            
            recursos = datos_completos["recursos"]
            solicitante = datos_completos["solicitante"]
            
            word_content = generar_word_solicitud_fin(numero_solicitud, recursos, solicitante)
            
            if not word_content:
                yield rx.toast.error("❌ Error al generar el documento")
                self.loading_fin = False
                return
            
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"Solicitud_Fin_{numero_solicitud}_{fecha_actual}.docx"
            
            self.close_generar_dialog_fin()
            
            yield rx.toast.success(f"✅ Documento generado: {nombre_archivo}")
            
            return rx.download(
                data=word_content,
                filename=nombre_archivo
            )
            
        except Exception as e:
            print(f"❌ Error generando documento: {e}")
            import traceback
            traceback.print_exc()
            yield rx.toast.error("❌ Error al generar el documento")
        finally:
            self.loading_fin = False
    
    # ==================== MÉTODOS EXISTENTES (RECURSOS RM) ====================
    
    @rx.event
    def sign_in(self):
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
            if user.get("rol") == "admin":
                self.is_authenticated = True
                self.current_admin = user
                
                self.username = ""
                self.password = ""
                
                yield rx.toast.success("✅ Inicio de sesión exitoso")
                yield rx.redirect(Route.ADMIN_RM_DASHBOARD.value)
            else:
                self.error_message = "No tienes permisos para acceder a este panel"
                yield rx.toast.error("❌ No tienes permisos")
        else:
            self.error_message = response["error"] or "Error al iniciar sesión"
            yield rx.toast.error(self.error_message)
        
        self.loading = False
    
    @rx.event
    def load_data(self):
        """Carga las solicitudes RM pendientes para admin"""
        self.loading = True
        yield
        
        solicitudes_pendientes = SolicitudesRMApi.get_solicitudes_rm_pendientes_admin()
        
        solicitudes_procesadas = []
        for solicitud in solicitudes_pendientes:
            solicitud_procesada = solicitud.copy()
            
            # Formatear fechas
            if "fecha_creacion" in solicitud_procesada and solicitud_procesada["fecha_creacion"]:
                fecha = solicitud_procesada["fecha_creacion"]
                if isinstance(fecha, str) and len(fecha) >= 10:
                    solicitud_procesada["fecha_creacion"] = fecha[:10]
            
            if "fecha_aprobacion_tecnica" in solicitud_procesada and solicitud_procesada["fecha_aprobacion_tecnica"]:
                fecha = solicitud_procesada["fecha_aprobacion_tecnica"]
                if isinstance(fecha, str) and len(fecha) >= 10:
                    solicitud_procesada["fecha_aprobacion_tecnica"] = fecha[:10]
            
            if "Fecha" in solicitud_procesada and solicitud_procesada["Fecha"]:
                fecha = solicitud_procesada["Fecha"]
                if isinstance(fecha, str) and len(fecha) >= 10:
                    solicitud_procesada["Fecha"] = fecha[:10]
            
            # Extraer datos del primer recurso para compatibilidad (opcional)
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
            
            # AÑADIR: número de recursos
            solicitud_procesada["num_recursos"] = len(recursos)
            
            solicitudes_procesadas.append(solicitud_procesada)
        
        self.solicitudes_pendientes = solicitudes_procesadas
        self.reset_recursos_pagination()
        self.loading = False
    
    def filter_solicitudes(self, search_value: str):
        self.search_value = search_value
        if not search_value:
            return self.load_data()
        
        search_term = search_value.lower()
        filtered = []
        for s in self.solicitudes_pendientes:
            if (search_term in s.get("Centro costo", "").lower() or
                search_term in s.get("Orden trabajo", "").lower() or
                search_term in s.get("Descripcion", "").lower()):
                filtered.append(s)
        
        self.solicitudes_pendientes = filtered
        self.reset_recursos_pagination()
    
    # Diálogos para recursos RM
    def open_aprobar_dialog(self, solicitud: dict):
        self.selected_solicitud = solicitud
        self.show_aprobar_dialog = True
    
    def close_aprobar_dialog(self):
        self.show_aprobar_dialog = False
        self.selected_solicitud = {}
    
    def open_rechazar_dialog(self, solicitud: dict):
        self.selected_solicitud = solicitud
        self.show_rechazar_dialog = True
        self.motivo_rechazo = ""
    
    def close_rechazar_dialog(self):
        self.show_rechazar_dialog = False
        self.selected_solicitud = {}
        self.motivo_rechazo = ""
    
    def set_show_aprobar_dialog(self, show: bool):
        self.show_aprobar_dialog = show
        if not show:
            self.selected_solicitud = {}
    
    def set_show_rechazar_dialog(self, show: bool):
        self.show_rechazar_dialog = show
        if not show:
            self.selected_solicitud = {}
            self.motivo_rechazo = ""

    # Métodos para diálogo de detalles de recursos
    def open_detalle_dialog_recursos(self, solicitud: dict):
        self.solicitud_detalle_recursos = solicitud
        self.recursos_detalle_recursos = solicitud.get("recursos", [])
        self.show_detalle_dialog_recursos = True
    
    def close_detalle_dialog_recursos(self):
        self.show_detalle_dialog_recursos = False
        self.solicitud_detalle_recursos = {}
        self.recursos_detalle_recursos = []
    
    def set_show_detalle_dialog_recursos(self, show: bool):
        self.show_detalle_dialog_recursos = show
        if not show:
            self.solicitud_detalle_recursos = {}
            self.recursos_detalle_recursos = []
    
    # Métodos de aprobación (recursos)
    @rx.event
    def aprobar_solicitud(self):
        if not self.selected_solicitud:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return

        solicitud_id = self.selected_solicitud.get("id")
        admin_usuario = self.current_admin.get("usuario", "Maikel")

        self.loading = True
        yield

        try:
            result = SolicitudesRMApi.aprobar_por_admin(solicitud_id, admin_usuario)

            if result:
                self.close_aprobar_dialog()
                yield from self.load_data()
                yield rx.toast.success("✅ Solicitud aprobada por Administración")
            else:
                yield rx.toast.error("❌ Error al aprobar la solicitud")
        except Exception as e:
            print(f"❌ Error en aprobar_solicitud: {e}")
            yield rx.toast.error(f"❌ Error interno: {str(e)}")
        finally:
            self.loading = False
            yield
    
    @rx.event
    def rechazar_solicitud(self):
        if not self.selected_solicitud:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return

        solicitud_id = self.selected_solicitud.get("id")
        motivo = self.motivo_rechazo if self.motivo_rechazo else "Rechazado por Administración"

        self.loading = True
        yield

        try:
            result = SolicitudesRMApi.rechazar_solicitud_rm(solicitud_id, motivo)

            if result:
                self.close_rechazar_dialog()
                yield from self.load_data()
                yield rx.toast.success("✅ Solicitud rechazada")
            else:
                yield rx.toast.error("❌ Error al rechazar la solicitud")
        except Exception as e:
            print(f"❌ Error en rechazar_solicitud: {e}")
            yield rx.toast.error(f"❌ Error interno: {str(e)}")
        finally:
            self.loading = False
            yield
    
    @rx.event
    def sign_out(self):
        self.is_authenticated = False
        self.current_admin = {}
        yield rx.toast.success("✅ Sesión cerrada exitosamente")
        yield rx.redirect(Route.ADMIN_RM_LOGIN.value)
    
    # Variables computadas
    @rx.var
    def solicitudes_count(self) -> int:
        return len(self.solicitudes_pendientes)
    
    @rx.var
    def solicitudes_fin_count(self) -> int:
        return len(self.solicitudes_fin_pendientes)
    
    @rx.var
    def admin_name(self) -> str:
        return self.current_admin.get("usuario", "Administrador")
    
    @rx.var
    def admin_cargo(self) -> str:
        return self.current_admin.get("cargo", "Presidente")
    
    @rx.var
    def total_recursos_pendientes(self) -> int:
        total = 0
        for solicitud in self.solicitudes_pendientes:
            total += len(solicitud.get("recursos", []))
        return total
    
    def reset_loading_states(self):
        self.loading = False
        self.loading_fin = False

    # ==================================================
    # MÉTODOS DE PAGINACIÓN PARA RECURSOS RM
    # ==================================================
    
    def calculate_recursos_pagination(self):
        total_items = len(self.solicitudes_pendientes)

        if total_items == 0:
            self.recursos_total_pages = 1
            self.recursos_paginated = []
        else:
            self.recursos_total_pages = max(1, (total_items + self.recursos_items_per_page - 1) // self.recursos_items_per_page)

        if self.recursos_current_page > self.recursos_total_pages:
            self.recursos_current_page = max(1, self.recursos_total_pages)

        start_idx = (self.recursos_current_page - 1) * self.recursos_items_per_page
        end_idx = min(start_idx + self.recursos_items_per_page, total_items)

        if total_items > 0:
            self.recursos_paginated = self.solicitudes_pendientes[start_idx:end_idx]
        else:
            self.recursos_paginated = []

        self.calculate_recursos_page_numbers()

    def calculate_recursos_page_numbers(self):
        max_pages_to_show = 4
        current = self.recursos_current_page
        total = self.recursos_total_pages

        if total <= max_pages_to_show:
            self.recursos_page_numbers = list(range(1, total + 1))
            return

        start = max(1, current - 1)
        end = min(total, start + max_pages_to_show - 1)

        if end - start + 1 < max_pages_to_show:
            start = max(1, end - max_pages_to_show + 1)

        self.recursos_page_numbers = list(range(start, end + 1))

    def go_to_page_recursos(self, page_number: int):
        if 1 <= page_number <= self.recursos_total_pages:
            self.recursos_current_page = page_number
            self.calculate_recursos_pagination()

    def next_page_recursos(self):
        if self.recursos_current_page < self.recursos_total_pages:
            self.recursos_current_page += 1
            self.calculate_recursos_pagination()

    def previous_page_recursos(self):
        if self.recursos_current_page > 1:
            self.recursos_current_page -= 1
            self.calculate_recursos_pagination()

    def reset_recursos_pagination(self):
        self.recursos_current_page = 1
        self.calculate_recursos_pagination()

    # ==================================================
    # MÉTODOS DE PAGINACIÓN PARA FINANCIAMIENTO
    # ==================================================
    
    def calculate_fin_pagination(self):
        total_items = len(self.solicitudes_fin_pendientes)

        if total_items == 0:
            self.fin_total_pages = 1
            self.financiamiento_paginated = []
        else:
            self.fin_total_pages = max(1, (total_items + self.fin_items_per_page - 1) // self.fin_items_per_page)

        if self.fin_current_page > self.fin_total_pages:
            self.fin_current_page = max(1, self.fin_total_pages)

        start_idx = (self.fin_current_page - 1) * self.fin_items_per_page
        end_idx = min(start_idx + self.fin_items_per_page, total_items)

        if total_items > 0:
            self.financiamiento_paginated = self.solicitudes_fin_pendientes[start_idx:end_idx]
        else:
            self.financiamiento_paginated = []

        self.calculate_fin_page_numbers()

    def calculate_fin_page_numbers(self):
        max_pages_to_show = 4
        current = self.fin_current_page
        total = self.fin_total_pages

        if total <= max_pages_to_show:
            self.fin_page_numbers = list(range(1, total + 1))
            return

        start = max(1, current - 1)
        end = min(total, start + max_pages_to_show - 1)

        if end - start + 1 < max_pages_to_show:
            start = max(1, end - max_pages_to_show + 1)

        self.fin_page_numbers = list(range(start, end + 1))

    def go_to_page_fin(self, page_number: int):
        if 1 <= page_number <= self.fin_total_pages:
            self.fin_current_page = page_number
            self.calculate_fin_pagination()

    def next_page_fin(self):
        if self.fin_current_page < self.fin_total_pages:
            self.fin_current_page += 1
            self.calculate_fin_pagination()

    def previous_page_fin(self):
        if self.fin_current_page > 1:
            self.fin_current_page -= 1
            self.calculate_fin_pagination()

    def reset_fin_pagination(self):
        self.fin_current_page = 1
        self.calculate_fin_pagination()