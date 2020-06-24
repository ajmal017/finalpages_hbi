from django.db import models
from django.utils import timezone
from members.models import Member

DOCUMENT_CHOICES = (
    ("PROPOSAL", "proposal"),
    ("EPROOF", "eproof"),
    ("POWERPOINT", "powerpoint"),
    ("BROCHURE", "brochure"),
    ("CERTIFICATE", "certificate"),
    ("MANUAL", "manual"),
)


COUNTRY_CHOICES = (
    ("ALL COUNTRIES", "All Countries"),
    ("BRUNEI", "Brunei"),
    ("CAMBODIA", "Cambodia"),
    ("HONG KONG", "Hong Kong"),
    ("INDONESIA", "Indonesia"),
    ("LAOS", "Laos"),
    ("MALAYSIA", "Malaysia"),
    ("MONGOLIA", "Mongolia"),
    ("MYANMAR", "Myanmar"),
    ("PAKISTAN", "Pakistan"),
    ("PHILIPPINES", "Philippines"),
    ("SINGAPORE", "Singapore"),
    ("THAILAND", "Thailand"),
    ("VIETNAM", "Vietnam"),
)




class Listing(models.Model):
    title = models.CharField(max_length=100)
    contributor = models.ForeignKey(Member, null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=DOCUMENT_CHOICES, default="miscellaneous")
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES, default="All")
    document_file = models.FileField(upload_to='documents/docfiles/%Y/%m/%d/')
    cover = models.ImageField(upload_to='documents/covers/%Y/%m/%d/', default="photos/images/preview1.png")
    preview_1 = models.ImageField(upload_to='documents/previews/%Y/%m/%d/', default="photos/images/preview1.png")
    preview_2 = models.ImageField(upload_to='documents/previews/%Y/%m/%d/', default="photos/images/preview1.png")
    preview_3 = models.ImageField(upload_to='documents/previews/%Y/%m/%d/', default="photos/images/preview1.png")
    list_date = models.DateTimeField(default=timezone.now, blank=False)
    is_published = models.BooleanField(default=True)

    def __str__(self):
      return self.title

    def delete(self, *args, **kwargs):
      self.docfile.delete()
      self.cover.delete()
      self.preview_1.delete()
      self.preview_2.delete()
      self.preview_3.delete()
      super().delete(*args, **kwargs)


class Eproof(models.Model):
    eproof_document = models.FileField(upload_to='documents/docfiles/%Y/%m/%d/')
    card_image = models.FileField(upload_to='documents/docfiles/%Y/%m/%d/')
    title = models.CharField(max_length=100)
    description = models.TextField(default=None)
    contributor = models.ForeignKey(Member, null=True, blank=True, on_delete=models.CASCADE)
    list_date = models.DateTimeField(default=timezone.now, blank=False)
    is_published = models.BooleanField(default=False)

    def __str__(self):
      return self.title

    def delete(self, *args, **kwargs):
      self.docfile.delete()
      self.card_image.delete()
      super().delete(*args, **kwargs)


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default=None)
    contributor = models.ForeignKey(Member, null=True, blank=True, on_delete=models.CASCADE)
    list_date = models.DateTimeField(default=timezone.now, blank=False)
    is_published = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=DOCUMENT_CHOICES)
    document_file = models.FileField(upload_to='documents/docfiles/%Y/%m/%d/')
    cover_file = models.ImageField(upload_to='documents/covers/%Y/%m/%d/', default="photos/images/preview1.png")
    image1_file = models.ImageField(upload_to='documents/images/%Y/%m/%d/', default="photos/images/preview1.png")
    image2_file = models.ImageField(upload_to='documents/images/%Y/%m/%d/', default="photos/images/preview1.png")
    image3_file = models.ImageField(upload_to='documents/images/%Y/%m/%d/', default="photos/images/preview1.png")

    def __str__(self):
      return self.title

    def delete(self, *args, **kwargs):
      self.document_file.delete()
      self.cover_file.delete()
      self.image1_file.delete()
      self.image2_file.delete()
      self.image3_file.delete()
      super().delete(*args, **kwargs)