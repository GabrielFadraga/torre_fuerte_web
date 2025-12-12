import reflex as rx
from TFuerte.components.info_text import info_text
import TFuerte.styles.styles as styles
from TFuerte.styles.colors import Text_tx, Color_tx

class ExampleState(rx.State):
    # A base var for the list of colors to cycle through.
    colors: list[str] = ["black", "red", "green", "blue", "purple"]

    # A base var for the index of the current color.
    index: int = 0

    @rx.event
    def next_color(self):
        """An event handler to go to the next color."""
        # Event handlers can modify the base vars.
        # Here we reference the base vars `colors` and `index`.
        self.index = (self.index + 1) % len(self.colors)

    @rx.var
    def color(self) -> str:
        """A computed var that returns the current color."""
        # Computed vars update automatically when the state changes.
        return self.colors[self.index]


def event1():
    return rx.heading(
        "ESTAMOS ACTUALIZANDO LA SECCIÓN ACTUAL",
        # Event handlers can be bound to event triggers.
        on_click=ExampleState.next_color,
        # State vars can be bound to component props.
        color=ExampleState.color,
        _hover={"cursor": "pointer"},
    )