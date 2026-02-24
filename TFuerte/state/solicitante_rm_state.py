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
    # NUEVO: filtro y lista filtrada
    precios_search_value: str = ""
    precios_filtered: List[dict] = []
    
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
    # PAGINACIÓN PARA PRECIOS DISPONIBLES
    # ==================================================
    precios_paginated: List[dict] = []
    current_page_precios: int = 1
    items_per_page_precios: int = 10
    total_pages_precios: int = 1
    page_numbers_precios: List[int] = []

    # ==================================================
    # PAGINACIÓN PARA MIS SOLICITUDES RM
    # ==================================================
    rm_solicitudes_paginated: List[dict] = []
    rm_current_page: int = 1
    rm_items_per_page: int = 10
    rm_total_pages: int = 1
    rm_page_numbers: List[int] = []

    # ==================================================
    # PAGINACIÓN PARA HISTORIAL FINANCIAMIENTO
    # ==================================================
    fin_solicitudes_paginated: List[dict] = []
    fin_current_page: int = 1
    fin_items_per_page: int = 10
    fin_total_pages: int = 1
    fin_page_numbers: List[int] = []

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
    
    @rx.event
    def crear_solicitud_rm(self, form_data: dict):
        """Crea una solicitud con múltiples recursos"""
        if not self.is_authenticated_rm:
            yield rx.toast.error("❌ No estás autenticado")
            return

        if not self.recursos:
            yield rx.toast.error("❌ Debes agregar al menos un recurso")
            return

        self.loading_form_rm = True
        yield

        try:
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

            if not response:
                yield rx.toast.error("❌ Error al crear la solicitud")
                return

            # Éxito
            self.recursos = []
            self.centro_costo = ""
            self.fecha = ""
            self.orden_trabajo = ""
            self.show_success = True

            yield rx.toast.success(f"✅ Solicitud creada con {len(response.get('recursos', []))} recursos")
            
            yield from self.load_mis_solicitudes_rm()

        except Exception as e:
            print(f"❌ Error en crear_solicitud_rm: {e}")
            import traceback
            traceback.print_exc()
            yield rx.toast.error(f"❌ Error al crear la solicitud: {str(e)}")
        finally:
            self.loading_form_rm = False
            yield
    
    @rx.event
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

        try:
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

            if not response:
                yield rx.toast.error("❌ Error al crear la solicitud de financiamiento")
                return

            # Éxito
            self.recursos_fin = []
            self.area_solicitante_fin = ""
            self.fecha_fin = ""
            self.numero_contrato_fin = ""
            self.orden_trabajo_fin = ""
            self.recurso_fin_servicio = ""
            self.recurso_fin_descripcion = ""
            self.recurso_fin_cantidad = ""
            self.show_success_fin = True

            yield rx.toast.success(f"✅ Solicitud de financiamiento creada con {len(response)} productos")
            
            yield from self.load_mis_solicitudes_fin()

        except Exception as e:
            print(f"❌ Error en crear_solicitud_fin: {e}")
            import traceback
            traceback.print_exc()
            yield rx.toast.error(f"❌ Error al crear la solicitud de financiamiento: {str(e)}")
        finally:
            self.loading_fin = False
            yield
    
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
            self.reset_rm_pagination()
        
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
            self.reset_fin_pagination()
        
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
    # PRECIOS DISPONIBLES (con paginación y filtro)
    # ==================================================
    
    @rx.event
    def load_precios_disponibles(self):
        """Carga los precios disponibles y calcula la paginación"""
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
            self.precios_filtered = precios_con_final  # inicialmente todos
            self.reset_precios_pagination()
        except Exception as e:
            print(f"Error cargando precios: {e}")
            self.precios_disponibles = []
            self.precios_filtered = []
            self.reset_precios_pagination()
        
        self.precios_loading = False

    # NUEVO: método para filtrar precios
    def filter_precios(self, search_value: str):
        """Filtra los precios por tipo o descripción"""
        self.precios_search_value = search_value
        
        if not search_value:
            self.precios_filtered = self.precios_disponibles
        else:
            search_term = search_value.lower()
            filtered = []
            for p in self.precios_disponibles:
                tipo = p.get("Tipo", "").lower()
                desc = p.get("Descripcion", "").lower()
                if search_term in tipo or search_term in desc:
                    filtered.append(p)
            self.precios_filtered = filtered
        
        self.reset_precios_pagination()  # vuelve a página 1 y recalcula
    
    # ==================================================
    # MÉTODOS DE PAGINACIÓN PARA PRECIOS (ahora sobre filtered)
    # ==================================================
    
    def calculate_precios_pagination(self):
        """Calcula la paginación para la tabla de precios disponibles."""
        total_items = len(self.precios_filtered)

        if total_items == 0:
            self.total_pages_precios = 1
            self.precios_paginated = []
        else:
            self.total_pages_precios = max(1, (total_items + self.items_per_page_precios - 1) // self.items_per_page_precios)

        if self.current_page_precios > self.total_pages_precios:
            self.current_page_precios = max(1, self.total_pages_precios)

        start_idx = (self.current_page_precios - 1) * self.items_per_page_precios
        end_idx = min(start_idx + self.items_per_page_precios, total_items)

        if total_items > 0:
            self.precios_paginated = self.precios_filtered[start_idx:end_idx]
        else:
            self.precios_paginated = []

        self.calculate_precios_page_numbers()

    def calculate_precios_page_numbers(self):
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
        if 1 <= page_number <= self.total_pages_precios:
            self.current_page_precios = page_number
            self.calculate_precios_pagination()

    def next_page_precios(self):
        if self.current_page_precios < self.total_pages_precios:
            self.current_page_precios += 1
            self.calculate_precios_pagination()

    def previous_page_precios(self):
        if self.current_page_precios > 1:
            self.current_page_precios -= 1
            self.calculate_precios_pagination()

    def reset_precios_pagination(self):
        self.current_page_precios = 1
        self.calculate_precios_pagination()

    # ==================================================
    # MÉTODOS DE PAGINACIÓN PARA MIS SOLICITUDES RM
    # ==================================================
    
    def calculate_rm_pagination(self):
        """Calcula la paginación para la tabla de solicitudes RM."""
        total_items = len(self.mis_solicitudes_rm)

        if total_items == 0:
            self.rm_total_pages = 1
            self.rm_solicitudes_paginated = []
        else:
            self.rm_total_pages = max(1, (total_items + self.rm_items_per_page - 1) // self.rm_items_per_page)

        if self.rm_current_page > self.rm_total_pages:
            self.rm_current_page = max(1, self.rm_total_pages)

        start_idx = (self.rm_current_page - 1) * self.rm_items_per_page
        end_idx = min(start_idx + self.rm_items_per_page, total_items)

        if total_items > 0:
            self.rm_solicitudes_paginated = self.mis_solicitudes_rm[start_idx:end_idx]
        else:
            self.rm_solicitudes_paginated = []

        self.calculate_rm_page_numbers()

    def calculate_rm_page_numbers(self):
        max_pages_to_show = 4
        current = self.rm_current_page
        total = self.rm_total_pages

        if total <= max_pages_to_show:
            self.rm_page_numbers = list(range(1, total + 1))
            return

        start = max(1, current - 1)
        end = min(total, start + max_pages_to_show - 1)

        if end - start + 1 < max_pages_to_show:
            start = max(1, end - max_pages_to_show + 1)

        self.rm_page_numbers = list(range(start, end + 1))

    def go_to_page_rm(self, page_number: int):
        if 1 <= page_number <= self.rm_total_pages:
            self.rm_current_page = page_number
            self.calculate_rm_pagination()

    def next_page_rm(self):
        if self.rm_current_page < self.rm_total_pages:
            self.rm_current_page += 1
            self.calculate_rm_pagination()

    def previous_page_rm(self):
        if self.rm_current_page > 1:
            self.rm_current_page -= 1
            self.calculate_rm_pagination()

    def reset_rm_pagination(self):
        self.rm_current_page = 1
        self.calculate_rm_pagination()

    # ==================================================
    # MÉTODOS DE PAGINACIÓN PARA HISTORIAL FINANCIAMIENTO
    # ==================================================
    
    def calculate_fin_pagination(self):
        """Calcula la paginación para la tabla de historial de financiamiento."""
        total_items = len(self.mis_solicitudes_fin)

        if total_items == 0:
            self.fin_total_pages = 1
            self.fin_solicitudes_paginated = []
        else:
            self.fin_total_pages = max(1, (total_items + self.fin_items_per_page - 1) // self.fin_items_per_page)

        if self.fin_current_page > self.fin_total_pages:
            self.fin_current_page = max(1, self.fin_total_pages)

        start_idx = (self.fin_current_page - 1) * self.fin_items_per_page
        end_idx = min(start_idx + self.fin_items_per_page, total_items)

        if total_items > 0:
            self.fin_solicitudes_paginated = self.mis_solicitudes_fin[start_idx:end_idx]
        else:
            self.fin_solicitudes_paginated = []

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
    
    def reset_loading_states(self):
        """Resetea todos los estados de carga al cargar la página"""
        self.loading_form_rm = False
        self.loading_fin = False
        self.precios_loading = False
        self.loading_historial_rm = False
        self.loading_auth_rm = False