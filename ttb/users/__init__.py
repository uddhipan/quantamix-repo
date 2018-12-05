from flask import Blueprint

main = Blueprint('users', __name__)

from . import routes 
from ..models import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

