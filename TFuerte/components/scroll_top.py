import reflex as rx

def scroll_to_top() -> rx.Component:
    return rx.box(
        # Botón simple y visible
        rx.button(
            rx.icon(
                tag="arrow-up",
                color="white",
            ),
            # Estilos básicos
            background="#194264FF",
            border_radius="50%",
            width="50px",
            height="50px",
            padding="0",
            display="flex",
            align_items="center",
            justify_content="center",
            position="fixed",
            bottom="20px",
            right="20px",
            z_index="10000",
            # Efectos hover
            _hover={
                "background": "#0f2a42",
                "transform": "scale(1.1)",
            },
            # Transición
            transition="all 0.3s ease",
            # Sombra
            box_shadow="0 4px 12px rgba(0, 0, 0, 0.3)",
            # Acción
            on_click=rx.call_script("window.scrollTo({top: 0, behavior: 'smooth'})"),
        ),
        # Script simple para mostrar/ocultar
        rx.script(
            """
            // Mostrar el botón cuando se haga scroll
            window.addEventListener('scroll', function() {
                const scrollY = window.scrollY;
                const button = document.querySelector('[data-scroll-top]');
                if (scrollY > 300) {
                    button.style.display = 'flex';
                } else {
                    button.style.display = 'none';
                }
            });
            
            // Inicializar estado
            document.querySelector('[data-scroll-top]').style.display = 'none';
            """
        ),
        # Identificador para el script
        **{"data-scroll-top": True}
    )

# Versión alternativa usando estado de Reflex (más confiable)
class ScrollState(rx.State):
    show_button: bool = False
    
    def on_scroll(self, scroll_position: dict):
        # Mostrar botón después de 300px de scroll
        self.show_button = scroll_position["scrollY"] > 300
    
    def scroll_to_top(self):
        # Devolver el comando JavaScript para scroll suave
        return rx.call_script("window.scrollTo({top: 0, behavior: 'smooth'})")

def scroll_to_top_state() -> rx.Component:
    return rx.box(
        # Escuchar eventos de scroll
        rx.html(
            """
            <script>
                // Función para enviar posición de scroll al estado
                function trackScroll() {
                    const scrollY = window.scrollY;
                    window.dispatchEvent(new CustomEvent('reflex_scroll', {
                        detail: { scrollY: scrollY }
                    }));
                }
                
                window.addEventListener('scroll', trackScroll);
                window.addEventListener('load', trackScroll);
            </script>
            """
        ),
        # Botón controlado por estado
        rx.cond(
            ScrollState.show_button,
            rx.button(
                rx.icon(
                    tag="arrow-up",
                    color="white",
                    font_size="20px",
                ),
                background="#194264FF",
                border_radius="50%",
                width="55px",
                height="55px",
                padding="0",
                display="flex",
                align_items="center",
                justify_content="center",
                position="fixed",
                bottom="25px",
                right="25px",
                z_index="10000",
                _hover={
                    "background": "#0f2a42",
                    "transform": "scale(1.15)",
                    "box_shadow": "0 6px 20px rgba(25, 66, 100, 0.4)",
                },
                border="2px solid rgba(255,255,255,0.2)",
                transition="all 0.3s ease",
                box_shadow="0 4px 15px rgba(0, 0, 0, 0.3)",
                on_click=ScrollState.scroll_to_top,
            )
        ),
        # Escuchar el evento personalizado de scroll
        rx.html(
            """
            <script>
                window.addEventListener('reflex_scroll', (event) => {
                    const detail = event.detail;
                    // Aquí necesitaríamos una forma de actualizar el estado de Reflex
                    // Por ahora usaremos el método anterior
                });
            </script>
            """
        ),
        on_scroll=ScrollState.on_scroll,
    )

# Versión más simple que siempre es visible (para probar)
def scroll_to_top_always_visible() -> rx.Component:
    return rx.button(
        rx.icon(
            tag="arrow-up",
            color="white",
            font_size="20px",
        ),
        background="#194264FF",
        border_radius="50%",
        width="55px",
        height="55px",
        padding="0",
        display="flex",
        align_items="center",
        justify_content="center",
        position="fixed",
        bottom="25px",
        right="25px",
        z_index="10000",
        _hover={
            "background": "#0f2a42",
            "transform": "scale(1.15)",
        },
        border="2px solid rgba(255,255,255,0.2)",
        transition="all 0.3s ease",
        box_shadow="0 4px 15px rgba(0, 0, 0, 0.3)",
        on_click=rx.call_script("window.scrollTo({top: 0, behavior: 'smooth'})"),
        title="Volver al inicio",
    )

# Versión final recomendada (usa esta)
def scroll_top_button() -> rx.Component:
    return rx.box(
        # Botón
        rx.button(
            rx.icon(
                tag="chevron-up",
                color="white",
                font_size="24px",
            ),
            id="scroll-top-btn",
            background="linear-gradient(135deg, #194264FF 0%, #0f2a42 100%)",
            border_radius="50%",
            width="60px",
            height="60px",
            padding="0",
            display="none",  # Inicialmente oculto
            align_items="center",
            justify_content="center",
            position="fixed",
            bottom="30px",
            right="30px",
            z_index="10000",
            _hover={
                "background": "linear-gradient(135deg, #0f2a42 0%, #194264FF 100%)",
                "transform": "scale(1.1)",
            },
            border="2px solid rgba(255,255,255,0.3)",
            transition="all 0.3s ease",
            box_shadow="0 5px 20px rgba(0, 0, 0, 0.4)",
            on_click=rx.call_script("window.scrollTo({top: 0, behavior: 'smooth'})"),
        ),
        # Script completo
        rx.script(
            """
            // Función para mostrar/ocultar el botón
            function toggleScrollButton() {
                const btn = document.getElementById('scroll-top-btn');
                if (window.scrollY > 400) {
                    btn.style.display = 'flex';
                    btn.style.opacity = '1';
                } else {
                    btn.style.opacity = '0';
                    setTimeout(() => {
                        if (window.scrollY <= 400) {
                            btn.style.display = 'none';
                        }
                    }, 300);
                }
            }
            
            // Event listeners
            window.addEventListener('scroll', toggleScrollButton);
            window.addEventListener('load', toggleScrollButton);
            window.addEventListener('resize', toggleScrollButton);
            
            // Inicializar
            toggleScrollButton();
            """
        ),
    )