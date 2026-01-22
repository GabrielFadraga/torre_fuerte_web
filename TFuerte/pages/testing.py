import reflex as rx
import csv
import io
import json
from typing import List
from TFuerte.api.SupabaseAPI import get_test_data, insert_test_data, update_test_data, delete_test_data
from TFuerte.routes import Route
import TFuerte.styles.styles as styles
from datetime import datetime


class TestingState(rx.State):
    """Estado que maneja los datos de Supabase para la tabla"""
    
    # Variable donde se almacenan los datos
    table_data: List[dict] = []
    
    # Variable para controlar la carga
    loading: bool = False
    
    # Variable para almacenar el tamaño de los datos
    data_size_kb: float = 0.0
    
    # Variables para selección y edición
    selected_users: List[int] = []  # IDs de usuarios seleccionados
    editing_user_id: int = 0  # ID del usuario que se está editando
    edit_form_data: dict = {}  # Datos del formulario de edición
    show_delete_dialog: bool = False  # Controlar visibilidad del diálogo de eliminación
    
    def load_data(self):
        """Carga los datos desde Supabase y los guarda en el estado"""
        self.loading = True
        yield  # Yield para permitir que la UI se actualice
        
        # Obtener datos usando tu función existente
        data = get_test_data()
        
        if data:
            # Asegurar que todos los números de teléfono sean strings
            for item in data:
                if "phone" in item and item["phone"] is not None:
                    item["phone"] = str(item["phone"])
            
            # ORDENAR POR ID DE MANERA ASCENDENTE
            data.sort(key=lambda x: x.get('id', 0))
            
            self.table_data = data
            # Calcular tamaño de los datos
            self.calculate_data_size()
            print(f"✅ Datos cargados en el estado: {len(data)} registros")
            
            # Mostrar toast informativo
            yield rx.toast.info(
                f"Datos cargados: {len(data)} registros",
                position="top-right",
                duration=3000
            )
        else:
            print("⚠️  No se obtuvieron datos de Supabase")
            self.table_data = []
            self.data_size_kb = 0.0
            
            # Mostrar toast de error
            yield rx.toast.error(
                "No se pudieron cargar los datos",
                position="top-right",
                duration=3000
            )
        
        self.loading = False
    
    def calculate_data_size(self):
        """Calcula el tamaño de los datos en KB"""
        if not self.table_data:
            self.data_size_kb = 0.0
            return
        
        # Calcular tamaño aproximado
        total_chars = 0
        for item in self.table_data:
            # Sumar longitud de todos los valores como strings
            for value in item.values():
                total_chars += len(str(value))
        
        # Convertir a KB (aproximado)
        self.data_size_kb = total_chars / 1024
    
    def _convert_to_csv(self) -> str:
        """Convierte los datos de la tabla a formato CSV"""
        
        # Asegurarse de que hay datos cargados
        if not self.table_data:
            print("⚠️  No hay datos para convertir a CSV")
            return ""
        
        # Definir los nombres de las columnas basados en las claves del primer elemento
        if self.table_data:
            fieldnames = list(self.table_data[0].keys())
        else:
            fieldnames = []
        
        # Crear un buffer en memoria para el CSV
        output = io.StringIO()
        
        # Crear el escritor CSV
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        # Escribir encabezados y datos
        writer.writeheader()
        for item in self.table_data:
            writer.writerow(item)
        
        # Obtener el string CSV
        csv_data = output.getvalue()
        output.close()
        
        print(f"✅ CSV generado: {len(csv_data)} bytes")
        return csv_data
    
    def download_csv_data(self):
        """Descarga los datos en formato CSV"""
        csv_data = self._convert_to_csv()
        
        if not csv_data:
            return rx.toast.error(
                "❌ No hay datos para descargar",
                position="top-right",
                duration=3000
            )
        
        # Mostrar toast de éxito
        yield rx.toast.success(
            "Descargando archivo CSV...",
            position="top-right",
            duration=2000
        )
        
        # Devolver la descarga
        return rx.download(
            data=csv_data,
            filename="datos_supabase.csv",
        )
    
    def download_json_data(self):
        """Descarga los datos en formato JSON"""
        if not self.table_data:
            return rx.toast.error(
                "❌ No hay datos para descargar",
                position="top-right",
                duration=3000
            )
        
        # Convertir a JSON formateado
        json_data = json.dumps(self.table_data, indent=2, ensure_ascii=False)
        
        # Mostrar toast de éxito
        yield rx.toast.success(
            "Descargando archivo JSON...",
            position="top-right",
            duration=2000
        )
        
        # Devolver la descarga
        return rx.download(
            data=json_data,
            filename="datos_supabase.json",
        )
    
    def show_download_info(self):
        """Muestra información sobre las descargas"""
        return rx.toast.info(
            "📥 Los datos descargados contienen todos los campos mostrados en la tabla.",
            position="bottom-right",
            duration=4000
        )
    
    # ==============================================
    # MÉTODOS PARA SELECCIÓN DE USUARIOS
    # ==============================================
    
    def toggle_user_selection(self, user_id: int):
        """Alterna la selección de un usuario"""
        # Convertir la lista de selected_users a una lista de Python
        current = list(self.selected_users)
        if user_id in current:
            current.remove(user_id)
        else:
            current.append(user_id)
        self.selected_users = current
        print(f"Usuarios seleccionados: {self.selected_users}")
    
    def clear_selection(self):
        """Limpia la selección de usuarios"""
        self.selected_users = []
    
    # ==============================================
    # MÉTODOS PARA AGREGAR USUARIOS
    # ==============================================
    
    def add_user_to_db(self, form_data: dict):
        """Agrega un nuevo usuario a la base de datos"""
        print(f"📤 Recibiendo datos del formulario: {form_data}")
        
        # Validar campos requeridos
        required_fields = ["name", "surname", "email", "phone"]
        missing_fields = [field for field in required_fields if field not in form_data or not form_data[field]]
        
        if missing_fields:
            return rx.toast.error(
                f"❌ Faltan campos requeridos: {', '.join(missing_fields)}",
                position="top-right",
                duration=4000
            )
        
        # Preparar datos para Supabase
        user_data = {
            "name": form_data["name"],
            "surname": form_data["surname"],
            "email": form_data["email"],
            "phone": str(form_data["phone"]),
            "init_date": form_data.get("init_date", datetime.now().strftime("%Y-%m-%d"))
        }
        
        # Insertar en Supabase
        result = insert_test_data(user_data)
        
        if result:
            # Actualizar datos localmente y mostrar mensaje
            self.loading = True
            yield
            
            # Obtener datos actualizados
            data = get_test_data()
            if data:
                for item in data:
                    if "phone" in item and item["phone"] is not None:
                        item["phone"] = str(item["phone"])
                
                # ORDENAR POR ID DESPUÉS DE AGREGAR
                data.sort(key=lambda x: x.get('id', 0))
                self.table_data = data
                self.calculate_data_size()
            
            self.loading = False
            
            return rx.toast.success(
                f"✅ Usuario {user_data['name']} agregado correctamente",
                position="top-right",
                duration=3000
            )
        else:
            return rx.toast.error(
                "❌ Error al agregar usuario. Verifica la conexión.",
                position="top-right",
                duration=4000
            )
    
    # ==============================================
    # MÉTODOS PARA EDITAR USUARIOS
    # ==============================================
    
    def open_edit_dialog(self):
        """Abre el diálogo para editar usuario"""
        if len(self.selected_users) != 1:
            return rx.toast.error(
                "❌ Por favor, selecciona exactamente un usuario para editar",
                position="top-right",
                duration=3000
            )
        
        # Obtener el usuario seleccionado
        user_id = self.selected_users[0]
        user = next((item for item in self.table_data if item["id"] == user_id), None)
        
        if user:
            self.editing_user_id = user_id
            self.edit_form_data = {
                "name": user["name"],
                "surname": user["surname"],
                "email": user["email"],
                "phone": user["phone"],
                "init_date": user["init_date"]
            }
            return rx.set_value("edit_dialog", True)
        else:
            return rx.toast.error(
                "❌ No se encontró el usuario seleccionado",
                position="top-right",
                duration=3000
            )
    
    def update_user_in_db(self, form_data: dict):
        """Actualiza un usuario en la base de datos"""
        print(f"📤 Actualizando usuario ID: {self.editing_user_id} con datos: {form_data}")
        
        # Validar campos requeridos
        required_fields = ["name", "surname", "email", "phone"]
        missing_fields = [field for field in required_fields if field not in form_data or not form_data[field]]
        
        if missing_fields:
            return rx.toast.error(
                f"❌ Faltan campos requeridos: {', '.join(missing_fields)}",
                position="top-right",
                duration=4000
            )
        
        # Preparar datos para Supabase
        user_data = {
            "name": form_data["name"],
            "surname": form_data["surname"],
            "email": form_data["email"],
            "phone": str(form_data["phone"]),
            "init_date": form_data.get("init_date", self.edit_form_data.get("init_date"))
        }
        
        # Actualizar en Supabase
        result = update_test_data(self.editing_user_id, user_data)
        
        if result:
            # Cerrar diálogo y limpiar selección
            self.selected_users = []
            self.editing_user_id = 0
            self.edit_form_data = {}
            
            # Actualizar datos localmente
            self.loading = True
            yield
            
            # Obtener datos actualizados
            data = get_test_data()
            if data:
                for item in data:
                    if "phone" in item and item["phone"] is not None:
                        item["phone"] = str(item["phone"])
                
                # ORDENAR POR ID DESPUÉS DE ACTUALIZAR
                data.sort(key=lambda x: x.get('id', 0))
                self.table_data = data
                self.calculate_data_size()
            
            self.loading = False
            
            # Mostrar mensaje de éxito
            return rx.toast.success(
                f"✅ Usuario {user_data['name']} actualizado correctamente",
                position="top-right",
                duration=3000
            )
        else:
            return rx.toast.error(
                "❌ Error al actualizar usuario. Verifica la conexión.",
                position="top-right",
                duration=4000
            )
    
    # ==============================================
    # MÉTODOS PARA ELIMINAR USUARIOS
    # ==============================================
    
    def open_delete_dialog(self):
        """Abre el diálogo de confirmación para eliminar usuarios"""
        if not self.selected_users:
            return rx.toast.error(
                "❌ No hay usuarios seleccionados para eliminar",
                position="top-right",
                duration=3000
            )
        
        self.show_delete_dialog = True
    
    def close_delete_dialog(self):
        """Cierra el diálogo de eliminación"""
        self.show_delete_dialog = False
    
    def delete_selected_users(self):
        """Elimina los usuarios seleccionados de la base de datos"""
        if not self.selected_users:
            self.show_delete_dialog = False
            return rx.toast.error(
                "❌ No hay usuarios seleccionados para eliminar",
                position="top-right",
                duration=3000
            )
        
        print(f"🗑️  Eliminando usuarios: {self.selected_users}")
        
        # Eliminar en Supabase
        result = delete_test_data(self.selected_users)
        
        if result:
            # Cerrar diálogo y limpiar selección
            self.selected_users = []
            self.show_delete_dialog = False
            
            # Actualizar datos localmente
            self.loading = True
            yield
            
            # Obtener datos actualizados
            data = get_test_data()
            if data:
                for item in data:
                    if "phone" in item and item["phone"] is not None:
                        item["phone"] = str(item["phone"])
                
                # ORDENAR POR ID DESPUÉS DE ELIMINAR
                data.sort(key=lambda x: x.get('id', 0))
                self.table_data = data
                self.calculate_data_size()
            
            self.loading = False
            
            # Mostrar mensaje de éxito
            return rx.toast.success(
                "✅ Usuarios eliminados correctamente",
                position="top-right",
                duration=3000
            )
        else:
            self.show_delete_dialog = False
            return rx.toast.error(
                "❌ Error al eliminar usuarios. Verifica la conexión.",
                position="top-right",
                duration=4000
            )

