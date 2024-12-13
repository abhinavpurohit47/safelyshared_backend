# Generated by Django 5.1.4 on 2024-12-13 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_uploadedfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='EncryptionKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_name', models.CharField(max_length=255, unique=True)),
                ('key_value', models.BinaryField()),
            ],
        ),
        migrations.RemoveField(
            model_name='uploadedfile',
            name='file',
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='encrypted_content',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='file_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
