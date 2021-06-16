import csv
import random
from funkcje import *

Zdrowy = "Zdrowy"
Chory = "Chory"
Ozdrowialy = "Ozdrowialy"

# graf wygenerowany przy pomocy PaRMAT: https://github.com/kubajal/PaRMAT
# power law itp.
with open('krawedzie.csv', newline='') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  graf = {}
  for wiersz in reader:
    poczatek = int(wiersz[0])
    koniec = int(wiersz[1])
    if(poczatek not in graf):
      graf[poczatek] = [koniec]
    else:
      graf[poczatek] = graf[poczatek] + [koniec]
    if(koniec not in graf):
      graf[koniec] = [poczatek]
    else:
      graf[koniec] = graf[koniec] + [poczatek]

poczatkowy_stan = {}
with open('wezly.csv', newline='') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  i = 0
  for wiersz in reader:
    if(wiersz[0] == "1"):
      poczatkowy_stan[i] = Zdrowy
    else:
      poczatkowy_stan[i] = Chory
    i = i + 1
poczatkowy_stan["numer"] = 0

# print(stary_stan)
# print("------")

liczba_wezlow = len(graf.keys())
# print("liczba_wezlow=" + str(liczba_wezlow))

gamma = 0.05
beta = 0.10
r = beta / gamma

def symuluj(koniec_symulacji=200):
  stary_stan = poczatkowy_stan
  kroki = [stary_stan]
  chorzy = []
  ozdrowiali = []
  
  for t in range(0, koniec_symulacji):
    nowy_krok = {}
    nowy_krok["numer"] = t
    for chore_osoby_t in graf:
      if(stary_stan[chore_osoby_t] == Chory):
        if(random.random() < gamma):
          nowy_krok[chore_osoby_t] = Ozdrowialy
        else:
          nowy_krok[chore_osoby_t] = Chory
      elif(stary_stan[chore_osoby_t] == Zdrowy):
        sasiedzi = [chore_osoby_t for chore_osoby_t in graf]
        chorzy_sasiedzi = [chore_osoby_t for chore_osoby_t in graf if stary_stan[chore_osoby_t] == Chory]
        prog = beta * float(len(chorzy_sasiedzi)) / float(len(sasiedzi))
        # print("prog=" + str(prog) + ", r=" + str(r))
        if(random.random() < prog):
          nowy_krok[chore_osoby_t] = Chory
        else:
          nowy_krok[chore_osoby_t] = Zdrowy
      elif(stary_stan[chore_osoby_t] == Ozdrowialy):
          nowy_krok[chore_osoby_t] = Ozdrowialy
    chore_osoby_t = [chore_osoby_t for chore_osoby_t in nowy_krok if nowy_krok[chore_osoby_t] == Chory]
    liczba_chorych_t = len(chore_osoby_t)
    ozdrowiale_osoby_t = [chore_osoby_t for chore_osoby_t in nowy_krok if nowy_krok[chore_osoby_t] == Ozdrowialy]
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

koniec_symulacji = 200
liczba_symulacji = 5
for i in range(0, liczba_symulacji):
  symulacja = symuluj(koniec_symulacji)
  wynik["chorzy"] = wynik["chorzy"] + symulacja["chorzy"]
  wynik["ozdrowiali"] = wynik["ozdrowiali"] + symulacja["ozdrowiali"]
  wynik["iteracje"] = wynik["iteracje"] + [j for j in range(0, koniec_symulacji)]
  wynik["nr_symulacji"] = wynik["nr_symulacji"] + [i for j in range(0, koniec_symulacji)]

with open('symulacje.csv', 'w') as plik:
  plik.write("chorzy,ozdrowiali,iteracje,nr_symulacji\n")
  for i in range(0, koniec_symulacji * liczba_symulacji):
    wiersz = str(wynik["chorzy"][i])
    wiersz = wiersz + "," + str(wynik["ozdrowiali"][i])
    wiersz = wiersz + "," + str(wynik["iteracje"][i])
    wiersz = wiersz + "," + str(wynik["nr_symulacji"][i]) + '\n'
    plik.write(wiersz)
