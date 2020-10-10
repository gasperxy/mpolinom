# Generated by Django 3.0.4 on 2020-10-10 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0008_auto_20201009_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='mpolynom',
            name='new_comments_authors',
            field=models.CharField(blank=True, max_length=5000),
        ),
        migrations.AlterField(
            model_name='mpolynom',
            name='new_comments',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mpolynom',
            name='new_keywords',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='mpolynom',
            name='new_links',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mpolynom',
            name='new_references',
            field=models.TextField(blank=True),
        ),
    ]
