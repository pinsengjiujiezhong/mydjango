# Generated by Django 2.0 on 2019-09-16 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_course_org'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(default=1, upload_to='courses/%Y/%m', verbose_name='logo'),
            preserve_default=False,
        ),
    ]