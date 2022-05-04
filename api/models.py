from django.db import models

# Create your models here.

class StationDatas(models.Model):
    ID = models.AutoField(primary_key=True)
    Date = models.CharField(max_length=15)
    Time = models.IntegerField()
    T = models.FloatField()
    Tmax = models.FloatField()
    Tmin = models.FloatField()
    RH = models.FloatField()
    RHmax = models.FloatField()
    RHmin = models.FloatField()
    PtOrvalhoinst = models.FloatField()
    PtOrvalhomax = models.FloatField()
    PtOrvalhomin = models.FloatField()
    P = models.FloatField()
    Pmax = models.FloatField()
    Pmin = models.FloatField()
    u2 = models.FloatField()
    Vdir = models.FloatField()
    Vraj = models.FloatField()
    Rn = models.FloatField()
    PREC = models.FloatField()
