import reflex as rx
from TFuerte.styles.colors import Text_tx, Color_tx
from rxconfig import config
from TFuerte.routes import Route
import TFuerte.styles.styles as styles


@rx.page(
    route=Route.NEW.value,
    title="Nuestros proyectos",
    description="Aquí evidenciamos los logros de Torre Fuerte",
    image="tff.png"
)

# Definimos la estructura de la página
def new() -> rx.Component:
    return rx.vstack(
        # Header/Navbar
        rx.hstack(
            rx.vstack(
                rx.heading("TORRE FUERTE", size="9", color="white"),
                rx.text("Con la mirada en lo alto", color="white", size="5"),
                spacing="1"
            ),
            rx.spacer(),
            rx.hstack(
                rx.link("Inicio", href="#inicio", color="white", _hover={"color": "orange"}, size="6"),
                rx.link("Servicios", href="#servicios", color="white", _hover={"color": "orange"}, size="6"),
                rx.link("Nosotros", href="#nosotros", color="white", _hover={"color": "orange"}, size="6"),
                rx.link("Contacto", href="#contacto", color="white", _hover={"color": "orange"}, size="6"),
                spacing="4"
            ),
            background_color="#355B7F",
            padding="1.5rem",
            position="sticky",
            top="0",
            z_index="1000",
            width="100%"
        ),
        
        # Hero Section
        rx.center(
            rx.vstack(
                rx.heading(
                    "Expertos en Soluciones Industriales", 
                    size="8", 
                    color="white",
                    text_align="center"
                ),
                rx.text(
                    "Brindamos servicios de reparación, mantenimiento y rehabilitación de equipos industriales con los más altos estándares de calidad.",
                    color="white",
                    text_align="center",
                    max_width="600px"
                ),
                rx.link(
                    rx.button(
                        "Contáctanos",
                        background_color="orange",
                        color="white",
                        _hover={"background_color": "orange"}
                    ),
                    href="#contacto"
                ),
                spacing="5",
                align="center"
            ),
            background_image="linear-gradient(rgba(13, 59, 102, 0.8), rgba(13, 59, 102, 0.9))",
            #background_size="cover",
            background_position="center",
            height="500px",
            width="100%",
            id="inicio"
        ),
        
        # Services Section
        rx.box(
            rx.vstack(
                rx.heading("Nuestros Servicios", size="7", color="blue", text_align="center"),
                rx.text("Soluciones integrales para la industria", color="gray", text_align="center"),
                rx.hstack(
                    rx.box(
                        rx.vstack(
                            rx.image(src="tf1.png", width="50px", height="50px"),
                            rx.heading("Mecánica Industrial", size="5", color="blue"),
                            rx.text("Reparación y mantenimiento de maquinaria industrial, fabricación de piezas y componentes mecánicos.", color="gray.600", text_align="center"),
                            align="center",
                            spacing="3"
                        ),
                        background_color="white",
                        padding="2rem",
                        border_radius="lg",
                        box_shadow="lg",
                        width="100%"
                    ),
                    rx.box(
                        rx.vstack(
                            rx.image(src="tf3.png", width="50px", height="50px"),
                            rx.heading("Electricidad Industrial", size="5", color="blue"),
                            rx.text("Instalación, mantenimiento y reparación de sistemas eléctricos industriales y automatización.", color="gray", text_align="center"),
                            align="center",
                            spacing="3"
                        ),
                        background_color="white",
                        padding="2rem",
                        border_radius="lg",
                        box_shadow="lg",
                        width="100%"
                    ),
                    rx.box(
                        rx.vstack(
                            rx.image(src="tf2.png", width="50px", height="50px"),
                            rx.heading("Automatización", size="5", color="blue"),
                            rx.text("Diseño e implementación de sistemas de control automático para procesos industriales.", color="gray", text_align="center"),
                            align="center",
                            spacing="3"
                        ),
                        background_color="white",
                        padding="2rem",
                        border_radius="lg",
                        box_shadow="lg",
                        width="100%"
                    ),
                    spacing="5",
                    width="100%",
                    justify="center",
                    flex_direction=["column", "column", "row"]
                ),
                spacing="5",
                width="100%",
                max_width="1200px",
                align="center",
                padding_y="4rem"
            ),
            background_color="gray",
            display="flex",
            justify_content="center",
            id="servicios"
        ),
        
        # About Section
        rx.box(
            rx.hstack(
                rx.vstack(
                    rx.heading("Torre Fuerte", size="7", color="blue"),
                    rx.text(
                        "Nos dedicamos a brindar servicios de reparación, mantenimiento y rehabilitación de equipos industriales en las especialidades de mecánica, electricidad y automática.",
                        color="gray"
                    ),
                    rx.text(
                        "Contamos con talleres de mecánica industrial equipados con máquinas y herramientas de última generación, operados por técnicos altamente capacitados y con amplia experiencia en el sector.",
                        color="gray"
                    ),
                    rx.text(
                        "Nuestra filosofía se basa en la excelencia técnica, la responsabilidad y el compromiso con nuestros clientes, siempre con la mirada en lo alto, buscando superar expectativas y brindar soluciones que agreguen valor a sus operaciones.",
                        color="gray"
                    ),
                    spacing="4",
                    align="start",
                    width="100%"
                ),
                rx.image(
                    src="https://images.unsplash.com/photo-1581094794329-c8112a89af12?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
                    alt="Taller de Torre Fuerte",
                    border_radius="lg",
                    box_shadow="lg",
                    width="100%",
                    max_width="500px"
                ),
                spacing="5",
                width="100%",
                max_width="1500px",
                flex_direction=["column", "column", "row"]
            ),
            display="flex",
            justify_content="center",
            padding_y="4rem",
            background_color="white",
            id="nosotros"
        ),
        
        # Footer
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.heading("Torre Fuerte", size="5", color="white"),
                        rx.text("Empresa líder en servicios industriales especializados, con años de experiencia brindando soluciones confiables y de alta calidad.", color="gray"),
                        rx.hstack(
                            rx.link(rx.image(src="user1.png", width="30px", height="30px"), href="#"),
                            rx.link(rx.image(src="user1.png", width="30px", height="30px"), href="#"),
                            rx.link(rx.image(src="user1.png", width="30px", height="30px"), href="#"),
                            rx.link(rx.image(src="user1.png", width="30px", height="30px"), href="#"),
                            spacing="3"
                        ),
                        align="start",
                        spacing="3"
                    ),
                    rx.vstack(
                        rx.heading("Servicios", size="5", color="white"),
                        rx.link("Mecánica Industrial", href="#", color="gray"),
                        rx.link("Electricidad Industrial", href="#", color="gray"),
                        rx.link("Automatización", href="#", color="gray"),
                        rx.link("Mantenimiento Preventivo", href="#", color="gray"),
                        rx.link("Rehabilitación de Equipos", href="#", color="gray"),
                        align="start",
                        spacing="2"
                    ),
                    rx.vstack(
                        rx.heading("Contacto", size="5", color="white"),
                        rx.text("Av. Industrial 123, Zona Industrial", color="gray"),
                        rx.text("(123) 456-7890", color="gray"),
                        rx.text("info@torrefuerte.com", color="gray"),
                        rx.text("Lun-Vie: 8:00 - 18:00", color="gray"),
                        align="start",
                        spacing="2"
                    ),
                    spacing="5",
                    width="100%",
                    max_width="1200px",
                    flex_direction=["column", "column", "row", "row"]
                ),
                rx.divider(border_color="gray"),
                rx.text("© 2023 Torre Fuerte - Todos los derechos reservados", color="gray"),
                spacing="5",
                width="100%",
                max_width="1200px",
                align="center"
            ),
            background_color="orange",
            padding="2rem",
            display="flex",
            justify_content="center",
            id="contacto"
        ),
        width="100%",
        spacing="0"
    )