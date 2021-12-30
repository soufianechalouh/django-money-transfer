# Generated by Django 4.0 on 2021-12-30 16:34

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_user_is_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('status', models.CharField(choices=[('AC', 'ACTIVE'), ('ON', 'ON_HOLD'), ('AR', 'ARCHIVED')], default='AC', max_length=2)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amount', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('comment', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('IP', 'IN_PROGRESS'), ('EX', 'EXECUTED'), ('CA', 'CANCELED')], default='IP', max_length=2)),
                ('log', models.TextField(blank=True, null=True)),
                ('destination', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user')),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfers', to='users.user', to_field='username')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
