import reflex as rx
from enum import Enum

class Route(Enum):
    INDEX = "/"
    ABOUT = "/about"
    SERVICES = "/services"
    PROJECTS = "/projects"
    TEAM = "/team"