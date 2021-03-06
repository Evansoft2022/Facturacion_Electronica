# Generated by Django 3.2.8 on 2022-04-05 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        ('data', '0003_payroll_type_document_identification_type_contract_type_worker'),
        ('client', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='POS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.TextField()),
                ('prefix', models.TextField()),
                ('code', models.TextField()),
                ('quanty', models.TextField()),
                ('description', models.TextField()),
                ('price', models.TextField()),
                ('tax', models.TextField()),
                ('notes', models.TextField()),
                ('date', models.TextField()),
                ('ipo', models.TextField()),
                ('discount', models.TextField()),
                ('type', models.TextField(default='FE')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
            ],
        ),
        migrations.CreateModel(
            name='Wallet_POS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.TextField()),
                ('date', models.TextField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
                ('pos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.pos')),
            ],
        ),
        migrations.CreateModel(
            name='Payment_Form_Invoice_POS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_due_date', models.TextField()),
                ('duration_measure', models.TextField()),
                ('payment_form_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.payment_form')),
                ('payment_method_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data.payment_method')),
                ('pos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.pos')),
            ],
        ),
    ]
