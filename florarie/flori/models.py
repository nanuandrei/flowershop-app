from django.db import models
from django.contrib.auth.models import User

# Create your models here.
tip_CHOICES = (
    ('Floare','Floare'),
    ('Buchet', 'Buchet'),
    ('Ghiveci', 'Ghiveci')
)

class Produse(models.Model):
    nume=models.CharField(max_length=60)
    poza = models.ImageField(upload_to='poze/', default='poze/none.png',
                                  null=True, blank=True)
    descriere=models.TextField()
    pret=models.FloatField()
    pret_cumparare = models.FloatField()
    stoc=models.IntegerField(default=0)
    tip = models.CharField(max_length=9, choices=tip_CHOICES, default='Floare')

class Poze(models.Model):
    poza = models.ImageField(upload_to='poze/', default='poze/none.png', null=True, blank=True)
    produse_id = models.ForeignKey(Produse, on_delete=models.CASCADE, null=True, blank=True)


class Useri(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    adresa=models.TextField()
    telefon=models.CharField(max_length=12)


class Comanda(models.Model):
    pret_achizitie=models.FloatField()
    numar = models.PositiveSmallIntegerField(default=1)
    data = models.DateField(auto_now_add=True)
    produs = models.ForeignKey(Produse, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(Useri, on_delete=models.CASCADE, null=True, blank=True)
    finalizat = models.BooleanField(default=False)


