# Generated by Django 5.0.6 on 2024-06-28 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='date_of_birth',
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('created', 'Создано'), ('in_progress', 'В процессе'), ('done', 'Готово')], default='created', max_length=20),
        ),
    ]
