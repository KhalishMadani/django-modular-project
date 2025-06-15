from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView

# Create your views here.
class LoginUser(LoginView):
    template_name = "product/login.html"

    def get_success_url(self):
        return reverse_lazy('product_list')
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)