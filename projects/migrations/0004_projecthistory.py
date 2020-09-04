# Generated by Django 3.0.6 on 2020-09-04 19:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0003_project_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=128)),
                ('old_value', models.CharField(max_length=128)),
                ('new_value', models.CharField(max_length=128)),
                ('date_changed', models.DateTimeField(auto_now_add=True)),
                ('icon_type', models.CharField(max_length=200)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]