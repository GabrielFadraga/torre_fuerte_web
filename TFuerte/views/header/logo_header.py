import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles
from TFuerte.styles.colors import Text_tx, Color_tx

def president_message() -> rx.Component:
    return rx.vstack(
        # Hero Section renovada con logo sobre fondo blanco
        rx.box(
            rx.hstack(
                # Columna izquierda - Logo sobre fondo blanco
                rx.box(
                    rx.vstack(
                        rx.image(
                            src="sf.png",
                            height="400px",
                            width="auto",
                            filter="drop-shadow(0 15px 40px rgba(25, 66, 100, 0.2))",
                            transition="transform 0.5s ease",
                            _hover={
                                "transform": "scale(1.02)",
                            }
                        ),
                        align_items="center",
                        justify="center",
                        height="100%",
                    ),
                    flex="1",
                    min_width="400px",
                    padding=styles.Spacer.VERY_BIG.value,
                    background="white",
                    position="relative",
                    border_right="1px solid #e2e8f0",
                ),
                
                # Columna derecha - Presentación
                rx.box(
                    rx.vstack(
                        rx.box(
                            "MENSAJE INSTITUCIONAL",
                            color="#194264",
                            font_size="14px",
                            font_weight="bold",
                            letter_spacing="3px",
                            margin_bottom="20px",
                            text_transform="uppercase",
                            opacity="0.8",
                        ),
                        
                        rx.heading(
                            "Soluciones industriales basadas en resultados.",
                            size="9",
                            color="#194264",
                            font_weight="bold",
                            text_align="left",
                            line_height="1.1",
                            margin_bottom="16px",
                        ),
                        
                        rx.text(
                            "Lic. Maikel Torres López - Presidente",
                            font_size="20px",
                            color="#64748b",
                            font_weight="medium",
                            text_align="left",
                            letter_spacing="0.5px",
                            margin_bottom="30px",
                        ),
                        
                        # Línea decorativa
                        rx.box(
                            width="80px",
                            height="4px",
                            background="linear-gradient(90deg, #194264, #2a5a8a)",
                            margin_bottom="40px",
                            border_radius="2px",
                        ),
                        
                        # Texto de introducción
                        rx.box(
                            rx.text(
                                "Es un honor presentarles Torre Fuerte SURL, su aliado estratégico en soluciones "
                                "industriales integrales. Nos hemos consolidado "
                                "como referentes nacionales en el mantenimiento y rehabilitación de equipos industriales.",
                                font_size="18px",
                                color="#194264",
                                line_height="1.7",
                                font_weight="500",
                            ),
                            width="100%",
                            padding="24px",
                            background="linear-gradient(135deg, rgba(25, 66, 100, 0.05) 0%, rgba(42, 90, 138, 0.02) 100%)",
                            border_left="4px solid #194264",
                            border_radius="0 8px 8px 0",
                            margin_bottom="20px",
                        ),
                        
                        align_items="start",
                        spacing="4",
                        height="100%",
                        justify="center",
                    ),
                    flex="2",
                    padding=styles.Spacer.VERY_BIG.value,
                    background="linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%)",
                ),
                
                align_items="stretch",
                spacing="0",
                width="100%",
                min_height="600px",
            ),
            width="100%",
            background="white",
        ),
        
        # Sección de valor diferencial
        rx.box(
            rx.hstack(
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "Nuestro Compromiso con la Excelencia",
                            size="6",
                            color="#194264",
                            margin_bottom="24px",
                            font_weight="bold",
                        ),
                        rx.text(
                            "Nuestro valor diferencial radica en la combinación de experticia técnica, "
                            "tecnologías avanzadas y un enfoque orientado a resultados tangibles que "
                            "impactan positivamente en su productividad y rentabilidad.",
                            font_size="17px",
                            color="#194264",
                            line_height="1.7",
                            margin_bottom="20px",
                        ),
                        rx.text(
                            "Confíe en Torre Fuerte para elevar los estándares de rendimiento de sus operaciones industriales. "
                            "Estamos comprometidos con su éxito operacional y nos dedicamos a construir relaciones "
                            "a largo plazo basadas en la excelencia, confiabilidad y valor agregado.",
                            font_size="17px",
                            color="#194264",
                            line_height="1.7",
                            opacity="0.9",
                        ),
                        align_items="start",
                        spacing="4",
                    ),
                    flex="1",
                    padding=styles.Spacer.VERY_BIG.value,
                ),
                
                rx.box(
                    rx.vstack(
                        rx.box(
                            width="100%",
                            height="300px",
                            background="linear-gradient(135deg, #194264 0%, #2a5a8a 100%)",
                            border_radius="12px",
                            position="relative",
                            overflow="hidden",
                            _before={
                                "content": "''",
                                "position": "absolute",
                                "top": "0",
                                "left": "0",
                                "right": "0",
                                "bottom": "0",
                                "background": "radial-gradient(circle at 30% 70%, rgba(255,255,255,0.1) 0%, transparent 50%)",
                            }
                        ),
                        align_items="center",
                        justify="center",
                        height="100%",
                    ),
                    flex="1",
                    min_width="400px",
                ),
                
                align_items="center",
                spacing="0",
                width="100%",
            ),
            width="100%",
            background="linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 100%)",
        ),
        
        # Cita del presidente
        rx.box(
            rx.center(
                rx.vstack(
                    rx.box(
                        rx.text(
                            '"En Torre Fuerte, abordamos cada proyecto con la convicción de que su éxito industrial '
                            'es nuestro compromiso más firme"',
                            font_size=["24px", "26px", "28px"],
                            color="#194264",
                            font_style="italic",
                            font_weight="600",
                            line_height="1.5",
                            text_align="center",
                            max_width="800px",
                        ),
                        width="100%",
                        padding=styles.Spacer.VERY_BIG.value,
                        background="white",
                        border_radius="16px",
                        box_shadow="0 10px 40px rgba(25, 66, 100, 0.1)",
                        position="relative",
                        overflow="hidden",
                        _before={
                            "content": "''",
                            "position": "absolute",
                            "top": "0",
                            "left": "0",
                            "width": "6px",
                            "height": "100%",
                            "background": "linear-gradient(180deg, #194264, #2a5a8a)",
                        }
                    ),
                    align_items="center",
                    spacing="6",
                ),
                width="100%",
            ),
            width="100%",
            padding=styles.Spacer.VERY_BIG.value,
            background="linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%)",
        ),
        
        # Sección de contacto y firma
        rx.box(
            rx.hstack(
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "Contacto Directivo",
                            size="6",
                            color="#194264",
                            margin_bottom="24px",
                            font_weight="bold",
                        ),
                        
                        rx.vstack(
                            rx.text(
                                "Lic. Maikel Torres López",
                                font_size="18px",
                                color="#194264",
                                font_weight="bold",
                                margin_bottom="4px",
                            ),
                            rx.text(
                                "Presidente",
                                font_size="16px",
                                color="#64748b",
                                margin_bottom="20px",
                            ),
                            rx.link(
                            rx.button(
                                "Solicitar Reunión Ejecutiva",
                                background="linear-gradient(135deg, #194264 0%, #2a5a8a 100%)",
                                color="white",
                                padding_x="30px",
                                padding_y="16px",
                                font_size="16px",
                                font_weight="bold",
                                border_radius="8px",
                                box_shadow="0 4px 15px rgba(25, 66, 100, 0.3)",
                                transition="all 0.3s ease",
                                _hover={
                                    "transform": "translateY(-2px)",
                                    "box_shadow": "0 8px 25px rgba(25, 66, 100, 0.4)",
                                    "background": "linear-gradient(135deg, #2a5a8a 0%, #194264 100%)",
                                },
                            ),
                            href="https://wa.me/message/OKIP2WN55MKEK1",
                            is_external=True,
                            width="100%",
                        ),
                            align_items="start",
                            spacing="3",
                        ),
                        
                        align_items="start",
                        spacing="6",
                    ),
                    flex="1",
                    padding=styles.Spacer.VERY_BIG.value,
                ),
                
                rx.box(
                    rx.vstack(
                        # Firma del presidente con animación
                        rx.box(
                            rx.vstack(
                                rx.image(
                                    src="maykeltf.png",
                                    height="80px",
                                    width="auto",
                                    margin_bottom="16px",
                                    filter="drop-shadow(0 5px 15px rgba(0,0,0,0.1))",
                                    transition="transform 0.3s ease",
                                    _hover={
                                        "transform": "scale(1.05)",
                                    }
                                ),
                                rx.box(
                                    width="150px",
                                    height="1px",
                                    background="linear-gradient(90deg, transparent, #194264, transparent)",
                                    margin_bottom="16px",
                                ),
                                rx.text(
                                    "Firma del Presidente",
                                    font_size="14px",
                                    color="#64748b",
                                    font_style="italic",
                                ),
                                align_items="center",
                                spacing="2",
                            ),
                            width="100%",
                            padding="24px",
                            background="white",
                            border_radius="8px",
                            box_shadow="0 4px 12px rgba(0,0,0,0.05)",
                            transition="all 0.3s ease",
                            _hover={
                                "box_shadow": "0 8px 25px rgba(0,0,0,0.1)",
                                "transform": "translateY(-5px)",
                            }
                        ),
                        
                        align_items="center",
                        spacing="6",
                        height="100%",
                    ),
                    flex="1",
                    padding=styles.Spacer.VERY_BIG.value,
                    background="linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 100%)",
                ),
                
                align_items="start",
                spacing="0",
                width="100%",
            ),
            width="100%",
            background="white",
        ),

        # Sección de ubicación en formato horizontal (como footer minimalista)
        rx.box(
            rx.hstack(
                # Información de ubicación
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "Nuestra Sede Corporativa",
                            size="5",
                            color="#194264",
                            margin_bottom="16px",
                            font_weight="bold",
                        ),
                        rx.hstack(
                            rx.vstack(
                                rx.text(
                                    "📍 Calle E, esquina 15, Vedado",
                                    font_size="16px",
                                    color="#194264",
                                    font_weight="500",
                                    margin_bottom="4px",
                                ),
                                rx.text(
                                    "Plaza de la Revolución, La Habana, Cuba",
                                    font_size="16px",
                                    color="#194264",
                                    font_weight="500",
                                ),
                                align_items="start",
                                spacing="2",
                            ),
                            rx.box(
                                width="2px",
                                height="40px",
                                background="linear-gradient(180deg, #194264, #2a5a8a)",
                                margin_x="40px",
                                opacity="0.5",
                            ),
                            rx.image(
                                src="ubu.jpg",
                                width="200px",
                                height="120px",
                                object_fit="cover",
                                border_radius="12px",
                                box_shadow="0 4px 12px rgba(0,0,0,0.1)",
                                transition="all 0.3s ease",
                                _hover={
                                    "transform": "scale(1.05)",
                                    "box_shadow": "0 8px 20px rgba(0,0,0,0.15)",
                                }
                            ),
                            align_items="center",
                            justify="center",
                            spacing="4",
                            width="100%",
                        ),
                        align_items="center",
                        spacing="4",
                    ),
                    width="100%",
                    padding=styles.Spacer.LARGE.value,
                ),
                
                align_items="center",
                justify="center",
                width="100%",
            ),
            width="100%",
            padding_y=styles.Spacer.VERY_BIG.value,
            background="white",
            border_top="1px solid #e2e8f0",
            # Animación sutil de entrada
            opacity="0",
            animation="fadeInUp 0.8s ease-out forwards",
            style={
                "@keyframes fadeInUp": {
                    "0%": {
                        "opacity": "0",
                        "transform": "translateY(30px)"
                    },
                    "100%": {
                        "opacity": "1",
                        "transform": "translateY(0)"
                    }
                }
            }
        ),
        
        spacing="0",
        width="100%",
        align_items="center",
        background="#FFFFFF",
    )

