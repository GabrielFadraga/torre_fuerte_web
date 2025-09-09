import reflex as rx
import datetime
from TFuerte.styles.colors import Text_tx 

def footer() -> rx.Component:
    return rx.vstack(
        rx.image(src="torre.png", border_radius="15px 15px", height="50px"),
        rx.link(f"2024 - {datetime.date.today().year} by:torrefuertemipyme", 
                href="https://www.instagram.com/torre_fuerte_surl?igsh=NGdkZDJxZnluNnM=",
                is_external=True,
                color=Text_tx.Footer.value),
                

        rx.text("BULIDING SOFTWARE WITH ❤️ FROM HAVANA"),
        align_items="center",
        margin_bottom="32px",
        font_size="14px",
        spacing="1",
        color=Text_tx.Footer.value
    )