# ==============================================
# COMPONENTE DE TABLA CON ANCHO COMPLETO
# ==============================================
def supabase_table() -> rx.Component:
    """Componente que muestra los datos de Supabase en una tabla de Reflex con ancho completo"""
    
    # Estilos para la tabla
    table_style = {
        "width": "100%",
        "min_width": "1400px",  # Ancho mínimo para todas las columnas
        "table_layout": "fixed",
        "border_collapse": "collapse",
    }
    
    header_style = {
        "background": "#4f46e5",
        "color": "white",
        "font_weight": "bold",
        "padding": "16px 12px",
        "text_align": "left",
        "border_right": "1px solid rgba(255, 255, 255, 0.2)",
    }
    
    cell_style = {
        "padding": "14px 12px",
        "border_bottom": "1px solid #e5e7eb",
        "vertical_align": "middle",
    }
    
    # Crear la tabla con estructura más flexible
    return rx.box(
        # Encabezado fijo
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell(
                        "Seleccionar",
                        style={
                            **header_style,
                            "width": "100px",
                            "min_width": "100px",
                        }
                    ),
                    rx.table.column_header_cell(
                        "ID",
                        style={
                            **header_style,
                            "width": "80px",
                            "min_width": "80px",
                        }
                    ),
                    rx.table.column_header_cell(
                        "Nombre",
                        style={
                            **header_style,
                            "width": "200px",
                            "min_width": "200px",
                        }
                    ),
                    rx.table.column_header_cell(
                        "Apellido",
                        style={
                            **header_style,
                            "width": "200px",
                            "min_width": "200px",
                        }
                    ),
                    rx.table.column_header_cell(
                        "Email",
                        style={
                            **header_style,
                            "width": "300px",
                            "min_width": "300px",
                        }
                    ),
                    rx.table.column_header_cell(
                        "Teléfono",
                        style={
                            **header_style,
                            "width": "180px",
                            "min_width": "180px",
                        }
                    ),
                    rx.table.column_header_cell(
                        "Fecha de Inicio",
                        style={
                            **header_style,
                            "width": "150px",
                            "min_width": "150px",
                        }
                    ),
                )
            ),
            style=table_style,
        ),
        
        # Cuerpo de la tabla con scroll
        rx.scroll_area(
            rx.table.root(
                rx.table.body(
                    rx.foreach(
                        TestingState.table_data,
                        lambda item: rx.table.row(
                            # Checkbox para selección
                            rx.table.cell(
                                rx.checkbox(
                                    checked=TestingState.selected_users.contains(item["id"]),
                                    on_change=lambda checked, item_id=item["id"]: TestingState.toggle_user_selection(item_id)
                                ),
                                style={
                                    **cell_style,
                                    "width": "100px",
                                    "min_width": "100px",
                                    "text_align": "center",
                                }
                            ),
                            rx.table.cell(
                                rx.badge(
                                    item["id"],
                                    variant="solid",
                                    color_scheme="blue",
                                    style={
                                        "background": "#4f46e5",
                                        "color": "white",
                                        "padding": "6px 12px",
                                        "border_radius": "12px",
                                        "font_weight": "bold",
                                    }
                                ),
                                style={
                                    **cell_style,
                                    "width": "80px",
                                    "min_width": "80px",
                                }
                            ),
                            rx.table.cell(
                                rx.text(
                                    item["name"],
                                    style={
                                        "font_weight": "500",
                                        "color": "#1f2937",
                                    }
                                ),
                                style={
                                    **cell_style,
                                    "width": "200px",
                                    "min_width": "200px",
                                }
                            ),
                            rx.table.cell(
                                rx.text(
                                    item["surname"],
                                    style={
                                        "font_weight": "500",
                                        "color": "#1f2937",
                                    }
                                ),
                                style={
                                    **cell_style,
                                    "width": "200px",
                                    "min_width": "200px",
                                }
                            ),
                            rx.table.cell(
                                rx.link(
                                    item["email"],
                                    href=f"mailto:{item['email']}",
                                    style={
                                        "color": "#2563eb",
                                        "text_decoration": "none",
                                        "font_weight": "500",
                                    },
                                    _hover={
                                        "text_decoration": "underline",
                                    }
                                ),
                                style={
                                    **cell_style,
                                    "width": "300px",
                                    "min_width": "300px",
                                }
                            ),
                            rx.table.cell(
                                rx.text(
                                    item["phone"],
                                    style={
                                        "color": "#6b7280",
                                        "font_family": "monospace",
                                    }
                                ),
                                style={
                                    **cell_style,
                                    "width": "180px",
                                    "min_width": "180px",
                                }
                            ),
                            rx.table.cell(
                                rx.badge(
                                    item["init_date"],
                                    variant="outline",
                                    style={
                                        "color": "#059669",
                                        "border_color": "#10b981",
                                        "background": "#f0fdf4",
                                        "padding": "6px 12px",
                                        "border_radius": "6px",
                                    }
                                ),
                                style={
                                    **cell_style,
                                    "width": "150px",
                                    "min_width": "150px",
                                }
                            ),
                            _hover={
                                "background_color": "#f9fafb",
                            },
                        )
                    )
                ),
                style=table_style,
            ),
            type="always",
            scrollbars="horizontal",
            style={
                "width": "100%",
                "height": "600px",  # Altura fija para scroll vertical
                "overflow_y": "auto",  # Scroll vertical automático
                "border": "1px solid #e5e7eb",
                "border_radius": "8px",
            }
        ),
        width="100%",
    )

