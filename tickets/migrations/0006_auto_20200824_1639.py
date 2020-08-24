# Generated by Django 3.0.6 on 2020-08-24 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_history_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('OPEN', 'Open'), ('IN_PROGRESS', 'In Progress'), ('RESOLVED', 'Resolved'), ('CLOSED', 'Closed'), ('WAITING_ON_MORE_INFO', 'Waiting on More Info')], default='OPEN', max_length=128),
        ),
    ]
