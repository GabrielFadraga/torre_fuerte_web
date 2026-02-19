import reflex as rx
from typing import List
from TFuerte.api.solicitudes_api import SolicitudesAPI
from datetime import datetime
import uuid
import traceback

class SolicitanteDashboardState(rx.State):
    """Estado para el dashboard de solicitantes"""
    
    # Formulario de nueva solicitud múltiple
    destino: str = ""
    
    # Lista de recursos en el formulario
    recursos_form: List[dict] = []
    
    # Mis solicitudes (agrupadas)
    mis_solicitudes: List[dict] = []
    
    # ID del solicitante
    solicitante_id: int = 0
    solicitante_custom_id: int = 0
    
    # Estados de UI
    loading: bool = False
    
    # ID del grupo actual para la próxima solicitud
    grupo_id_actual: str = ""

    # ==================================================
    # PAGINACIÓN PARA MIS SOLICITUDES
    # ==================================================
    mis_solicitudes_paginated: List[dict] = []
    mis_current_page: int = 1
    mis_items_per_page: int = 5          # Número de tarjetas por página
    mis_total_pages: int = 1
    mis_page_numbers: List[int] = []

    def _fetch_and_group_solicitudes(self) -> List[dict]:
        """Obtiene y agrupa las solicitudes del solicitante actual (sin eventos)."""
        if not self.solicitante_custom_id:
            print("⚠️ No hay custom_id disponible")
            return []
        
        solicitudes = SolicitudesAPI.get_solicitudes_by_solicitante(self.solicitante_custom_id)
        if not solicitudes:
            return []
        
        grupos = {}
        for solicitud in solicitudes:
            grupo_id = solicitud.get("solicitud_grupo_id") or f"individual_{solicitud.get('id')}"
            
            if grupo_id not in grupos:
                fecha_solicitud = solicitud.get("fecha_solicitud", "")
                fecha_formateada = ""
                if fecha_solicitud:
                    try:
                        fecha_formateada = fecha_solicitud.split('T')[0] if 'T' in fecha_solicitud else fecha_solicitud[:10]
                    except:
                        fecha_formateada = fecha_solicitud[:10] if len(fecha_solicitud) >= 10 else fecha_solicitud
                
                grupos[grupo_id] = {
                    "grupo_id": grupo_id,
                    "solicitudes": [],
                    "estado": solicitud.get("estado", "pendiente"),
                    "fecha_solicitud": fecha_solicitud,
                    "fecha_formateada": fecha_formateada,
                    "destino": solicitud.get("Destino", "")
                }
            
            grupos[grupo_id]["solicitudes"].append(solicitud)
        
        for grupo in grupos.values():
            grupo["num_recursos"] = len(grupo["solicitudes"])
        
        grupos_lista = list(grupos.values())
        grupos_lista.sort(key=lambda x: x.get("fecha_solicitud", ""), reverse=True)
        return grupos_lista
    
    # Computed vars para estadísticas
    @rx.var
    def computed_total_solicitudes(self) -> int:
        return len(self.mis_solicitudes)
    
    @rx.var
    def computed_total_recursos(self) -> int:
        total = 0
        for grupo in self.mis_solicitudes:
            total += len(grupo.get("solicitudes", []))
        return total
    
    @rx.var
    def tiene_recursos_en_formulario(self) -> bool:
        """Verifica si hay recursos en el formulario"""
        return len(self.recursos_form) > 0
    
    @rx.var
    def is_loading(self) -> bool:
        """Combina el loading propio y el de AlmacenState."""
        from TFuerte.state.almacen_state import AlmacenState
        return self.loading | AlmacenState.loading
    
    def on_load(self):
        """Se ejecuta al cargar la página"""
        print("🔄 on_load: Cargando dashboard...")
        # Generar un nuevo ID de grupo para la próxima solicitud
        self.grupo_id_actual = str(uuid.uuid4())[:8]
        return SolicitanteDashboardState.load_mis_solicitudes
    
    @rx.event
    def load_mis_solicitudes(self):
        """Carga las solicitudes del solicitante actual con indicador de carga."""
        self.loading = True
        yield
        
        try:
            self.mis_solicitudes = self._fetch_and_group_solicitudes()
            self.reset_mis_pagination()
            print(f"✅ {len(self.mis_solicitudes)} grupos de solicitudes cargados")
        except Exception as e:
            print(f"❌ Error cargando solicitudes: {e}")
            traceback.print_exc()
            self.mis_solicitudes = []
            self.reset_mis_pagination()
            yield rx.toast.error("Error al cargar solicitudes", position="top-right")
        finally:
            self.loading = False
    
    def set_destino(self, destino: str):
        self.destino = destino
    
    def agregar_recurso_form(self):
        """Agrega un nuevo recurso al formulario"""
        nuevo_recurso = {
            "descripcion": "",
            "cantidad": "",
            "observacion": "",
            "index": len(self.recursos_form)
        }
        self.recursos_form.append(nuevo_recurso)
    
    def eliminar_recurso_form(self, index: int):
        """Elimina un recurso del formulario"""
        if 0 <= index < len(self.recursos_form):
            self.recursos_form.pop(index)
            # Reindexar los recursos restantes
            for i, recurso in enumerate(self.recursos_form):
                recurso["index"] = i
    
    def get_recurso_field(self, index: int, field: str):
        """Obtiene el valor de un campo de un recurso"""
        if 0 <= index < len(self.recursos_form):
            return self.recursos_form[index].get(field, "")
        return ""
    
    def set_recurso_field(self, index: int, field: str, value: str):
        """Establece el valor de un campo de un recurso"""
        if 0 <= index < len(self.recursos_form):
            if field in self.recursos_form[index]:
                self.recursos_form[index][field] = value
    
    @rx.event
    def crear_solicitud_multiple(self):
        """Crea una solicitud con múltiples recursos."""
        if len(self.recursos_form) == 0:
            yield rx.toast.error("❌ Debe agregar al menos un recurso")
            return
        if not self.destino.strip():
            yield rx.toast.error("❌ El destino es requerido")
            return
        
        for i, recurso in enumerate(self.recursos_form):
            if not recurso.get("descripcion", "").strip():
                yield rx.toast.error(f"❌ Descripción del recurso #{i+1} requerida")
                return
            try:
                cantidad = int(recurso.get("cantidad", "0"))
                if cantidad <= 0: raise ValueError
            except:
                yield rx.toast.error(f"❌ Cantidad inválida en recurso #{i+1}")
                return
        
        if not self.solicitante_custom_id:
            yield rx.toast.error("❌ No hay sesión activa. Inicia sesión nuevamente.")
            return
        
        self.loading = True
        yield
        
        recursos_creados = 0
        try:
            for i, recurso in enumerate(self.recursos_form):
                solicitud_data = {
                    "Descripcion": recurso.get("descripcion", "").strip(),
                    "Cantidad": int(recurso.get("cantidad", "0")),
                    "Observacion": recurso.get("observacion", "").strip() or None,
                    "Destino": self.destino.strip(),
                    "solicitante_id": self.solicitante_id,
                    "custom": self.solicitante_custom_id,
                    "estado": "pendiente",
                    "fecha_solicitud": datetime.now().isoformat(),
                    "solicitud_grupo_id": self.grupo_id_actual,
                    "item_index": i + 1
                }
                
                result = SolicitudesAPI.create_solicitud(solicitud_data)
                if result:
                    recursos_creados += 1
                else:
                    print(f"⚠️ Error creando recurso #{i+1}")
            
            self.mis_solicitudes = self._fetch_and_group_solicitudes()
            self.reset_mis_pagination()
            
            self.recursos_form = []
            self.destino = ""
            self.grupo_id_actual = str(uuid.uuid4())[:8]
            
            yield rx.toast.success(f"✅ Solicitud creada con {recursos_creados} recursos")
            
        except Exception as e:
            print(f"❌ Error en crear_solicitud_multiple: {e}")
            traceback.print_exc()
            yield rx.toast.error("❌ Error interno al crear la solicitud")
        finally:
            self.loading = False
    
    @rx.event
    def set_solicitante_info(self, solicitante_info: dict):
        """Establece la información del solicitante después del login"""
        self.solicitante_id = solicitante_info.get("id", 0)
        self.solicitante_custom_id = solicitante_info.get("id_custom", 0)
        print(f"✅ Información del solicitante establecida: ID={self.solicitante_id}, CustomID={self.solicitante_custom_id}")
    
    @rx.event
    def ver_detalle_grupo(self, grupo_id: str):
        """Muestra los detalles de un grupo de solicitudes"""
        print(f"🔍 Ver detalles del grupo: {grupo_id}")
        
        grupo_encontrado = None
        for grupo in self.mis_solicitudes:
            if grupo.get("grupo_id") == grupo_id:
                grupo_encontrado = grupo
                break
        
        if grupo_encontrado:
            num_recursos = len(grupo_encontrado.get("solicitudes", []))
            yield rx.toast.info(
                f"Grupo {grupo_id}: {num_recursos} recursos, Destino: {grupo_encontrado.get('destino', '')}",
                position="top-right",
                duration=4000
            )
        else:
            yield rx.toast.error(
                f"Grupo {grupo_id} no encontrado",
                position="top-right",
                duration=3000
            )
    
    def limpiar_recursos_form(self):
        """Limpia todos los recursos del formulario"""
        self.recursos_form = []
        self.destino = ""

    # ==================================================
    # MÉTODOS DE PAGINACIÓN PARA MIS SOLICITUDES
    # ==================================================

    def calculate_mis_pagination(self):
        total_items = len(self.mis_solicitudes)

        if total_items == 0:
            self.mis_total_pages = 1
            self.mis_solicitudes_paginated = []
        else:
            self.mis_total_pages = max(1, (total_items + self.mis_items_per_page - 1) // self.mis_items_per_page)

        if self.mis_current_page > self.mis_total_pages:
            self.mis_current_page = max(1, self.mis_total_pages)

        start_idx = (self.mis_current_page - 1) * self.mis_items_per_page
        end_idx = min(start_idx + self.mis_items_per_page, total_items)

        if total_items > 0:
            self.mis_solicitudes_paginated = self.mis_solicitudes[start_idx:end_idx]
        else:
            self.mis_solicitudes_paginated = []

        self.calculate_mis_page_numbers()

    def calculate_mis_page_numbers(self):
        max_pages_to_show = 4
        current = self.mis_current_page
        total = self.mis_total_pages

        if total <= max_pages_to_show:
            self.mis_page_numbers = list(range(1, total + 1))
            return

        start = max(1, current - 1)
        end = min(total, start + max_pages_to_show - 1)

        if end - start + 1 < max_pages_to_show:
            start = max(1, end - max_pages_to_show + 1)

        self.mis_page_numbers = list(range(start, end + 1))

    def go_to_page_mis(self, page_number: int):
        if 1 <= page_number <= self.mis_total_pages:
            self.mis_current_page = page_number
            self.calculate_mis_pagination()

    def next_page_mis(self):
        if self.mis_current_page < self.mis_total_pages:
            self.mis_current_page += 1
            self.calculate_mis_pagination()

    def previous_page_mis(self):
        if self.mis_current_page > 1:
            self.mis_current_page -= 1
            self.calculate_mis_pagination()

    def reset_mis_pagination(self):
        self.mis_current_page = 1
        self.calculate_mis_pagination()