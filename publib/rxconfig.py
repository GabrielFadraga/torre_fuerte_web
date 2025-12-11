import reflex as rx


config = rx.Config(
    app_name="TFuerte",
    cors_allowed_origins=[
        "http://localhost:3000",
        "https://torrefuerteweb-production.up.railway.app"
    ],
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)