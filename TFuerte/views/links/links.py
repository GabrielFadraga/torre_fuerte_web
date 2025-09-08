import reflex as rx
from TFuerte.components.link_button import link_button
from TFuerte.components.title import title
from TFuerte.routes import Route

def links() -> rx.Component:
    return rx.vstack(
        title("Nuestro trabajo"),
        link_button("Servicios", Route.SERVICES.value, "notebook-tabs", is_external=False),
        link_button("Proyectos", Route.PROJECTS.value, "folder-open-dot", is_external=False),

        title("Nuestras redes"),
        link_button("Facebook", "https://www.facebook.com/torrefuerte.surl", "facebook", is_external=True),
        link_button("Instagram", "https://www.instagram.com/torre_fuerte_surl?igsh=NGdkZDJxZnluNnM=", "instagram", is_external=True),

        title("Atención al cliente"),
        link_button("Whatsapp", "https://wa.me/message/OKIP2WN55MKEK1", "square-user", is_external=True),
        link_button("Gmail", "https://mail.google.com/mail/?view=cm&fs=1&to=maidomm78@gmail.com", "mail-minus", is_external=True),

        title("Más información"),
        link_button("Sobre nosotros", Route.ABOUT.value, "building-2", is_external=False),
        link_button("Nuestro equipo", Route.TEAM.value, "user-round", is_external=False),
        width="100%",
    )