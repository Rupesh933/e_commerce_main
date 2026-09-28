from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.category.models import Category
from apps.store.models import Product


CATEGORIES = {
    "Electronics": [
        ("Wireless Bluetooth Headphones", "Comfortable over-ear headphones with rich sound and a 30-hour battery.", 2499, 35),
        ("Portable Bluetooth Speaker", "Compact, water-resistant speaker for music at home or outdoors.", 1899, 28),
        ("Smart Fitness Watch", "Track daily activity, workouts, heart rate, and notifications.", 3299, 20),
        ("USB-C Fast Charger", "A compact 30 W charger for phones, tablets, and other USB-C devices.", 899, 60),
        ("Wireless Optical Mouse", "Ergonomic wireless mouse with adjustable precision and quiet clicks.", 699, 45),
        ("1080p Webcam", "Full HD webcam with a built-in microphone for calls and streaming.", 1599, 18),
    ],
    "Fashion": [
        ("Everyday Cotton T-Shirt", "Soft cotton crew-neck T-shirt for comfortable everyday wear.", 599, 50),
        ("Classic Denim Jacket", "A versatile denim jacket with a relaxed fit and sturdy buttons.", 2199, 16),
        ("Canvas Sneakers", "Lightweight lace-up sneakers with a cushioned sole.", 1499, 24),
        ("Minimal Leather Wallet", "Slim wallet with multiple card slots and a secure coin pocket.", 999, 30),
        ("Polarized Sunglasses", "UV-protective polarized lenses in a lightweight frame.", 1299, 22),
        ("Everyday Backpack", "Durable 20-litre backpack with padded laptop storage.", 1799, 19),
    ],
    "Home & Kitchen": [
        ("Stainless Steel Water Bottle", "Insulated bottle that keeps drinks hot or cold for hours.", 799, 40),
        ("Ceramic Coffee Mug Set", "Set of two glazed ceramic mugs for coffee, tea, and more.", 649, 32),
        ("Non-Stick Frying Pan", "Easy-clean 26 cm frying pan with a comfortable heat-resistant handle.", 1199, 21),
        ("Cotton Cushion Cover Set", "Pair of textured cotton cushion covers with hidden zips.", 549, 26),
        ("LED Desk Lamp", "Adjustable desk lamp with three brightness levels and warm light.", 1399, 14),
        ("Bamboo Cutting Board", "Naturally durable bamboo board for everyday food preparation.", 699, 25),
    ],
    "Books": [
        ("The Art of Simple Living", "A practical guide to building calmer and more intentional daily routines.", 399, 32),
        ("Gardening for Beginners", "An approachable introduction to growing herbs, flowers, and vegetables.", 499, 18),
        ("The Curious Universe", "Explore the stars, planets, and big questions of modern astronomy.", 599, 15),
        ("Quick Weeknight Meals", "A collection of simple recipes designed for busy evenings.", 449, 27),
        ("Stories from the Coast", "A warm collection of short fiction set in seaside towns.", 349, 20),
        ("Learn Python by Doing", "Hands-on programming exercises for new Python learners.", 699, 12),
    ],
}


class Command(BaseCommand):
    help = "Add 24 sample products across four shop categories. Safe to run more than once."

    def handle(self, *args, **options):
        added_categories = 0
        added_products = 0

        for category_name, products in CATEGORIES.items():
            category, created = Category.objects.get_or_create(
                slug=slugify(category_name),
                defaults={
                    "category_name": category_name,
                    "description": f"Sample {category_name.lower()} for your store.",
                },
            )
            added_categories += int(created)

            for name, description, price, stock in products:
                _, created = Product.objects.get_or_create(
                    slug=slugify(name),
                    defaults={
                        "product_name": name,
                        "description": description,
                        "price": price,
                        "stock": stock,
                        "is_availbale": True,
                        "category": category,
                    },
                )
                added_products += int(created)

        self.stdout.write(
            self.style.SUCCESS(
                f"Added {added_categories} categories and {added_products} products "
                f"({Product.objects.count()} products total)."
            )
        )
