import reflex as rx


config = rx.Config(
    app_name="TFuerte",
    api_url="https://torre-fuerte-web.onrender.com",

    cors_allowed_origins=[
        "http://localhost:3000",
        "https://www.torrefuertesurl.com",
    ],
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)