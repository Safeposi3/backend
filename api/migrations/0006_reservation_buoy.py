# Generated by Django 4.2.1 on 2023-05-27 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_reservation_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='buoy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='api.buoys'),
            preserve_default=False,
        ),
    ]
