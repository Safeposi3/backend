# Generated by Django 4.2.1 on 2023-05-30 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_reservation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('UNPAID', 'Unpaid'), ('PAID', 'Paid'), ('CANCELLED', 'Cancelled')], default='UNPAID', max_length=10),
        ),
    ]
