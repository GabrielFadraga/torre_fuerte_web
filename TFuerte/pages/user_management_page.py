# TFuerte/pages/user_management_page.py
import reflex as rx
from TFuerte.state.super_admin_auth_state import SuperAdminAuthState
from TFuerte.state.user_management_state import UserManagementState
from TFuerte.components.navbar import navbar
from TFuerte.routes import Route

@rx.page(
    route=Route.USER_MANAGEMENT.value,
    title="Gestión de Usuarios del Sistema",
    on_load=[
        SuperAdminAuthState.check_auth,
        UserManagementState.load_all_data,
    ],
)
def user_management_page() -> rx.Component:
    """Panel de administración de usuarios del sistema"""

    # Diálogo para agregar usuario
    def add_user_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title(
                    f"Agregar usuario - {UserManagementState.current_table.replace('_', ' ').title()}",
                    color="#1e293b",
                ),
                rx.form(
                    rx.vstack(
                        rx.match(
                            UserManagementState.current_table,
                            ("super_admin", rx.vstack(
                                rx.input(
                                    placeholder="Username",
                                    name="username",
                                    required=True,
                                    on_change=lambda v: UserManagementState.update_add_form_field("username", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Password",
                                    name="password",
                                    type="password",
                                    required=True,
                                    on_change=lambda v: UserManagementState.update_add_form_field("password", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                spacing="3",
                                width="100%",
                            )),
                            ("admin_tf", rx.vstack(
                                rx.input(
                                    placeholder="Usuario",
                                    name="usuario",
                                    required=True,
                                    on_change=lambda v: UserManagementState.update_add_form_field("usuario", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Clave",
                                    name="clave",
                                    type="password",
                                    required=True,
                                    on_change=lambda v: UserManagementState.update_add_form_field("clave", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                spacing="3",
                                width="100%",
                            )),
                            ("autorizacion", rx.vstack(
                                rx.input(
                                    placeholder="User",
                                    name="user",
                                    required=True,
                                    on_change=lambda v: UserManagementState.update_add_form_field("user", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Password",
                                    name="password",
                                    type="password",
                                    required=True,
                                    on_change=lambda v: UserManagementState.update_add_form_field("password", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                spacing="3",
                                width="100%",
                            )),
                            ("admin_recursos", rx.vstack(
                                rx.input(
                                    placeholder="Usuario",
                                    name="usuario",
                                    required=True,
                                    on_change=lambda v: UserManagementState.update_add_form_field("usuario", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Password",
                                    name="password",
                                    type="password",
                                    required=True,
                                    on_change=lambda v: UserManagementState.update_add_form_field("password", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Cargo",
                                    name="cargo",
                                    on_change=lambda v: UserManagementState.update_add_form_field("cargo", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Rol",
                                    name="rol",
                                    on_change=lambda v: UserManagementState.update_add_form_field("rol", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                spacing="3",
                                width="100%",
                            )),
                            ("solicitantes", rx.vstack(
                                rx.input(
                                    placeholder="Usuario",
                                    name="usuario",
                                    required=True,
                                    on_change=lambda v: UserManagementState.update_add_form_field("usuario", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Clave",
                                    name="clave",
                                    type="password",
                                    required=True,
                                    on_change=lambda v: UserManagementState.update_add_form_field("clave", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Cargo",
                                    name="cargo",
                                    on_change=lambda v: UserManagementState.update_add_form_field("cargo", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                spacing="3",
                                width="100%",
                            )),
                            ("commercial_admin", rx.vstack(
                                rx.input(
                                    placeholder="Username",
                                    name="username",
                                    required=True,
                                    on_change=lambda v: UserManagementState.update_add_form_field("username", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Password",
                                    name="password",
                                    type="password",
                                    required=True,
                                    on_change=lambda v: UserManagementState.update_add_form_field("password", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                spacing="3",
                                width="100%",
                            )),
                            ("commercial", rx.vstack(
                                rx.input(
                                    placeholder="Username",
                                    name="username",
                                    required=True,
                                    on_change=lambda v: UserManagementState.update_add_form_field("username", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Password",
                                    name="password",
                                    type="password",
                                    required=True,
                                    on_change=lambda v: UserManagementState.update_add_form_field("password", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                spacing="3",
                                width="100%",
                            )),
                        ),
                        rx.hstack(
                            rx.dialog.close(
                                rx.button(
                                    "Cancelar",
                                    type="button",
                                    variant="soft",
                                    color_scheme="gray",
                                    on_click=UserManagementState.close_add_dialog,
                                    style={"background": "#f1f5f9", "color": "#1e293b"},
                                )
                            ),
                            rx.button(
                                "Guardar",
                                type="submit",
                                color_scheme="green",
                                style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                            ),
                            spacing="3",
                            justify="end",
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    on_submit=UserManagementState.add_user,
                    reset_on_submit=True,
                ),
                max_width="500px",
                style={"background": "white", "color": "#1e293b"},
            ),
            open=UserManagementState.show_add_dialog,
            on_open_change=UserManagementState.close_add_dialog,
        )

    # Diálogo para editar usuario
    def edit_user_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.dialog.title(
                    f"Editar usuario - {UserManagementState.current_table.replace('_', ' ').title()}",
                    color="#1e293b",
                ),
                rx.form(
                    rx.vstack(
                        rx.match(
                            UserManagementState.current_table,
                            ("super_admin", rx.vstack(
                                rx.input(
                                    placeholder="Username",
                                    name="username",
                                    required=True,
                                    default_value=UserManagementState.edit_form_data.get("username", ""),
                                    on_change=lambda v: UserManagementState.update_edit_form_field("username", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Password",
                                    name="password",
                                    type="password",
                                    required=True,
                                    default_value=UserManagementState.edit_form_data.get("password", ""),
                                    on_change=lambda v: UserManagementState.update_edit_form_field("password", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                spacing="3",
                                width="100%",
                            )),
                            ("admin_tf", rx.vstack(
                                rx.input(
                                    placeholder="Usuario",
                                    name="usuario",
                                    required=True,
                                    default_value=UserManagementState.edit_form_data.get("usuario", ""),
                                    on_change=lambda v: UserManagementState.update_edit_form_field("usuario", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Clave",
                                    name="clave",
                                    type="password",
                                    required=True,
                                    default_value=UserManagementState.edit_form_data.get("clave", ""),
                                    on_change=lambda v: UserManagementState.update_edit_form_field("clave", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                spacing="3",
                                width="100%",
                            )),
                            ("autorizacion", rx.vstack(
                                rx.input(
                                    placeholder="User",
                                    name="user",
                                    required=True,
                                    default_value=UserManagementState.edit_form_data.get("user", ""),
                                    on_change=lambda v: UserManagementState.update_edit_form_field("user", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Password",
                                    name="password",
                                    type="password",
                                    required=True,
                                    default_value=UserManagementState.edit_form_data.get("password", ""),
                                    on_change=lambda v: UserManagementState.update_edit_form_field("password", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                spacing="3",
                                width="100%",
                            )),
                            ("admin_recursos", rx.vstack(
                                rx.input(
                                    placeholder="Usuario",
                                    name="usuario",
                                    required=True,
                                    default_value=UserManagementState.edit_form_data.get("usuario", ""),
                                    on_change=lambda v: UserManagementState.update_edit_form_field("usuario", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Password",
                                    name="password",
                                    type="password",
                                    required=True,
                                    default_value=UserManagementState.edit_form_data.get("password", ""),
                                    on_change=lambda v: UserManagementState.update_edit_form_field("password", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Cargo",
                                    name="cargo",
                                    default_value=UserManagementState.edit_form_data.get("cargo", ""),
                                    on_change=lambda v: UserManagementState.update_edit_form_field("cargo", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Rol",
                                    name="rol",
                                    default_value=UserManagementState.edit_form_data.get("rol", ""),
                                    on_change=lambda v: UserManagementState.update_edit_form_field("rol", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                spacing="3",
                                width="100%",
                            )),
                            ("solicitantes", rx.vstack(
                                rx.input(
                                    placeholder="Usuario",
                                    name="usuario",
                                    required=True,
                                    default_value=UserManagementState.edit_form_data.get("usuario", ""),
                                    on_change=lambda v: UserManagementState.update_edit_form_field("usuario", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Clave",
                                    name="clave",
                                    type="password",
                                    required=True,
                                    default_value=UserManagementState.edit_form_data.get("clave", ""),
                                    on_change=lambda v: UserManagementState.update_edit_form_field("clave", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Cargo",
                                    name="cargo",
                                    default_value=UserManagementState.edit_form_data.get("cargo", ""),
                                    on_change=lambda v: UserManagementState.update_edit_form_field("cargo", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                spacing="3",
                                width="100%",
                            )),
                            ("commercial_admin", rx.vstack(
                                rx.input(
                                    placeholder="Username",
                                    name="username",
                                    required=True,
                                    default_value=UserManagementState.edit_form_data.get("username", ""),
                                    on_change=lambda v: UserManagementState.update_edit_form_field("username", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Password",
                                    name="password",
                                    type="password",
                                    required=True,
                                    default_value=UserManagementState.edit_form_data.get("password", ""),
                                    on_change=lambda v: UserManagementState.update_edit_form_field("password", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                spacing="3",
                                width="100%",
                            )),
                            ("commercial", rx.vstack(
                                rx.input(
                                    placeholder="Username",
                                    name="username",
                                    required=True,
                                    default_value=UserManagementState.edit_form_data.get("username", ""),
                                    on_change=lambda v: UserManagementState.update_edit_form_field("username", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                rx.input(
                                    placeholder="Password",
                                    name="password",
                                    type="password",
                                    required=True,
                                    default_value=UserManagementState.edit_form_data.get("password", ""),
                                    on_change=lambda v: UserManagementState.update_edit_form_field("password", v),
                                    width="100%",
                                    background="gray",
                                    color="#1e293b",
                                    border="1px solid #e2e8f0",
                                ),
                                spacing="3",
                                width="100%",
                            )),
                        ),
                        rx.hstack(
                            rx.dialog.close(
                                rx.button(
                                    "Cancelar",
                                    type="button",
                                    variant="soft",
                                    color_scheme="gray",
                                    on_click=UserManagementState.close_edit_dialog,
                                    style={"background": "#f1f5f9", "color": "#1e293b"},
                                )
                            ),
                            rx.button(
                                "Guardar",
                                type="submit",
                                color_scheme="green",
                                style={"background": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "color": "white"},
                            ),
                            spacing="3",
                            justify="end",
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    on_submit=UserManagementState.update_user,
                    reset_on_submit=False,
                ),
                max_width="500px",
                style={"background": "white", "color": "#1e293b"},
            ),
            open=UserManagementState.show_edit_dialog,
            on_open_change=UserManagementState.close_edit_dialog,
        )

    # Componente de confirmación de eliminación (mejorado visualmente)
    def delete_confirm_dialog(table_key: str, user_id: int, user_name: str):
        return rx.alert_dialog.root(
            rx.alert_dialog.trigger(
                rx.button(
                    rx.icon("trash-2", size=16),
                    variant="solid",
                    color_scheme="red",
                    size="2",
                    style={
                        "background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
                        "color": "white",
                        "padding": "8px 12px",
                        "border_radius": "6px",
                        "cursor": "pointer",
                        "font_weight": "500",
                        "min_width": "36px",
                    }
                )
            ),
            rx.alert_dialog.content(
                rx.alert_dialog.title("Confirmar eliminación", color="#1e293b"),
                rx.alert_dialog.description(
                    f"¿Estás seguro de que deseas eliminar al usuario '{user_name}'? Esta acción no se puede deshacer.",
                    color="#475569",
                ),
                rx.hstack(
                    rx.alert_dialog.cancel(
                        rx.button("Cancelar", variant="soft", color_scheme="gray", style={"color": "#1e293b"})
                    ),
                    rx.alert_dialog.action(
                        rx.button(
                            "Eliminar",
                            color_scheme="red",
                            on_click=lambda: UserManagementState.delete_user(table_key, user_id),
                            style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
                        )
                    ),
                    spacing="3",
                ),
                max_width="400px",
                style={"background": "white", "border_radius": "12px"},
            ),
        )

    # Tabla genérica para mostrar usuarios (con estilos responsivos mejorados)
    def user_table(users: rx.Var, table_key: str, fields: list, description: str):
        field_titles = {
            "username": "Usuario",
            "password": "Contraseña",
            "usuario": "Usuario",
            "clave": "Contraseña",
            "user": "Usuario",
            "cargo": "Cargo",
            "rol": "Rol",
        }
        headers = [field_titles.get(f, f.replace('_', ' ').title()) for f in fields]

        return rx.card(
            rx.vstack(
                rx.hstack(
                    rx.text(description, size="2", color="#64748b"),
                    rx.spacer(),
                    rx.button(
                        "➕ Agregar",
                        on_click=lambda: UserManagementState.open_add_dialog(table_key),
                        size="2",
                        variant="solid",
                        color_scheme="green",
                        style={
                            "background": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
                            "color": "white",
                            "padding": "8px 16px",
                            "border_radius": "6px",
                            "font_weight": "500",
                            "white_space": "nowrap",
                        },
                    ),
                    width="100%",
                    margin_bottom="1rem",
                ),
                rx.cond(
                    users.length() == 0,
                    rx.center(
                        rx.text("No hay usuarios registrados", color="#64748b", font_style="italic"),
                        padding="2rem",
                    ),
                    rx.scroll_area(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    *[rx.table.column_header_cell(
                                        h, 
                                        style={
                                            "background": "#f1f5f9", 
                                            "color": "#1e293b", 
                                            "font_weight": "600",
                                            "padding": "12px 8px",
                                            "white_space": "nowrap",
                                        }
                                    ) for h in headers],
                                    rx.table.column_header_cell(
                                        "Acciones", 
                                        style={
                                            "background": "#f1f5f9", 
                                            "color": "#1e293b", 
                                            "font_weight": "600",
                                            "text_align": "center",
                                            "padding": "12px 8px",
                                            "white_space": "nowrap",
                                        }
                                    ),
                                )
                            ),
                            rx.table.body(
                                rx.foreach(
                                    users,
                                    lambda user: rx.table.row(
                                        *[
                                            rx.table.cell(
                                                rx.text(
                                                    str(user.get(f, "")),
                                                    color="#1e293b",
                                                    font_weight="500" if f in ["username", "usuario", "user"] else "normal",
                                                ),
                                                style={"padding": "10px 8px", "white_space": "nowrap"},
                                            )
                                            for f in fields
                                        ],
                                        rx.table.cell(
                                            rx.hstack(
                                                rx.button(
                                                    rx.icon("pencil", size=16),
                                                    on_click=lambda: UserManagementState.open_edit_dialog(table_key, user["id"], user),
                                                    variant="solid",
                                                    size="2",
                                                    color_scheme="blue",
                                                    style={
                                                        "background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
                                                        "color": "white",
                                                        "padding": "8px 12px",
                                                        "border_radius": "6px",
                                                        "cursor": "pointer",
                                                        "min_width": "36px",
                                                    }
                                                ),
                                                delete_confirm_dialog(table_key, user["id"], user.get(fields[0], "")),
                                                spacing="2",
                                                justify="center",
                                            ),
                                            style={"padding": "10px 8px", "text_align": "center"},
                                        ),
                                        _hover={"background_color": "#f8fafc"},
                                    ),
                                )
                            ),
                            style={"width": "100%", "border_collapse": "collapse", "min_width": "600px"},
                        ),
                        type="always",
                        scrollbars="horizontal",
                        style={"max_height": "400px", "overflow_y": "auto", "border": "1px solid #e2e8f0", "border_radius": "8px"},
                    ),
                ),
                spacing="3",
                align="start",
                width="100%",
            ),
            padding="1.5rem",
            margin_bottom="1.5rem",
            style={
                "background": "white",
                "border_radius": "12px",
                "box_shadow": "0 1px 3px rgba(0,0,0,0.1)",
                "border": "1px solid #e2e8f0",
            },
        )

    # Contenido principal con pestañas
    def main_content():
        return rx.vstack(
            rx.heading("Administración de Usuarios del Sistema", size="7", color="#1e293b", margin_bottom="0.5rem"),
            rx.text("Gestión centralizada de todos los usuarios del sistema", size="3", color="#64748b", margin_bottom="2rem"),
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("Super Administradores", value="super_admin"),
                    rx.tabs.trigger("AdminTF", value="admin_tf"),
                    rx.tabs.trigger("Autorización", value="autorizacion"),
                    rx.tabs.trigger("Admin Recursos", value="admin_recursos"),
                    rx.tabs.trigger("Solicitantes", value="solicitantes"),
                    rx.tabs.trigger("Comercial Admin", value="commercial_admin"),
                    rx.tabs.trigger("Comercial", value="commercial"),
                ),
                rx.tabs.content(
                    user_table(
                        UserManagementState.super_admin_users,
                        "super_admin",
                        ["username", "password"],
                        UserManagementState.table_descriptions["super_admin"]
                    ),
                    value="super_admin",
                ),
                rx.tabs.content(
                    user_table(
                        UserManagementState.admin_tf_users,
                        "admin_tf",
                        ["usuario", "clave"],
                        UserManagementState.table_descriptions["admin_tf"]
                    ),
                    value="admin_tf",
                ),
                rx.tabs.content(
                    user_table(
                        UserManagementState.autorizacion_users,
                        "autorizacion",
                        ["user", "password"],
                        UserManagementState.table_descriptions["autorizacion"]
                    ),
                    value="autorizacion",
                ),
                rx.tabs.content(
                    user_table(
                        UserManagementState.admin_recursos_users,
                        "admin_recursos",
                        ["usuario", "password", "cargo", "rol"],
                        UserManagementState.table_descriptions["admin_recursos"]
                    ),
                    value="admin_recursos",
                ),
                rx.tabs.content(
                    user_table(
                        UserManagementState.solicitantes_users,
                        "solicitantes",
                        ["usuario", "clave", "cargo"],
                        UserManagementState.table_descriptions["solicitantes"]
                    ),
                    value="solicitantes",
                ),
                rx.tabs.content(
                    user_table(
                        UserManagementState.commercial_admin_users,
                        "commercial_admin",
                        ["username", "password"],
                        UserManagementState.table_descriptions["commercial_admin"]
                    ),
                    value="commercial_admin",
                ),
                rx.tabs.content(
                    user_table(
                        UserManagementState.commercial_users,
                        "commercial",
                        ["username", "password"],
                        UserManagementState.table_descriptions["commercial"]
                    ),
                    value="commercial",
                ),
                default_value="super_admin",
                width="100%",
            ),
            rx.divider(margin_y="2rem"),
            rx.hstack(
                rx.button(
                    "🚪 Cerrar Sesión",
                    on_click=SuperAdminAuthState.logout,
                    color_scheme="red",
                    variant="solid",
                    size="2",
                    style={"background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "color": "white"},
                ),
                justify="end",
                width="100%",
            ),
            spacing="4",
            align="start",
            width="100%",
            padding="2rem",
        )

    return rx.cond(
        SuperAdminAuthState.is_authenticated,
        rx.box(
            navbar("Gestión de Usuarios"),
            rx.center(
                rx.box(
                    main_content(),
                    width="100%",
                    max_width="1400px",
                ),
                width="100%",
            ),
            add_user_dialog(),
            edit_user_dialog(),
            width="100%",
            min_height="100vh",
            background="#f8fafc",
        ),
        rx.center(
            rx.vstack(
                rx.spinner(size="3"),
                rx.text("No autenticado. Redirigiendo...", color="#1e293b"),
                rx.button(
                    "Ir al Login",
                    on_click=lambda: rx.redirect(Route.SUPER_ADMIN_LOGIN.value),
                    style={"background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)", "color": "white"},
                ),
                spacing="3",
                align="center",
            ),
            height="100vh",
        ),
    )