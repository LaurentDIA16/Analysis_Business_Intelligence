from django.db import models

# Create your models here.
class Zone(models.Model):
    nameZone = models.CharField(primary_key=True, max_length=50)

    class Meta:
        
        db_table = 'Zone'

class Country(models.Model):
    nameCountry = models.CharField(primary_key=True, max_length=50)
    nameZone = models.ForeignKey('Zone', models.DO_NOTHING, db_column='nameZone', blank=True, null=True)

    class Meta:
        
        db_table = 'Country'

class DetailInvoice(models.Model):
    stockCode = models.ForeignKey('Product', models.DO_NOTHING, db_column='stockCode', blank=True, null=True)
    invoiceNo = models.ForeignKey('Invoice', models.DO_NOTHING, db_column='invoiceNo', blank=True, null=True)
    unitPrice = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    detailInvoice_id = models.AutoField(primary_key=True)

    class Meta:
        
        db_table = 'DetailInvoice'

class Invoice(models.Model):
    invoiceNo = models.CharField(primary_key=True, max_length=6)
    invoiceDate = models.CharField(blank=True, max_length=25, null=True)
    customerID = models.CharField(max_length=5, blank=True, null=True)
    nameCountry = models.ForeignKey(Country, models.DO_NOTHING, db_column='nameCountry')

    class Meta:
        
        db_table = 'Invoice'

class Product(models.Model):
    stockCode = models.CharField(primary_key=True, max_length=50)
    description = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        
        db_table = 'Product'