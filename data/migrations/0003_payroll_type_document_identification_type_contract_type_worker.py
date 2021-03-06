# Generated by Django 3.2.8 on 2022-03-23 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_payment_form_payment_method_type_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payroll_Type_Document_Identification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.IntegerField()),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Type_Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.IntegerField()),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Type_Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_id', models.IntegerField()),
                ('name', models.CharField(max_length=80)),
            ],
        ),
    ]
