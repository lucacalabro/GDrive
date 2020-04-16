# Generated by Django 3.0.5 on 2020-04-16 09:30

from django.db import migrations, models
import formuploadtogdrive.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field1', models.CharField(max_length=20)),
                ('field2', models.CharField(max_length=20)),
                ('document', models.FileField(upload_to=formuploadtogdrive.models.path_and_rename)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Utenti',
            },
        ),
    ]
