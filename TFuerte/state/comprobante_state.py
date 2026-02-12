# TFuerte/state/comprobante_state.py
import reflex as rx
from typing import List
from TFuerte.api.comprobante_api import ComprobanteAPI
from TFuerte.api.solicitudes_api import SolicitudesAPI
from TFuerte.api.almacen_api import AlmacenAPI
from TFuerte.api.registrotf_api import RegistroTFAPI
from datetime import datetime
from TFuerte.state.auth_state import AuthState  # AGREGAR ESTA IMPORT

class ComprobanteState(rx.State):
    """Estado para manejar la generación de comprobantes"""
    
    # Variables para el formulario de comprobante
    destino_comprobante: str = ""
    fecha_salida_comprobante: str = ""
    recibido_por: str = ""
    observaciones_comprobante: str = ""
    
    # Datos del comprobante actual
    comprobante_actual: dict = {}
    detalles_comprobante: List[dict] = []
    
    # Productos seleccionados para el comprobante
    productos_seleccionados: List[dict] = []
    
    # Cálculos del comprobante
    subtotal: float = 0.0
    total: float = 0.0
    
    # Datos de firmas
    aprobado_por: str = ""
    despachado_por: str = ""
    cargo_despachado: str = ""

    cargo_aprobado: str = ""
    
    # UI State
    loading_comprobante: bool = False
    show_comprobante_dialog: bool = False
    
    def on_load_comprobante(self):
        """Carga datos iniciales para el comprobante"""
        # Obtener la fecha actual
        self.fecha_salida_comprobante = datetime.now().strftime("%Y-%m-%d")
        
        # Obtener datos del jefe de almacén
        jefe_almacen = ComprobanteAPI.get_jefe_almacen()
        if jefe_almacen:
            self.despachado_por = jefe_almacen.get("user", "")
            self.cargo_despachado = jefe_almacen.get("cargo", "")
        
        # Obtener datos del administrador ACTUAL en sesión
        # Usar get_state para acceder al estado de AdminAuthState
        try:
            from TFuerte.state.admin_auth_state import AdminAuthState
            
            # Obtener el estado actual de AdminAuthState
            admin_auth_state = AdminAuthState()
            current_admin = admin_auth_state.current_admin
            
            if current_admin and isinstance(current_admin, dict):
                admin_user = current_admin.get("user", "")
                if admin_user:
                    admin_data = ComprobanteAPI.get_admin_by_username(admin_user)
                    if admin_data:
                        self.aprobado_por = admin_user
                        self.cargo_aprobado = admin_data.get("cargo", "Administrador")
                        return
            
            # Si no hay admin en sesión o no se pudo obtener, usar el primero de la tabla
            administrador = ComprobanteAPI.get_administrador()
            if administrador:
                self.aprobado_por = administrador.get("user", "")
                self.cargo_aprobado = administrador.get("cargo", "Administrador")
                
        except Exception as e:
            print(f"⚠️ Error cargando admin en on_load_comprobante: {e}")
            # Fallback: usar el primer administrador
            administrador = ComprobanteAPI.get_administrador()
            if administrador:
                self.aprobado_por = administrador.get("user", "")
                self.cargo_aprobado = administrador.get("cargo", "Administrador")
    
    def calcular_totales(self):
        """Calcula los totales del comprobante"""
        subtotal = 0.0
        
        for producto in self.productos_seleccionados:
            precio = producto.get("precio", 0)
            cantidad = producto.get("cantidad_salida", 1)
            importe = precio * cantidad
            producto["importe"] = importe
            subtotal += importe
        
        self.subtotal = subtotal
        self.total = subtotal
    
    def agregar_producto_comprobante(self, producto: dict):
        """Agrega un producto al comprobante actual"""
        # Verificar si el producto ya está en la lista
        for p in self.productos_seleccionados:
            if p.get("numero") == producto.get("Numero"):
                # Actualizar cantidad
                p["cantidad_salida"] += 1
                self.calcular_totales()
                return
        
        # Obtener precio del producto
        descripcion = producto.get("Descripcion del producto", "")
        precio = ComprobanteAPI.get_precio_by_descripcion(descripcion)
        
        if precio == 0:
            # Usar el precio del almacén como respaldo
            precio = producto.get("Precio", 0)
        
        nuevo_producto = {
            "numero": producto.get("Numero"),
            "codigo": producto.get("Codigo", ""),
            "descripcion": descripcion,
            "um": producto.get("UM", ""),
            "cantidad_salida": 1,  # Cantidad por defecto
            "precio": precio,
            "importe": precio,
            "saldo_disponible": producto.get("Saldo", 100)  # Agregar saldo disponible
        }
        
        self.productos_seleccionados.append(nuevo_producto)
        self.calcular_totales()

    # También necesito agregar métodos setter para los campos del formulario:
    def set_destino_comprobante(self, destino: str):
        self.destino_comprobante = destino

    def set_fecha_salida_comprobante(self, fecha: str):
        self.fecha_salida_comprobante = fecha

    def set_recibido_por(self, recibido_por: str):
        self.recibido_por = recibido_por

    def set_observaciones_comprobante(self, observaciones: str):
        self.observaciones_comprobante = observaciones

    def set_show_comprobante_dialog(self, show: bool):
        self.show_comprobante_dialog = show
    
    def eliminar_producto_comprobante(self, index: int):
        """Elimina un producto del comprobante"""
        if 0 <= index < len(self.productos_seleccionados):
            self.productos_seleccionados.pop(index)
            self.calcular_totales()
    
    # MÉTODO MODIFICADO - Ahora recibe un string y lo convierte
    def actualizar_cantidad_producto(self, index: int, valor: str):
        """Actualiza la cantidad de un producto en el comprobante"""
        # Convertir el string a int, manejando valores vacíos
        try:
            if valor is None or valor == "":
                cantidad = 1
            else:
                cantidad = int(valor)
        except (ValueError, TypeError):
            cantidad = 1
        
        if 0 <= index < len(self.productos_seleccionados):
            if cantidad > 0:
                # Verificar que no exceda el saldo disponible
                saldo_disponible = self.productos_seleccionados[index].get("saldo_disponible", 100)
                if cantidad > saldo_disponible:
                    cantidad = saldo_disponible
                
                self.productos_seleccionados[index]["cantidad_salida"] = cantidad
                self.calcular_totales()
    
    # TFuerte/state/comprobante_state.py - Método generar_comprobante completo con cambios

    @rx.event
    def generar_comprobante(self):
        """Genera un nuevo comprobante en la base de datos"""
        if not self.productos_seleccionados:
            return rx.toast.error(
                "❌ No hay productos seleccionados para el comprobante",
                position="top-right",
                duration=4000
            )
        
        if not self.destino_comprobante or not self.fecha_salida_comprobante:
            return rx.toast.error(
                "❌ Destino y fecha de salida son requeridos",
                position="top-right",
                duration=4000
            )
        
        self.loading_comprobante = True
        yield
        
        try:
            # Generar ID único para el grupo de solicitud
            import uuid
            solicitud_grupo_id = str(uuid.uuid4())[:8]
            
            # BUSCAR ADMINISTRADOR QUE APROBÓ (NUEVO CÓDIGO)
            admin_aprobador = None
            
            # Buscar en productos seleccionados
            for producto in self.productos_seleccionados:
                descripcion = producto.get("descripcion", "")
                admin_data = ComprobanteAPI.get_admin_que_aprobo_solicitud(descripcion)
                if admin_data and admin_data.get("user"):
                    admin_aprobador = admin_data.get("user", "")
                    break
            
            # Si no se encontró, usar el valor ya cargado en el estado
            if not admin_aprobador:
                admin_aprobador = self.aprobado_por
            
            # Crear el comprobante principal (ACTUALIZADO)
            comprobante_data = {
                "solicitud_grupo_id": solicitud_grupo_id,
                "destino": self.destino_comprobante,
                "fecha_salida": self.fecha_salida_comprobante,
                "total": self.total,
                "aprobado_por": admin_aprobador,  # Usar el admin encontrado
                "despachado_por": self.despachado_por,
                "recibido_por": self.recibido_por,
                "firma_aprobado": f"{admin_aprobador}.png" if admin_aprobador else "",
                "firma_despachado": f"{self.despachado_por}.png" if self.despachado_por else "",
                "firma_recibido": f"{self.recibido_por}.png" if self.recibido_por else "",
                "observaciones": self.observaciones_comprobante
            }
            
            comprobante = ComprobanteAPI.crear_comprobante(comprobante_data)
            
            if not comprobante:
                yield rx.toast.error(
                    "❌ Error al crear el comprobante",
                    position="top-right",
                    duration=4000
                )
                self.loading_comprobante = False
                return
            
            # Crear los detalles del comprobante
            for producto in self.productos_seleccionados:
                detalle_data = {
                    "comprobante_id": comprobante["id"],
                    "codigo": producto.get("codigo", ""),
                    "descripcion": producto.get("descripcion", ""),
                    "um": producto.get("um", ""),
                    "cantidad": producto.get("cantidad_salida", 0),
                    "precio": producto.get("precio", 0),
                    "importe": producto.get("importe", 0)
                }
                
                ComprobanteAPI.crear_detalle_comprobante(detalle_data)
            
            # Limpiar el formulario
            self.productos_seleccionados = []
            self.destino_comprobante = ""
            self.recibido_por = ""
            self.observaciones_comprobante = ""
            self.subtotal = 0.0
            self.total = 0.0
            
            yield rx.toast.success(
                f"✅ Comprobante #{comprobante['id']} generado exitosamente",
                position="top-right",
                duration=4000
            )
            
            # Cerrar el diálogo
            self.show_comprobante_dialog = False
            
        except Exception as e:
            print(f"❌ Error generando comprobante: {e}")
            import traceback
            traceback.print_exc()
            yield rx.toast.error(
                "❌ Error interno al generar comprobante",
                position="top-right",
                duration=4000
            )
        
        self.loading_comprobante = False
    
    def abrir_dialogo_comprobante(self):
        """Abre el diálogo para generar comprobante"""
        if not self.productos_seleccionados:
            return rx.toast.error(
                "❌ No hay productos seleccionados",
                position="top-right",
                duration=3000
            )
        
        self.show_comprobante_dialog = True
    
    def cerrar_dialogo_comprobante(self):
        """Cierra el diálogo de comprobante"""
        self.show_comprobante_dialog = False
    
    # TFuerte/state/comprobante_state.py - Corregir generar_comprobante_word

    @rx.event
    def generar_comprobante_word(self):
        """Genera el documento Word del comprobante"""
        if not self.productos_seleccionados:
            return rx.toast.error(
                "❌ No hay productos seleccionados para el comprobante",
                position="top-right",
                duration=3000
            )
        
        if not self.destino_comprobante or not self.fecha_salida_comprobante:
            return rx.toast.error(
                "❌ Destino y fecha de salida son requeridos",
                position="top-right",
                duration=3000
            )
        
        self.loading_comprobante = True
        yield
        
        try:
            # 1. Obtener jefe de almacén (despachado por)
            jefe_almacen = ComprobanteAPI.get_jefe_almacen()
            despachado_por = jefe_almacen.get("user", "") if jefe_almacen else ""
            cargo_despachado = jefe_almacen.get("cargo", "") if jefe_almacen else ""
            
            # 2. Obtener administrador que APROBÓ (BUSCAR EN SOLICITUDES)
            admin_aprobador = None
            cargo_aprobador = "Administrador"
            
            # Primero buscar en los productos seleccionados
            for producto in self.productos_seleccionados:
                descripcion = producto.get("descripcion", "")
                # Buscar el administrador que aprobó esta solicitud
                admin_data = ComprobanteAPI.get_admin_que_aprobo_solicitud(descripcion)
                if admin_data and admin_data.get("user"):
                    admin_aprobador = admin_data.get("user", "")
                    cargo_aprobador = admin_data.get("cargo", "Administrador")
                    break
            
            # Si no se encontró, intentar obtener el admin actual de la sesión
            if not admin_aprobador:
                try:
                    from TFuerte.state.admin_auth_state import AdminAuthState
                    
                    # Obtener el estado actual
                    admin_auth_state = AdminAuthState()
                    current_admin = admin_auth_state.current_admin
                    
                    if current_admin and isinstance(current_admin, dict):
                        admin_user = current_admin.get("user", "")
                        if admin_user:
                            admin_data = ComprobanteAPI.get_admin_by_username(admin_user)
                            if admin_data:
                                admin_aprobador = admin_user
                                cargo_aprobador = admin_data.get("cargo", "Administrador")
                except Exception as e:
                    print(f"⚠️ Error obteniendo admin de sesión: {e}")
            
            # Si aún no hay admin, usar el primero de la tabla
            if not admin_aprobador:
                administrador = ComprobanteAPI.get_administrador()
                if administrador:
                    admin_aprobador = administrador.get("user", "")
                    cargo_aprobador = administrador.get("cargo", "Administrador")
            
            # 3. El recibido por ya está en self.recibido_por
            
            # Preparar datos del comprobante
            comprobante_data = {
                "destino": self.destino_comprobante,
                "fecha_salida": self.fecha_salida_comprobante,
                "total": self.total,
                "aprobado_por": admin_aprobador or "",
                "cargo_aprobado": cargo_aprobador,
                "despachado_por": despachado_por,
                "cargo_despachado": cargo_despachado,
                "recibido_por": self.recibido_por,
                "firma_aprobado": f"{admin_aprobador}.png" if admin_aprobador else "",
                "firma_despachado": f"{despachado_por}.png" if despachado_por else "",
                "firma_recibido": f"{self.recibido_por}.png" if self.recibido_por else "",
                "observaciones": self.observaciones_comprobante
            }
            
            # Preparar detalles del comprobante
            detalles_data = []
            for i, producto in enumerate(self.productos_seleccionados, 1):
                detalle = {
                    "codigo": producto.get("codigo", ""),
                    "descripcion": producto.get("descripcion", ""),
                    "um": producto.get("um", ""),
                    "cantidad": producto.get("cantidad_salida", 0),
                    "precio": producto.get("precio", 0),
                    "importe": producto.get("importe", 0)
                }
                detalles_data.append(detalle)
            
            # Importar y usar el generador de Word
            from TFuerte.utilss.comprobante_word_generator import generar_comprobante_word
            
            # Generar el documento
            word_content = generar_comprobante_word(comprobante_data, detalles_data)
            
            # Crear nombre del archivo
            from datetime import datetime
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"Comprobante_Salida_{fecha_actual}.docx"
            
            yield rx.toast.success(
                f"✅ Documento Word generado: {nombre_archivo}",
                position="top-right",
                duration=3000
            )
            
            # Retornar el archivo para descarga
            return rx.download(
                data=word_content,
                filename=nombre_archivo
            )
            
        except Exception as e:
            print(f"❌ Error generando documento Word: {e}")
            import traceback
            traceback.print_exc()
            yield rx.toast.error(
                "❌ Error al generar el documento Word",
                position="top-right",
                duration=3000
            )
        finally:
            self.loading_comprobante = False