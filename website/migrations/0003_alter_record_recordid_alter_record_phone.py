# Generated by Django 4.2.7 on 2024-01-30 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_remove_record_id_record_recordid_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='RecordID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='record',
            name='phone',
            field=models.CharField(default='2457000000000', max_length=15),
        ),
    ]