import reflex as rx
from typing import List
from TFuerte.api.almacen_api import AlmacenAPI

class AlmacenViewState(rx.State):
    """Estado para vista de solo lectura de Almacén"""
    
    # Datos del almacén
    almacen_data: List[dict] = []
    filtered_data: List[dict] = []
    
    # Estados de UI
    loading: bool = False
    search_value: str = ""
    sort_value: str = ""
    
    # Estadísticas
    total_productos: int = 0
    valor_total: float = 0.0

    # ==================================================
    # PAGINACIÓN
    # ==================================================
    almacen_paginated: List[dict] = []
    current_page: int = 1
    items_per_page: int = 10
    total_pages: int = 1
    page_numbers: List[int] = []
    
    def load_data(self):
        """Carga los datos desde Supabase en modo solo lectura"""
        self.loading = True
        yield
        
        data = AlmacenAPI.get_all_items()
        
        if data:
            # Normalizar datos
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
            self.filtered_data = data
            self.calcular_estadisticas()
            self.reset_pagination()
            print(f"✅ Datos cargados (solo lectura): {len(data)} registros")
        else:
            self.almacen_data = []
            self.filtered_data = []
            self.total_productos = 0
            self.valor_total = 0.0
            self.reset_pagination()
        
        self.loading = False
    
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
    
    def filter_values(self, search_value: str):
        """Filtra los datos por descripción"""
        self.search_value = search_value
        self.current_page = 1  # Resetear a primera página al filtrar
        
        if not search_value:
            self.filtered_data = self.almacen_data
        else:
            search_term = search_value.lower()
            filtered = []
            for item in self.almacen_data:
                if search_term in item.get("Descripcion del producto", "").lower():
                    filtered.append(item)
            self.filtered_data = filtered
        
        self.calcular_estadisticas()
        self.calculate_pagination()
    
    def sort_values(self, sort_value: str):
        """Ordena los datos por la columna especificada"""
        self.sort_value = sort_value
        self.current_page = 1  # Resetear a primera página al ordenar
        
        if not sort_value:
            return
        
        # Ordenar los datos
        self.filtered_data = sorted(self.filtered_data, key=lambda x: x.get(sort_value, ""))
        self.calculate_pagination()

    # ==================================================
    # MÉTODOS DE PAGINACIÓN
    # ==================================================

    def calculate_pagination(self):
        total_items = len(self.filtered_data)

        if total_items == 0:
            self.total_pages = 1
            self.almacen_paginated = []
        else:
            self.total_pages = max(1, (total_items + self.items_per_page - 1) // self.items_per_page)

        if self.current_page > self.total_pages:
            self.current_page = max(1, self.total_pages)

        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, total_items)

        if total_items > 0:
            self.almacen_paginated = self.filtered_data[start_idx:end_idx]
        else:
            self.almacen_paginated = []

        self.calculate_page_numbers()

    def calculate_page_numbers(self):
        max_pages_to_show = 4
        current = self.current_page
        total = self.total_pages

        if total <= max_pages_to_show:
            self.page_numbers = list(range(1, total + 1))
            return

        start = max(1, current - 1)
        end = min(total, start + max_pages_to_show - 1)

        if end - start + 1 < max_pages_to_show:
            start = max(1, end - max_pages_to_show + 1)

        self.page_numbers = list(range(start, end + 1))

    def go_to_page(self, page_number: int):
        if 1 <= page_number <= self.total_pages:
            self.current_page = page_number
            self.calculate_pagination()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.calculate_pagination()

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.calculate_pagination()

    def reset_pagination(self):
        self.current_page = 1
        self.calculate_pagination()