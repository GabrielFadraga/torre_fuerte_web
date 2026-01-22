# TFuerte/state/almacen_state.py
import reflex as rx
import csv
import io
import json
from typing import List
from TFuerte.api.almacen_api import AlmacenAPI
from TFuerte.api.registrotf_api import RegistroTFAPI

class AlmacenState(rx.State):
    """Estado que maneja los datos de Supabase para la tabla Almacen"""
    
    almacen_data: List[dict] = []
    filtered_data: List[dict] = []  # Datos filtrados para mostrar
    loading: bool = False
    selected_items: List[int] = []
    editing_item_numero: int = 0
    edit_form_data: dict = {}
    show_delete_dialog: bool = False
    show_entrada_dialog: bool = False
    show_salida_dialog: bool = False
    operation_type: str = ""
    total_productos: int = 0
    valor_total: float = 0.0
    search_value: str = ""  # Valor de búsqueda
    sort_value: str = ""  # Valor para ordenar
    
    # Nuevos atributos para los formularios de entrada/salida
    entrada_form_data: dict = {}
    salida_form_data: dict = {}
    
    def load_data(self):
        """Carga los datos desde Supabase"""
        self.loading = True
        yield
        
        data = AlmacenAPI.get_all_items()
        
        if data:
            # Normalizar nombres de columnas
            for item in data:
                if "Fecha de salida" in item:
                    item["Fecha de salida"] = item["Fecha de salida"]
                elif "Fecha de salida" not in item:
                    item["Fecha de salida"] = None
                
                if "Cantidad S" in item and item["Cantidad S"] is None:
                    item["Cantidad S"] = 0
            
            # Ordenar por Numero
            data.sort(key=lambda x: x.get('Numero', 0))
            self.almacen_data = data
            # Aplicar filtros actuales a los nuevos datos
            yield self.load_entries()
            self.calcular_estadisticas()
            print(f"✅ Datos cargados: {len(data)} registros")
            
            yield rx.toast.info(
                f"Datos cargados: {len(data)} registros",
                position="top-right",
                duration=3000
            )
        else:
            self.almacen_data = []
            self.filtered_data = []
            self.total_productos = 0
            self.valor_total = 0.0
            
            yield rx.toast.error(
                "No se pudieron cargar los datos",
                position="top-right",
                duration=3000
            )
        
        self.loading = False
    
    def load_entries(self):
        """Filtra y ordena los datos según los valores de búsqueda y orden"""
        # Comenzar con todos los datos
        result = self.almacen_data.copy()
        
        # Aplicar filtro si hay valor de búsqueda
        if self.search_value != "":
            search_term = self.search_value.lower()
            result = [
                item
                for item in result
                if search_term in item.get("Descripcion del producto", "").lower()
            ]
        
        # Aplicar ordenación si se seleccionó una columna
        if self.sort_value != "":
            result = sorted(result, key=lambda x: x.get(self.sort_value, ""))
        
        self.filtered_data = result
        self.calcular_estadisticas()
    
    @rx.event
    def sort_values(self, sort_value: str):
        """Actualiza el valor de ordenación y recarga los datos"""
        self.sort_value = sort_value
        self.load_entries()
    
    @rx.event
    def filter_values(self, search_value: str):
        """Actualiza el valor de búsqueda y recarga los datos"""
        self.search_value = search_value
        self.load_entries()
    
    def calcular_estadisticas(self):
        """Calcula estadísticas de los datos filtrados"""
        if not self.filtered_data:
            self.total_productos = 0
            self.valor_total = 0.0
            return
        
        self.total_productos = len(self.filtered_data)
        total_valor = 0.0
        
        for item in self.filtered_data:
            precio = item.get('Precio', 0) or 0
            saldo = item.get('Saldo', 0) or 0
            total_valor += float(precio) * float(saldo)
        
        self.valor_total = total_valor
    
    # Métodos para selección de productos
    def toggle_item_selection(self, item_numero: int):
        """Alterna la selección de un producto usando Numero"""
        current = list(self.selected_items)
        if item_numero in current:
            current.remove(item_numero)
        else:
            current.append(item_numero)
        self.selected_items = current
        print(f"Productos seleccionados (Numero): {self.selected_items}")
    
    def clear_selection(self):
        """Limpia la selección de productos"""
        self.selected_items = []
    
    # Métodos para agregar productos
    def add_item_to_db(self, form_data: dict):
        """Agrega un nuevo producto a la base de datos"""
        print(f"📤 Recibiendo datos del formulario: {form_data}")
        
        required_fields = ["codigo", "descripcion", "tipo", "um", "fecha_entrada", "cantidad_e", "precio"]
        missing_fields = [field for field in required_fields if field not in form_data or not form_data[field]]
        
        if missing_fields:
            return rx.toast.error(
                f"❌ Faltan campos requeridos: {', '.join(missing_fields)}",
                position="top-right",
                duration=4000
            )
        
        # Calcular el próximo Numero
        all_items = AlmacenAPI.get_all_items()
        if all_items:
            numeros = []
            for item in all_items:
                if "Numero" in item and item["Numero"] is not None:
                    try:
                        numeros.append(int(item["Numero"]))
                    except:
                        continue
            
            if numeros:
                next_numero = max(numeros) + 1
            else:
                next_numero = 1
        else:
            next_numero = 1
        
        cantidad_e = int(form_data["cantidad_e"]) if form_data["cantidad_e"] else 0
        cantidad_s = int(form_data.get("cantidad_s", 0)) if form_data.get("cantidad_s") else 0
        
        # Validar que si hay salida, no exceda la entrada
        if cantidad_s > cantidad_e:
            return rx.toast.error(
                f"❌ La cantidad de salida ({cantidad_s}) no puede ser mayor que la cantidad de entrada ({cantidad_e})",
                position="top-right",
                duration=4000
            )
        
        item_data = {
            "Numero": next_numero,
            "Codigo": form_data["codigo"],
            "Descripcion del producto": form_data["descripcion"],
            "Tipo de producto": form_data["tipo"],
            "UM": form_data["um"],
            "Fecha de entrada": form_data["fecha_entrada"],
            "Cantidad E": cantidad_e,
            "Precio": float(form_data["precio"]),
        }
        
        # Solo incluir campos de salida si hay valor
        if form_data.get("fecha_salida") and form_data["fecha_salida"].strip():
            item_data["Fecha de salida"] = form_data["fecha_salida"]
        
        if cantidad_s > 0:
            item_data["Cantidad S"] = cantidad_s
        
        print(f"📦 Datos preparados para Supabase: {item_data}")
        
        result = AlmacenAPI.insert_item(item_data)
        
        if result:
            # Recargar datos usando yield para evitar problemas
            self.loading = True
            yield
            
            data = AlmacenAPI.get_all_items()
            if data:
                for item in data:
                    if "Fecha de salida" in item:
                        item["Fecha de salida"] = item["Fecha de salida"]
                
                data.sort(key=lambda x: x.get('Numero', 0))
                self.almacen_data = data
                # Aplicar filtros actuales
                self.load_entries()
                self.calcular_estadisticas()
            
            self.loading = False
            
            return rx.toast.success(
                f"✅ Producto {item_data['Codigo']} agregado correctamente",
                position="top-right",
                duration=3000
            )
        else:
            return rx.toast.error(
                "❌ Error al agregar producto",
                position="top-right",
                duration=4000
            )
    
    # Métodos para dar entrada
    def open_entrada_dialog(self):
        """Abre el diálogo para dar entrada a un producto"""
        if len(self.selected_items) != 1:
            return rx.toast.error(
                "❌ Selecciona exactamente un producto para dar entrada",
                position="top-right",
                duration=3000
            )
        
        item_numero = self.selected_items[0]
        item = next((item for item in self.almacen_data if item.get("Numero") == item_numero), None)
        
        if item:
            self.editing_item_numero = item_numero
            self.operation_type = "entrada"
            self.edit_form_data = {
                "codigo": item.get("Codigo", ""),
                "descripcion": item.get("Descripcion del producto", ""),
                "fecha_entrada": item.get("Fecha de entrada", ""),
                "cantidad_e": str(item.get("Cantidad E", 0)),
                "precio": str(item.get("Precio", 0))
            }
            # Inicializar datos adicionales para RegistroTF
            self.entrada_form_data = {
                "recibe": "",
                "destino": "",
                "cliente": ""
            }
            self.show_entrada_dialog = True
            print(f"📝 Datos para entrada: {self.edit_form_data}")
        else:
            return rx.toast.error(
                "❌ No se encontró el producto",
                position="top-right",
                duration=3000
            )
    
    def close_entrada_dialog(self):
        """Cierra el diálogo de entrada"""
        self.show_entrada_dialog = False
        self.edit_form_data = {}
        self.entrada_form_data = {}
    
    def update_entrada_in_db(self, form_data: dict):
        """Actualiza solo los campos de entrada de un producto y registra en RegistroTF"""
        print(f"📤 Actualizando entrada del producto Numero: {self.editing_item_numero}")
        
        required_fields = ["fecha_entrada", "cantidad_e", "precio"]
        missing_fields = [field for field in required_fields if field not in form_data or not form_data[field]]
        
        if missing_fields:
            return rx.toast.error(
                f"❌ Faltan campos requeridos: {', '.join(missing_fields)}",
                position="top-right",
                duration=4000
            )
        
        cantidad_e = int(form_data["cantidad_e"]) if form_data["cantidad_e"] else 0
        
        # 1. ACTUALIZAR TABLA ALMACEN
        item_data = {
            "Fecha de entrada": form_data["fecha_entrada"],
            "Cantidad E": cantidad_e,
            "Precio": float(form_data["precio"]),
            "Fecha de salida": None,
            "Cantidad S": 0,
        }
        
        print(f"📦 Datos para actualizar entrada en Almacen: {item_data}")
        result = AlmacenAPI.update_item(self.editing_item_numero, item_data)
        
        if not result:
            return rx.toast.error(
                "❌ Error al actualizar entrada en Almacen",
                position="top-right",
                duration=4000
            )
        
        # 2. REGISTRAR EN TABLA RegistroTF
        item_actual = next((item for item in self.almacen_data if item.get("Numero") == self.editing_item_numero), None)
        
        if item_actual:
            registro_data = {
                "Producto": item_actual.get("Descripcion del producto", ""),
                "Fecha E": form_data["fecha_entrada"],
                "Cant E": cantidad_e,
                "Fecha S": None,
                "Cant S": 0,
                "Recibe": self.entrada_form_data.get("recibe", ""),
                "Destino": self.entrada_form_data.get("destino", ""),
                "Cliente": self.entrada_form_data.get("cliente", ""),
            }
            
            print(f"📝 Insertando registro en RegistroTF: {registro_data}")
            registro_result = RegistroTFAPI.insert_registro(registro_data)
            
            if not registro_result:
                print("⚠️  No se pudo insertar en RegistroTF, pero la entrada en Almacén se realizó")
        
        # 3. LIMPIAR Y RECARGAR
        self.selected_items = []
        self.editing_item_numero = 0
        self.edit_form_data = {}
        self.entrada_form_data = {}
        self.show_entrada_dialog = False
        
        # Recargar datos
        self.loading = True
        yield
        
        data = AlmacenAPI.get_all_items()
        if data:
            for item in data:
                if "Fecha de salida" in item:
                    item["Fecha de salida"] = item["Fecha de salida"]
            
            data.sort(key=lambda x: x.get('Numero', 0))
            self.almacen_data = data
            self.load_entries()
            self.calcular_estadisticas()
        
        self.loading = False
        
        return rx.toast.success(
            "✅ Entrada actualizada correctamente y registrada en histórico",
            position="top-right",
            duration=3000
        )
    
    # Métodos para dar salida
    def open_salida_dialog(self):
        """Abre el diálogo para dar salida a un producto"""
        if len(self.selected_items) != 1:
            return rx.toast.error(
                "❌ Selecciona exactamente un producto para dar salida",
                position="top-right",
                duration=3000
            )
        
        item_numero = self.selected_items[0]
        item = next((item for item in self.almacen_data if item.get("Numero") == item_numero), None)
        
        if item:
            self.editing_item_numero = item_numero
            self.operation_type = "salida"
            self.edit_form_data = {
                "codigo": item.get("Codigo", ""),
                "descripcion": item.get("Descripcion del producto", ""),
                "fecha_salida": item.get("Fecha de salida", "") or "",
                "cantidad_s": str(item.get("Cantidad S", 0)),
                "precio": str(item.get("Precio", 0))
            }
            # Inicializar datos adicionales para RegistroTF
            self.salida_form_data = {
                "recibe": "",
                "destino": "",
                "cliente": ""
            }
            self.show_salida_dialog = True
            print(f"📝 Datos para salida: {self.edit_form_data}")
        else:
            return rx.toast.error(
                "❌ No se encontró el producto",
                position="top-right",
                duration=3000
            )
    
    def close_salida_dialog(self):
        """Cierra el diálogo de salida"""
        self.show_salida_dialog = False
        self.edit_form_data = {}
        self.salida_form_data = {}
    
    def update_salida_in_db(self, form_data: dict):
        """Actualiza solo los campos de salida de un producto y registra en RegistroTF"""
        print(f"📤 Actualizando salida del producto Numero: {self.editing_item_numero}")
        
        required_fields = ["fecha_salida", "cantidad_s", "precio"]
        missing_fields = [field for field in required_fields if field not in form_data or not form_data[field]]
        
        if missing_fields:
            return rx.toast.error(
                f"❌ Faltan campos requeridos: {', '.join(missing_fields)}",
                position="top-right",
                duration=4000
            )
        
        cantidad_s = int(form_data["cantidad_s"]) if form_data["cantidad_s"] else 0
        
        # Validar contra saldo disponible
        item_actual = next((item for item in self.almacen_data if item.get("Numero") == self.editing_item_numero), None)
        
        if item_actual:
            saldo_actual = item_actual.get("Saldo", 0) or 0
            
            if cantidad_s > saldo_actual:
                return rx.toast.error(
                    f"❌ Cantidad de salida ({cantidad_s}) no puede ser mayor que el saldo disponible ({saldo_actual})",
                    position="top-right",
                    duration=4000
                )
        
        # 1. ACTUALIZAR TABLA ALMACEN
        item_data = {
            "Fecha de salida": form_data["fecha_salida"],
            "Cantidad S": cantidad_s,
            "Precio": float(form_data["precio"]),
            "Fecha de entrada": None,
            "Cantidad E": 0,
        }
        
        print(f"📦 Datos para actualizar salida en Almacen: {item_data}")
        result = AlmacenAPI.update_item(self.editing_item_numero, item_data)
        
        if not result:
            return rx.toast.error(
                "❌ Error al actualizar salida en Almacen",
                position="top-right",
                duration=4000
            )
        
        # 2. REGISTRAR EN TABLA RegistroTF
        registro_data = {
            "Producto": item_actual.get("Descripcion del producto", ""),
            "Fecha E": None,
            "Cant E": 0,
            "Fecha S": form_data["fecha_salida"],
            "Cant S": cantidad_s,
            "Recibe": self.salida_form_data.get("recibe", ""),
            "Destino": self.salida_form_data.get("destino", ""),
            "Cliente": self.salida_form_data.get("cliente", ""),
        }
        
        print(f"📝 Insertando registro en RegistroTF: {registro_data}")
        registro_result = RegistroTFAPI.insert_registro(registro_data)
        
        if not registro_result:
            print("⚠️  No se pudo insertar en RegistroTF, pero la salida en Almacén se realizó")
        
        # 3. LIMPIAR Y RECARGAR
        self.selected_items = []
        self.editing_item_numero = 0
        self.edit_form_data = {}
        self.salida_form_data = {}
        self.show_salida_dialog = False
        
        # Recargar datos
        self.loading = True
        yield
        
        data = AlmacenAPI.get_all_items()
        if data:
            for item in data:
                if "Fecha de salida" in item:
                    item["Fecha de salida"] = item["Fecha de salida"]
            
            data.sort(key=lambda x: x.get('Numero', 0))
            self.almacen_data = data
            self.load_entries()
            self.calcular_estadisticas()
        
        self.loading = False
        
        return rx.toast.success(
            "✅ Salida actualizada correctamente y registrada en histórico",
            position="top-right",
            duration=3000
        )
    
    # Métodos para eliminar productos
    def open_delete_dialog(self):
        """Abre el diálogo de confirmación para eliminar productos"""
        if not self.selected_items:
            return rx.toast.error(
                "❌ No hay productos seleccionados",
                position="top-right",
                duration=3000
            )
        
        self.show_delete_dialog = True
    
    def close_delete_dialog(self):
        """Cierra el diálogo de eliminación"""
        self.show_delete_dialog = False
    
    def delete_selected_items(self):
        """Elimina los productos seleccionados"""
        if not self.selected_items:
            self.show_delete_dialog = False
            return rx.toast.error(
                "❌ No hay productos seleccionados",
                position="top-right",
                duration=3000
            )
        
        print(f"🗑️  Eliminando productos: {self.selected_items}")
        result = AlmacenAPI.delete_items(self.selected_items)
        
        if result is not None:
            self.selected_items = []
            self.show_delete_dialog = False
            
            # Recargar datos usando yield
            self.loading = True
            yield
            
            data = AlmacenAPI.get_all_items()
            if data:
                for item in data:
                    if "Fecha de salida" in item:
                        item["Fecha de salida"] = item["Fecha de salida"]
                
                data.sort(key=lambda x: x.get('Numero', 0))
                self.almacen_data = data
                # Aplicar filtros actuales
                self.load_entries()
                self.calcular_estadisticas()
            
            self.loading = False
            
            return rx.toast.success(
                "✅ Productos eliminados correctamente",
                position="top-right",
                duration=3000
            )
        else:
            self.show_delete_dialog = False
            return rx.toast.error(
                "❌ Error al eliminar productos",
                position="top-right",
                duration=4000
            )
    
    # Métodos para descargar datos
    def download_csv_data(self):
        """Descarga los datos en formato CSV"""
        if not self.almacen_data:
            return rx.toast.error(
                "❌ No hay datos para descargar",
                position="top-right",
                duration=3000
            )
        
        fieldnames = ["Numero", "Codigo", "Descripcion del producto", "Tipo de producto", 
                     "UM", "Fecha de entrada", "Cantidad E", "Fecha de salida", 
                     "Cantidad S", "Saldo", "Precio", "Importe"]
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in self.almacen_data:
            row = {}
            for field in fieldnames:
                row[field] = item.get(field, "")
            writer.writerow(row)
        
        csv_data = output.getvalue()
        output.close()
        
        yield rx.toast.success(
            "Descargando archivo CSV...",
            position="top-right",
            duration=2000
        )
        
        return rx.download(
            data=csv_data,
            filename="almacen_data.csv",
        )
    
    def download_json_data(self):
        """Descarga los datos en formato JSON"""
        if not self.almacen_data:
            return rx.toast.error(
                "❌ No hay datos para descargar",
                position="top-right",
                duration=3000
            )
        
        json_data = json.dumps(self.almacen_data, indent=2, ensure_ascii=False)
        
        yield rx.toast.success(
            "Descargando archivo JSON...",
            position="top-right",
            duration=2000
        )
        
        return rx.download(
            data=json_data,
            filename="almacen_data.json",
        )
    
    # Nuevos métodos para manejar los campos adicionales
    def update_entrada_form_field(self, field_name: str, value: str):
        """Actualiza un campo específico del formulario de entrada"""
        self.entrada_form_data[field_name] = value
        print(f"Campo {field_name} actualizado a: {value}")
    
    def update_salida_form_field(self, field_name: str, value: str):
        """Actualiza un campo específico del formulario de salida"""
        self.salida_form_data[field_name] = value
        print(f"Campo {field_name} actualizado a: {value}")

    # TFuerte/state/almacen_state.py - AGREGAR NUEVO MÉTODO
    def dar_salida_para_solicitud_aprobada(self, form_data: dict):
        """Da salida para una solicitud previamente aprobada"""
        print(f"📤 Procesando salida para solicitud aprobada")
        
        if len(self.selected_items) != 1:
            return rx.toast.error(
                "❌ Selecciona exactamente un producto para dar salida",
                position="top-right",
                duration=3000
            )
        
        item_numero = self.selected_items[0]
        item = next((item for item in self.almacen_data if item.get("Numero") == item_numero), None)
        
        if not item:
            return rx.toast.error(
                "❌ No se encontró el producto",
                position="top-right",
                duration=3000
            )
        
        # 1. Buscar solicitud aprobada para este producto
        from TFuerte.api.solicitudes_api import SolicitudesAPI
        solicitudes = SolicitudesAPI.get_all_solicitudes()
        solicitud_aprobada = None
        
        for solicitud in solicitudes:
            if (solicitud.get("estado") == "aprobada" and
                solicitud.get("Descripcion", "").lower() in item.get("Descripcion del producto", "").lower()):
                solicitud_aprobada = solicitud
                break
        
        if not solicitud_aprobada:
            return rx.toast.error(
                "❌ No hay solicitudes aprobadas para este producto",
                position="top-right",
                duration=4000
            )
        
        # 2. Validar cantidad
        cantidad_solicitada = solicitud_aprobada.get("Cantidad", 0)
        cantidad_s = int(form_data["cantidad_s"]) if form_data["cantidad_s"] else 0
        
        if cantidad_s != cantidad_solicitada:
            return rx.toast.error(
                f"❌ La cantidad de salida ({cantidad_s}) debe coincidir con la cantidad solicitada ({cantidad_solicitada})",
                position="top-right",
                duration=4000
            )
        
        # 3. Validar saldo disponible
        saldo_actual = item.get("Saldo", 0) or 0
        if cantidad_s > saldo_actual:
            return rx.toast.error(
                f"❌ Cantidad de salida ({cantidad_s}) no puede ser mayor que el saldo disponible ({saldo_actual})",
                position="top-right",
                duration=4000
            )
        
        # 4. Actualizar tabla Almacen
        item_data = {
            "Fecha de salida": form_data["fecha_salida"],
            "Cantidad S": cantidad_s,
            "Precio": float(form_data.get("precio", item.get("Precio", 0))),
            "Fecha de entrada": None,
            "Cantidad E": 0,
        }
        
        print(f"📦 Datos para actualizar salida en Almacen: {item_data}")
        result = AlmacenAPI.update_item(item_numero, item_data)
        
        if not result:
            return rx.toast.error(
                "❌ Error al actualizar salida en Almacen",
                position="top-right",
                duration=4000
            )
        
        # 5. Registrar en tabla RegistroTF
        registro_data = {
            "Producto": item.get("Descripcion del producto", ""),
            "Fecha E": None,
            "Cant E": 0,
            "Fecha S": form_data["fecha_salida"],
            "Cant S": cantidad_s,
            "Recibe": form_data["recibe"],
            "Destino": form_data["destino"],
            "Cliente": form_data["cliente"],
        }
        
        from TFuerte.api.registrotf_api import RegistroTFAPI
        registro_result = RegistroTFAPI.insert_registro(registro_data)
        
        if not registro_result:
            print("⚠️  No se pudo insertar en RegistroTF")
        
        # 6. Actualizar estado de la solicitud a "completada"
        SolicitudesAPI.completar_solicitud(solicitud_aprobada["id"])
        
        # 7. Limpiar y recargar
        self.selected_items = []
        self.editing_item_numero = 0
        
        # Recargar datos
        self.loading = True
        yield
        
        data = AlmacenAPI.get_all_items()
        if data:
            for item in data:
                if "Fecha de salida" in item:
                    item["Fecha de salida"] = item["Fecha de salida"]
            
            data.sort(key=lambda x: x.get('Numero', 0))
            self.almacen_data = data
            self.load_entries()
            self.calcular_estadisticas()
        
        self.loading = False
        
        return rx.toast.success(
            "✅ Salida realizada correctamente para solicitud aprobada",
            position="top-right",
            duration=3000
        )

    def tiene_solicitudes_aprobadas(self) -> bool:
        """Verifica si el producto seleccionado tiene solicitudes aprobadas"""
        if len(self.selected_items) != 1:
            return False
        
        item_numero = self.selected_items[0]
        producto = next((item for item in self.almacen_data if item.get("Numero") == item_numero), None)
        
        if not producto:
            return False
        
        # Buscar en solicitudes
        from TFuerte.api.solicitudes_api import SolicitudesAPI
        solicitudes = SolicitudesAPI.get_all_solicitudes()
        
        for solicitud in solicitudes:
            if (solicitud.get("estado") == "aprobada" and
                solicitud.get("Descripcion", "").lower() in producto.get("Descripcion del producto", "").lower()):
                return True
        
        return False
    
    # TFuerte/state/almacen_state.py - AGREGAR ESTE MÉTODO
    @rx.var
    def producto_tiene_solicitudes_aprobadas(self) -> bool:
        """Variable computada que verifica si el producto seleccionado tiene solicitudes aprobadas"""
        if len(self.selected_items) != 1:
            return False
        
        # Obtener el producto seleccionado
        item_numero = self.selected_items[0]
        producto = None
        
        for item in self.almacen_data:
            if item.get("Numero") == item_numero:
                producto = item
                break
        
        if not producto:
            return False
        
        # Obtener descripción del producto
        descripcion = producto.get("Descripcion del producto", "").lower()
        
        # Obtener solicitudes aprobadas
        from TFuerte.api.solicitudes_api import SolicitudesAPI
        try:
            solicitudes = SolicitudesAPI.get_all_solicitudes()
            for solicitud in solicitudes:
                if (solicitud.get("estado") == "aprobada" and 
                    solicitud.get("Descripcion", "").lower() in descripcion):
                    return True
        except Exception as e:
            print(f"Error verificando solicitudes aprobadas: {e}")
        
        return False
    
    # TFuerte/state/almacen_state.py - AGREGAR ESTOS MÉTODOS
