from django.test import TestCase
from django.urls import reverse

from apps.category.models import Category
from apps.store.models import Product


class AdminProductsTests(TestCase):
    def test_all_categories_label_does_not_get_used_as_category_id(self):
        Category.objects.create(category_name="Electronics", slug="electronics")

        response = self.client.get(
            reverse("admin_products"),
            {"category": "All Categories"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "All Categories")
        self.assertContains(response, "Electronics")

    def test_products_render_as_separate_table_rows(self):
        category = Category.objects.create(
            category_name="Electronics",
            slug="electronics",
        )
        for name, slug in (("Laptop", "laptop"), ("Phone", "phone")):
            Product.objects.create(
                product_name=name,
                slug=slug,
                price=100,
                stock=5,
                category=category,
                images="products/test.jpg",
            )

        response = self.client.get(reverse("admin_products"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode().count("<tr>"), 3)
        self.assertContains(response, "Laptop")
        self.assertContains(response, "Phone")
