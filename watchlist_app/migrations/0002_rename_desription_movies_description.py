# Generated by Django 4.0.5 on 2022-08-16 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movies',
            old_name='desription',
            new_name='description',
        ),
    ]