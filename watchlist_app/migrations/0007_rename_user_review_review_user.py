# Generated by Django 4.0.5 on 2022-09-17 21:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0006_review_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='user',
            new_name='review_user',
        ),
    ]