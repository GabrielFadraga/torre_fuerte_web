import reflex as rx
from typing import List, Dict, Any
from TFuerte.api.solicitante_auth_api import SolicitanteAuthAPI
from TFuerte.api.solicitudes_rm_api import SolicitudesRMApi
from TFuerte.api.financiamiento_api import FinanciamientoApi
from TFuerte.routes import Route

class SolicitanteRMState(rx.State):
    """Estado para el solicitante de recursos y materiales con financiamiento"""
    
    # AUTENTICACIÓN
    current_solicitante_rm: dict = {}
    is_authenticated_rm: bool = False
    usuario_rm: str = ""
    clave_rm: str = ""
    error_message_rm: str = ""
    loading_auth_rm: bool = False
    
    # FORMULARIO RECURSOS
    centro_costo: str = ""
    fecha: str = ""
    orden_trabajo: str = ""
    loading_form_rm: bool = False
    show_success: bool = False
    
    # RECURSOS TEMPORALES
    recursos: List[dict] = []
    recurso_descripcion: str = ""
    recurso_unidad_medida: str = ""
    recurso_cantidad: str = ""
    recurso_observaciones: str = ""
    
    # HISTORIAL RECURSOS
    mis_solicitudes_rm: List[dict] = []
    loading_historial_rm: bool = False
    
    # PRECIOS DISPONIBLES
    precios_disponibles: List[dict] = []
    precios_loading: bool = False
    
    # FINANCIAMIENTO
    area_solicitante_fin: str = ""
    fecha_fin: str = ""
    numero_contrato_fin: str = ""
    orden_trabajo_fin: str = ""
    loading_fin: bool = False
    show_success_fin: bool = False
    
    # Recursos temporales para financiamiento
    recursos_fin: List[dict] = []
    recurso_fin_servicio: str = ""
    recurso_fin_descripcion: str = ""
    recurso_fin_cantidad: str = ""
    
    # Historial financiamiento
    mis_solicitudes_fin: List[dict] = []
    
    # Tipos de productos para select
    tipos_productos: List[str] = []
    
    # ==================================================
    # SETTERS
    # ==================================================
    
    def set_centro_costo(self, centro_costo: str):
        self.centro_costo = centro_costo
    
    def set_fecha(self, fecha: str):
        self.fecha = fecha
    
    def set_orden_trabajo(self, orden_trabajo: str):
        self.orden_trabajo = orden_trabajo
    
    def set_recurso_descripcion(self, descripcion: str):
        self.recurso_descripcion = descripcion
    
    def set_recurso_unidad_medida(self, unidad_medida: str):
        self.recurso_unidad_medida = unidad_medida
    
    def set_recurso_cantidad(self, cantidad: str):
        self.recurso_cantidad = cantidad
    
    def set_recurso_observaciones(self, observaciones: str):
        self.recurso_observaciones = observaciones
    
    def set_usuario_rm(self, usuario: str):
        self.usuario_rm = usuario
    
    def set_clave_rm(self, clave: str):
        self.clave_rm = clave
    
    def set_area_solicitante_fin(self, area: str):
        self.area_solicitante_fin = area
    
    def set_fecha_fin(self, fecha: str):
        self.fecha_fin = fecha
    
    def set_numero_contrato_fin(self, numero: str):
        self.numero_contrato_fin = numero
    
    def set_orden_trabajo_fin(self, orden: str):
        self.orden_trabajo_fin = orden
    
    def set_recurso_fin_servicio(self, servicio: str):
        self.recurso_fin_servicio = servicio
    
    def set_recurso_fin_descripcion(self, descripcion: str):
        self.recurso_fin_descripcion = descripcion
    
    def set_recurso_fin_cantidad(self, cantidad: str):
        self.recurso_fin_cantidad = cantidad
    
    # ==================================================
    # MÉTODOS DE AUTENTICACIÓN
    # ==================================================
    
    def sign_in_rm(self, form_data: dict = None):
        """Inicia sesión como solicitante RM"""
        self.loading_auth_rm = True
        
        username = form_data.get("username", "") if form_data else self.usuario_rm
        password = form_data.get("password", "") if form_data else self.clave_rm
        
        if not username or not password:
            self.error_message_rm = "Usuario y contraseña son requeridos"
            self.loading_auth_rm = False
            return rx.toast.error("❌ Usuario y contraseña son requeridos")
        
        response = SolicitanteAuthAPI.sign_in(username, password)
        
        if response.get("success"):
            self.is_authenticated_rm = True
            self.current_solicitante_rm = response.get("user", {})
            self.usuario_rm = ""
            self.clave_rm = ""
            self.error_message_rm = ""
            
            self.load_tipos_productos()
            self.loading_auth_rm = False
            
            return rx.redirect(Route.SOLICITANTE_RM_FORM.value)
        else:
            self.error_message_rm = response.get("error", "Error al iniciar sesión")
            self.loading_auth_rm = False
            return rx.toast.error(f"❌ {self.error_message_rm}")
    
    def sign_out_rm(self):
        """Cierra sesión del solicitante RM"""
        self.is_authenticated_rm = False
        self.current_solicitante_rm = {}
        self.mis_solicitudes_rm = []
        self.mis_solicitudes_fin = []
        self.recursos = []
        self.recursos_fin = []
        
        return rx.redirect(Route.SOLICITANTERM_LOGIN.value)
    
    # ==================================================
    # MÉTODOS PARA RECURSOS RM
    # ==================================================
    
    def agregar_recurso(self):
        """Agrega un recurso a la lista temporal"""
        if not self.recurso_descripcion or not self.recurso_cantidad:
            return rx.toast.error("❌ Descripción y cantidad son requeridos")
        
        try:
            cantidad = float(self.recurso_cantidad)
        except:
            return rx.toast.error("❌ Cantidad debe ser un número válido")
        
        nuevo_recurso = {
            "descripcion": self.recurso_descripcion,
            "unidad_medida": self.recurso_unidad_medida,
            "cantidad": cantidad,
            "observaciones": self.recurso_observaciones
        }
        
        self.recursos = self.recursos + [nuevo_recurso]
        
        self.recurso_descripcion = ""
        self.recurso_unidad_medida = ""
        self.recurso_cantidad = ""
        self.recurso_observaciones = ""
        
        return rx.toast.success(f"✅ Recurso agregado ({len(self.recursos)} total)")
    
    def eliminar_recurso(self, idx: int):
        """Elimina un recurso de la lista temporal"""
        if isinstance(idx, dict):
            idx = idx.get("idx", 0)
        
        idx_int = int(idx)
        
        if idx_int >= 0 and idx_int < len(self.recursos):
            nueva_lista = []
            for i, recurso in enumerate(self.recursos):
                if i != idx_int:
                    nueva_lista.append(recurso)
            self.recursos = nueva_lista
            return rx.toast.success("🗑️ Recurso eliminado")
        return rx.toast.error("❌ Índice inválido")
    
    # ==================================================
    # MÉTODOS PARA FINANCIAMIENTO
    # ==================================================
    
    def load_tipos_productos(self):
        """Carga los tipos de productos disponibles"""
        try:
            tipos = FinanciamientoApi.get_tipos_productos()
            if tipos:
                self.tipos_productos = tipos
        except Exception as e:
            print(f"❌ Error cargando tipos de productos: {e}")
            self.tipos_productos = [
                "Electricidad", "Plomeria", "Corte y desbaste", "Tornillos y expansiones",
                "Herramientas", "Laminado y soldadura", "Rodamiento y sellos",
                "Pintura", "Silicona y juntas", "Climatizacion", "Medios de proteccion",
                "Lubricantes", "Baterias", "Señaleticas", "Material construccion"
            ]
    
    def agregar_recurso_fin(self):
        """Agrega un recurso a la lista temporal de financiamiento"""
        if not self.recurso_fin_descripcion or not self.recurso_fin_cantidad:
            return rx.toast.error("❌ Descripción y cantidad son requeridos")
        
        if not self.recurso_fin_servicio:
            return rx.toast.error("❌ Debes seleccionar un tipo de servicio")
        
        try:
            cantidad = int(self.recurso_fin_cantidad)
            if cantidad <= 0:
                raise ValueError
        except:
            return rx.toast.error("❌ La cantidad debe ser un número entero mayor a 0")
        
        nuevo_recurso = {
            "servicio": self.recurso_fin_servicio,
            "descripcion": self.recurso_fin_descripcion,
            "cantidad": cantidad
        }
        
        self.recursos_fin = self.recursos_fin + [nuevo_recurso]
        
        self.recurso_fin_servicio = ""
        self.recurso_fin_descripcion = ""
        self.recurso_fin_cantidad = ""
        
        return rx.toast.success(f"✅ Producto agregado ({len(self.recursos_fin)} total)")
    
    def eliminar_recurso_fin(self, idx: int):
        """Elimina un recurso de la lista temporal de financiamiento"""
        if isinstance(idx, dict):
            idx = idx.get("idx", 0)
        
        idx_int = int(idx)
        
        if idx_int >= 0 and idx_int < len(self.recursos_fin):
            nueva_lista = []
            for i, recurso in enumerate(self.recursos_fin):
                if i != idx_int:
                    nueva_lista.append(recurso)
            self.recursos_fin = nueva_lista
            return rx.toast.success("🗑️ Producto eliminado")
        return rx.toast.error("❌ Índice inválido")
    
    # ==================================================
    # CREAR SOLICITUDES
    # ==================================================
    
    def crear_solicitud_rm(self, form_data: dict):
        """Crea una solicitud con múltiples recursos"""
        if not self.is_authenticated_rm:
            return rx.toast.error("❌ No estás autenticado")
        
        if not self.recursos:
            return rx.toast.error("❌ Debes agregar al menos un recurso")
        
        self.loading_form_rm = True
        yield
        
        solicitud_data = {
            "Centro costo": form_data.get("centro_costo", ""),
            "Fecha": form_data.get("fecha", ""),
            "Orden trabajo": form_data.get("orden_trabajo", ""),
            "solicitante_id": self.current_solicitante_rm.get("id")
        }
        
        recursos_api = []
        for recurso in self.recursos:
            recursos_api.append({
                "descripcion": recurso["descripcion"],
                "unidad_medida": recurso.get("unidad_medida", ""),
                "cantidad": recurso["cantidad"],
                "observaciones": recurso.get("observaciones", "")
            })
        
        response = SolicitudesRMApi.create_solicitud_rm(solicitud_data, recursos_api)
        
        if response:
            self.recursos = []
            self.centro_costo = ""
            self.fecha = ""
            self.orden_trabajo = ""
            self.show_success = True
            
            yield self.load_mis_solicitudes_rm()
            yield rx.toast.success(f"✅ Solicitud creada con {len(response.get('recursos', []))} recursos")
        else:
            yield rx.toast.error("❌ Error al crear la solicitud")
        
        self.loading_form_rm = False
    
    def crear_solicitud_fin(self, form_data: dict):
        """Crea una solicitud de financiamiento con múltiples productos"""
        if not self.is_authenticated_rm:
            yield rx.toast.error("❌ No estás autenticado")
            return
        
        if not self.recursos_fin:
            yield rx.toast.error("❌ Debes agregar al menos un producto")
            return
        
        if not all([self.area_solicitante_fin, self.fecha_fin, self.orden_trabajo_fin]):
            yield rx.toast.error("❌ Área solicitante, fecha y orden de trabajo son requeridos")
            return
        
        self.loading_fin = True
        yield
        
        recursos_api = []
        for recurso in self.recursos_fin:
            recurso_data = {
                "Area solicitante": self.area_solicitante_fin,
                "Fecha": self.fecha_fin,
                "Servicio": recurso["servicio"],
                "Numero de contrato/suplemento": self.numero_contrato_fin,
                "Orden de trabajo": self.orden_trabajo_fin,
                "Descripcion": recurso["descripcion"],
                "Cantidad": recurso["cantidad"],
                "solicitante_id": self.current_solicitante_rm.get("id")
            }
            recursos_api.append(recurso_data)
        
        response = FinanciamientoApi.create_solicitud_fin_multi(recursos_api)
        
        if response:
            self.recursos_fin = []
            self.area_solicitante_fin = ""
            self.fecha_fin = ""
            self.numero_contrato_fin = ""
            self.orden_trabajo_fin = ""
            self.recurso_fin_servicio = ""
            self.recurso_fin_descripcion = ""
            self.recurso_fin_cantidad = ""
            self.show_success_fin = True
            
            yield self.load_mis_solicitudes_fin()
            yield rx.toast.success(f"✅ Solicitud de financiamiento creada con {len(response)} productos")
        else:
            yield rx.toast.error("❌ Error al crear la solicitud de financiamiento")
        
        self.loading_fin = False
    
    # ==================================================
    # CARGAR HISTORIALES
    # ==================================================
    
    def load_mis_solicitudes_rm(self):
        """Carga las solicitudes del solicitante actual"""
        if not self.is_authenticated_rm:
            return
        
        self.loading_historial_rm = True
        yield
        
        solicitante_id = self.current_solicitante_rm.get("id")
        if solicitante_id:
            solicitudes_data = SolicitudesRMApi.get_solicitudes_rm_by_solicitante(solicitante_id)
            
            solicitudes = []
            for s in solicitudes_data:
                fecha_creacion = s.get("fecha_creacion", "")
                fecha_display = fecha_creacion[:10] if fecha_creacion and len(fecha_creacion) >= 10 else fecha_creacion
                
                solicitud = {
                    "id": str(s.get("id", "")),
                    "centro_costo": s.get("Centro costo", ""),
                    "fecha": s.get("Fecha", ""),
                    "orden_trabajo": s.get("Orden trabajo", ""),
                    "estado": s.get("estado", "pendiente"),
                    "fecha_creacion_display": fecha_display or "",
                    "num_recursos": len(s.get("recursos", [])),
                    "observaciones": s.get("Observaciones", "")
                }
                solicitudes.append(solicitud)
            
            self.mis_solicitudes_rm = solicitudes
        
        self.loading_historial_rm = False
    
    def load_mis_solicitudes_fin(self):
        """Carga las solicitudes de financiamiento del solicitante actual"""
        if not self.is_authenticated_rm:
            return
        
        self.loading_fin = True
        yield
        
        solicitante_id = self.current_solicitante_rm.get("id")
        if solicitante_id:
            solicitudes_data = FinanciamientoApi.get_solicitudes_fin_by_solicitante(solicitante_id)
            
            solicitudes_agrupadas = {}
            for solicitud in solicitudes_data:
                numero_solicitud = solicitud.get("numero_solicitud")
                if not numero_solicitud:
                    continue
                
                if numero_solicitud not in solicitudes_agrupadas:
                    solicitudes_agrupadas[numero_solicitud] = {
                        "numero_solicitud": numero_solicitud,
                        "Area solicitante": solicitud.get("Area solicitante", ""),
                        "Fecha": solicitud.get("Fecha", ""),
                        "Orden de trabajo": solicitud.get("Orden de trabajo", ""),
                        "Total": FinanciamientoApi.get_total_solicitud_fin(numero_solicitud),
                        "estado": solicitud.get("estado", "pendiente_revfin"),
                        "num_recursos": 1,
                        "recursos": [solicitud]
                    }
                else:
                    solicitudes_agrupadas[numero_solicitud]["num_recursos"] += 1
                    solicitudes_agrupadas[numero_solicitud]["recursos"].append(solicitud)
                    solicitudes_agrupadas[numero_solicitud]["Total"] = FinanciamientoApi.get_total_solicitud_fin(numero_solicitud)
            
            self.mis_solicitudes_fin = list(solicitudes_agrupadas.values())
        
        self.loading_fin = False
    
    # ==================================================
    # DIÁLOGOS
    # ==================================================
    
    def close_success_dialog(self):
        """Cierra el diálogo de éxito de recursos"""
        self.show_success = False
    
    def close_success_dialog_fin(self):
        """Cierra el diálogo de éxito de financiamiento"""
        self.show_success_fin = False
    
    # ==================================================
    # PRECIOS DISPONIBLES
    # ==================================================
    
    def load_precios_disponibles(self):
        """Carga los precios disponibles"""
        self.precios_loading = True
        yield
        
        try:
            precios = FinanciamientoApi.get_all_precios()
            
            precios_con_final = []
            for precio in precios:
                precio_base = float(precio.get('Precio', 0))
                precio_final = precio_base * 1.25
                
                precio_modificado = precio.copy()
                precio_modificado['Precio_str'] = f"{precio_base:.2f}"
                precio_modificado['Precio_final_str'] = f"{precio_final:.2f}"
                precios_con_final.append(precio_modificado)
            
            self.precios_disponibles = precios_con_final
        except Exception as e:
            print(f"Error cargando precios: {e}")
            self.precios_disponibles = []
        
        self.precios_loading = False
    
    # ==================================================
    # VARIABLES COMPUTADAS
    # ==================================================
    
    @rx.var
    def total_recursos(self) -> int:
        """Total de recursos en la lista temporal"""
        return len(self.recursos)
    
    @rx.var
    def total_recursos_fin(self) -> int:
        """Total de productos en la lista temporal de financiamiento"""
        return len(self.recursos_fin)
    
    @rx.var
    def total_solicitudes(self) -> int:
        """Total de solicitudes en el historial de recursos"""
        return len(self.mis_solicitudes_rm)
    
    @rx.var
    def total_solicitudes_fin(self) -> int:
        """Total de solicitudes en el historial de financiamiento"""
        return len(self.mis_solicitudes_fin)
    
    @rx.var
    def usuario_actual(self) -> str:
        """Nombre del usuario actual"""
        return self.current_solicitante_rm.get("usuario", "Usuario")