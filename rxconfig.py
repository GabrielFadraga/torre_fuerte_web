import reflex as rx


config = rx.Config(
    app_name="TFuerte",
    cors_allowed_origins=[
        "http://localhost:3000",
        #"https://torrefuerteweb-production.up.railway.app"
        "https://gabriel-20mrw5de.b4a.run/"
    ],
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)