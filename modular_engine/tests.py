# modular_engine/tests.py
from django.test import TestCase
from django.urls import reverse
from .models import Module


class ModuleModelTest(TestCase):
    def test_module_str(self):
        module = Module.objects.create(name="Product")
        self.assertEqual(str(module), "Product")

    def test_default_installed_false(self):
        module = Module.objects.create(name="Billing")
        self.assertFalse(module.installed)

    def test_version_optional(self):
        module = Module.objects.create(name="Shipping")
        self.assertIsNone(module.version)


class ModuleViewsTest(TestCase):
    def setUp(self):
        self.module = Module.objects.create(name="Product", installed=False)

    def test_engine_template_view(self):
        response = self.client.get(reverse('module_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "modular_engine/index.html")
        self.assertIn(self.module, response.context['modules'])

    def test_install_module_view(self):
        response = self.client.get(reverse('install_module', args=[self.module.name]))
        self.module.refresh_from_db()
        self.assertRedirects(response, reverse('module_list'))
        self.assertTrue(self.module.installed)
        self.assertEqual(self.module.version, "1.0.0")

    def test_uninstall_module_view(self):
        self.module.installed = True
        self.module.save()
        response = self.client.get(reverse('uninstall_module', args=[self.module.name]))
        self.module.refresh_from_db()
        self.assertRedirects(response, reverse('module_list'))
        self.assertFalse(self.module.installed)

    def test_module_not_installed_view(self):
        response = self.client.get(reverse('module_not_installed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "modular_engine/module_disabled.html")
