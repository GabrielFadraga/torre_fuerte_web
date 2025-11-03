import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles
from TFuerte.styles.colors import Text_tx, Color_tx

# Iconos específicos para cada servicio - asignados por relación semántica
SERVICE_ICONS = {
    1: "🧼",   # Lavandería industrial
    2: "⚙️",   # Equipos dinámicos y estáticos
    3: "🔋",   # Grupos electrógenos y energía solar
    4: "🔥",   # Calderas de baja presión
    5: "🛠️",   # Soldadura especializada
    6: "❄️",   # Sistemas de climatización
    7: "🏭",   # Fabricación de piezas de repuesto
    8: "⚡",   # Mantenimiento eléctrico industrial
    9: "🚢",   # Sistemas electro-automáticos navales
    10: "🤖",  # Automatización industrial
    11: "📐",  # Pailería y desarrollos metálicos
}

def modern_service_card(title: str, description: str, service_number: int) -> rx.Component:
    """Componente de tarjeta moderno con íconos semánticos"""
    # Extraer el número real del servicio del título
    actual_service_number = None
    if ". " in title:
        try:
            actual_service_number = int(title.split(". ")[0])
        except ValueError:
            actual_service_number = service_number
    else:
        actual_service_number = service_number
    
    # Obtener el ícono correspondiente al servicio
    icon = SERVICE_ICONS.get(actual_service_number, "🔧")
    
    return rx.card(
        rx.vstack(
            # Header con número y icono en círculo
            rx.hstack(
                # Número con fondo de acento
                rx.box(
                    rx.text(
                        f"{actual_service_number:02d}",
                        font_size="14px",
                        font_weight="bold",
                        color="white",
                    ),
                    background=Color_tx.Primary.value,
                    padding_x="12px",
                    padding_y="6px",
                    border_radius="12px",
                ),
                
                # Icono en círculo
                rx.center(
                    rx.text(
                        icon,
                        font_size="24px",
                    ),
                    background="linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)",
                    border=f"2px solid {Color_tx.Primary.value}",
                    border_radius="50%",
                    width="50px",
                    height="50px",
                ),
                
                justify="between",
                align_items="center",
                width="100%",
                margin_bottom=styles.Spacer.MEDIUM.value,
            ),
            
            # Título
            rx.heading(
                title.split(". ", 1)[1] if ". " in title else title,
                font_size=["18px", "20px"],
                color=Text_tx.Black.value,
                text_align="left",
                font_weight="bold",
                line_height="1.3",
                width="100%",
            ),
            
            # Descripción
            rx.box(
                rx.text(
                    description,
                    font_size=["14px", "15px"],
                    color=Text_tx.Black.value,
                    text_align="left",
                    line_height="1.6",
                ),
                width="100%",
                max_height="120px",
                overflow="hidden",
                position="relative",
            ),
            
            align_items="start",
            spacing="4",
            width="100%",
            height="100%",
            padding=styles.Spacer.LARGE.value,
        ),
        # Estilos de la tarjeta
        background="white",
        border="1px solid #e2e8f0",
        border_radius="24px",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        position="relative",
        overflow="hidden",
        _before={
            "content": "''",
            "position": "absolute",
            "top": "0",
            "left": "0",
            "right": "0",
            "height": "4px",
            "background": f"linear-gradient(90deg, {Color_tx.Primary.value}, {Color_tx.Secondary.value})",
        },
        _hover={
            "transform": "translateY(-8px)",
            "box_shadow": "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
            "border_color": Color_tx.Primary.value,
        },
        transition="all 0.3s ease-in-out",
        width="100%",
        height="100%",
        cursor="pointer",
    )