# ==============================================
# DIÁLOGO PARA AGREGAR USUARIO
# ==============================================
def add_user_dialog() -> rx.Component:
    """Componente de diálogo para agregar nuevo usuario"""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "➕ Agregar Usuario",
                variant="solid",
                color_scheme="green",
                size="2",
            ),
        ),
        rx.dialog.content(
            rx.dialog.title("Agregar Nuevo Usuario"),
            rx.dialog.description(
                "Completa el formulario para agregar un nuevo usuario a la base de datos.",
            ),
            rx.form(
                rx.vstack(
                    rx.input(
                        placeholder="Nombre *",
                        name="name",
                        required=True,
                        size="3",
                        margin_bottom="1rem",
                    ),
                    rx.input(
                        placeholder="Apellido *",
                        name="surname",
                        required=True,
                        size="3",
                        margin_bottom="1rem",
                    ),
                    rx.input(
                        placeholder="Email *",
                        name="email",
                        type="email",
                        required=True,
                        size="3",
                        margin_bottom="1rem",
                    ),
                    rx.input(
                        placeholder="Teléfono *",
                        name="phone",
                        type="tel",
                        required=True,
                        size="3",
                        margin_bottom="1rem",
                    ),
                    rx.input(
                        placeholder="Fecha de inicio (YYYY-MM-DD)",
                        name="init_date",
                        type="date",
                        size="3",
                        margin_bottom="2rem",
                    ),
                    rx.hstack(
                        rx.dialog.close(
                            rx.button(
                                "Cancelar",
                                variant="soft",
                                color_scheme="gray",
                                size="2",
                            ),
                        ),
                        rx.button(
                            "Agregar Usuario",
                            type="submit",
                            variant="solid",
                            color_scheme="green",
                            size="2",
                        ),
                        spacing="3",
                        justify="end",
                        width="100%",
                    ),
                    spacing="1",
                ),
                on_submit=TestingState.add_user_to_db,
                reset_on_submit=True,
            ),
            max_width="500px",
        ),
    )

