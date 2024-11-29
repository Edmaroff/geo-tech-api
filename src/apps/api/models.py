from django.db import models


class Station(models.Model):
    ne = models.CharField(max_length=255, unique=True, verbose_name="ID станции")
    address = models.TextField(verbose_name="Адрес")
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    gsm = models.BooleanField(default=False, verbose_name="GSM")
    umts = models.BooleanField(default=False, verbose_name="UMTS")
    lte = models.BooleanField(default=False, verbose_name="LTE")
    status = models.BooleanField(verbose_name="Статус")

    def __str__(self):
        return self.ne

    class Meta:
        verbose_name = "Станция"
        verbose_name_plural = "Станции"
        ordering = ["ne"]
