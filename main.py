import csv
import random
from funkcje import *

zdrowy = "Zdrowy"
chory = "Chory"
ozdrowialy = "Ozdrowialy"

def wrapper_symulacji(parametry = {}):
  nazwa="symulacja"
  gamma=0.05
  beta=0.10
  koniec_symulacji=200
  liczba_symulacji=5
  krawedzie="krawedzie.csv"
  wezly="wezly.csv"
  if("nazwa" in parametry):
    nazwa = parametry["nazwa"]
  if("gamma" in parametry):
    gamma = parametry["gamma"]
  if("beta" in parametry):
    beta = parametry["beta"]
  if("koniec_symulacji" in parametry):
    koniec_symulacji = parametry["koniec_symulacji"]
  if("liczba_symulacji" in parametry):
    liczba_symulacji = parametry["liczba_symulacji"]
  if("krawedzie" in parametry):
    krawedzie = parametry["krawedzie"]
  if("wezly" in parametry):
    wezly = parametry["wezly"]

  with open(krawedzie, newline='') as plik:
    reader = csv.reader(plik, delimiter=',')
    graf = {}
    for tekst in reader:
      poczatek = int(tekst[0])
      koniec = int(tekst[1])
      if(poczatek not in graf):
        graf[poczatek] = [koniec]
      else:
        graf[poczatek] = graf[poczatek] + [koniec]
      if(koniec not in graf):
        graf[koniec] = [poczatek]
      else:
        graf[koniec] = graf[koniec] + [poczatek]

  poczatkowy_stan = {}
  with open(wezly, newline='') as plik:
    reader = csv.reader(plik, delimiter=',')
    i = 0
    for tekst in reader:
      if(tekst[0] == "1"):
        poczatkowy_stan[i] = zdrowy
      else:
        poczatkowy_stan[i] = chory
      i = i + 1
  poczatkowy_stan["numer"] = 0

  def symuluj(koniec_symulacji=200):
    stary_stan = poczatkowy_stan
    kroki = [stary_stan]
    chorzy = []
    ozdrowiali = []
    
    for t in range(0, koniec_symulacji):
      nowy_krok = {}
      nowy_krok["numer"] = t
      for chore_osoby_t in graf:
        if(stary_stan[chore_osoby_t] == chory):
          if(random.random() < gamma):
            nowy_krok[chore_osoby_t] = ozdrowialy
          else:
            nowy_krok[chore_osoby_t] = chory
        elif(stary_stan[chore_osoby_t] == zdrowy):
          sasiedzi = [chore_osoby_t for chore_osoby_t in graf]
          chorzy_sasiedzi = [chore_osoby_t for chore_osoby_t in graf if stary_stan[chore_osoby_t] == chory]
          prog = beta * float(len(chorzy_sasiedzi)) / float(len(sasiedzi))
          # print("prog=" + str(prog) + ", r=" + str(r))
          if(random.random() < prog):
            nowy_krok[chore_osoby_t] = chory
          else:
            nowy_krok[chore_osoby_t] = zdrowy
        elif(stary_stan[chore_osoby_t] == ozdrowialy):
            nowy_krok[chore_osoby_t] = ozdrowialy
      chore_osoby_t = [chore_osoby_t for chore_osoby_t in nowy_krok if nowy_krok[chore_osoby_t] == chory]
      liczba_chorych_t = len(chore_osoby_t)
      ozdrowiale_osoby_t = [chore_osoby_t for chore_osoby_t in nowy_krok if nowy_krok[chore_osoby_t] == ozdrowialy]
      liczba_ozdrowialych_t = len(ozdrowiale_osoby_t)
      # print("S:I:R (t=" + str(t) + "): " + str(100-liczba_chorych_t-liczba_ozdrowialych_t) + ":" + str(liczba_chorych_t) + ":" + str(liczba_ozdrowialych_t))
      
      kroki = kroki + [nowy_krok]
      chorzy = chorzy + [liczba_chorych_t]
      ozdrowiali = ozdrowiali + [liczba_ozdrowialych_t]
      stary_stan = nowy_krok

    return {
      "chorzy": chorzy,
      "ozdrowiali": ozdrowiali,
      "kroki": kroki
    }
  
  wynik = {
    "chorzy": [],
    "ozdrowiali": [],
    "iteracje": [],
    "nr_symulacji": []
  }

  for i in range(0, liczba_symulacji):
    symulacja = symuluj(koniec_symulacji)
    wynik["chorzy"] = wynik["chorzy"] + symulacja["chorzy"]
    wynik["ozdrowiali"] = wynik["ozdrowiali"] + symulacja["ozdrowiali"]
    wynik["iteracje"] = wynik["iteracje"] + [j for j in range(0, koniec_symulacji)]
    wynik["nr_symulacji"] = wynik["nr_symulacji"] + [i for j in range(0, koniec_symulacji)]

  with open(nazwa + ".csv", 'w') as plik:
    plik.write("chorzy,ozdrowiali,iteracje,nr_symulacji\n")
    tekst=""
    for i in range(0, koniec_symulacji * liczba_symulacji):
      tekst = tekst + str(wynik["chorzy"][i])
      tekst = tekst + "," + str(wynik["ozdrowiali"][i])
      tekst = tekst + "," + str(wynik["iteracje"][i])
      tekst = tekst + "," + str(wynik["nr_symulacji"][i]) + '\n'
    plik.write(tekst)

konfiguracja = [
  {
    "nazwa": "bezskalowa",
    "wezly": "wezly.csv",
    "krawedzie": "krawedzie.csv",
    "liczba_symulacji": 100
  }
]

for symulacja in konfiguracja:
  wrapper_symulacji(symulacja)