def open_salida_dialog(self):
    """Abre el diálogo para dar salida a un producto con solicitud aprobada"""
    # Verificar que haya un producto seleccionado
    if len(self.selected_items) != 1:
        return rx.toast.error(
            "❌ Selecciona exactamente un producto para dar salida",
            position="top-right",
            duration=3000
        )
    
    # Verificar que el producto tenga solicitudes aprobadas
    if not self.producto_tiene_solicitudes_aprobadas:
        return rx.toast.error(
            "❌ El producto seleccionado no tiene solicitudes aprobadas",
            position="top-right",
            duration=3000
        )
    
    item_numero = self.selected_items[0]
    item = next((item for item in self.almacen_data if item.get("Numero") == item_numero), None)
    
    if item:
        self.editing_item_numero = item_numero
        self.operation_type = "salida"
        self.edit_form_data = {
            "codigo": item.get("Codigo", ""),
            "descripcion": item.get("Descripcion del producto", ""),
            "fecha_salida": item.get("Fecha de salida", "") or "",
            "cantidad_s": str(item.get("Cantidad S", 0)),
            "precio": str(item.get("Precio", 0))
        }
        # Inicializar datos adicionales para RegistroTF
        self.salida_form_data = {
            "recibe": "",
            "destino": "",
            "cliente": ""
        }
        self.show_salida_dialog = True
        print(f"📝 Datos para salida: {self.edit_form_data}")
    else:
        return rx.toast.error(
            "❌ No se encontró el producto",
            position="top-right",
            duration=3000
        )

