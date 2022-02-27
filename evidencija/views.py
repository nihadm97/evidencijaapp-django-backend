import json
import datetime

from django.core.mail import send_mail
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from evidencija.models import korisnik, evidencija, kuca, predmet
from django.core import serializers
def test(request):
    return HttpResponse("Test")

@api_view(['POST'])
def registracija(request):
     ime = request.data.get('ime')
     prezime = request.data.get('prezime')
     username = request.data.get('ime_korisnika')
     email = request.data.get('email')
     password = request.data.get('password')
     password1 = request.data.get('password1')
     traziime = korisnik.objects.filter(ime_korisnika=username)
     traziemail = korisnik.objects.filter(email=email)
     if traziime:
         print("Korisničko ime zauzeto")
         return HttpResponse("Korisničko ime zauzeto")
     elif traziemail:
         print("Email je registrovan sa drugim profilom")
         return HttpResponse("Email je registrovan sa drugim profilom")
     elif password1!=password:
         print("Lozinke se ne podudaraju")
         return HttpResponse("Lozinke se ne podudaraju")
     else:
        osoba = korisnik()
        osoba.ime_korisnika = username
        osoba.password = password
        osoba.ime = ime
        osoba.prezime = prezime
        osoba.password = password
        osoba.email = email
        osoba.save()
        return HttpResponse("Registrovan korisnik")


@api_view(['POST'])
def prijava(request):
   username = request.data.get('ime_korisnika')
   password = request.data.get('password')
   trazi = korisnik.objects.filter(ime_korisnika= username).filter(password=password)
   if trazi:
        korisnik.objects.filter(ime_korisnika=username).update(status="Aktivan")
        return HttpResponse("Uspješna prijava")
   else:
        return HttpResponse("Pogrešno korisničko ime ili lozinka")

@api_view(['POST'])
def evidencijanastave(request):
   predmet = request.data.get('predmet')
   datum = request.data.get('datum')
   oblik = request.data.get('oblik')
   start = request.data.get('start')
   end = request.data.get('end')
   broj = request.data.get('broj')
   cas = evidencija()
   cas.predmet = predmet
   cas.datum = datum
   cas.oblik = oblik
   cas.start = start
   cas.end = end
   cas.broj = broj
   cas.save()
   return HttpResponse("Upisana evidencija")


@api_view(['POST'])
def odjava(request):
    username=request.data.get('username')
    objekti=korisnik.objects.filter(ime_korisnika=username).update(status="Nije aktivan")
    return HttpResponse("Uspješna odjava")

@api_view(['POST'])
def stil(request):
    stil=request.data.get('oblik')
    objekti=korisnik.objects.filter(status="Aktivan").update(stil=stil)
    return HttpResponse("Uspješna promjena stila")

@api_view(['POST'])
def urediprofil(request):
    ime = request.data.get('ime')
    prezime = request.data.get('prezime')
    sifra = request.data.get('sifra')
    sifra1 = request.data.get('sifra1')
    if sifra==sifra1:
        objekti=korisnik.objects.filter(status="Aktivan").update(ime= ime, prezime= prezime, password= sifra)
        return HttpResponse("Uspješno spremljene promjene")
    else:
        return HttpResponse("Lozinke se ne podudaraju")


@api_view(['POST'])
def radodkuce(request):
   osoblje = request.data.get('osoblje')
   datum = request.data.get('datum')
   oblik = request.data.get('oblik')
   rad = kuca()
   rad.osoblje = osoblje
   rad.datum = datum
   rad.oblik = oblik
   rad.save()
   return HttpResponse("Uspješno poslan zahtjev za rad od kuće")


@api_view(['POST'])
def obrisipredmet(request):
   ime = request.data.get('predmet')
   predmet.objects.filter(ime=ime).delete()
   return HttpResponse("Predmet je uspješno obrisan")

@api_view(['POST'])
def email(request):
   email = request.data.get('email')
   pwd = korisnik.objects.filter(email=email).values("password")
   for course in pwd:
       password = (course['password'])
       send_mail(
            'Zahtjev za zaboravljenu lozinku na evidencija-app',
            'Vaša lozinka je ' + password,
            "evidencijaapp@gmail.com",
            [email],
            fail_silently=False,
            )
   return HttpResponse("Lozinka vam je uspješno poslan na email")


@api_view(['POST'])
def dodajpredmet(request):
   ime = request.data.get('predmet')
   profesor = request.data.get('profesor')
   asistent = request.data.get('asistent')
   trazipredmet = predmet.objects.filter(ime=ime)
   if trazipredmet:
       return HttpResponse("Predmet već postoji, ako želite urediti predmet prvo ga obrišite")
   novi = predmet()
   novi.ime = ime
   novi.profesor = profesor
   novi.asistent = asistent
   novi.semestar = 0
   novi.save()
   return HttpResponse("Uspješno dodan predmet")

