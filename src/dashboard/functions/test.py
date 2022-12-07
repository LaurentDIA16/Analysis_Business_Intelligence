from dashboard.models import Product, Invoice, DetailInvoice, Country, Zone

Product.objects.all().delete()
Invoice.objects.all().delete()
DetailInvoice.objects.all().delete()
Country.objects.all().delete()
Zone.objects.all().delete()

Product.objects.create(stockCode='71053',description='WHITE METAL LANTERN')
sc = Product.objects.get(pk='71053')

Zone.objects.create(nameZone='Earth')
zn = Zone.objects.get(pk='Earth')

Country.objects.create(nameZone=zn, nameCountry='France')
cn = Country.objects.get(pk='France')

Invoice.objects.create(invoiceNo='536365',invoiceDate='12/01/2010  08:26:00',customerID='17850',nameCountry=cn)
io = Invoice.objects.get(pk='536365')

DetailInvoice.objects.create(stockCode=sc,invoiceNo=io,unitPrice='3.39',quantity='6',detailInvoice_id=1)