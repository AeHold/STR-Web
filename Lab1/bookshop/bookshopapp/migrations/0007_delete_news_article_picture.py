# Generated by Django 4.2.5 on 2023-09-14 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshopapp', '0006_news'),
    ]

    operations = [
        migrations.DeleteModel(
            name='News',
        ),
        migrations.AddField(
            model_name='article',
            name='picture',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
