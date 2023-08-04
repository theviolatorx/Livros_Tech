from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Categories2AppConfig(AppConfig):
    name = "myproject.apps.categories2"
    verbose_name = _("Categories using TreeBeard")
