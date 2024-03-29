# Generated by Django 2.0 on 2019-10-19 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20191019_1416'),
        ('courses', '0008_video_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='instructions',
            field=models.CharField(default='', max_length=200, verbose_name='课程须知'),
        ),
        migrations.AddField(
            model_name='course',
            name='learning',
            field=models.CharField(default='', max_length=200, verbose_name='能学到什么'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Teacher', verbose_name='讲课老师'),
        ),
    ]
