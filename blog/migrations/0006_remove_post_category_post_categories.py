# Generated by Django 4.1.7 on 2023-02-16 04:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0005_post_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="category",
        ),
        migrations.AddField(
            model_name="post",
            name="categories",
            field=models.ManyToManyField(blank=True, null=True, to="blog.category"),
        ),
    ]
