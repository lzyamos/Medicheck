# Generated by Django 4.2.7 on 2024-02-17 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('ConditionID', models.AutoField(primary_key=True, serialize=False)),
                ('ConditionName', models.CharField(max_length=100)),
                ('Description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('RecordID', models.CharField(default='100001', max_length=10, primary_key=True, serialize=False)),
                ('Created_at', models.DateTimeField(auto_now_add=True)),
                ('First_name', models.CharField(max_length=50)),
                ('Last_name', models.CharField(max_length=50)),
                ('Email', models.CharField(max_length=100)),
                ('Phone', models.CharField(default='2457000000000', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('SymptomID', models.AutoField(primary_key=True, serialize=False)),
                ('SymptomName', models.CharField(max_length=100)),
                ('Description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('UserID', models.AutoField(primary_key=True, serialize=False)),
                ('Username', models.CharField(max_length=50, unique=True)),
                ('Password', models.CharField(max_length=100)),
                ('Email', models.CharField(max_length=100, unique=True)),
                ('FirstName', models.CharField(max_length=50)),
                ('LastName', models.CharField(max_length=50)),
                ('RegistrationDate', models.DateTimeField(auto_now_add=True)),
                ('Created_at', models.DateTimeField(auto_now_add=True)),
                ('Phone', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserTestHistory',
            fields=[
                ('TestHistoryID', models.AutoField(primary_key=True, serialize=False)),
                ('TestName', models.CharField(max_length=100)),
                ('TestDate', models.DateField()),
                ('TestResult', models.CharField(max_length=100)),
                ('Notes', models.TextField()),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserSymptom',
            fields=[
                ('UserSymptomID', models.AutoField(primary_key=True, serialize=False)),
                ('Severity', models.IntegerField()),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('SymptomID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.symptom')),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserCondition',
            fields=[
                ('UserConditionID', models.AutoField(primary_key=True, serialize=False)),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('ConditionID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.condition')),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.user')),
            ],
        ),
    ]
