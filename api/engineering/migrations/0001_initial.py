# Generated by Django 5.0.1 on 2024-02-06 06:50

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
            name='Account',
            fields=[
                ('account_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('account_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('project_name', models.CharField(max_length=50)),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engineering.account')),
            ],
        ),
        migrations.CreateModel(
            name='User_Project_Mapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engineering.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
