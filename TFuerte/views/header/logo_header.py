import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles
from TFuerte.styles.colors import Text_tx

def logo() -> rx.Component:
    return rx.hstack(
        rx.image(
            src="sf.png",
            height="50em",
        ),
        
        rx.vstack(
            rx.hstack(
        rx.heading(
                "Mensaje del presidente",
                size="8",
                margin="1em"
            ),
            rx.vstack( 
        rx.text("""Es un honor presentarles Torre Fuerte SURL, su aliado estratégico en soluciones 
                industriales integrales. Con la mirada siempre en lo alto, nos hemos consolidado 
                como referentes nacionales en el mantenimiento, reparación y rehabilitación de 
                equipos industriales, brindando servicios especializados en las áreas de mecánica,
                electricidad y automática.""",
                width="100%",
                font_size=styles.Spacer.BIG.value,
                margin="1em"
                ),
                    rx.text("""Nuestro valor diferencial radica en la combinación de expertise técnico, 
                            tecnologías avanzadas y un enfoque orientado a resultados tangibles que 
                            impactan positivamente en su productividad y rentabilidad. Confíe en Torre 
                            Fuerte para elevar los estándares de performance de sus operaciones industriales. 
                            Estamos comprometidos con su éxito operativo y nos dedicamos a construir relaciones 
                            a largo plazo basadas en la excelencia, confiabilidad y valor agregado.""",
                width="100%",
                font_size=styles.Spacer.BIG.value,
                margin="1em"
                ),
                rx.text(""" "En Torre Fuerte, elevamos cada proyecto con la convicción de que su éxito industrial 
                            es nuestro compromiso más firme" """,
                width="100%",
                font_size=styles.Spacer.BIG.value,
                margin="1em"
                ),
                rx.text("Presidente: Lic. Maykel Torres López",
                width="100%",
                font_size=styles.Spacer.LARGE.value,
                padding_x="510px"
                ),
                width="100%",
                spacing="1",
            ),
                
                width="100%",
                spacing="9"
                
        ),

        spacing="2",
        width="100%",
        color=Text_tx.Black.value,
        #font_size=styles.Spacer.BIG.value,
        #style=styles.title_style,
        #weight="bold",

    ),
        
        """rx.image(
            src="tf12.jpg",
            height="40em",
            border_radius="2em 2em",
            margin="2em"
        ),"""
    )