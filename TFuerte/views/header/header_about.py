import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles
from TFuerte.styles.colors import Text_tx, Color_tx

def value_card(icon: str, title: str, description: str, index: int) -> rx.Component:
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
                font_size=["16px", "18px", "20px"],
                color=Color_tx.Primary.value,
                font_weight="bold",
                text_align="center",
                margin_bottom=styles.Spacer.SMALL.value,
            ),
            rx.text(
                description,
                font_size=["12px", "14px", "15px"],
                color=Text_tx.Black.value,
                text_align="center",
                line_height="1.5",
            ),
            align_items="center",
            spacing="3",
        ),
        background="white",
        border_radius="15px",
        padding=styles.Spacer.MEDIUM.value,
        box_shadow="0 4px 12px rgba(0, 0, 0, 0.08)",
        transform="translateY(0px)",
        transition="all 0.3s ease-in-out",
        _hover={
            "transform": "translateY(-5px)",
            "box_shadow": "0 12px 24px rgba(25, 66, 100, 0.15)",
        },
        animation=f"fadeInUp 0.6s ease-out {index * 0.1}s both",
        height="100%",
        min_height="280px",
    )

def quality_policy_section() -> rx.Component:
    """Sección de Política de Calidad con diseño moderno"""
    return rx.center(
        rx.box(
            # Desktop
            rx.desktop_only(
                rx.hstack(
                    # Texto de la política
                    rx.box(
                        rx.vstack(
                            rx.box(
                                "POLÍTICA DE CALIDAD",
                                background=f"linear-gradient(135deg, {Color_tx.Primary.value} 0%, #2a5a8a 100%)",
                                color="white",
                                padding_x="20px",
                                padding_y="8px",
                                border_radius="20px",
                                font_size="14px",
                                font_weight="bold",
                                margin_bottom=styles.Spacer.MEDIUM.value,
                            ),
                            rx.heading(
                                "Compromiso con la Excelencia",
                                font_size=["24px", "28px", "32px"],
                                color=Color_tx.Primary.value,
                                font_weight="bold",
                                margin_bottom=styles.Spacer.MEDIUM.value,
                                text_align="left",
                            ),
                            rx.vstack(
                                rx.hstack(
                                    rx.icon(
                                        tag="check_circle",
                                        color=Color_tx.Primary.value,
                                        font_size="20px",
                                        flex_shrink="0",
                                    ),
                                    rx.text(
                                        "Garantizar la satisfacción del cliente mediante servicios de alta calidad",
                                        font_size=["14px", "16px"],
                                        color=Text_tx.Black.value,
                                        line_height="1.6",
                                    ),
                                    align_items="start",
                                    spacing="3",
                                ),
                                rx.hstack(
                                    rx.icon(
                                        tag="check_circle", 
                                        color=Color_tx.Primary.value,
                                        font_size="20px",
                                        flex_shrink="0",
                                    ),
                                    rx.text(
                                        "Mejora continua de procesos y sistemas de gestión",
                                        font_size=["14px", "16px"],
                                        color=Text_tx.Black.value,
                                        line_height="1.6",
                                    ),
                                    align_items="start",
                                    spacing="3",
                                ),
                                rx.hstack(
                                    rx.icon(
                                        tag="check_circle",
                                        color=Color_tx.Primary.value,
                                        font_size="20px",
                                        flex_shrink="0",
                                    ),
                                    rx.text(
                                        "Cumplimiento de requisitos legales y regulatorios",
                                        font_size=["14px", "16px"],
                                        color=Text_tx.Black.value,
                                        line_height="1.6",
                                    ),
                                    align_items="start",
                                    spacing="3",
                                ),
                                rx.hstack(
                                    rx.icon(
                                        tag="check_circle",
                                        color=Color_tx.Primary.value,
                                        font_size="20px",
                                        flex_shrink="0",
                                    ),
                                    rx.text(
                                        "Desarrollo profesional continuo de nuestro equipo",
                                        font_size=["14px", "16px"],
                                        color=Text_tx.Black.value,
                                        line_height="1.6",
                                    ),
                                    align_items="start",
                                    spacing="3",
                                ),
                                spacing="3",
                                align_items="start",
                            ),
                            align_items="start",
                            spacing="4",
                        ),
                        flex="1",
                        padding=styles.Spacer.LARGE.value,
                        animation="fadeInLeft 0.8s ease-out",
                    ),
                    
                    # Imagen de la política de calidad con efectos
                    rx.box(
                        rx.vstack(
                            rx.box(
                                rx.image(
                                    src="calidadtf.png",
                                    width="100%",
                                    max_width="400px",
                                    border_radius="20px",
                                    box_shadow="0 15px 35px rgba(25, 66, 100, 0.2)",
                                    transition="all 0.5s ease-in-out",
                                    _hover={
                                        "transform": "scale(1.02)",
                                        "box_shadow": "0 20px 45px rgba(25, 66, 100, 0.3)",
                                    }
                                ),
                                position="relative",
                                _before={
                                    "content": "''",
                                    "position": "absolute",
                                    "top": "-10px",
                                    "left": "-10px",
                                    "right": "-10px",
                                    "bottom": "-10px",
                                    "background": f"linear-gradient(135deg, {Color_tx.Primary.value}20, transparent)",
                                    "border_radius": "25px",
                                    "z_index": "-1",
                                    "opacity": "0",
                                    "transition": "all 0.5s ease",
                                },
                                _hover={
                                    "_before": {
                                        "opacity": "1",
                                        "top": "-15px",
                                        "left": "-15px", 
                                        "right": "-15px",
                                        "bottom": "-15px",
                                    }
                                }
                            ),
                            rx.text(
                                "Certificación de Calidad",
                                font_size="14px",
                                color=Text_tx.Black.value,
                                font_weight="medium",
                                text_align="center",
                                margin_top=styles.Spacer.SMALL.value,
                            ),
                            align_items="center",
                            spacing="3",
                        ),
                        flex="1",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        padding=styles.Spacer.LARGE.value,
                        animation="fadeInRight 0.8s ease-out 0.2s both",
                    ),
                    
                    spacing="8",
                    align_items="center",
                    width="100%",
                    max_width="1200px",
                )
            ),
            
            # Mobile/Tablet
            rx.mobile_and_tablet(
                rx.vstack(
                    rx.box(
                        rx.vstack(
                            rx.box(
                                "POLÍTICA DE CALIDAD",
                                background=f"linear-gradient(135deg, {Color_tx.Primary.value} 0%, #2a5a8a 100%)",
                                color="white",
                                padding_x="16px",
                                padding_y="6px",
                                border_radius="15px",
                                font_size="12px",
                                font_weight="bold",
                                margin_bottom=styles.Spacer.SMALL.value,
                            ),
                            rx.heading(
                                "Compromiso con la Excelencia",
                                font_size=["20px", "22px"],
                                color=Color_tx.Primary.value,
                                font_weight="bold",
                                margin_bottom=styles.Spacer.MEDIUM.value,
                                text_align="center",
                            ),
                            rx.vstack(
                                rx.hstack(
                                    rx.icon(
                                        tag="check_circle",
                                        color=Color_tx.Primary.value,
                                        font_size="18px",
                                        flex_shrink="0",
                                    ),
                                    rx.text(
                                        "Garantizar la satisfacción del cliente mediante servicios de alta calidad",
                                        font_size="13px",
                                        color=Text_tx.Black.value,
                                        line_height="1.5",
                                    ),
                                    align_items="start",
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.icon(
                                        tag="check_circle",
                                        color=Color_tx.Primary.value,
                                        font_size="18px",
                                        flex_shrink="0",
                                    ),
                                    rx.text(
                                        "Mejora continua de procesos y sistemas de gestión",
                                        font_size="13px",
                                        color=Text_tx.Black.value,
                                        line_height="1.5",
                                    ),
                                    align_items="start",
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.icon(
                                        tag="check_circle",
                                        color=Color_tx.Primary.value,
                                        font_size="18px",
                                        flex_shrink="0",
                                    ),
                                    rx.text(
                                        "Cumplimiento de requisitos legales y regulatorios",
                                        font_size="13px",
                                        color=Text_tx.Black.value,
                                        line_height="1.5",
                                    ),
                                    align_items="start",
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.icon(
                                        tag="check_circle",
                                        color=Color_tx.Primary.value,
                                        font_size="18px",
                                        flex_shrink="0",
                                    ),
                                    rx.text(
                                        "Desarrollo profesional continuo de nuestro equipo",
                                        font_size="13px",
                                        color=Text_tx.Black.value,
                                        line_height="1.5",
                                    ),
                                    align_items="start",
                                    spacing="2",
                                ),
                                spacing="2",
                                align_items="start",
                            ),
                            align_items="center",
                            spacing="3",
                        ),
                        padding=styles.Spacer.MEDIUM.value,
                        animation="fadeInUp 0.6s ease-out",
                    ),
                    
                    rx.box(
                        rx.vstack(
                            rx.image(
                                src="calidadtf.png",
                                width="100%",
                                max_width="300px",
                                border_radius="15px",
                                box_shadow="0 10px 25px rgba(25, 66, 100, 0.15)",
                            ),
                            rx.text(
                                "Certificación de Calidad", 
                                font_size="12px",
                                color=Text_tx.Black.value,
                                font_weight="medium",
                                text_align="center",
                                margin_top=styles.Spacer.SMALL.value,
                            ),
                            align_items="center",
                            spacing="2",
                        ),
                        padding=styles.Spacer.MEDIUM.value,
                        animation="fadeInUp 0.6s ease-out 0.2s both",
                    ),
                    
                    spacing="4",
                    align_items="center",
                    width="100%",
                    max_width="1200px",
                )
            ),
            
            width="100%",
            max_width="1200px",
        ),
        width="100%",
        padding_y=styles.Spacer.VERY_BIG.value,
        background="linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%)",
        position="relative",
        overflow="hidden",
    )

