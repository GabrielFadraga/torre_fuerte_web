import reflex as rx
from typing import List
from datetime import datetime
from TFuerte.api.solicitudes_rm_api import SolicitudesRMApi
from TFuerte.api.admin_rm_api import AdminRMApi
from TFuerte.api.solicitante_auth_api import SolicitanteAuthAPI
from TFuerte.api.financiamiento_api import FinanciamientoApi
from TFuerte.utilss.word_generator import generar_word_solicitud_rm
from TFuerte.routes import Route

class LogisticaState(rx.State):
    """Estado para el dashboard de Jefe de Logística (Miguel)"""
    
    # Datos
    solicitudes_pendientes: List[dict] = []
    solicitudes_completadas: List[dict] = []
    
    # Estados de UI
    loading: bool = False
    loading_completadas: bool = False
    show_aprobar_dialog: bool = False
    show_rechazar_dialog: bool = False
    show_generar_dialog: bool = False
    selected_solicitud: dict = {}
    search_value: str = ""
    
    # ==================================================
    # NUEVO: Diálogo de detalles de recursos
    # ==================================================
    show_detalle_dialog: bool = False
    solicitud_detalle: dict = {}
    recursos_detalle: List[dict] = []
    
    # Variable para el motivo del rechazo
    motivo_rechazo: str = ""
    
    # Usuario actual
    current_admin: dict = {}
    is_authenticated: bool = False
    
    # Credenciales para login
    username: str = ""
    password: str = ""
    error_message: str = ""
    
    # Variables para gestión de precios
    precios: List[dict] = []
    loading_precios: bool = False
    nuevo_tipo: str = ""
    nueva_descripcion: str = ""
    nuevo_precio: str = ""
    tipos_disponibles: List[str] = []
    
    # Variables para diálogos de precios
    show_editar_precio_dialog: bool = False
    show_eliminar_precio_dialog: bool = False
    selected_precio: dict = {}
    precio_editado_tipo: str = ""
    precio_editado_descripcion: str = ""
    precio_editado_precio: str = ""
    
    # ==================================================
    # PAGINACIÓN PARA PRECIOS
    # ==================================================
    precios_paginated: List[dict] = []
    current_page_precios: int = 1
    items_per_page_precios: int = 10
    total_pages_precios: int = 1
    page_numbers_precios: List[int] = []

    # ==================================================
    # PAGINACIÓN PARA PENDIENTES
    # ==================================================
    pendientes_paginated: List[dict] = []
    pendientes_current_page: int = 1
    pendientes_items_per_page: int = 10
    pendientes_total_pages: int = 1
    pendientes_page_numbers: List[int] = []

    # ==================================================
    # SETTERS BÁSICOS
    # ==================================================
    
    def set_username(self, username: str):
        """Setter para el nombre de usuario"""
        self.username = username
    
    def set_password(self, password: str):
        """Setter para la contraseña"""
        self.password = password
    
    def set_motivo_rechazo(self, motivo: str):
        """Setter para el motivo del rechazo"""
        self.motivo_rechazo = motivo
    
    # Setters para formulario de precios
    def set_nuevo_tipo(self, tipo: str):
        self.nuevo_tipo = tipo
    
    def set_nueva_descripcion(self, descripcion: str):
        self.nueva_descripcion = descripcion
    
    def set_nuevo_precio(self, precio: str):
        self.nuevo_precio = precio
    
    def set_precio_editado_tipo(self, tipo: str):
        self.precio_editado_tipo = tipo
    
    def set_precio_editado_descripcion(self, descripcion: str):
        self.precio_editado_descripcion = descripcion
    
    def set_precio_editado_precio(self, precio: str):
        self.precio_editado_precio = precio
    
    # ==================================================
    # AUTENTICACIÓN
    # ==================================================
    
    @rx.event
    def sign_in(self):
        """Inicia sesión como Jefe de Logística"""
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
            # Verificar que sea el rol correcto
            if user.get("rol") == "logistica":
                self.is_authenticated = True
                self.current_admin = user
                
                self.username = ""
                self.password = ""
                
                yield rx.toast.success(
                    "✅ Inicio de sesión exitoso",
                    position="top-right",
                    duration=3000
                )
                
                # Redirigir al dashboard
                yield rx.redirect(Route.LOGISTICA_DASHBOARD.value)
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
    
    # ==================================================
    # CARGAR DATOS
    # ==================================================
    
    @rx.event
    def load_data(self):
        """Carga las solicitudes pendientes para logística"""
        self.loading = True
        yield
        
        # Cargar solicitudes pendientes de aprobación logística
        solicitudes_pendientes = SolicitudesRMApi.get_solicitudes_rm_pendientes_logistica()
        
        # Formatear fechas y extraer primer recurso
        solicitudes_procesadas = []
        for solicitud in solicitudes_pendientes:
            # Crear copia para no modificar el original
            solicitud_procesada = solicitud.copy()
            
            # Formatear fechas
            solicitud_procesada = self._formatear_fechas_solicitud(solicitud_procesada)
            
            # Extraer datos del primer recurso para facilitar el acceso (opcional)
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
        self.reset_pendientes_pagination()
        self.loading = False
    
    @rx.event
    def load_completadas(self):
        """Carga las solicitudes completadas (aprobadas por logística)"""
        self.loading_completadas = True
        yield
        
        try:
            solicitudes = SolicitudesRMApi.get_solicitudes_rm_completadas()
            
            # Formatear fechas y extraer primer recurso
            solicitudes_procesadas = []
            for solicitud in solicitudes:
                # Crear copia para no modificar el original
                solicitud_procesada = solicitud.copy()
                
                # Formatear fechas
                solicitud_procesada = self._formatear_fechas_solicitud(solicitud_procesada)
                
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
                
                # AÑADIR: número de recursos (opcional para completadas)
                solicitud_procesada["num_recursos"] = len(recursos)
                
                solicitudes_procesadas.append(solicitud_procesada)
            
            self.solicitudes_completadas = solicitudes_procesadas
            print(f"✅ {len(solicitudes)} solicitudes completadas cargadas")
        except Exception as e:
            print(f"❌ Error cargando solicitudes completadas: {e}")
            import traceback
            traceback.print_exc()
            self.solicitudes_completadas = []
        
        self.loading_completadas = False
    
    @rx.event
    def load_precios(self):
        """Carga todos los precios de productos"""
        self.loading_precios = True
        yield

        try:
            precios_data = FinanciamientoApi.get_all_precios()
            self.precios = precios_data

            # Extraer tipos únicos
            tipos = set()
            for precio in precios_data:
                if precio.get("Tipo"):
                    tipos.add(precio["Tipo"])

            self.tipos_disponibles = sorted(list(tipos))
            print(f"✅ {len(self.precios)} precios cargados, {len(self.tipos_disponibles)} tipos disponibles")
            
            # Calcular paginación
            self.calculate_precios_pagination()
            
        except Exception as e:
            print(f"❌ Error cargando precios: {e}")
            self.precios = []
            self.tipos_disponibles = []
            self.precios_paginated = []
            self.total_pages_precios = 1
            self.current_page_precios = 1

        self.loading_precios = False
    
    def _formatear_fechas_solicitud(self, solicitud: dict) -> dict:
        """Formatea las fechas de una solicitud en el backend"""
        if not solicitud:
            return solicitud
        
        # Crear copia para no modificar el original
        solicitud_formateada = solicitud.copy()
        
        # Función auxiliar para formatear fecha
        def formatear_fecha(fecha):
            if not fecha:
                return ""
            if isinstance(fecha, str):
                # Intentar obtener solo la parte de la fecha (YYYY-MM-DD)
                if len(fecha) >= 10:
                    return fecha[:10]
                return fecha
            elif isinstance(fecha, datetime):
                return fecha.strftime("%Y-%m-%d")
            return str(fecha)
        
        # Campos de fecha a formatear
        campos_fecha = [
            "fecha_creacion",
            "fecha_aprobacion_tecnica", 
            "fecha_aprobacion_admin",
            "fecha_aprobacion_logistica",
            "Fecha"
        ]
        
        for campo in campos_fecha:
            if campo in solicitud_formateada:
                solicitud_formateada[campo] = formatear_fecha(solicitud_formateada[campo])
        
        return solicitud_formateada
    
    # ==================================================
    # FILTRADO
    # ==================================================
    
    def filter_solicitudes(self, search_value: str):
        """Filtra las solicitudes por término de búsqueda"""
        self.search_value = search_value
        
        if not search_value:
            # Recargar todas
            return self.load_data()
        
        # Filtrar localmente
        search_term = search_value.lower()
        filtered = []
        for s in self.solicitudes_pendientes:
            if (search_term in s.get("Descripcion", "").lower() or
                search_term in s.get("Centro costo", "").lower() or
                search_term in s.get("Orden trabajo", "").lower() or
                search_term in s.get("Observaciones", "").lower()):
                filtered.append(s)
        
        self.solicitudes_pendientes = filtered
        self.reset_pendientes_pagination()
    
    # ==================================================
    # DIÁLOGOS PARA SOLICITUDES
    # ==================================================
    
    def open_aprobar_dialog(self, solicitud: dict):
        """Abre el diálogo para aprobar solicitud"""
        self.selected_solicitud = solicitud
        self.show_aprobar_dialog = True
    
    def close_aprobar_dialog(self):
        """Cierra el diálogo de aprobación"""
        self.show_aprobar_dialog = False
        self.selected_solicitud = {}
    
    def open_rechazar_dialog(self, solicitud: dict):
        """Abre el diálogo para rechazar solicitud"""
        self.selected_solicitud = solicitud
        self.show_rechazar_dialog = True
        # Limpiar el motivo anterior
        self.motivo_rechazo = ""
    
    def close_rechazar_dialog(self):
        """Cierra el diálogo de rechazo"""
        self.show_rechazar_dialog = False
        self.selected_solicitud = {}
        # Limpiar el motivo
        self.motivo_rechazo = ""
    
    def open_generar_dialog(self, solicitud: dict):
        """Abre el diálogo para generar documento"""
        self.selected_solicitud = solicitud
        self.show_generar_dialog = True
    
    def close_generar_dialog(self):
        """Cierra el diálogo de generación"""
        self.show_generar_dialog = False
        self.selected_solicitud = {}
    
    def set_show_aprobar_dialog(self, show: bool):
        """Setter para show_aprobar_dialog"""
        self.show_aprobar_dialog = show
        if not show:
            self.selected_solicitud = {}
    
    def set_show_rechazar_dialog(self, show: bool):
        """Setter para show_rechazar_dialog"""
        self.show_rechazar_dialog = show
        if not show:
            self.selected_solicitud = {}
            self.motivo_rechazo = ""
    
    def set_show_generar_dialog(self, show: bool):
        """Setter para show_generar_dialog"""
        self.show_generar_dialog = show
        if not show:
            self.selected_solicitud = {}
    
    # ==================================================
    # NUEVO: Diálogo de detalles
    # ==================================================
    def open_detalle_dialog(self, solicitud: dict):
        self.solicitud_detalle = solicitud
        self.recursos_detalle = solicitud.get("recursos", [])
        self.show_detalle_dialog = True
    
    def close_detalle_dialog(self):
        self.show_detalle_dialog = False
        self.solicitud_detalle = {}
        self.recursos_detalle = []
    
    def set_show_detalle_dialog(self, show: bool):
        self.show_detalle_dialog = show
        if not show:
            self.solicitud_detalle = {}
            self.recursos_detalle = []
    
    # ==================================================
    # DIÁLOGOS PARA PRECIOS
    # ==================================================
    
    def open_editar_precio_dialog(self, precio: dict):
        """Abre el diálogo para editar precio"""
        self.selected_precio = precio
        self.precio_editado_tipo = precio.get("Tipo", "")
        self.precio_editado_descripcion = precio.get("Descripcion", "")
        self.precio_editado_precio = str(precio.get("Precio", 0))
        self.show_editar_precio_dialog = True
    
    def close_editar_precio_dialog(self):
        """Cierra el diálogo de edición de precio"""
        self.show_editar_precio_dialog = False
        self.selected_precio = {}
        self.precio_editado_tipo = ""
        self.precio_editado_descripcion = ""
        self.precio_editado_precio = ""
    
    def open_eliminar_precio_dialog(self, precio: dict):
        """Abre el diálogo para eliminar precio"""
        self.selected_precio = precio
        self.show_eliminar_precio_dialog = True
    
    def close_eliminar_precio_dialog(self):
        """Cierra el diálogo de eliminación de precio"""
        self.show_eliminar_precio_dialog = False
        self.selected_precio = {}
    
    def set_show_editar_precio_dialog(self, show: bool):
        """Setter para show_editar_precio_dialog"""
        self.show_editar_precio_dialog = show
        if not show:
            self.selected_precio = {}
            self.precio_editado_tipo = ""
            self.precio_editado_descripcion = ""
            self.precio_editado_precio = ""
    
    def set_show_eliminar_precio_dialog(self, show: bool):
        """Setter para show_eliminar_precio_dialog"""
        self.show_eliminar_precio_dialog = show
        if not show:
            self.selected_precio = {}
    
    # ==================================================
    # APROBACIÓN/RECHAZO DE SOLICITUDES
    # ==================================================
    
    @rx.event
    def aprobar_solicitud(self):
        """Aprueba la solicitud seleccionada (nivel logística)"""
        if not self.selected_solicitud:
            yield rx.toast.error(
                "❌ No hay solicitud seleccionada",
                position="top-right",
                duration=4000
            )
            return

        solicitud_id = self.selected_solicitud.get("id")
        admin_usuario = self.current_admin.get("usuario", "Miguel")

        try:
            result = SolicitudesRMApi.aprobar_por_logistica(solicitud_id, admin_usuario)

            if result:
                self.close_aprobar_dialog()
                # ✅ CORREGIDO: usar yield from para ejecutar el generador
                yield from self.load_data()
                yield rx.toast.success(
                    "✅ Solicitud aprobada por Logística",
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
            import traceback
            traceback.print_exc()
            yield rx.toast.error(
                f"❌ Error interno: {str(e)}",
                position="top-right",
                duration=4000
            )
    
    @rx.event
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
        motivo = self.motivo_rechazo if self.motivo_rechazo else "Rechazado por Logística"

        try:
            result = SolicitudesRMApi.rechazar_solicitud_rm(solicitud_id, motivo)

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
            import traceback
            traceback.print_exc()
            yield rx.toast.error(
                f"❌ Error interno: {str(e)}",
                position="top-right",
                duration=4000
            )
    
    # ==================================================
    # GESTIÓN DE PRECIOS
    # ==================================================
    
    @rx.event
    def agregar_precio(self):
        """Agrega un nuevo precio"""
        if not self.nuevo_tipo or not self.nueva_descripcion or not self.nuevo_precio:
            yield rx.toast.error("❌ Todos los campos son requeridos")
            return

        try:
            precio_float = float(self.nuevo_precio)
            if precio_float <= 0:
                raise ValueError
        except:
            yield rx.toast.error("❌ El precio debe ser un número válido mayor a 0")
            return

        precio_data = {
            "Tipo": self.nuevo_tipo,
            "Descripcion": self.nueva_descripcion,
            "Precio": precio_float
        }

        result = FinanciamientoApi.create_precio(precio_data)

        if result:
            # Limpiar formulario
            self.nuevo_tipo = ""
            self.nueva_descripcion = ""
            self.nuevo_precio = ""

            # ✅ CORREGIDO: usar yield from para ejecutar el generador
            yield from self.load_precios()

            yield rx.toast.success("✅ Producto agregado correctamente")
        else:
            yield rx.toast.error("❌ Error al agregar el producto")
    
    @rx.event
    def actualizar_precio(self):
        """Actualiza un precio existente"""
        if not self.selected_precio:
            yield rx.toast.error("❌ No hay producto seleccionado")
            return

        precio_id = self.selected_precio.get("id")

        # Validar campos
        if not all([self.precio_editado_tipo, self.precio_editado_descripcion, self.precio_editado_precio]):
            yield rx.toast.error("❌ Todos los campos son requeridos")
            return

        try:
            precio_float = float(self.precio_editado_precio)
            if precio_float <= 0:
                raise ValueError
        except:
            yield rx.toast.error("❌ El precio debe ser un número válido mayor a 0")
            return

        precio_data = {
            "Tipo": self.precio_editado_tipo,
            "Descripcion": self.precio_editado_descripcion,
            "Precio": precio_float
        }

        result = FinanciamientoApi.update_precio(precio_id, precio_data)

        if result:
            # Limpiar campos editados
            self.precio_editado_tipo = ""
            self.precio_editado_descripcion = ""
            self.precio_editado_precio = ""

            # Cerrar diálogo
            self.show_editar_precio_dialog = False
            self.selected_precio = {}

            # ✅ CORREGIDO
            yield from self.load_precios()

            yield rx.toast.success("✅ Producto actualizado correctamente")
        else:
            yield rx.toast.error("❌ Error al actualizar el producto")
    
    @rx.event
    def eliminar_precio(self):
        """Elimina un precio"""
        if not self.selected_precio:
            yield rx.toast.error("❌ No hay producto seleccionado")
            return

        precio_id = self.selected_precio.get("id")

        result = FinanciamientoApi.delete_precio(precio_id)

        if result:
            # Cerrar diálogo
            self.show_eliminar_precio_dialog = False
            self.selected_precio = {}

            # ✅ CORREGIDO
            yield from self.load_precios()

            yield rx.toast.success("✅ Producto eliminado correctamente")
        else:
            yield rx.toast.error("❌ Error al eliminar el producto")
    
    # ==================================================
    # GENERACIÓN DE DOCUMENTOS
    # ==================================================
    
    @rx.event
    def generar_documento(self):
        """Genera el documento Word para la solicitud seleccionada"""
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
            # Obtener datos COMPLETOS de la solicitud (con recursos)
            solicitud_completa = SolicitudesRMApi.get_solicitud_rm_by_id(solicitud_id)
            
            if not solicitud_completa or "recursos" not in solicitud_completa:
                yield rx.toast.error(
                    "❌ No se pudo obtener información completa de la solicitud",
                    position="top-right",
                    duration=4000
                )
                self.loading = False
                return
            
            # Obtener datos del solicitante
            solicitante_id = solicitud_completa.get("solicitante_id")
            solicitantes = SolicitanteAuthAPI.get_all_solicitantes()
            solicitante = None
            
            for s in solicitantes:
                if s.get("id") == solicitante_id:
                    solicitante = s
                    break
            
            if not solicitante:
                yield rx.toast.error(
                    "❌ No se encontró información del solicitante",
                    position="top-right",
                    duration=4000
                )
                self.loading = False
                return
            
            # Verificar que la solicitud esté completamente aprobada
            if not (solicitud_completa.get("aprobado_tecnica") and 
                    solicitud_completa.get("aprobado_admin") and 
                    solicitud_completa.get("aprobado_logistica")):
                yield rx.toast.error(
                    "❌ La solicitud debe estar completamente aprobada para generar el documento",
                    position="top-right",
                    duration=4000
                )
                self.loading = False
                return
            
            # Generar el documento Word (ahora con múltiples recursos)
            word_content = generar_word_solicitud_rm(solicitud_completa, solicitante)
            
            # Crear nombre del archivo
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"Solicitud_RM_{solicitud_id}_{fecha_actual}.docx"
            
            self.close_generar_dialog()
            
            yield rx.toast.success(
                f"✅ Documento generado: {nombre_archivo}",
                position="top-right",
                duration=3000
            )
            
            # Retornar el archivo para descarga
            return rx.download(
                data=word_content,
                filename=nombre_archivo
            )
            
        except Exception as e:
            print(f"❌ Error generando documento: {e}")
            import traceback
            traceback.print_exc()
            yield rx.toast.error(
                "❌ Error al generar el documento",
                position="top-right",
                duration=4000
            )
        finally:
            self.loading = False
    
    # ==================================================
    # CERRAR SESIÓN
    # ==================================================
    
    @rx.event
    def sign_out(self):
        """Cierra sesión del jefe de logística"""
        self.is_authenticated = False
        self.current_admin = {}
        
        yield rx.toast.success(
            "✅ Sesión cerrada exitosamente",
            position="top-right",
            duration=3000
        )
        
        yield rx.redirect(Route.LOGISTICA_LOGIN.value)
    
    # ==================================================
    # VARIABLES COMPUTADAS
    # ==================================================
    
    @rx.var
    def solicitudes_pendientes_count(self) -> int:
        """Retorna el número de solicitudes pendientes"""
        return len(self.solicitudes_pendientes)
    
    @rx.var
    def solicitudes_completadas_count(self) -> int:
        """Retorna el número de solicitudes completadas"""
        return len(self.solicitudes_completadas)
    
    @rx.var
    def precios_count(self) -> int:
        """Retorna el número de precios registrados"""
        return len(self.precios)
    
    @rx.var
    def admin_name(self) -> str:
        """Retorna el nombre del administrador"""
        return self.current_admin.get("usuario", "Jefe de Logística")
    
    @rx.var
    def admin_cargo(self) -> str:
        """Retorna el cargo del administrador"""
        return self.current_admin.get("cargo", "Jefe Área Logística")
    
    def reset_loading_states(self):
        """Resetea todos los estados de carga al cargar la página"""
        self.loading = False
        self.loading_completadas = False
        self.loading_precios = False

    # ==================================================
    # MÉTODOS DE PAGINACIÓN PARA PRECIOS
    # ==================================================

    def calculate_precios_pagination(self):
        """Calcula la paginación para la tabla de precios"""
        total_items = len(self.precios)

        if total_items == 0:
            self.total_pages_precios = 1
            self.precios_paginated = []
        else:
            self.total_pages_precios = max(1, (total_items + self.items_per_page_precios - 1) // self.items_per_page_precios)

        # Asegurar que la página actual esté dentro de los límites
        if self.current_page_precios > self.total_pages_precios:
            self.current_page_precios = max(1, self.total_pages_precios)

        start_idx = (self.current_page_precios - 1) * self.items_per_page_precios
        end_idx = min(start_idx + self.items_per_page_precios, total_items)

        if total_items > 0:
            self.precios_paginated = self.precios[start_idx:end_idx]
        else:
            self.precios_paginated = []

        self.calculate_precios_page_numbers()

    def calculate_precios_page_numbers(self):
        """Calcula los números de página a mostrar en los botones"""
        max_pages_to_show = 4
        current = self.current_page_precios
        total = self.total_pages_precios

        if total <= max_pages_to_show:
            self.page_numbers_precios = list(range(1, total + 1))
            return

        start = max(1, current - 1)
        end = min(total, start + max_pages_to_show - 1)

        if end - start + 1 < max_pages_to_show:
            start = max(1, end - max_pages_to_show + 1)

        self.page_numbers_precios = list(range(start, end + 1))

    def go_to_page_precios(self, page_number: int):
        """Navega a una página específica de precios"""
        if 1 <= page_number <= self.total_pages_precios:
            self.current_page_precios = page_number
            self.calculate_precios_pagination()

    def next_page_precios(self):
        """Página siguiente de precios"""
        if self.current_page_precios < self.total_pages_precios:
            self.current_page_precios += 1
            self.calculate_precios_pagination()

    def previous_page_precios(self):
        """Página anterior de precios"""
        if self.current_page_precios > 1:
            self.current_page_precios -= 1
            self.calculate_precios_pagination()

    def reset_precios_pagination(self):
        """Resetea la paginación de precios a la primera página"""
        self.current_page_precios = 1
        if hasattr(self, 'precios') and self.precios:
            self.calculate_precios_pagination()

    # ==================================================
    # MÉTODOS DE PAGINACIÓN PARA PENDIENTES
    # ==================================================

    def calculate_pendientes_pagination(self):
        """Calcula la paginación para la tabla de solicitudes pendientes"""
        total_items = len(self.solicitudes_pendientes)

        if total_items == 0:
            self.pendientes_total_pages = 1
            self.pendientes_paginated = []
        else:
            self.pendientes_total_pages = max(1, (total_items + self.pendientes_items_per_page - 1) // self.pendientes_items_per_page)

        # Asegurar que la página actual esté dentro de los límites
        if self.pendientes_current_page > self.pendientes_total_pages:
            self.pendientes_current_page = max(1, self.pendientes_total_pages)

        start_idx = (self.pendientes_current_page - 1) * self.pendientes_items_per_page
        end_idx = min(start_idx + self.pendientes_items_per_page, total_items)

        if total_items > 0:
            self.pendientes_paginated = self.solicitudes_pendientes[start_idx:end_idx]
        else:
            self.pendientes_paginated = []

        self.calculate_pendientes_page_numbers()

    def calculate_pendientes_page_numbers(self):
        """Calcula los números de página a mostrar en los botones"""
        max_pages_to_show = 4
        current = self.pendientes_current_page
        total = self.pendientes_total_pages

        if total <= max_pages_to_show:
            self.pendientes_page_numbers = list(range(1, total + 1))
            return

        start = max(1, current - 1)
        end = min(total, start + max_pages_to_show - 1)

        if end - start + 1 < max_pages_to_show:
            start = max(1, end - max_pages_to_show + 1)

        self.pendientes_page_numbers = list(range(start, end + 1))

    def go_to_page_pendientes(self, page_number: int):
        """Navega a una página específica de solicitudes pendientes"""
        if 1 <= page_number <= self.pendientes_total_pages:
            self.pendientes_current_page = page_number
            self.calculate_pendientes_pagination()

    def next_page_pendientes(self):
        """Página siguiente de solicitudes pendientes"""
        if self.pendientes_current_page < self.pendientes_total_pages:
            self.pendientes_current_page += 1
            self.calculate_pendientes_pagination()

    def previous_page_pendientes(self):
        """Página anterior de solicitudes pendientes"""
        if self.pendientes_current_page > 1:
            self.pendientes_current_page -= 1
            self.calculate_pendientes_pagination()

    def reset_pendientes_pagination(self):
        """Resetea la paginación de solicitudes pendientes a la primera página"""
        self.pendientes_current_page = 1
        self.calculate_pendientes_pagination()