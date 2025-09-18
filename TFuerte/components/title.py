import reflex as rx
import TFuerte.styles.styles as styles
from TFuerte.styles.colors import Text_tx 

def title(text: str) -> rx.Component:
        return rx.text(
                        text,
                        style=styles.title_style,
                        size="9",
                        #font_size=styles.Spacer.BIG.value,
                        color=Text_tx.Header.value,
                        weight="medium",
        )