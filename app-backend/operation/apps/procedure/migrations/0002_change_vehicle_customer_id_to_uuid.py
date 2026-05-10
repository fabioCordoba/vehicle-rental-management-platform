from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("procedure", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="procedure", name="vehicle_id"),
        migrations.RemoveField(model_name="procedure", name="customer_id"),
        migrations.AddField(
            model_name="procedure",
            name="vehicle_id",
            field=models.UUIDField(),
        ),
        migrations.AddField(
            model_name="procedure",
            name="customer_id",
            field=models.UUIDField(),
        ),
    ]
