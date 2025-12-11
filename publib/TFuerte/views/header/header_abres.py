import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles
from TFuerte.styles.colors import Text_tx

def value_card(icon: str, title: str, description: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.box(
                rx.text(
                    icon,
                    font_size="3em",
                ),
                margin_bottom=styles.Spacer.MEDIUM.value,
            ),
            rx.heading(
                title,
                size="7",
                color="#194264FF",
                font_weight="bold",
                text_align="center",
                margin_bottom=styles.Spacer.SMALL.value,
            ),
            rx.text(
                description,
                size="5",
                color="#64748B",
                text_align="center",
                line_height="1.6",
            ),
            align_items="center",
            spacing="4",
        ),
        background="white",
        border_radius="20px",
        padding=styles.Spacer.LARGE.value,
        box_shadow="0 10px 30px rgba(0, 0, 0, 0.08)",
        _hover={
            "transform": "translateY(-8px)",
            "box_shadow": "0 20px 40px rgba(25, 66, 100, 0.15)",
            "transition": "all 0.3s ease",
        },
        height="100%",
        min_height="300px",
        width="100%",
        margin=styles.Spacer.EXTRA_SMALL.value,
    )

def mission_vision_section(title: str, content: str, is_even: bool = False) -> rx.Component:
    return rx.center(
        # Versión Desktop (horizontal)
        rx.box(
            rx.hstack(
                # Elemento visual decorativo
                rx.box(
                    rx.image(
                    src="alt.png",
                    ),
                    flex="1",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    padding=styles.Spacer.LARGE.value,
                ),
                
                # Contenido de texto
                rx.box(
                    rx.vstack(
                        rx.heading(
                            title,
                            font_size=styles.Spacer.BIG.value,
                            color="#194264FF" if is_even else "#2a5a8a",
                            font_weight="bold",
                            margin_bottom=styles.Spacer.MEDIUM.value,
                        ),
                        rx.text(
                            content,
                            font_size=styles.Spacer.LARGE.value,
                            color="#475569",
                            line_height="1.7",
                            text_align="left",
                        ),
                        align_items="start",
                        spacing="5",
                    ),
                    flex="2",
                    padding=styles.Spacer.LARGE.value,
                ),
                spacing="6",
                align_items="center",
                width="100%",
                max_width="1200px",
                direction="row-reverse" if is_even else "row",
            ),
            display=["none", "none", "flex", "flex"],  # Solo en desktop
        ),
        
        # Versión Mobile (vertical)
        rx.box(
            rx.vstack(
                rx.heading(
                    title,
                    font_size=styles.Spacer.BIG.value,
                    color="#194264FF" if is_even else "#2a5a8a",
                    font_weight="bold",
                    margin_bottom=styles.Spacer.MEDIUM.value,
                    text_align="center",
                ),
                rx.text(
                    content,
                    font_size=styles.Spacer.LARGE.value,
                    color="#475569",
                    line_height="1.7",
                    text_align="center",
                ),
                rx.box(
                    rx.box(
                        width="100px",
                        height="100px",
                        background=f"linear-gradient(135deg, {'#194264FF' if is_even else '#2a5a8a'} 0%, {'#194264FF22' if is_even else '#2a5a8a22'} 100%)",
                        border_radius="50%",
                        opacity="0.7",
                    ),
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    margin_top=styles.Spacer.LARGE.value,
                ),
                align_items="center",
                spacing="5",
                width="100%",
                padding_x=styles.Spacer.MEDIUM.value,
            ),
            display=["flex", "flex", "none", "none"],  # Solo en mobile
        ),
        
        width="100%",
        padding_y=styles.Spacer.VERY_BIG.value,
        background="linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 100%)" if is_even else "white",
    )