# ==============================================
# DIÁLOGO PARA EDITAR USUARIO
# ==============================================
def edit_user_dialog() -> rx.Component:
    """Componente de diálogo para editar usuario existente"""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "✏️ Editar Usuario",
                on_click=TestingState.open_edit_dialog,
                variant="solid",
                color_scheme="amber",
                size="2",
                is_disabled=TestingState.selected_users.length() != 1,
            ),
        ),
        rx.dialog.content(
            rx.dialog.title("Editar Usuario"),
            rx.dialog.description(
                "Modifica los datos del usuario seleccionado.",
            ),
            rx.form(
                rx.vstack(
                    rx.input(
                        placeholder="Nombre *",
                        name="name",
                        default_value=rx.cond(
                            TestingState.edit_form_data,
                            TestingState.edit_form_data.get("name", ""),
                            ""
                        ),
                        required=True,
                        size="3",
                        margin_bottom="1rem",
                    ),
                    rx.input(
                        placeholder="Apellido *",
                        name="surname",
                        default_value=rx.cond(
                            TestingState.edit_form_data,
                            TestingState.edit_form_data.get("surname", ""),
                            ""
                        ),
                        required=True,
                        size="3",
                        margin_bottom="1rem",
                    ),
                    rx.input(
                        placeholder="Email *",
                        name="email",
                        type="email",
                        default_value=rx.cond(
                            TestingState.edit_form_data,
                            TestingState.edit_form_data.get("email", ""),
                            ""
                        ),
                        required=True,
                        size="3",
                        margin_bottom="1rem",
                    ),
                    rx.input(
                        placeholder="Teléfono *",
                        name="phone",
                        type="tel",
                        default_value=rx.cond(
                            TestingState.edit_form_data,
                            TestingState.edit_form_data.get("phone", ""),
                            ""
                        ),
                        required=True,
                        size="3",
                        margin_bottom="1rem",
                    ),
                    rx.input(
                        placeholder="Fecha de inicio (YYYY-MM-DD)",
                        name="init_date",
                        type="date",
                        default_value=rx.cond(
                            TestingState.edit_form_data,
                            TestingState.edit_form_data.get("init_date", ""),
                            ""
                        ),
                        size="3",
                        margin_bottom="2rem",
                    ),
                    rx.hstack(
                        rx.dialog.close(
                            rx.button(
                                "Cancelar",
                                variant="soft",
                                color_scheme="gray",
                                size="2",
                            ),
                        ),
                        rx.button(
                            "Actualizar Usuario",
                            type="submit",
                            variant="solid",
                            color_scheme="amber",
                            size="2",
                        ),
                        spacing="3",
                        justify="end",
                        width="100%",
                    ),
                    spacing="1",
                ),
                on_submit=TestingState.update_user_in_db,
                reset_on_submit=False,
            ),
            max_width="500px",
        ),
    )

