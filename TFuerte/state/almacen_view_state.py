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
            print(f"✅ Datos cargados (solo lectura): {len(data)} registros")
        else:
            self.almacen_data = []
            self.filtered_data = []
            self.total_productos = 0
            self.valor_total = 0.0
        
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
    
    def sort_values(self, sort_value: str):
        """Ordena los datos por la columna especificada"""
        self.sort_value = sort_value
        
        if not sort_value:
            return
        
        # Ordenar los datos
        sorted_data = sorted(self.filtered_data, key=lambda x: x.get(sort_value, ""))
        self.filtered_data = sorted_data