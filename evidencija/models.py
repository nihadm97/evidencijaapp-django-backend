from django.db import models

class korisnik(models.Model):
    ime_korisnika = models.CharField(max_length=30)
    ime = models.CharField(max_length=30)
    prezime = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=10)
    oblik = models.CharField(max_length=30)
    status = models.CharField(max_length=30, default="Nije aktivan")
    stil = models.CharField(max_length=30, default="Standardna")


class evidencija(models.Model):
    predmet = models.CharField(max_length=30)
    datum = models.DateField()
    oblik = models.CharField(max_length=50)
    start = models.TimeField()
    end = models.TimeField()
    broj = models.IntegerField()
    weekday = models.CharField(max_length=20, default="")

class kuca(models.Model):
    osoblje = models.CharField(max_length=30)
    datum = models.DateField()
    oblik = models.CharField(max_length=30)
    status = models.CharField(max_length=30, default="Nije obrađeno")

class predmet(models.Model):
    ime = models.CharField(max_length=30)
    profesor = models.CharField(max_length=30)
    asistent = models.CharField(max_length=30)
    semestar = models.CharField(max_length=30)


