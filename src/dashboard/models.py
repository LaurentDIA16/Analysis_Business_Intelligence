from django.db import models

# Create your models here.
class Country(models.Model):
    country = models.CharField(primary_key=True, max_length=50)
    zone = models.CharField(max_length=50, blank=True, null=True)


class DetailInvoice(models.Model):
    stockcode = models.ForeignKey('Product', models.DO_NOTHING, db_column='stockcode', blank=True, null=True)
    invoiceno = models.ForeignKey('Invoice', models.DO_NOTHING, db_column='invoiceno', blank=True, null=True)
    unitprice = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    quantity = models.DecimalField(max_digits=8, decimal_places=0, blank=False, null=False)
    totalcost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default="0")
    detailInvoice_id = models.AutoField(primary_key=True)
        
    class Meta:
        unique_together = ("invoiceno", "stockcode")


class Invoice(models.Model):
    invoiceno = models.CharField(primary_key=True, max_length=7)
    invoicedate = models.CharField(max_length=25, blank=True, null=True)
    customerid = models.DecimalField(max_digits=8, decimal_places=1, blank=True, null=True)
    country = models.ForeignKey(Country, models.DO_NOTHING, db_column='country')


class Product(models.Model):
    stockcode = models.CharField(primary_key=True, max_length=50)
    description = models.CharField(max_length=80, blank=True, null=True)


class Datatransfert(models.Model):
    invoiceno = models.CharField(max_length=7, blank=False, null=False)
    stockcode = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=80, blank=True, null=True)
    quantity = models.DecimalField(max_digits=8, decimal_places=0, blank=False, null=False)
    invoicedate = models.CharField(max_length=25, blank=False, null=False)
    unitprice = models.DecimalField(max_digits=8, decimal_places=2, blank=False, null=False)
    customerid = models.DecimalField(max_digits=8, decimal_places=1, blank=True, null=True)
    country = models.CharField(max_length=50, blank=False, null=False)
    totalcost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, default="0")

    #     #Calculer le coût total d'une ligne de commande le prix multiplié par la quantité
    # def save(self, *args, **kwargs):
    #     self.totalcost = self.unitprice * self.quantity
    #     super(Datatransfert, self).save(*args, **kwargs)