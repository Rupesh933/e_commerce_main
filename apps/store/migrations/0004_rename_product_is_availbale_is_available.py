from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_variation"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="is_availbale",
            new_name="is_available",
        ),
    ]
