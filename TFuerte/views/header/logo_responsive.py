import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles
from TFuerte.styles.colors import Text_tx

def logo_resp() -> rx.Component:
    return rx.vstack(
        rx.image(
            src="sf.png",
            height="35em",
        ),
        rx.heading(
                "Mensaje del presidente",
                margin="0.5em",
                color="black",
                font_size=styles.Spacer.LARGE.value,
            ),
        rx.text("""Es un honor presentarles Torre Fuerte SURL, su aliado estratégico en soluciones 
                industriales integrales. Con la mirada siempre en lo alto, nos hemos consolidado 
                como referentes nacionales en el mantenimiento, reparación y rehabilitación de 
                equipos industriales, brindando servicios especializados en las áreas de mecánica,
                electricidad y automática.""",
                font_size=styles.Spacer.DEFAULT.value,
                margin=styles.Spacer.MEDIUM.value,
                color="black",
                ),
                rx.text("""Nuestro valor diferencial radica en la combinación de expertise técnico, 
                        tecnologías avanzadas y un enfoque orientado a resultados tangibles que 
                        impactan positivamente en su productividad y rentabilidad. Confíe en Torre 
                        Fuerte para elevar los estándares de performance de sus operaciones industriales. 
                        Estamos comprometidos con su éxito operativo y nos dedicamos a construir relaciones 
                        a largo plazo basadas en la excelencia, confiabilidad y valor agregado.""",
                font_size=styles.Spacer.DEFAULT.value,
                margin=styles.Spacer.MEDIUM.value,
                color="black",
                ),
                rx.text(""" "En Torre Fuerte, elevamos cada proyecto con la convicción de que su éxito industrial 
                        es nuestro compromiso más firme" """,
                font_size=styles.Spacer.DEFAULT.value,
                margin=styles.Spacer.MEDIUM.value,
                color="black",
                ),
                rx.text("Presidente: Lic. Maykel Torres López",
                font_size=styles.Spacer.MEDIUM.value,
                margin=styles.Spacer.SMALL.value,
                padding_x=styles.Spacer.SMS_P.value,
                color="black",
                ),

    spacing="2",
    width="100%",
    justify="center",
)