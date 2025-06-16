from django.shortcuts import redirect
from modular_engine.models import Module

class ModuleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.startswith('/product/'):
            try:
                module = Module.objects.get(name='product_module')
                if not module.installed:
                    return redirect('module_not_installed')
            except Module.DoesNotExist:
                return redirect('module_not_installed')

        return self.get_response(request)
