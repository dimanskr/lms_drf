# Generated by Django 5.1.3 on 2024-11-26 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0004_subscription"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="course",
            options={
                "ordering": ("name",),
                "verbose_name": "курс",
                "verbose_name_plural": "курсы",
            },
        ),
    ]
