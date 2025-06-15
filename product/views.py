from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages

from .models import Product
from .forms import ProductForm


# Create your views here.
class ListviewProduct(ListView):
    model = Product
    template_name = "product/product.html"
    context_object_name = 'products'


class ProductBaseView:
    """Base view to handle common context data"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f"{self.title} was successful.")
        return super().form_valid(form)
    
    
class ProductCreate(ProductBaseView, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product/forms.html"
    context_object_name = 'form'
    success_url = reverse_lazy('product_list')
    title = "Create New Product"
    

class ProductUpdate(ProductBaseView, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product/forms.html"
    context_object_name = 'form'
    success_url = reverse_lazy('product_list')
    title = "Update Product"


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "The product was deleted successfully.")
        
        if request.headers.get('HX-Request'):  # HTMX support
            return JsonResponse({"message": "The product was deleted successfully."})

        return response