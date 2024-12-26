# Generated by Django 5.1.4 on 2024-12-26 23:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_token', models.CharField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('users', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Tokens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
