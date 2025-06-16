from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.list import ListView

from .models import Module


# Create your views here.
class EngineTemplateView(ListView):
    model = Module
    template_name = "modular_engine/index.html"
    context_object_name = "modules"

def install_module(request, obj_name):
    module = get_object_or_404(Module, name=obj_name)
    module.installed = True
    module.version = "1.0.0"
    module.save()
    return redirect(reverse('module_list'))

def uninstall_module(request, obj_name):
    module = get_object_or_404(Module, name=obj_name)
    module.installed = False
    module.save()
    return redirect(reverse('module_list'))

def module_not_installed(request):
    return render(request, "modular_engine/module_disabled.html")