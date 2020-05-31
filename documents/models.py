from django.conf import settings
from django.db import models
User = settings.AUTH_USER_MODEL

class RawProductModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=1000)
    def __str__(self):
        return self.title

class ProductModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=1000, default=1)
    #pdf = models.FileField(upload_to='proposals/pdfs/%Y/%m/%d/')
    #cover = models.ImageField(upload_to='proposals/covers/%Y/%m/%d/', blank=True)
    def __str__(self):
        return self.title

class ProposalModel(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    pdf = models.FileField(upload_to='proposals/pdfs/%Y/%m/%d/')
    cover = models.ImageField(upload_to='proposals/covers/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)

class PurchaseOrderModel(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    pdf = models.FileField(upload_to='po/pdfs/%Y/%m/%d/')
    cover = models.ImageField(upload_to='po/covers/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)

