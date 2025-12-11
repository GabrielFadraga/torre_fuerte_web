import reflex as rx
import TFuerte.styles.styles as styles

def link_button(text: str, url: str, tag: str, is_external=True) -> rx.Component:
    return rx.link( 
        rx.button(
            rx.hstack(
                rx.icon(
                        tag,
                        #width=styles.Spacer.DEFAULT.value,
                        #height=styles.Spacer.DEFAULT.value,
                        #margin=styles.Spacer.DEFAULT.value,
                    ),
                rx.vstack(
                    rx.text(text, style=styles.button_title_style),
                    align_items="start",
                    width="100%",
                    ),
                ),
        size="4",
        variant="soft",
        color_scheme="indigo",
        width="100%",
        style=styles.button_title_style,
        body=styles.button_body_style,

    ), 
    width="100%",
    href=url,
    is_external=is_external,
)