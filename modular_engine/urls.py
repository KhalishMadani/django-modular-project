from django.urls import path
from .views import (
    EngineTemplateView,
    install_module,
    uninstall_module
    )

urlpatterns = [
    path(
        'module/',
        EngineTemplateView.as_view(),
        name="module_list"
    ),

    path(
        'install-module/<str:obj_name>/',
        install_module,
        name="install_module"
    ),

    path(
        'unisntall-module/<str:obj_name>/',
        uninstall_module,
        name="uninstall_module"
    ),
]
