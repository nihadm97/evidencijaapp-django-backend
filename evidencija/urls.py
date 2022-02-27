from django.urls import path
from evidencija import views

urlpatterns = [
    path('registracija/', views.registracija, name = "registracija"),
    path('prijava/', views.prijava, name = "prijava"),
    path('evidencija/', views.evidencijanastave, name = "evidencija"),
    path('pocetna/', views.pocetna, name = "pocetna"),
    path('predmeti/', views.predmeti, name = "predmeti"),
    path('osoblje/', views.osoblje, name = "osoblje"),
    path('osoblje1/', views.osoblje1, name = "osoblje1"),
    path('kuca/', views.radodkuce, name = "kuca"),
    path('radodkuce/', views.osobljekuca, name = "osobljekuca"),
    path('obrisipredmet/', views.obrisipredmet, name = "obrisipredmet"),
    path('dodajpredmet/', views.dodajpredmet, name = "dodajpredmet"),
    path('upisikorisnika/', views.upisikorisnika, name = "upisikorisnika"),
    path('korisnici/', views.korisnici, name = "korisnici"),
    path('', views.test, name = "home"),
    path('username/', views.username, name = "username"),
    path('postavke/', views.postavke, name = "postavke"),
    path('odjava/', views.odjava, name = "odjava"),
    path('stil/', views.stil, name = "stil"),
    path('urediprofil/', views.urediprofil, name = "urediprofil"),
    path('email/', views.email, name = "email"),


]