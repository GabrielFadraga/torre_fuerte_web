import reflex as rx
import TFuerte.styles.styles as styles

def title(text: str) -> rx.Component:
        return rx.heading(
                        text,
                        style=styles.title_style,
                        font_size=styles.Spacer.BIG.value,
        )