def service_category_grid(services: list, category_title: str, category_description: str) -> rx.Component:
    """Grid de servicios que mantiene la numeración correcta"""
    service_cards = []
    
    for service in services:
        # Extraer el número del servicio del título
        service_number = 1
        if ". " in service["title"]:
            try:
                service_number = int(service["title"].split(". ")[0])
            except ValueError:
                # Si no se puede extraer el número, usar un valor por defecto
                service_number = 1
        
        service_cards.append(modern_service_card(service["title"], service["description"], service_number))
    
    return rx.vstack(
        # Header de categoría
        rx.center(
            rx.vstack(
                rx.box(
                    category_title,
                    background="linear-gradient(135deg, #194264FF 0%, #2a5a8a 100%)",
                    color="white",
                    padding_x="20px",
                    padding_y="8px",
                    border_radius="20px",
                    font_size="14px",
                    font_weight="bold",
                    margin_bottom=styles.Spacer.SMALL.value,
                ),
                rx.heading(
                    category_description,
                    font_size=["24px", "28px", "32px"],
                    color=Text_tx.Black.value,
                    text_align="center",
                    font_weight="bold",
                    max_width="600px",
                    line_height="1.2",
                ),
                align_items="center",
                spacing="4",
            ),
            width="100%",
            padding_y=styles.Spacer.LARGE.value,
        ),
        
        # Grid de servicios
        rx.box(
            # Versión desktop - 3 columnas
            rx.desktop_only(
                rx.flex(
                    *service_cards,
                    direction="row",
                    wrap="wrap",
                    justify="center",
                    spacing="6",
                    width="100%",
                )
            ),
            # Versión tablet - 2 columnas
            rx.tablet_only(
                rx.flex(
                    *service_cards,
                    direction="row",
                    wrap="wrap",
                    justify="center",
                    spacing="6",
                    width="100%",
                )
            ),
            # Versión móvil - 1 columna
            rx.mobile_only(
                rx.vstack(
                    *service_cards,
                    spacing="6",
                    width="100%",
                )
            ),
            width="100%",
        ),
        
        spacing="6",
        width="100%",
    )

