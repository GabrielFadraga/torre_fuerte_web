import reflex as rx


config = rx.Config(
    app_name="TFuerte",
    api_url="https://torrefuerteweb-production.up.railway.app",

    cors_allowed_origins=[
        "http://localhost:3000",
        "https://www.torrefuertesurl.com",
    ],
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)