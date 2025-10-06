import reflex as rx

class Config(rx.Config):
    pass

config = rx.Config(
    app_name="TFuerte",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)