@api_view(['POST'])
def upisikorisnika(request):
   ime = request.data.get('ime')
   prezime = request.data.get('prezime')
   oblik = request.data.get('oblik')
   novi = korisnik()
   novi.ime = ime
   novi.prezime = prezime
   novi.oblik = oblik
   novi.ime_korisnika = ""
   novi.email = ""
   novi.password = ""
   novi.save()
   return HttpResponse("Uspješno dodan korisnik")


@api_view(['GET'])
def pocetna(request):
    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(7)
    objekti = evidencija.objects.all()
    username = korisnik.objects.get(status="Aktivan")
    for i in objekti:
        objekti.filter(datum = start_week).update(weekday = "Ponedjeljak")
        objekti.filter(datum=start_week+datetime.timedelta(1)).update(weekday="Utorak")
        objekti.filter(datum=start_week+datetime.timedelta(2)).update(weekday="Srijeda")
        objekti.filter(datum=start_week+datetime.timedelta(3)).update(weekday="Četvrtak")
        objekti.filter(datum=start_week+datetime.timedelta(4)).update(weekday="Petak")
        objekti.filter(datum=start_week+datetime.timedelta(5)).update(weekday="Subota")
        objekti.filter(datum=start_week+datetime.timedelta(6)).update(weekday="Nedjelja")
    if username.oblik == "Šef odsjeka" or username.oblik == "Dekan":
        lista = json.dumps(list(objekti.filter(datum__range=[start_week, end_week]).values("predmet", "start", "oblik", "end", "broj", "weekday")), cls=DjangoJSONEncoder)
        return HttpResponse(lista)
    else:
        if username.oblik == "Profesor":
            predmeti = predmet.objects.filter(profesor = username.ime + " " + username.prezime).values("ime")
            termini = predmet.objects.none()
            for i in predmeti:
                termini |= evidencija.objects.filter(predmet = i['ime'], datum__range=[start_week, end_week]).values("predmet", "start", "oblik", "end", "broj", "weekday")
            lista = json.dumps(list(termini), cls=DjangoJSONEncoder)
            return HttpResponse(lista)
        elif username.oblik == "Asistent":
            predmeti = predmet.objects.filter(asistent=username.ime + "" + username.prezime).values("ime")
            termini = predmet.objects.none()
            for i in predmeti:
                termini |= evidencija.objects.filter(predmet=i['ime'], datum__range=[start_week, end_week]).values("predmet", "start", "oblik", "end", "broj", "weekday")
            lista = json.dumps(list(termini), cls=DjangoJSONEncoder)
            return HttpResponse(lista)

@api_view(['GET'])
def username(request):
    objekti=korisnik.objects.filter(status="Aktivan")
    lista = serializers.serialize('json', objekti)
    return HttpResponse(lista)


@api_view(['GET'])
def predmeti(request):
    objekti = predmet.objects.all()
    predmeti = serializers.serialize('json', objekti)
    return HttpResponse(predmeti)


@api_view(['GET'])
def korisnici(request):
    objekti = korisnik.objects.all()
    korisnici = serializers.serialize('json', objekti)
    return HttpResponse(korisnici)

@api_view(['GET'])
def postavke(request):
    objekti=korisnik.objects.filter(status="Aktivan")
    korisnici = serializers.serialize('json', objekti)
    return HttpResponse(korisnici)


@api_view(['GET'])
def osobljekuca(request):
    objekti = kuca.objects.all()
    date = datetime.date.today()
    start_week = date - datetime.timedelta(date.weekday())
    end_week = start_week + datetime.timedelta(7)
    lista = json.dumps(list(objekti.filter(datum__range=[start_week, end_week]).values("osoblje", "oblik", "status", "datum")), cls=DjangoJSONEncoder)
    return HttpResponse(lista)


@api_view(['GET'])
def osoblje(request):
    objekti = predmet.objects.all()
    osoblje = serializers.serialize('json', objekti)
    return HttpResponse(osoblje)

@api_view(['GET'])
def osoblje1(request):
    objekti = predmet.objects.all()
    username = korisnik.objects.get(status="Aktivan")
    if username.oblik == "Šef odsjeka" or username.oblik == "Dekan":
        lista = json.dumps(list(objekti.values("ime", "profesor", "asistent")), cls=DjangoJSONEncoder)
        return HttpResponse(lista)
    else:
        if username.oblik == "Profesor":
            predmeti = predmet.objects.filter(profesor=username.ime + " " + username.prezime).values("ime")
            termini = predmet.objects.none()
            for i in predmeti:
                termini |= predmet.objects.filter(ime=i['ime']).values("ime", "profesor", "asistent")
            lista = json.dumps(list(termini), cls=DjangoJSONEncoder)
            return HttpResponse(lista)
        elif username.oblik == "Asistent":
            predmeti = predmet.objects.filter(asistent=username.ime + "" + username.prezime).values("ime")
            termini = predmet.objects.none()
            for i in predmeti:
                termini |= predmet.objects.filter(ime=i['ime']).values("ime", "profesor", "asistent")
            lista = json.dumps(list(termini), cls=DjangoJSONEncoder)
            return HttpResponse(lista)



