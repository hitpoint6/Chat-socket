# Generated by Django 3.1.3 on 2020-11-16 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='authors',
            field=models.ManyToManyField(blank=True, to='chat.Participant'),
        ),
    ]