def dar_salida_para_solicitud_aprobada(self, form_data: dict):
    """Da salida para una solicitud previamente aprobada"""
    print(f"📤 Procesando salida para solicitud aprobada")
    
    if len(self.selected_items) != 1:
        return rx.toast.error(
            "❌ Selecciona exactamente un producto para dar salida",
            position="top-right",
            duration=3000
        )
    
    item_numero = self.selected_items[0]
    item = next((item for item in self.almacen_data if item.get("Numero") == item_numero), None)
    
    if not item:
        return rx.toast.error(
            "❌ No se encontró el producto",
            position="top-right",
            duration=3000
        )
    
    # 1. Buscar solicitud aprobada para este producto
    from TFuerte.api.solicitudes_api import SolicitudesAPI
    solicitudes = SolicitudesAPI.get_all_solicitudes()
    solicitud_aprobada = None
    
    for solicitud in solicitudes:
        if (solicitud.get("estado") == "aprobada" and
            solicitud.get("Descripcion", "").lower() in item.get("Descripcion del producto", "").lower()):
            solicitud_aprobada = solicitud
            break
    
    if not solicitud_aprobada:
        return rx.toast.error(
            "❌ No hay solicitudes aprobadas para este producto",
            position="top-right",
            duration=4000
        )
    
    # 2. Validar cantidad
    cantidad_solicitada = solicitud_aprobada.get("Cantidad", 0)
    cantidad_s = int(form_data["cantidad_s"]) if form_data["cantidad_s"] else 0
    
    if cantidad_s != cantidad_solicitada:
        return rx.toast.error(
            f"❌ La cantidad de salida ({cantidad_s}) debe coincidir con la cantidad solicitada ({cantidad_solicitada})",
            position="top-right",
            duration=4000
        )
    
    # 3. Validar saldo disponible
    saldo_actual = item.get("Saldo", 0) or 0
    if cantidad_s > saldo_actual:
        return rx.toast.error(
            f"❌ Cantidad de salida ({cantidad_s}) no puede ser mayor que el saldo disponible ({saldo_actual})",
            position="top-right",
            duration=4000
        )
    
    # 4. Actualizar tabla Almacen
    item_data = {
        "Fecha de salida": form_data["fecha_salida"],
        "Cantidad S": cantidad_s,
        "Precio": float(form_data.get("precio", item.get("Precio", 0))),
        "Fecha de entrada": None,
        "Cantidad E": 0,
    }
    
    print(f"📦 Datos para actualizar salida en Almacen: {item_data}")
    result = AlmacenAPI.update_item(item_numero, item_data)
    
    if not result:
        return rx.toast.error(
            "❌ Error al actualizar salida en Almacen",
            position="top-right",
            duration=4000
        )
    
    # 5. Registrar en tabla RegistroTF
    registro_data = {
        "Producto": item.get("Descripcion del producto", ""),
        "Fecha E": None,
        "Cant E": 0,
        "Fecha S": form_data["fecha_salida"],
        "Cant S": cantidad_s,
        "Recibe": form_data["recibe"],
        "Destino": form_data["destino"],
        "Cliente": form_data["cliente"],
    }
    
    from TFuerte.api.registrotf_api import RegistroTFAPI
    registro_result = RegistroTFAPI.insert_registro(registro_data)
    
    if not registro_result:
        print("⚠️  No se pudo insertar en RegistroTF")
    
    # 6. Actualizar estado de la solicitud a "completada"
    SolicitudesAPI.completar_solicitud(solicitud_aprobada["id"])
    
    # 7. Limpiar y recargar
    self.selected_items = []
    self.editing_item_numero = 0
    self.edit_form_data = {}
    self.salida_form_data = {}
    self.show_salida_dialog = False
    
    # Recargar datos
    self.loading = True
    yield
    
    data = AlmacenAPI.get_all_items()
    if data:
        for item in data:
            if "Fecha de salida" in item:
                item["Fecha de salida"] = item["Fecha de salida"]
        
        data.sort(key=lambda x: x.get('Numero', 0))
        self.almacen_data = data
        self.load_entries()
        self.calcular_estadisticas()
    
    self.loading = False
    
    return rx.toast.success(
        "✅ Salida realizada correctamente para solicitud aprobada",
        position="top-right",
        duration=3000
    )

