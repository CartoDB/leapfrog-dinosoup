# Generated by Django 2.1.1 on 2018-09-27 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_deploy_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='repo_path',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]