def president_message_mobile() -> rx.Component:
    return rx.vstack(
        # Header móvil
        rx.box(
            rx.center(
                rx.vstack(
                    rx.image(
                        src="sf.png",
                        height="200px",
                        width="auto",
                        filter="drop-shadow(0 8px 20px rgba(25, 66, 100, 0.2))",
                        margin_bottom=styles.Spacer.MEDIUM.value,
                    ),
                    rx.box(
                        width="120px",
                        height="3px",
                        background="linear-gradient(90deg, #194264, #2a5a8a)",
                        margin_bottom="20px",
                    ),
                    rx.box(
                        "MENSAJE INSTITUCIONAL",
                        color="#194264",
                        font_size="12px",
                        font_weight="bold",
                        letter_spacing="2px",
                        text_transform="uppercase",
                        opacity="0.8",
                    ),
                    rx.heading(
                        "Soluciones industriales basadas en resultados.",
                        size="6",
                        color="#194264",
                        font_weight="bold",
                        text_align="center",
                        line_height="1.2",
                        margin_top="16px",
                    ),
                    rx.text(
                        "Lic. Maikel Torres López - Presidente",
                        font_size="16px",
                        color="#64748b",
                        font_weight="medium",
                        text_align="center",
                    ),
                    align_items="center",
                    spacing="4",
                ),
                width="100%",
            ),
            width="100%",
            padding_y=styles.Spacer.VERY_BIG.value,
            background="white",
        ),
        
        # Contenido móvil
        rx.vstack(
            # Introducción
            rx.box(
                rx.vstack(
                    rx.heading(
                        "Nuestro Compromiso",
                        size="5",
                        color="#194264",
                        margin_bottom="16px",
                        font_weight="bold",
                    ),
                    rx.text(
                        "Es un honor presentarles Torre Fuerte SURL, su aliado estratégico en soluciones "
                        "industriales integrales. Nos hemos consolidado "
                        "como referentes nacionales en el mantenimiento y rehabilitación de equipos industriales.",
                        font_size="16px",
                        color="#194264",
                        line_height="1.7",
                    ),
                    align_items="start",
                    spacing="4",
                ),
                width="100%",
                padding=styles.Spacer.LARGE.value,
                background="white",
                border_left="4px solid #194264",
            ),
            
            # Valor diferencial
            rx.box(
                rx.vstack(
                    rx.text(
                        "Nuestro valor diferencial radica en la combinación de experticia técnica, "
                        "tecnologías avanzadas y un enfoque orientado a resultados tangibles que "
                        "impactan positivamente en su productividad y rentabilidad.",
                        font_size="16px",
                        color="#194264",
                        line_height="1.7",
                    ),
                    align_items="start",
                    spacing="4",
                ),
                width="100%",
                padding=styles.Spacer.LARGE.value,
            ),
            
            # Cita
            rx.box(
                rx.vstack(
                    rx.text(
                        '"En Torre Fuerte, abordamos cada proyecto con la convicción de que su éxito industrial '
                        'es nuestro compromiso más firme"',
                        font_size="18px",
                        color="#194264",
                        font_style="italic",
                        font_weight="600",
                        line_height="1.5",
                        text_align="center",
                    ),
                    rx.box(
                        width="80px",
                        height="2px",
                        background="linear-gradient(90deg, #194264, #2a5a8a)",
                        margin_top="20px",
                    ),
                    align_items="center",
                    spacing="4",
                ),
                width="100%",
                padding=styles.Spacer.LARGE.value,
                background="linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 100%)",
                border="1px solid rgba(25, 66, 100, 0.1)",
                margin_y=styles.Spacer.LARGE.value,
            ),
            
            # Contacto
            rx.vstack(
                rx.text(
                    "Lic. Maikel Torres López",
                    font_size="18px",
                    color="#194264",
                    font_weight="bold",
                ),
                rx.text(
                    "Presidente - Torre Fuerte SURL",
                    font_size="15px",
                    color="#64748b",
                ),
                rx.link(
                rx.button(
                    "Solicitar Reunión",
                    background="linear-gradient(135deg, #194264 0%, #2a5a8a 100%)",
                    color="white",
                    width="100%",
                    margin_top="20px",
                    padding_y="14px",
                ),
                href="https://wa.me/message/OKIP2WN55MKEK1",
                is_external=True,
                width="100%",
            ),
                align_items="center",
                spacing="2",
                width="100%",
                padding=styles.Spacer.LARGE.value,
            ),

            # Ubicación en móvil
            rx.box(
                rx.vstack(
                    rx.heading(
                        "Nuestra Sede",
                        size="5",
                        color="#194264",
                        margin_bottom="16px",
                        font_weight="bold",
                        text_align="center",
                    ),
                    rx.text(
                        "📍 Calle E, esquina 15, Vedado",
                        font_size="16px",
                        color="#194264",
                        font_weight="500",
                        margin_bottom="4px",
                        text_align="center",
                    ),
                    rx.text(
                        "Plaza de la Revolución",
                        font_size="16px",
                        color="#194264",
                        font_weight="500",
                        margin_bottom="4px",
                        text_align="center",
                    ),
                    rx.text(
                        "La Habana, Cuba",
                        font_size="16px",
                        color="#194264",
                        font_weight="500",
                        margin_bottom="16px",
                        text_align="center",
                    ),
                    rx.image(
                        src="ubu.jpg",
                        width="100%",
                        height="200px",
                        object_fit="cover",
                        border_radius="12px",
                        margin_bottom="20px",
                    ),
                    align_items="center",
                    spacing="3",
                ),
                width="100%",
                padding=styles.Spacer.LARGE.value,
                background="white",
                border_top="1px solid #e2e8f0",
            ),
            
            spacing="4",
            width="100%",
        ),
        
        spacing="0",
        width="100%",
    )

def logo() -> rx.Component:
    return rx.box(
        rx.desktop_only(president_message()),
        rx.mobile_and_tablet(president_message_mobile()),
        width="100%",
    )