@rx.var
def producto_tiene_solicitudes_aprobadas(self) -> bool:
    """Variable computada que verifica si el producto seleccionado tiene solicitudes aprobadas"""
    # Primero verificar que haya un producto seleccionado
    if len(self.selected_items) != 1:
        return False
    
    item_numero = self.selected_items[0]
    
    # Buscar el producto en los datos
    producto = None
    for item in self.almacen_data:
        if item.get("Numero") == item_numero:
            producto = item
            break
    
    if not producto:
        return False
    
    # Buscar solicitudes aprobadas para este producto
    from TFuerte.api.solicitudes_api import SolicitudesAPI
    try:
        solicitudes = SolicitudesAPI.get_all_solicitudes()
        descripcion_producto = producto.get("Descripcion del producto", "").lower()
        
        for solicitud in solicitudes:
            if (solicitud.get("estado") == "aprobada" and 
                solicitud.get("Descripcion", "").lower() in descripcion_producto):
                return True
    except Exception as e:
        print(f"Error verificando solicitudes aprobadas: {e}")
    
    return False

def open_salida_dialog(self):
    """Abre el diálogo para dar salida a un producto con solicitud aprobada"""
    # Verificar que haya un producto seleccionado
    if len(self.selected_items) != 1:
        return rx.toast.error(
            "❌ Selecciona exactamente un producto para dar salida",
            position="top-right",
            duration=3000
        )
    
    # Verificar que el producto tenga solicitudes aprobadas
    # Usamos la variable computada
    if not self.producto_tiene_solicitudes_aprobadas:
        return rx.toast.error(
            "❌ El producto seleccionado no tiene solicitudes aprobadas",
            position="top-right",
            duration=3000
        )
    
    item_numero = self.selected_items[0]
    item = next((item for item in self.almacen_data if item.get("Numero") == item_numero), None)
    
    if item:
        self.editing_item_numero = item_numero
        self.operation_type = "salida"
        self.edit_form_data = {
            "codigo": item.get("Codigo", ""),
            "descripcion": item.get("Descripcion del producto", ""),
            "fecha_salida": item.get("Fecha de salida", "") or "",
            "cantidad_s": str(item.get("Cantidad S", 0)),
            "precio": str(item.get("Precio", 0))
        }
        # Inicializar datos adicionales para RegistroTF
        self.salida_form_data = {
            "recibe": "",
            "destino": "",
            "cliente": ""
        }
        self.show_salida_dialog = True
        print(f"📝 Datos para salida: {self.edit_form_data}")
    else:
        return rx.toast.error(
            "❌ No se encontró el producto",
            position="top-right",
            duration=3000
        )