def header_services() -> rx.Component:
    # Agrupar servicios en categorías lógicas
    maintenance_services = [
        {
            "title": "1. Mantenimiento y Reparación de Equipos de Lavandería Industrial",
            "description": "Diagnóstico y solución de fallas en lavadoras, secadoras y planchadoras industriales. Mantenimiento preventivo y correctivo para maximizar disponibilidad."
        },
        {
            "title": "2. Mantenimiento de Equipos Dinámicos y Estáticos",
            "description": "Servicios especializados para bombas, compresores, ventiladores y sistemas de transferencia de calor. Balanceo, alineación y reparación de componentes."
        },
        {
            "title": "4. Mantenimiento y Reparación de Calderas de Baja Presión",
            "description": "Inspecciones, limpieza química y mecánica, reparación de refractarios y pruebas hidrostáticas para operación segura y eficiente."
        },
        {
            "title": "6. Mantenimiento de Sistemas de Climatización",
            "description": "Servicios completos para aire acondicionado y refrigeración: instalación, mantenimiento preventivo y diagnóstico de fallas."
        }
    ]
    
    energy_services = [
        {
            "title": "3. Grupos Electrógenos y Sistemas de Energía Solar",
            "description": "Montaje, puesta en marcha, mantenimiento y reparación de sistemas de energía de respaldo y renovable."
        },
        {
            "title": "8. Mantenimiento Eléctrico Industrial",
            "description": "Diagnóstico y reparación de fallas en cuadros de distribución, cableados, breakers y sistemas de iluminación industrial."
        }
    ]
    
    specialized_services = [
        {
            "title": "5. Soldadura Especializada",
            "description": "Trabajos de soldadura certificada en acero negro e inoxidable para reparación y fabricación de equipos críticos."
        },
        {
            "title": "7. Fabricación de Piezas de Repuesto",
            "description": "Maquinado, cilindrado, fresado y rectificado para fabricación precisa de componentes y repuestos."
        },
        {
            "title": "9. Sistemas Electro-Automáticos Navales",
            "description": "Reparación y puesta a punto de sistemas de control, automatización y potencia eléctrica para embarcaciones."
        },
        {
            "title": "10. Automatización Industrial",
            "description": "Diagnóstico y reparación de sistemas de control con PLCs, sensores, actuadores y variadores de frecuencia."
        },
        {
            "title": "11. Pailería y Desarrollos Metálicos",
            "description": "Trazado y desarrollo preciso de planchas metálicas para ductos, tolvas, tanques y estructuras."
        }
    ]
    
    return rx.vstack(
        # Hero Section
        rx.center(
            rx.vstack(
                rx.box(
                    "SERVICIOS ESPECIALIZADOS",
                    background="linear-gradient(135deg, #194264FF 0%, #2a5a8a 100%)",
                    color="white",
                    padding_x="20px",
                    padding_y="8px",
                    border_radius="20px",
                    font_size="14px",
                    font_weight="bold",
                    margin_bottom=styles.Spacer.MEDIUM.value,
                ),
                rx.heading(
                    "Soluciones Técnicas Integrales",
                    font_size=["32px", "40px", "48px"],
                    color=Text_tx.Footer.value,
                    text_align="center",
                    font_weight="bold",
                    background="linear-gradient(135deg, #194264 0%, #2D3748 100%)",
                    background_clip="text",
                    margin_bottom=styles.Spacer.SMALL.value,
                    line_height="1.1",
                ),
                rx.text(
                    "Nos especializamos en mantenimiento industrial, energía y automatización, garantizando la eficiencia operativa de su empresa",
                    font_size=["16px", "18px", "20px"],
                    color=Text_tx.Footer.value,
                    text_align="center",
                    max_width="800px",
                    line_height="1.6",
                    margin_bottom=styles.Spacer.LARGE.value,
                ),
                
                # Stats bar
                rx.hstack(
                    #rx.divider(orientation="vertical", height="40px"),
                    rx.vstack(
                        rx.heading(
                            "300+",
                            font_size="32px",
                            color=Text_tx.Footer.value,
                            font_weight="bold",
                        ),
                        rx.text(
                            "Servicios completados",
                            font_size="14px",
                            color=Text_tx.Footer.value,
                        ),
                        align_items="center",
                        spacing="1",
                    ),
                    rx.divider(orientation="vertical", height="40px"),
                    rx.vstack(
                        rx.heading(
                            "24/7",
                            font_size="32px",
                            color=Text_tx.Footer.value,
                            font_weight="bold",
                        ),
                        rx.text(
                            "Soporte técnico",
                            font_size="14px",
                            color=Text_tx.Footer.value,
                        ),
                        align_items="center",
                        spacing="1",
                    ),
                    justify="center",
                    spacing="6",
                    padding_y=styles.Spacer.LARGE.value,
                ),
                
                align_items="center",
                spacing="6",
            ),
            width="100%",
            padding_y=styles.Spacer.VERY_BIG.value,
            background="linear-gradient(135deg, #194264FF 0%, #0f2a42 100%)",
            margin_bottom=styles.Spacer.LARGE.value,
        ),
        
        # Categoría 1: Mantenimiento Industrial
        service_category_grid(
            maintenance_services,
            "MANTENIMIENTO INDUSTRIAL",
            "Servicios de mantenimiento preventivo y correctivo"
        ),
        
        # Separador visual
        rx.center(
            rx.divider(width="100px", height="3px", background=Color_tx.Primary.value),
            width="100%",
            padding_y=styles.Spacer.LARGE.value,
        ),
        
        # Categoría 2: Energía y Electricidad
        service_category_grid(
            energy_services,
            "ENERGÍA Y ELECTRICIDAD", 
            "Soluciones energéticas confiables"
        ),
        
        # Separador visual
        rx.center(
            rx.divider(width="100px", height="3px", background=Color_tx.Primary.value),
            width="100%",
            padding_y=styles.Spacer.LARGE.value,
        ),
        
        # Categoría 3: Servicios Especializados
        service_category_grid(
            specialized_services,
            "SERVICIOS ESPECIALIZADOS",
            "Tecnología y fabricación avanzada"
        ),
        
        # CTA Section
        rx.link(
        rx.center(
            rx.vstack(
                rx.heading(
                    "¿Necesita un servicio específico?",
                    font_size=["24px", "28px", "32px"],
                    color="white",
                    text_align="center",
                    margin_bottom=styles.Spacer.SMALL.value,
                ),
                rx.text(
                    "Contáctenos para una evaluación personalizada de sus necesidades",
                    font_size=["16px", "18px"],
                    color="rgba(255,255,255,0.9)", 
                    text_align="center",
                    margin_bottom=styles.Spacer.LARGE.value,
                ),
                rx.button(
                    "Contactar",
                    background="white",
                    color=Color_tx.Primary.value,
                    padding_x="40px",
                    padding_y="20px",
                    border_radius="12px",
                    font_size="16px",
                    font_weight="bold",
                    _hover={
                        "background": "#f8fafc",
                        "transform": "translateY(-2px)",
                    },
                ),
                align_items="center",
                spacing="4",
            ),
            width="100%",
            padding_y=styles.Spacer.VERY_BIG.value,
            background="linear-gradient(135deg, #194264 0%, #2a5a8a 100%)",
            color="white",
        ),
        href="https://wa.me/message/OKIP2WN55MKEK1",
        is_external=True,
        width="100%",
    ),
        
        spacing="0",
        width="100%",
    )