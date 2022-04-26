# Generated by Django 3.2.8 on 2021-11-04 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('image', models.TextField(max_length=300)),
                ('description', models.TextField(max_length=300)),
                ('price', models.IntegerField()),
                ('current_bid', models.IntegerField(blank=True, default='0')),
                ('status', models.BooleanField(default=True)),
                ('category', models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.CASCADE, related_name='category_name', to='auctions.category')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id_prods', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]