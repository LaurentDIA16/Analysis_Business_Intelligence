# Generated by Django 3.1.7 on 2022-12-05 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('nameCountry', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Country',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('stockCode', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=80, null=True)),
            ],
            options={
                'db_table': 'Product',
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('nameZone', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Zone',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('invoiceNo', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('invoiceDate', models.DateTimeField(blank=True, null=True)),
                ('customerID', models.CharField(blank=True, max_length=5, null=True)),
                ('nameCountry', models.ForeignKey(db_column='nameCountry', on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.country')),
            ],
            options={
                'db_table': 'Invoice',
            },
        ),
        migrations.CreateModel(
            name='DetailInvoice',
            fields=[
                ('unitPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('detailInvoice_id', models.AutoField(primary_key=True, serialize=False)),
                ('invoiceNo', models.ForeignKey(blank=True, db_column='invoiceNo', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.invoice')),
                ('stockCode', models.ForeignKey(blank=True, db_column='stockCode', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.product')),
            ],
            options={
                'db_table': 'DetailInvoice',
            },
        ),
    ]
