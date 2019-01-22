# Generated by Django 2.1 on 2019-01-22 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_productimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('product', models.ManyToManyField(blank=True, to='main.Product')),
            ],
        ),
    ]
