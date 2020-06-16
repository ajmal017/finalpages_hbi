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
    ("MISCELLANEOUS", "miscellaneous"),
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
    docfile = models.FileField(upload_to='documents/docfiles/%Y/%m/%d/')
    cover = models.ImageField(upload_to='documents/covers/%Y/%m/%d/', blank=True)
    preview_1 = models.ImageField(upload_to='documents/previews/%Y/%m/%d/', blank=True)
    preview_2 = models.ImageField(upload_to='documents/previews/%Y/%m/%d/', blank=True)
    preview_3 = models.ImageField(upload_to='documents/previews/%Y/%m/%d/', blank=True)
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
    docfile = models.FileField(upload_to='documents/docfiles/%Y/%m/%d/')
    cardimage = models.FileField(upload_to='documents/docfiles/%Y/%m/%d/')
    title = models.CharField(max_length=100)
    contributor = models.ForeignKey(Member, null=True, blank=True, on_delete=models.CASCADE)
    list_date = models.DateTimeField(default=timezone.now, blank=False)
    is_published = models.BooleanField(default=True)

    def __str__(self):
      return self.title

    def delete(self, *args, **kwargs):
      self.docfile.delete()
      self.cardimage.delete()
      super().delete(*args, **kwargs)
