# Generated by Django 2.0.2 on 2018-02-13 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_demo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aritcle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(blank=True, max_length=500, null=True)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