def header_abres() -> rx.Component:
    values = [
        {
            "icon": "🛡️", 
            "title": "Seguridad y Prevención", 
            "description": "Priorizamos la integridad física en cada intervención con protocolos rigurosos que garantizan entornos de trabajo seguros."
        },
        {
            "icon": "⚡", 
            "title": "Excelencia Técnica", 
            "description": "Buscamos la perfección combinando conocimiento especializado con atención meticulosa a los detalles."
        },
        {
            "icon": "🤝", 
            "title": "Trabajo en Equipo", 
            "description": "Integramos diversas especialidades técnicas para ofrecer soluciones completas y colaborativas."
        },
        {
            "icon": "💡", 
            "title": "Innovación Responsable", 
            "description": "Incorporamos tecnologías avanzadas mejorando procesos sin comprometer la sostenibilidad."
        },
        {
            "icon": "🌱", 
            "title": "Compromiso Social", 
            "description": "Actuamos con integridad contribuyendo al desarrollo industrial y bienestar comunitario."
        }
    ]
    
    return rx.vstack(
        # Hero Section Moderna
        rx.center(
            rx.vstack(
                rx.box(
                    rx.heading(
                        "Liderando la Excelencia en Mantenimiento Industrial",
                        font_size=styles.Spacer.BIG.value,
                        color="white",
                        text_align="center",
                        font_weight="bold",
                        line_height="1.2",
                        margin_bottom=styles.Spacer.MEDIUM.value,
                    ),
                    rx.text(
                        "Transformando la gestión de activos industriales con soluciones innovadoras y sostenibles",
                        font_size=styles.Spacer.LARGE.value,
                        color="rgba(255, 255, 255, 0.9)",
                        text_align="center",
                        max_width="800px",
                        line_height="1.6",
                    ),
                    align_items="center",
                    spacing="6",
                ),
                
                # Estadísticas - Versión Desktop (horizontal)
                rx.box(
                    rx.hstack(
                        rx.vstack(
                            rx.heading(
                                "500+",
                                font_size=styles.Spacer.BIG.value,
                                color="white",
                                font_weight="bold",
                            ),
                            rx.text(
                                "Proyectos Exitosos",
                                font_size=styles.Spacer.LARGE.value,
                                color="rgba(255, 255, 255, 0.8)",
                            ),
                            align_items="center",
                            spacing="2",
                        ),
                        rx.vstack(
                            rx.heading(
                                "100%",
                                font_size=styles.Spacer.BIG.value,
                                color="white",
                                font_weight="bold",
                            ),
                            rx.text(
                                "Satisfacción Cliente",
                                font_size=styles.Spacer.LARGE.value,
                                color="rgba(255, 255, 255, 0.8)",
                            ),
                            align_items="center",
                            spacing="2",
                        ),
                        spacing="8",
                        justify="center",
                    ),
                    margin_top=styles.Spacer.VERY_BIG.value,
                    display=["none", "none", "flex", "flex"],  # Solo en desktop
                ),
                
                # Estadísticas - Versión Mobile (vertical)
                rx.box(
                    rx.vstack(
                        rx.vstack(
                            rx.heading(
                                "500+",
                                font_size=styles.Spacer.BIG.value,
                                color="white",
                                font_weight="bold",
                            ),
                            rx.text(
                                "Proyectos Exitosos",
                                font_size=styles.Spacer.LARGE.value,
                                color="rgba(255, 255, 255, 0.8)",
                            ),
                            align_items="center",
                            spacing="2",
                        ),
                        rx.vstack(
                            rx.heading(
                                "100%",
                                font_size=styles.Spacer.BIG.value,
                                color="white",
                                font_weight="bold",
                            ),
                            rx.text(
                                "Satisfacción Cliente",
                                font_size=styles.Spacer.LARGE.value,
                                color="rgba(255, 255, 255, 0.8)",
                            ),
                            align_items="center",
                            spacing="2",
                        ),
                        spacing="6",
                        align_items="center",
                    ),
                    margin_top=styles.Spacer.VERY_BIG.value,
                    display=["flex", "flex", "none", "none"],  # Solo en mobile
                ),
                align_items="center",
                spacing="8",
            ),
            width="100%",
            padding_y=styles.Spacer.VERY_BIG.value,
            background="linear-gradient(135deg, #194264FF 0%, #2a5a8a 100%)",
        ),
        
        # Misión
        mission_vision_section(
            "Nuestra Misión",
            "Ser referente nacional en el mantenimiento, reparación y rehabilitación de equipos industriales, promoviendo la eficiencia y ofreciendo soluciones que impulsen la eficacia, calidad y rentabilidad, creando un entorno de trabajo seguro, saludable y sostenible para minimizar el impacto ambiental.",
            False
        ),
        
        # Visión
        mission_vision_section(
            "Nuestra Visión", 
            "Aspiramos a transformar la gestión de activos industriales, garantizando la máxima disponibilidad de maquinarias y equipos, reduciendo costos y contribuyendo a un futuro industrial más seguro, innovador y sostenible.",
            True
        ),
        
        # Valores
        rx.center(
            rx.vstack(
                rx.heading(
                    "Nuestros Valores Fundamentales",
                    font_size=styles.Spacer.BIG.value,
                    color="#194264FF",
                    text_align="center",
                    font_weight="bold",
                    margin_bottom=styles.Spacer.SMALL.value,
                ),
                rx.text(
                    "Los principios que guían cada una de nuestras acciones y decisiones",
                    font_size=styles.Spacer.LARGE.value,
                    color="#64748B",
                    text_align="center",
                    max_width="600px",
                    margin_bottom=styles.Spacer.VERY_BIG.value,
                ),
                
                # Grid de valores - Versión Desktop (múltiples columnas)
                rx.box(
                    rx.flex(
                        *[
                            value_card(
                                value["icon"], 
                                value["title"], 
                                value["description"]
                            )
                            for value in values
                        ],
                        wrap="wrap",
                        justify="center",
                        spacing="6",
                        width="100%",
                    ),
                    width="100%",
                    max_width="1200px",
                    display=["none", "none", "flex", "flex"],  # Solo en desktop
                ),
                
                # Grid de valores - Versión Mobile (una columna)
                rx.box(
                    rx.vstack(
                        *[
                            value_card(
                                value["icon"], 
                                value["title"], 
                                value["description"]
                            )
                            for value in values
                        ],
                        spacing="6",
                        width="100%",
                        align_items="center",
                    ),
                    width="100%",
                    display=["flex", "flex", "none", "none"],  # Solo en mobile
                ),
                align_items="center",
                spacing="6",
            ),
            width="100%",
            padding_y=styles.Spacer.VERY_BIG.value,
            background="linear-gradient(135deg, #F0F7FF 0%, #FFFFFF 100%)",
        ),
        
        # Llamada a la acción
        rx.center(
            rx.vstack(
                rx.heading(
                    "¿Preparado para Optimizar sus Operaciones?",
                    font_size=styles.Spacer.BIG.value,
                    color="white",
                    text_align="center",
                    font_weight="bold",
                    margin_bottom=styles.Spacer.SMALL.value,
                ),
                rx.text(
                    "Descubra cómo nuestra experiencia puede impulsar la eficiencia y rentabilidad de su empresa",
                    font_size=styles.Spacer.LARGE.value,
                    color="rgba(255, 255, 255, 0.9)",
                    text_align="center",
                    margin_bottom=styles.Spacer.LARGE.value,
                    max_width="600px",
                ),
                
                # Botones - Versión Desktop (horizontal)
                rx.box(
                    rx.hstack(
                        rx.button(
                            "Solicitar Asesoría",
                            background="white",
                            color="#194264FF",
                            border_radius="12px",
                            padding_x=styles.Spacer.LARGE.value,
                            padding_y=styles.Spacer.MEDIUM.value,
                            font_size=styles.Spacer.LARGE.value,
                            font_weight="bold",
                            box_shadow="0 8px 20px rgba(255, 255, 255, 0.3)",
                            _hover={
                                "transform": "translateY(-2px)",
                                "box_shadow": "0 12px 25px rgba(255, 255, 255, 0.4)",
                            },
                        ),
                        rx.button(
                            "Conocer Servicios",
                            background="transparent",
                            color="white",
                            border="2px solid white",
                            border_radius="12px",
                            padding_x=styles.Spacer.LARGE.value,
                            padding_y=styles.Spacer.MEDIUM.value,
                            font_size=styles.Spacer.LARGE.value,
                            font_weight="bold",
                            _hover={
                                "background": "rgba(255, 255, 255, 0.1)",
                                "transform": "translateY(-2px)",
                            },
                        ),
                        spacing="4",
                        justify="center",
                    ),
                    display=["none", "none", "flex", "flex"],  # Solo en desktop
                ),
                
                # Botones - Versión Mobile (vertical)
                rx.center(
                rx.box(
                    rx.vstack(
                        rx.button(
                            "Conocer Servicios",
                            background="transparent",
                            color="white",
                            border="2px solid white",
                            border_radius="10px",
                            font_size=styles.Spacer.LARGE.value,
                            font_weight="bold",
                            _hover={
                                "background": "rgba(255, 255, 255, 0.1)",
                                "transform": "translateY(-2px)",
                            },
                            width="100%",
                            max_width="200px",
                            #margin=styles.Spacer.SMALL.value,
                        ),

                        spacing="4",
                        align_items="center",
                        margin=styles.Spacer.SMALL.value,
                    ),
                    display=["flex", "flex", "none", "none"],  # Solo en mobile
                    width="100%",
                    
                ),
            ),
                align_items="center",
                spacing="6",
                width="100%",
                margin=styles.Spacer.SMALL.value,
            ),
            width="100%",
            padding_y=styles.Spacer.VERY_BIG.value,
            background="linear-gradient(135deg, #194264FF 0%, #2a5a8a 100%)",
        ),
        
        spacing="0",
        width="100%",
        align="center",
    )