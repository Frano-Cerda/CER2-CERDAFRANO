# Generated by Django 5.1.2 on 2024-10-28 06:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('productoID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.IntegerField()),
                ('descripcion', models.TextField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='productos/')),
            ],
        ),
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='carrito', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(default='pendiente', max_length=50)),
                ('total', models.IntegerField()),
                ('fecha', models.DateTimeField(auto_now_add=True, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PedidoProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.producto')),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='productos',
            field=models.ManyToManyField(related_name='pedidos', through='core.PedidoProducto', to='core.producto'),
        ),
        migrations.CreateModel(
            name='CarritoProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='core.carrito')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.producto')),
            ],
        ),
    ]