# ==============================================
# DIÁLOGO PARA CONFIRMAR ELIMINACIÓN
# ==============================================
def delete_confirm_dialog() -> rx.Component:
    """Componente de diálogo para confirmar eliminación de usuarios"""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "🗑️ Eliminar Usuarios",
                on_click=TestingState.open_delete_dialog,
                variant="solid",
                color_scheme="red",
                size="2",
                is_disabled=TestingState.selected_users.length() == 0,
            ),
        ),
        rx.cond(
            TestingState.show_delete_dialog,
            rx.dialog.content(
                rx.dialog.title("Confirmar Eliminación"),
                rx.dialog.description(
                    rx.cond(
                        TestingState.selected_users.length() == 1,
                        "¿Estás seguro de que deseas eliminar el usuario seleccionado? Esta acción no se puede deshacer.",
                        f"¿Estás seguro de que deseas eliminar los {TestingState.selected_users.length()} usuarios seleccionados? Esta acción no se puede deshacer.",
                    )
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            on_click=TestingState.close_delete_dialog,
                            variant="soft",
                            color_scheme="gray",
                            size="2",
                        ),
                    ),
                    rx.button(
                        "Eliminar",
                        on_click=TestingState.delete_selected_users,
                        variant="solid",
                        color_scheme="red",
                        size="2",
                    ),
                    spacing="3",
                    justify="end",
                ),
                max_width="500px",
            ),
        ),
    )

