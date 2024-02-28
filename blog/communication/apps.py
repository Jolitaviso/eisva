from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CommunicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'communication'

    class Meta:
        verbose_name = _('communication')