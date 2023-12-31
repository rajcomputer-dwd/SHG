# Generated by Django 4.2.3 on 2023-07-20 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shgapp', '0005_shgdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='shgtransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sycode', models.BigIntegerField()),
                ('society_name', models.CharField(max_length=255)),
                ('branchname', models.CharField(max_length=255)),
                ('taluka', models.CharField(max_length=255)),
                ('group_no', models.BigIntegerField()),
                ('group_name', models.CharField(max_length=1000)),
                ('date_of_advance', models.DateField()),
                ('loan_amt', models.BigIntegerField()),
                ('opeaning_outstanding_amt', models.BigIntegerField()),
                ('recovery_period_from', models.DateField()),
                ('recovery_period_to', models.DateField()),
                ('recovery_date', models.DateField()),
                ('no_of_days', models.BigIntegerField()),
                ('new_outstanding_amt', models.BigIntegerField()),
                ('principal_received', models.BigIntegerField()),
                ('interest_received', models.FloatField()),
                ('interest1', models.FloatField()),
                ('intreset2', models.FloatField()),
            ],
        ),
    ]