# ==============================================
# PÁGINA PRINCIPAL CON ANCHO COMPLETO
# ==============================================
@rx.page(
    route=Route.TESTING.value,
    title="Tabla de Datos - Torre Fuerte",
    description="Visualización de datos desde Supabase",
    on_load=TestingState.load_data
)
def testing() -> rx.Component:
    """Página principal que muestra la tabla de datos"""
    
    return rx.box(
        rx.vstack(
            # TÍTULO Y DESCRIPCIÓN
            rx.heading(
                "📊 Datos de la Base de Datos",
                size="8",
                margin_bottom="1rem",
                color="#333333",
                width="100%",
            ),
            
            rx.text(
                "Esta tabla muestra información almacenada en Supabase. Puedes descargar los datos en diferentes formatos.",
                size="4",
                color="#333333",
                margin_bottom="2rem",
                width="100%",
            ),
            
            # PANEL DE BOTONES
            rx.box(
                rx.hstack(
                    # Botón para recargar datos
                    rx.button(
                        "🔄 Actualizar Datos",
                        on_click=TestingState.load_data,
                        loading=TestingState.loading,
                        variant="solid",
                        color_scheme="cyan",
                        size="2",
                    ),
                    
                    # Botón para descargar CSV
                    rx.button(
                        "📥 Descargar CSV",
                        on_click=TestingState.download_csv_data,
                        variant="solid",
                        color_scheme="cyan",
                        size="2",
                    ),
                    
                    # Botón para descargar JSON
                    rx.button(
                        "📥 Descargar JSON",
                        on_click=TestingState.download_json_data,
                        variant="solid",
                        color_scheme="cyan",
                        size="2",
                    ),
                    
                    # Botón para mostrar información sobre descargas
                    rx.button(
                        "💡 Info Descargas",
                        on_click=TestingState.show_download_info,
                        variant="solid",
                        color_scheme="cyan",
                        size="2"
                    ),
                    
                    # BOTONES CONDICIONALES
                    rx.cond(
                        TestingState.selected_users.length() > 0,
                        rx.hstack(
                            # Botón para limpiar selección
                            rx.button(
                                "🗑️ Limpiar Selección",
                                on_click=TestingState.clear_selection,
                                variant="solid",
                                color_scheme="amber",
                                size="2",
                            ),
                            
                            # Botón para editar usuario
                            rx.cond(
                                TestingState.selected_users.length() == 1,
                                edit_user_dialog(),
                            ),
                            
                            # Botón para eliminar usuarios
                            delete_confirm_dialog(),
                            
                            spacing="2",
                        ),
                    ),
                    
                    # Diálogo para agregar usuario
                    add_user_dialog(),
                    
                    spacing="3",
                    wrap="wrap",
                    gap="2",
                ),
                width="100%",
                margin_bottom="2rem",
            ),
            
            # CONTENIDO CONDICIONAL
            rx.cond(
                TestingState.loading,
                # Mientras carga
                rx.center(
                    rx.vstack(
                        rx.spinner(size="3"),
                        rx.text("Cargando datos...", margin_top="1rem", color="#333333"),
                        spacing="2",
                    ),
                    height="200px",
                    width="100%",
                ),
                # Cuando terminó de cargar
                rx.cond(
                    TestingState.table_data.length() > 0,
                    # Si hay datos
                    rx.vstack(
                        # Estadísticas
                        rx.box(
                            rx.hstack(
                                rx.badge(
                                    f"📊 Total: {TestingState.table_data.length()} registros",
                                    variant="solid",
                                    color_scheme="green"
                                ),
                                rx.badge(
                                    f"📁 Tamaño: {TestingState.data_size_kb:.1f} KB",
                                    variant="outline"
                                ),
                                rx.badge(
                                    f"👥 Seleccionados: {TestingState.selected_users.length()}",
                                    variant="soft",
                                    color_scheme="blue"
                                ),
                                spacing="3",
                                justify="end",
                            ),
                            width="100%",
                            margin_bottom="1rem",
                        ),
                        
                        # La tabla CON ANCHO COMPLETO
                        rx.box(
                            supabase_table(),
                            width="100%",
                            overflow="hidden",
                        ),
                        
                        # Información sobre funcionalidades
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("info", size=16, color="blue.500", margin_right="0.5rem"),
                                    rx.text("💡 Instrucciones de uso:", weight="bold", size="2", color="#333333"),
                                    spacing="2",
                                ),
                                rx.text(
                                    "1. Usa el botón '➕ Agregar Usuario' para añadir nuevos registros.",
                                    size="2",
                                    color="#333333",
                                ),
                                rx.text(
                                    "2. Selecciona usuarios con los checkboxes para editarlos o eliminarlos.",
                                    size="2",
                                    color="#333333",
                                ),
                                rx.text(
                                    "3. Los botones de '✏️ Editar Usuario' y '🗑️ Eliminar Usuarios' aparecerán cuando haya al menos un usuario seleccionado.",
                                    size="2",
                                    color="#333333",
                                ),
                                rx.text(
                                    "4. Para editar, selecciona exactamente UN usuario. Para eliminar, puedes seleccionar varios.",
                                    size="2",
                                    color="#333333",
                                ),
                                rx.text(
                                    "5. Usa '🗑️ Limpiar Selección' para deseleccionar todos los usuarios.",
                                    size="2",
                                    color="#333333",
                                ),
                                rx.text(
                                    "6. Usa la barra de scroll HORIZONTAL para ver todas las columnas de la tabla.",
                                    size="2",
                                    color="#333333",
                                    weight="medium",
                                ),
                                rx.text(
                                    "7. Usa la barra de scroll VERTICAL para ver más filas de la tabla.",
                                    size="2",
                                    color="#333333",
                                    weight="medium",
                                ),
                                rx.text(
                                    "8. Los usuarios están ordenados por ID de manera ascendente.",
                                    size="2",
                                    color="#333333",
                                    weight="medium",
                                ),
                            ),
                            width="100%",
                            padding="1.5rem",
                            border_radius="md",
                            background="blue.50",
                            margin_top="1rem",
                        ),
                        
                        width="100%",
                    ),
                    # Si no hay datos
                    rx.center(
                        rx.vstack(
                            rx.icon("database", size=32, color="gray.400"),
                            rx.text("No hay datos para mostrar", size="4", color="#333333",),
                            rx.hstack(
                                rx.button(
                                    "🔄 Intentar nuevamente",
                                    on_click=TestingState.load_data,
                                    size="2",
                                    margin_top="1rem"
                                ),
                                add_user_dialog(),
                                spacing="2",
                            ),
                            spacing="3",
                        ),
                        height="200px",
                        width="100%",
                    )
                )
            ),
            spacing="4",
            align="start",
            padding="2rem",
            width="100%",
        ),
        width="100%",
        style={
            "background": "linear-gradient(135deg, #f5f7ff 0%, #f0f2ff 100%)",
            "min_height": "100vh",
        }
    )