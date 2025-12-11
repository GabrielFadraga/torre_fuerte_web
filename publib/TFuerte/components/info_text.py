import reflex as rx

def info_text(title: str, body: str) -> rx.Component:
    return rx.box(
        rx.text.strong(title), 
        " ",
         body,
        as_="title",
        )
