import reflex as rx
import TFuerte.styles.styles as styles
from TFuerte.styles.colors import Text_tx 

def title(text: str) -> rx.Component:
        return rx.text(
                        text,
                        style=styles.title_style,
                        font_size=styles.Spacer.BIG.value,
                        color=Text_tx.Black.value,
                        weight="medium"
        )