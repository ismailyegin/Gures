# Generated by Django 2.2.6 on 2021-01-19 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sbs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='directorymember',
            name='commission',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='sbs.DirectoryCommission', verbose_name='Kurulu'),
            preserve_default=False,
        ),
    ]