def about_with_animations() -> rx.Component:
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
    
    return rx.box(
        rx.vstack(
            # Hero Section - Responsive
            rx.center(
                rx.vstack(
                    rx.box(
                        rx.heading(
                            "Liderando la Excelencia en Mantenimiento Industrial",
                            font_size=["20px", "24px", "32px", "40px", "48px"],
                            color="white",
                            text_align="center",
                            font_weight="bold",
                            line_height="1.2",
                            margin_bottom=styles.Spacer.MEDIUM.value,
                            animation="fadeInUp 0.8s ease-out",
                        ),
                        rx.text(
                            "Transformando la gestión de activos industriales con soluciones innovadoras y sostenibles",
                            font_size=["13px", "14px", "16px", "18px", "20px"],
                            color="rgba(255, 255, 255, 0.9)",
                            text_align="center",
                            max_width="800px",
                            line_height="1.5",
                            animation="fadeInUp 0.8s ease-out 0.2s both",
                        ),
                        align_items="center",
                        spacing="4",
                    ),
                    
                    # Estadísticas - Responsive
                    rx.box(
                        # Desktop
                        rx.desktop_only(
                            rx.hstack(
                                rx.vstack(
                                    rx.heading(
                                        "300+",
                                        font_size=["28px", "32px", "36px"],
                                        color="white",
                                        font_weight="bold",
                                        animation="countUp 1s ease-out 0.3s both",
                                    ),
                                    rx.text(
                                        "Servicios Exitosos",
                                        font_size="13px",
                                        color="rgba(255, 255, 255, 0.8)",
                                        font_weight="500",
                                    ),
                                    align_items="center",
                                    spacing="1",
                                ),
                                rx.vstack(
                                    rx.heading(
                                        "100%",
                                        font_size=["28px", "32px", "36px"],
                                        color="white",
                                        font_weight="bold",
                                        animation="countUp 1s ease-out 0.6s both",
                                    ),
                                    rx.text(
                                        "Satisfacción Cliente",
                                        font_size="13px",
                                        color="rgba(255, 255, 255, 0.8)",
                                        font_weight="500",
                                    ),
                                    align_items="center",
                                    spacing="1",
                                ),
                                spacing="6",
                                justify="center",
                                margin_top=styles.Spacer.LARGE.value,
                                animation="fadeInUp 0.8s ease-out 0.4s both",
                            )
                        ),
                        
                        # Mobile/Tablet
                        rx.mobile_and_tablet(
                            rx.vstack(
                                rx.hstack(
                                    rx.vstack(
                                        rx.heading(
                                            "300+",
                                            font_size=["22px", "24px", "26px"],
                                            color="white",
                                            font_weight="bold",
                                        ),
                                        rx.text(
                                            "Servicios Exitosos",
                                            font_size="11px",
                                            color="rgba(255, 255, 255, 0.8)",
                                            font_weight="500",
                                        ),
                                        align_items="center",
                                        spacing="1",
                                    ),
                                    rx.vstack(
                                        rx.heading(
                                            "100%",
                                            font_size=["22px", "24px", "26px"],
                                            color="white",
                                            font_weight="bold",
                                        ),
                                        rx.text(
                                            "Satisfacción Cliente",
                                            font_size="11px",
                                            color="rgba(255, 255, 255, 0.8)",
                                            font_weight="500",
                                        ),
                                        align_items="center",
                                        spacing="1",
                                    ),
                                    spacing="3",
                                    justify="center",
                                    wrap="wrap",
                                ),
                                margin_top=styles.Spacer.MEDIUM.value,
                                spacing="3",
                            )
                        ),
                    ),
                    
                    align_items="center",
                    spacing="6",
                ),
                width="100%",
                padding_y=styles.Spacer.VERY_BIG.value,
                background="linear-gradient(135deg, #194264FF 0%, #0f2a42 100%)",
            ),
            
            # Misión - Responsive
            rx.center(
                rx.box(
                    # Desktop
                    rx.desktop_only(
                        rx.hstack(
                            rx.box(
                                rx.image(
                                    src="m1.jpg",
                                    width="100%",
                                    max_width="350px",
                                    transition="transform 0.6s ease",
                                    _hover={
                                        "transform": "scale(1.03)",
                                    }
                                ),
                                flex="1",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                padding=styles.Spacer.LARGE.value,
                                animation="fadeInLeft 0.8s ease-out",
                            ),
                            
                            rx.box(
                                rx.vstack(
                                    rx.heading(
                                        "Nuestra Misión",
                                        font_size=["22px", "26px", "30px"],
                                        color=Color_tx.Primary.value,
                                        font_weight="bold",
                                        margin_bottom=styles.Spacer.MEDIUM.value,
                                        text_align="left",
                                    ),
                                    rx.text(
                                        "Ser referente nacional en el mantenimiento, reparación y rehabilitación de equipos industriales, promoviendo la eficiencia y ofreciendo soluciones que impulsen la eficacia, calidad y rentabilidad, creando un entorno de trabajo seguro, saludable y sostenible para minimizar el impacto ambiental.",
                                        font_size=["14px", "16px", "17px"],
                                        color=Text_tx.Black.value,
                                        line_height="1.6",
                                        text_align="left",
                                    ),
                                    align_items="start",
                                    spacing="4",
                                ),
                                flex="2",
                                padding=styles.Spacer.LARGE.value,
                                animation="fadeInRight 0.8s ease-out 0.2s both",
                            ),
                            
                            spacing="5",
                            align_items="center",
                            width="100%",
                            max_width="1200px",
                        )
                    ),
                    
                    # Mobile/Tablet
                    rx.mobile_and_tablet(
                        rx.vstack(
                            rx.box(
                                rx.image(
                                    src="m1.jpg",
                                    width="100%",
                                    max_width="250px",
                                ),
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                padding=styles.Spacer.MEDIUM.value,
                                animation="fadeInUp 0.6s ease-out",
                            ),
                            
                            rx.box(
                                rx.vstack(
                                    rx.heading(
                                        "Nuestra Misión",
                                        font_size=["20px", "22px"],
                                        color=Color_tx.Primary.value,
                                        font_weight="bold",
                                        margin_bottom=styles.Spacer.SMALL.value,
                                        text_align="center",
                                    ),
                                    rx.text(
                                        "Ser referente nacional en el mantenimiento, reparación y rehabilitación de equipos industriales, promoviendo la eficiencia y ofreciendo soluciones que impulsen la eficacia, calidad y rentabilidad, creando un entorno de trabajo seguro, saludable y sostenible para minimizar el impacto ambiental.",
                                        font_size=["13px", "14px"],
                                        color=Text_tx.Black.value,
                                        line_height="1.5",
                                        text_align="center",
                                        font_weight="500",
                                    ),
                                    align_items="center",
                                    spacing="3",
                                ),
                                padding=styles.Spacer.MEDIUM.value,
                                animation="fadeInUp 0.6s ease-out 0.2s both",
                            ),
                            
                            spacing="3",
                            align_items="center",
                            width="100%",
                            max_width="1200px",
                        )
                    ),
                    
                    width="100%",
                    max_width="1200px",
                ),
                width="100%",
                padding_y=styles.Spacer.VERY_BIG.value,
                background="white",
            ),
            
            # Visión - Responsive
            rx.center(
                rx.box(
                    # Desktop
                    rx.desktop_only(
                        rx.hstack(
                            rx.box(
                                rx.vstack(
                                    rx.heading(
                                        "Nuestra Visión",
                                        font_size=["22px", "26px", "30px"],
                                        color=Color_tx.Primary.value,
                                        font_weight="bold",
                                        margin_bottom=styles.Spacer.MEDIUM.value,
                                        text_align="left",
                                    ),
                                    rx.text(
                                        "Aspiramos a transformar la gestión de activos industriales, garantizando la máxima disponibilidad de maquinarias y equipos, reduciendo costos y contribuyendo a un futuro industrial más seguro, innovador y sostenible.",
                                        font_size=["14px", "16px", "17px"],
                                        color=Text_tx.Black.value,
                                        line_height="1.6",
                                        text_align="left",
                                    ),
                                    align_items="start",
                                    spacing="4",
                                ),
                                flex="2",
                                padding=styles.Spacer.LARGE.value,
                                animation="fadeInLeft 0.8s ease-out 0.2s both",
                            ),
                            
                            rx.box(
                                rx.image(
                                    src="v3.jpg",
                                    width="100%",
                                    max_width="350px",
                                    transition="transform 0.6s ease",
                                    _hover={
                                        "transform": "scale(1.03)",
                                    }
                                ),
                                flex="1",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                padding=styles.Spacer.LARGE.value,
                                animation="fadeInRight 0.8s ease-out",
                            ),
                            
                            spacing="5",
                            align_items="center",
                            width="100%",
                            max_width="1200px",
                        )
                    ),
                    
                    # Mobile/Tablet
                    rx.mobile_and_tablet(
                        rx.vstack(
                            rx.box(
                                rx.image(
                                    src="v3.jpg",
                                    width="100%",
                                    max_width="250px",
                                ),
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                padding=styles.Spacer.MEDIUM.value,
                                animation="fadeInUp 0.6s ease-out",
                            ),
                            
                            rx.box(
                                rx.vstack(
                                    rx.heading(
                                        "Nuestra Visión",
                                        font_size=["20px", "22px"],
                                        color=Color_tx.Primary.value,
                                        font_weight="bold",
                                        margin_bottom=styles.Spacer.SMALL.value,
                                        text_align="center",
                                    ),
                                    rx.text(
                                        "Aspiramos a transformar la gestión de activos industriales, garantizando la máxima disponibilidad de maquinarias y equipos, reduciendo costos y contribuyendo a un futuro industrial más seguro, innovador y sostenible.",
                                        font_size=["13px", "14px"],
                                        color=Text_tx.Black.value,
                                        line_height="1.5",
                                        text_align="center",
                                        font_weight="500",
                                    ),
                                    align_items="center",
                                    spacing="3",
                                ),
                                padding=styles.Spacer.MEDIUM.value,
                                animation="fadeInUp 0.6s ease-out 0.2s both",
                            ),
                            
                            spacing="3",
                            align_items="center",
                            width="100%",
                            max_width="1200px",
                        )
                    ),
                    
                    width="100%",
                    max_width="1200px",
                ),
                width="100%",
                padding_y=styles.Spacer.VERY_BIG.value,
                background="linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 100%)",
            ),
            
            # NUEVA SECCIÓN: Política de Calidad
            quality_policy_section(),
            
            # Valores - Responsive
            rx.center(
                rx.vstack(
                    rx.heading(
                        "Nuestros Valores Fundamentales",
                        font_size=["18px", "20px", "22px", "26px", "30px"],
                        color=Color_tx.Primary.value,
                        text_align="center",
                        font_weight="bold",
                        margin_bottom=styles.Spacer.SMALL.value,
                        animation="fadeInUp 0.6s ease-out",
                    ),
                    rx.text(
                        "Los principios que guían cada una de nuestras acciones y decisiones",
                        font_size=["13px", "14px", "15px", "17px"],
                        color=Text_tx.Black.value,
                        text_align="center",
                        max_width="600px",
                        margin_bottom=styles.Spacer.LARGE.value,
                        animation="fadeInUp 0.6s ease-out 0.2s both",
                    ),
                    
                    # Grid de valores - Responsive
                    rx.box(
                        # Desktop - 3 columnas
                        rx.desktop_only(
                            rx.flex(
                                *[
                                    rx.box(
                                        value_card(
                                            value["icon"], 
                                            value["title"], 
                                            value["description"],
                                            i
                                        ),
                                        width="30%",
                                        margin_bottom=styles.Spacer.MEDIUM.value,
                                    )
                                    for i, value in enumerate(values)
                                ],
                                wrap="wrap",
                                justify="center",
                                spacing="4",
                                width="100%",
                                max_width="1200px",
                            )
                        ),
                        
                        # Tablet - 2 columnas
                        rx.tablet_only(
                            rx.flex(
                                *[
                                    rx.box(
                                        value_card(
                                            value["icon"], 
                                            value["title"], 
                                            value["description"],
                                            i
                                        ),
                                        width="45%",
                                        margin_bottom=styles.Spacer.MEDIUM.value,
                                    )
                                    for i, value in enumerate(values)
                                ],
                                wrap="wrap",
                                justify="center",
                                spacing="4",
                                width="100%",
                                max_width="1200px",
                            )
                        ),
                        
                        # Mobile - 1 columna
                        rx.mobile_only(
                            rx.vstack(
                                *[
                                    value_card(
                                        value["icon"], 
                                        value["title"], 
                                        value["description"],
                                        i
                                    )
                                    for i, value in enumerate(values)
                                ],
                                spacing="4",
                                width="100%",
                            )
                        ),
                        
                        width="100%",
                        max_width="1200px",
                    ),
                    align_items="center",
                    spacing="5",
                ),
                width="100%",
                padding_y=styles.Spacer.VERY_BIG.value,
                background="linear-gradient(135deg, #F0F7FF 0%, #FFFFFF 100%)",
            ),
            
            spacing="0",
            width="100%",
            padding_y=styles.Spacer.DEFAULT.value,
        ),
        # Estilos CSS para animaciones
        rx.html("""
            <style>
                @keyframes fadeInUp {
                    from {
                        opacity: 0;
                        transform: translateY(20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
                
                @keyframes fadeInLeft {
                    from {
                        opacity: 0;
                        transform: translateX(-20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateX(0);
                    }
                }
                
                @keyframes fadeInRight {
                    from {
                        opacity: 0;
                        transform: translateX(20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateX(0);
                    }
                }
                
                @keyframes countUp {
                    from {
                        opacity: 0;
                        transform: scale(0.8);
                    }
                    to {
                        opacity: 1;
                        transform: scale(1);
                    }
                }
            </style>
        """),
        width="100%",
    )