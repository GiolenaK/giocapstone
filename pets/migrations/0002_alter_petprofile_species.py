# Generated by Django 5.1.5 on 2025-02-23 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petprofile',
            name='species',
            field=models.CharField(choices=[('Dog', 'Dog'), ('Cat', 'Cat'), ('Other', 'Other')], default='Dog', max_length=10),
        ),
    ]
