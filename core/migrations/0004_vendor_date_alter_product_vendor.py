# Generated by Django 4.2.7 on 2023-12-04 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_product_category_alter_product_featured_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendor', to='core.vendor', verbose_name='Fournisseur'),
        ),
    ]
