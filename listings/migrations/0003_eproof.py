# Generated by Django 2.2 on 2020-06-14 00:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('listings', '0002_listing_contributor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Eproof',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docfile', models.FileField(upload_to='documents/docfiles/%Y/%m/%d/')),
                ('cardimage', models.FileField(upload_to='documents/docfiles/%Y/%m/%d/')),
                ('title', models.CharField(max_length=100)),
                ('list_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_published', models.BooleanField(default=True)),
                ('contributor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
