# Generated by Django 4.2.5 on 2023-09-21 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_alter_transactions_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='payment_id',
            field=models.CharField(default=0, max_length=122, unique=True),
            preserve_default=False,
        ),
    ]
