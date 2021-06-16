import csv
import random
from funkcje import *

koniec_symulacji = 200

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

def symuluj():
  stary_stan = poczatkowy_stan
  kroki_symulacji = [stary_stan]
  
  for t in range(1, koniec_symulacji):
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
    print("S:I:R (t=" + str(t) + "): " + str(100-liczba_chorych_t-liczba_ozdrowialych_t) + ":" + str(liczba_chorych_t) + ":" + str(liczba_ozdrowialych_t))
    
    kroki_symulacji = kroki_symulacji + [nowy_krok]
    # print(nowy_krok)
    # print("###")
    stary_stan = nowy_krok
  


# print(kroki_symulacji)
# animuj(graf, kroki_symulacji)
# print(kroki_symulacji)
# animuj(graf, kroki_symulacji)