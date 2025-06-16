from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from .models import Product
from .forms import ProductForm

from modular_engine.models import Module


class ProductModelTest(TestCase):
    def test_create_product(self):
        product = Product.objects.create(
            name="Widget A",
            barcode="ABC123",
            price=1000,
            stock=5,
            dynamic_fields={"color": "red"}
        )
        self.assertEqual(str(product), "Widget A")
        self.assertEqual(product.dynamic_fields["color"], "red")
        self.assertEqual(product.stock, 5)


class ProductFormTest(TestCase):
    def test_form_valid_data(self):
        form = ProductForm(data={
            "name": "Product X",
            "barcode": "BARCODE1",
            "price": 1500,
            "stock": 10
        })
        self.assertTrue(form.is_valid())

    def test_form_missing_field(self):
        form = ProductForm(data={
            "name": "Missing Barcode",
            "price": 1500,
            "stock": 10
        })
        self.assertFalse(form.is_valid())
        self.assertIn("barcode", form.errors)


class ProductViewsTest(TestCase):
    def setUp(self):
        Module.objects.create(name="product_module", installed=True)
        self.product = Product.objects.create(
            name="Demo Product",
            barcode="DEMO123",
            price=500,
            stock=20
        )

    def test_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product.html')
        self.assertIn(self.product, response.context['products'])

    def test_create_view(self):
        response = self.client.post(reverse('product_create'), {
            "name": "New Product",
            "barcode": "NEW123",
            "price": 200,
            "stock": 10
        })
        self.assertRedirects(response, reverse('product_list'))
        self.assertTrue(Product.objects.filter(name="New Product").exists())

    def test_create_view_invalid(self):
        response = self.client.post(reverse('product_create'), {
            "barcode": "MISSING_NAME",
            "price": 100
        })
        self.assertEqual(response.status_code, 200)  # Form re-render
        self.assertFormError(response, 'form', 'name', 'This field is required.')

    def test_update_view(self):
        response = self.client.post(reverse('product_update', args=[self.product.pk]), {
            "name": "Updated Product",
            "barcode": "DEMO123",
            "price": 750,
            "stock": 15
        })
        self.assertRedirects(response, reverse('product_list'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Product")

    def test_delete_view(self):
        response = self.client.post(reverse('product_delete', args=[self.product.pk]))
        self.assertRedirects(response, reverse('product_list'))
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

class ProductDeleteViewTest(TestCase):
    def setUp(self):
        # Ensure the 'product' module is installed to pass middleware
        Module.objects.create(name="product_module", installed=True)

        self.product = Product.objects.create(
            name="Test Product",
            barcode="XYZ123",
            price=1000,
            stock=5
        )
        self.delete_url = reverse('product_delete', args=[self.product.pk])

    def test_standard_delete_redirects(self):
        response = self.client.post(self.delete_url)
        self.assertRedirects(response, reverse('product_list'))
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_htmx_delete_returns_json(self):
        response = self.client.post(self.delete_url, **{"HTTP_HX-Request": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertJSONEqual(response.content, {
            "message": "The product was deleted successfully."
        })
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

