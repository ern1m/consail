# Generated by Django 4.0 on 2022-10-15 16:38

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.user')),
            ],
            options={
                'verbose_name': 'student',
                'verbose_name_plural': 'students',
            },
            bases=('users.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
