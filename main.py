import csv
import random
from funkcje import *

dlugosc_choroby = 5
koniec_symulacji = 20

# graf wygenerowany przy pomocy PaRMAT: https://github.com/kubajal/PaRMAT
# power law itp.
with open('graf.csv', newline='') as csvfile:
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
with open('status.csv', newline='') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  i = 0
  for wiersz in reader:
    if(wiersz[0] == "1"):
      poczatkowy_stan[i] = [Status.Zdrowy, koniec_symulacji]
    else:
      poczatkowy_stan[i] = [Status.Chory, dlugosc_choroby]
    i = i + 1
poczatkowy_stan["numer"] = 0

# print(stary_stan)
# print("------")

liczba_wezlow = len(graf.keys())
# print("liczba_wezlow=" + str(liczba_wezlow))

def symulacja():
  kroki_symulacji = [poczatkowy_stan]
  stary_stan = poczatkowy_stan
  for t in range(1, koniec_symulacji):
    nowy_krok = {}
    nowy_krok["numer"] = t
    for wezel in graf:
      if(stary_stan[wezel][0] == Status.Chory):
        if(stary_stan[wezel][1] < t):
          nowy_krok[wezel] = [Status.Odporny, koniec_symulacji]
        else:
          nowy_krok[wezel] = [Status.Chory, stary_stan[wezel][1]]
      elif(stary_stan[wezel][0] == Status.Zdrowy):
        sasiedzi = [wezel for wezel in graf]
        chorzy_sasiedzi = [wezel for wezel in graf if stary_stan[wezel][0] == Status.Chory]
        prog = float(len(chorzy_sasiedzi)) / float(len(sasiedzi)) * float(liczba_wezlow)
        r = random.randint(0, 100)
        # print("prog=" + str(prog) + ", r=" + str(r))
        if(r < prog):
          nowy_krok[wezel] = [Status.Chory, t + dlugosc_choroby]
        else:
          nowy_krok[wezel] = [Status.Zdrowy, koniec_symulacji]
      elif(stary_stan[wezel][0] == Status.Odporny):
          nowy_krok[wezel] = [Status.Odporny, koniec_symulacji]
    kroki_symulacji = kroki_symulacji + [nowy_krok]
    stary_stan = nowy_krok
  return kroki_symulacji

wynik = symulacja()
animuj(graf, wynik)