def dar_salida_para_solicitud_aprobada(self, form_data: dict):
    """Da salida para una solicitud previamente aprobada"""
    print(f"📤 Procesando salida para solicitud aprobada")
    
    if len(self.selected_items) != 1:
        return rx.toast.error(
            "❌ Selecciona exactamente un producto para dar salida",
            position="top-right",
            duration=3000
        )
    
    item_numero = self.selected_items[0]
    item = next((item for item in self.almacen_data if item.get("Numero") == item_numero), None)
    
    if not item:
        return rx.toast.error(
            "❌ No se encontró el producto",
            position="top-right",
            duration=3000
        )
    
    # 1. Buscar solicitud aprobada para este producto
    from TFuerte.api.solicitudes_api import SolicitudesAPI
    solicitudes = SolicitudesAPI.get_all_solicitudes()
    solicitud_aprobada = None
    
    descripcion_producto = item.get("Descripcion del producto", "").lower()
    for solicitud in solicitudes:
        if (solicitud.get("estado") == "aprobada" and
            solicitud.get("Descripcion", "").lower() in descripcion_producto):
            solicitud_aprobada = solicitud
            break
    
    if not solicitud_aprobada:
        return rx.toast.error(
            "❌ No hay solicitudes aprobadas para este producto",
            position="top-right",
            duration=4000
        )
    
    # 2. Validar cantidad
    cantidad_solicitada = solicitud_aprobada.get("Cantidad", 0)
    cantidad_s = int(form_data["cantidad_s"]) if form_data["cantidad_s"] else 0
    
    if cantidad_s != cantidad_solicitada:
        return rx.toast.error(
            f"❌ La cantidad de salida ({cantidad_s}) debe coincidir con la cantidad solicitada ({cantidad_solicitada})",
            position="top-right",
            duration=4000
        )
    
    # 3. Validar saldo disponible
    saldo_actual = item.get("Saldo", 0) or 0
    if cantidad_s > saldo_actual:
        return rx.toast.error(
            f"❌ Cantidad de salida ({cantidad_s}) no puede ser mayor que el saldo disponible ({saldo_actual})",
            position="top-right",
            duration=4000
        )
    
    # 4. Actualizar tabla Almacen
    item_data = {
        "Fecha de salida": form_data["fecha_salida"],
        "Cantidad S": cantidad_s,
        "Precio": float(form_data.get("precio", item.get("Precio", 0))),
        "Fecha de entrada": None,
        "Cantidad E": 0,
    }
    
    print(f"📦 Datos para actualizar salida en Almacen: {item_data}")
    result = AlmacenAPI.update_item(item_numero, item_data)
    
    if not result:
        return rx.toast.error(
            "❌ Error al actualizar salida en Almacen",
            position="top-right",
            duration=4000
        )
    
    # 5. Registrar en tabla RegistroTF
    registro_data = {
        "Producto": item.get("Descripcion del producto", ""),
        "Fecha E": None,
        "Cant E": 0,
        "Fecha S": form_data["fecha_salida"],
        "Cant S": cantidad_s,
        "Recibe": form_data["recibe"],
        "Destino": form_data["destino"],
        "Cliente": form_data["cliente"],
    }
    
    from TFuerte.api.registrotf_api import RegistroTFAPI
    registro_result = RegistroTFAPI.insert_registro(registro_data)
    
    if not registro_result:
        print("⚠️  No se pudo insertar en RegistroTF")
    
    # 6. Actualizar estado de la solicitud a "completada"
    SolicitudesAPI.completar_solicitud(solicitud_aprobada["id"])
    
    # 7. Limpiar y recargar
    self.selected_items = []
    self.editing_item_numero = 0
    self.edit_form_data = {}
    self.salida_form_data = {}
    self.show_salida_dialog = False
    
    # Recargar datos
    self.loading = True
    yield
    
    data = AlmacenAPI.get_all_items()
    if data:
        for item in data:
            if "Fecha de salida" in item:
                item["Fecha de salida"] = item["Fecha de salida"]
        
        data.sort(key=lambda x: x.get('Numero', 0))
        self.almacen_data = data
        self.load_entries()
        self.calcular_estadisticas()
    
    self.loading = False
    
    return rx.toast.success(
        "✅ Salida realizada correctamente para solicitud aprobada",
        position="top-right",
        duration=3000
    )

def set_show_salida_dialog(self, show: bool):
    """Setter para show_salida_dialog"""
    self.show_salida_dialog = show

def close_salida_dialog(self):
    """Cierra el diálogo de salida"""
    self.show_salida_dialog = False
    self.edit_form_data = {}
    self.salida_form_data = {}