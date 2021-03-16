from django.db import models


class Material(models.Model):
    ayakkabi = models.CharField(max_length=120, blank=True, null=True)
    esofman = models.CharField(max_length=120, blank=True, null=True)
    tshirt = models.CharField(max_length=120, blank=True, null=True)
    guresayakkabi = models.CharField(max_length=120, blank=True, null=True)
    sporayakkabi = models.CharField(max_length=120, blank=True, null=True)
    klasikayakkabi = models.CharField(max_length=120, blank=True, null=True)
