# TFuerte/state/admin_rm_state.py
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
    
    # Estados de UI (FINANCIAMIENTO)
    loading_fin: bool = False
    show_aprobar_dialog_fin: bool = False
    show_rechazar_dialog_fin: bool = False
    show_generar_dialog_fin: bool = False
    selected_solicitud_fin: dict = {}
    search_value_fin: str = ""
    
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
                # Si no tiene número de solicitud, es una solicitud antigua
                # Le asignamos un número basado en su ID
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
                # El Total ya está calculado por el trigger, pero por si acaso sumamos
                solicitudes_agrupadas[numero_solicitud]["Total"] = max(
                    solicitudes_agrupadas[numero_solicitud]["Total"],
                    solicitud.get("Total", 0)
                )
        
        self.solicitudes_fin_pendientes = list(solicitudes_agrupadas.values())
        self.loading_fin = False
    
    def filter_solicitudes_fin(self, search_value: str):
        """Filtra las solicitudes de financiamiento por término de búsqueda"""
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
    
    @rx.event
    def aprobar_solicitud_fin(self):
        """Aprueba una solicitud de financiamiento"""
        if not self.selected_solicitud_fin:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return
        
        # Obtener todos los recursos de esta solicitud
        numero_solicitud = self.selected_solicitud_fin.get("numero_solicitud")
        recursos = FinanciamientoApi.get_solicitud_fin_by_numero(numero_solicitud)
        
        if not recursos:
            yield rx.toast.error("❌ No se encontraron recursos para esta solicitud")
            return
        
        admin_usuario = self.current_admin.get("usuario", "Maikel")
        
        # Aprobar cada recurso individualmente
        for recurso in recursos:
            result = FinanciamientoApi.aprobar_por_admin(recurso["id"], admin_usuario)
            if not result:
                yield rx.toast.error(f"❌ Error al aprobar recurso {recurso['id']}")
                return
        
        self.close_aprobar_dialog_fin()
        
        self.loading_fin = True
        yield
        yield self.load_data_fin()
        self.loading_fin = False
        
        yield rx.toast.success("✅ Solicitud de financiamiento aprobada")
    
    @rx.event
    def rechazar_solicitud_fin(self):
        """Rechaza una solicitud de financiamiento"""
        if not self.selected_solicitud_fin:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return
        
        # Obtener todos los recursos de esta solicitud
        numero_solicitud = self.selected_solicitud_fin.get("numero_solicitud")
        recursos = FinanciamientoApi.get_solicitud_fin_by_numero(numero_solicitud)
        
        if not recursos:
            yield rx.toast.error("❌ No se encontraron recursos para esta solicitud")
            return
        
        motivo = self.motivo_rechazo_fin if self.motivo_rechazo_fin else "Rechazado por Administración"
        
        # Rechazar cada recurso individualmente
        for recurso in recursos:
            result = FinanciamientoApi.rechazar_solicitud_fin(recurso["id"], motivo)
            if not result:
                yield rx.toast.error(f"❌ Error al rechazar recurso {recurso['id']}")
                return
        
        self.close_rechazar_dialog_fin()
        
        self.loading_fin = True
        yield
        yield self.load_data_fin()
        self.loading_fin = False
        
        yield rx.toast.success("✅ Solicitud de financiamiento rechazada")
    
    @rx.event
    def generar_documento_fin(self):
        """Genera el documento Word para la solicitud de financiamiento"""
        if not self.selected_solicitud_fin:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return
        
        numero_solicitud = self.selected_solicitud_fin.get("numero_solicitud")
        
        self.loading_fin = True
        yield
        
        try:
            # Obtener datos del solicitante
            recursos = FinanciamientoApi.get_solicitud_fin_by_numero(numero_solicitud)
            if not recursos:
                yield rx.toast.error("❌ No se encontraron recursos para esta solicitud")
                self.loading_fin = False
                return
            
            primer_recurso = recursos[0]
            solicitante_id = primer_recurso.get("solicitante_id")
            
            # Aquí necesitarías obtener el solicitante de la base de datos
            # Por ahora usaremos datos de ejemplo
            solicitante = {
                "id": solicitante_id,
                "usuario": "Solicitante",
                "cargo": "Solicitante"
            }
            
            # Generar el documento Word
            word_content = generar_word_solicitud_fin(numero_solicitud, solicitante)
            
            if not word_content:
                yield rx.toast.error("❌ Error al generar el documento")
                self.loading_fin = False
                return
            
            # Crear nombre del archivo
            from datetime import datetime
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"Solicitud_Fin_{numero_solicitud}_{fecha_actual}.docx"
            
            self.close_generar_dialog_fin()
            
            yield rx.toast.success(f"✅ Documento generado: {nombre_archivo}")
            
            # Retornar el archivo para descarga
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
        """Inicia sesión como Administrador/Presidente"""
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
                
                yield rx.toast.success(
                    "✅ Inicio de sesión exitoso",
                    position="top-right",
                    duration=3000
                )
                
                yield rx.redirect(Route.ADMIN_RM_DASHBOARD.value)
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
        """Carga las solicitudes RM pendientes para admin"""
        self.loading = True
        yield
        
        solicitudes_pendientes = SolicitudesRMApi.get_solicitudes_rm_pendientes_admin()
        
        # Formatear fechas y extraer primer recurso
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
            
            # Extraer datos del primer recurso
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
        self.loading = False
    
    def filter_solicitudes(self, search_value: str):
        """Filtra las solicitudes RM por término de búsqueda"""
        self.search_value = search_value
        
        if not search_value:
            return self.load_data()
        
        search_term = search_value.lower()
        filtered = []
        for s in self.solicitudes_pendientes:
            if (search_term in s.get("Centro costo", "").lower() or
                search_term in s.get("Orden trabajo", "").lower() or
                search_term in s.get("Observaciones", "").lower() or
                search_term in s.get("Descripcion", "").lower()):
                filtered.append(s)
        
        self.solicitudes_pendientes = filtered

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
                continue
            
            if numero_solicitud not in solicitudes_agrupadas:
                solicitudes_agrupadas[numero_solicitud] = {
                    "id": solicitud.get("id"),
                    "numero_solicitud": numero_solicitud,
                    "Area solicitante": solicitud.get("Area solicitante"),
                    "Fecha": solicitud.get("Fecha"),
                    "Orden de trabajo": solicitud.get("Orden de trabajo"),
                    "Total": FinanciamientoApi.get_total_solicitud_fin(numero_solicitud),
                    "estado": solicitud.get("estado", "aprobado_revfin"),
                    "num_recursos": 1,
                    "recursos": [solicitud]
                }
            else:
                solicitudes_agrupadas[numero_solicitud]["num_recursos"] += 1
                solicitudes_agrupadas[numero_solicitud]["recursos"].append(solicitud)
                # Recalcular total
                solicitudes_agrupadas[numero_solicitud]["Total"] = FinanciamientoApi.get_total_solicitud_fin(numero_solicitud)
        
        self.solicitudes_fin_pendientes = list(solicitudes_agrupadas.values())
        self.loading_fin = False
    
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
    
    @rx.event
    def aprobar_solicitud(self):
        if not self.selected_solicitud:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return
        
        solicitud_id = self.selected_solicitud.get("id")
        admin_usuario = self.current_admin.get("usuario", "Maikel")
        
        result = SolicitudesRMApi.aprobar_por_admin(solicitud_id, admin_usuario)
        
        if result:
            self.close_aprobar_dialog()
            
            self.loading = True
            yield
            yield self.load_data()
            self.loading = False
            
            yield rx.toast.success("✅ Solicitud aprobada por Administración")
        else:
            yield rx.toast.error("❌ Error al aprobar la solicitud")
    
    @rx.event
    def rechazar_solicitud(self):
        if not self.selected_solicitud:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return
        
        solicitud_id = self.selected_solicitud.get("id")
        motivo = self.motivo_rechazo if self.motivo_rechazo else "Rechazado por Administración"
        
        result = SolicitudesRMApi.rechazar_solicitud_rm(solicitud_id, motivo)
        
        if result:
            self.close_rechazar_dialog()
            
            self.loading = True
            yield
            yield self.load_data()
            self.loading = False
            
            yield rx.toast.success("✅ Solicitud rechazada")
        else:
            yield rx.toast.error("❌ Error al rechazar la solicitud")
    
    @rx.event
    def sign_out(self):
        self.is_authenticated = False
        self.current_admin = {}
        
        yield rx.toast.success(
            "✅ Sesión cerrada exitosamente",
            position="top-right",
            duration=3000
        )
        
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
                continue
            
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
                # Sumar el total si es necesario
                solicitudes_agrupadas[numero_solicitud]["Total"] += solicitud.get("Importe", 0)
        
        self.solicitudes_fin_pendientes = list(solicitudes_agrupadas.values())
        self.loading_fin = False
    
    def filter_solicitudes_fin(self, search_value: str):
        """Filtra las solicitudes de financiamiento por término de búsqueda"""
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
    
    def set_motivo_rechazo_fin(self, motivo: str):
        self.motivo_rechazo_fin = motivo
    
    @rx.event
    def aprobar_solicitud_fin(self):
        """Aprueba una solicitud de financiamiento"""
        if not self.selected_solicitud_fin:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return
        
        # Obtener todos los recursos de esta solicitud
        numero_solicitud = self.selected_solicitud_fin.get("numero_solicitud")
        recursos = FinanciamientoApi.get_solicitud_fin_by_numero(numero_solicitud)
        
        if not recursos:
            yield rx.toast.error("❌ No se encontraron recursos para esta solicitud")
            return
        
        admin_usuario = self.current_admin.get("usuario", "Maikel")
        
        # Aprobar cada recurso individualmente
        for recurso in recursos:
            result = FinanciamientoApi.aprobar_por_admin(recurso["id"], admin_usuario)
            if not result:
                yield rx.toast.error(f"❌ Error al aprobar recurso {recurso['id']}")
                return
        
        self.close_aprobar_dialog_fin()
        
        self.loading_fin = True
        yield
        yield self.load_data_fin()
        self.loading_fin = False
        
        yield rx.toast.success("✅ Solicitud de financiamiento aprobada")
    
    @rx.event
    def rechazar_solicitud_fin(self):
        """Rechaza una solicitud de financiamiento"""
        if not self.selected_solicitud_fin:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return
        
        # Obtener todos los recursos de esta solicitud
        numero_solicitud = self.selected_solicitud_fin.get("numero_solicitud")
        recursos = FinanciamientoApi.get_solicitud_fin_by_numero(numero_solicitud)
        
        if not recursos:
            yield rx.toast.error("❌ No se encontraron recursos para esta solicitud")
            return
        
        motivo = self.motivo_rechazo_fin if self.motivo_rechazo_fin else "Rechazado por Administración"
        
        # Rechazar cada recurso individualmente
        for recurso in recursos:
            result = FinanciamientoApi.rechazar_solicitud_fin(recurso["id"], motivo)
            if not result:
                yield rx.toast.error(f"❌ Error al rechazar recurso {recurso['id']}")
                return
        
        self.close_rechazar_dialog_fin()
        
        self.loading_fin = True
        yield
        yield self.load_data_fin()
        self.loading_fin = False
        
        yield rx.toast.success("✅ Solicitud de financiamiento rechazada")
    
    @rx.event
    def generar_documento_fin(self):
        """Genera el documento Word para la solicitud de financiamiento"""
        if not self.selected_solicitud_fin:
            yield rx.toast.error("❌ No hay solicitud seleccionada")
            return
        
        numero_solicitud = self.selected_solicitud_fin.get("numero_solicitud")
        
        self.loading_fin = True
        yield
        
        try:
            # Obtener datos completos (recursos + solicitante)
            from TFuerte.api.financiamiento_api import FinanciamientoApi
            datos_completos = FinanciamientoApi.get_solicitud_fin_con_solicitante(numero_solicitud)
            
            if not datos_completos.get("recursos"):
                yield rx.toast.error("❌ No se encontraron recursos para esta solicitud")
                self.loading_fin = False
                return
            
            recursos = datos_completos["recursos"]
            solicitante = datos_completos["solicitante"]
            
            # Generar el documento Word
            word_content = generar_word_solicitud_fin(numero_solicitud, recursos, solicitante)
            
            if not word_content:
                yield rx.toast.error("❌ Error al generar el documento")
                self.loading_fin = False
                return
            
            # Crear nombre del archivo
            from datetime import datetime
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"Solicitud_Fin_{numero_solicitud}_{fecha_actual}.docx"
            
            self.close_generar_dialog_fin()
            
            yield rx.toast.success(f"✅ Documento generado: {nombre_archivo}")
            
            # Retornar el archivo para descarga
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
    
    # Variables computadas adicionales
    @rx.var
    def solicitudes_fin_count(self) -> int:
        return len(self.solicitudes_fin_pendientes)