from django.apps import AppConfig
from suit.apps import DjangoSuitConfig


class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'

class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'