from django.conf import settings
from django.db import models
User = settings.AUTH_USER_MODEL

class Proposal(models.Model):
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

class PurchaseOrder(models.Model):
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

