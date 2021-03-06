# Generated by Django 2.0.2 on 2018-02-28 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_demo', '0005_auto_20180228_0601'),
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('comment', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='tag',
            field=models.TextField(blank=True, choices=[('teach', 'Teach'), ('life', 'Life')], max_length=5, null=True),
        ),
    ]
