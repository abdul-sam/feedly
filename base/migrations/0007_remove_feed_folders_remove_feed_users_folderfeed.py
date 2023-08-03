# Generated by Django 4.2.3 on 2023-08-03 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0006_favorite_favorite_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='folders',
        ),
        migrations.RemoveField(
            model_name='feed',
            name='users',
        ),
        migrations.CreateModel(
            name='FolderFeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folder_feeds', to='base.feed')),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folder_feeds', to='base.folder')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='folder_feeds', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]