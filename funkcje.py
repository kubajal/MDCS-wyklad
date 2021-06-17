import networkx as nx
import statistics
import matplotlib.pyplot as plt
from matplotlib.image import AxesImage
import matplotlib.animation as animation
from networkx import exception
import csv

stan_zdrowy = "Zdrowy"
stan_chory = "Chory"
stan_ozdrowialy = "Ozdrowialy"

def wczytaj_graf(krawedzie):
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

  return graf

def konwertuj_do_networkX(graf):
  G = nx.DiGraph()
  wezly = graf.keys()
  krawedzie = [(zrodlo, cel) for (zrodlo, cele) in graf.items() for cel in cele]
  for w in wezly:
    G.add_node(w)
  for e in krawedzie:
    G.add_edge(e[0], e[1])
  return G

def rysuj_graf(self, G):
  pos = nx.spectral_layout(G)
  nx.draw_networkx(G, pos)
  plt.show()

def konwertuj_slownik_do_networkX(graf = {'1': ['1']}):
  G = nx.DiGraph()
  wezly_zrodla = set(graf.keys())
  wezly_cele = set([w for lista in list(graf.values()) for w in lista]) # flattening
  if(not set.issubset(wezly_zrodla, wezly_cele)):
    raise Exception("Wezly docelowe nie sa podzbiorem wszystkich wezlow")
  for zrodlo in wezly_zrodla:
    G.add_node(zrodlo)
  for zrodlo in wezly_zrodla:
    for cel in graf[zrodlo]:
      G.add_edge(zrodlo, cel)
  return G
  
def animuj(graf, kroki):
  print(len(kroki))
  print("Konwertuje do networkX")
  G = konwertuj_do_networkX(graf)
  print("Obliczam pozycje")
  position = nx.spring_layout(G, iterations=10)
  figure, ax = plt.subplots(figsize=(10,8))
  def rysuj_krok(krok):
    ax.clear()
    # krok = k.copy()
    # print(krok)
    numer = krok["numer"]
    kolory = []
    wezly_id = []
    for wezel in graf:
      if(wezel != "numer"):
        wezly_id = wezly_id + [wezel]
        if(krok[wezel] == stan_chory):
          kolory = kolory + ["red"]
        elif(krok[wezel] == stan_zdrowy):
          kolory = kolory + ["green"]
        elif(krok[wezel] == stan_ozdrowialy):
          kolory = kolory + ["blue"]
        else:
          raise Exception("cos poszlo bardzo zle")
    ax.set_title(f"numer kroku: {numer}\n")
    nx.draw_networkx(G, position, nodelist=wezly_id, node_color=kolory)
    # plt.show()
  
  # print("Rysuje animacje")
  # for krok in kroki:
  #   rysuj_krok(krok)
  ani = animation.FuncAnimation(figure, rysuj_krok, kroki, repeat=False)
  ani.save('./symulacja.gif', writer='imagemagick')
  #plt.show()

def generuj_graf_erdos(plik_wyjsciowy="wejscie/erdos.csv", n=100, avg=5):
  p = avg/n
  graf = nx.gnp_random_graph(n,p)
  while(not nx.is_connected(graf)):
    graf = nx.gnp_random_graph(n,p)
  with open(plik_wyjsciowy, 'w') as plik:
    nx.write_edgelist(graf, plik_wyjsciowy, delimiter=',', data=False)
  stopnie = [graf.degree(wezel) for wezel in graf.nodes()]
  plt.hist(stopnie)
  print("sredni stopien: " + str(statistics.mean(stopnie)))
  plt.show()

def generuj_graf_barabasi(plik_wyjsciowy="wejscie/barabasi.csv", n=100, avg=2.5):
  m = avg
  graf = nx.barabasi_albert_graph(n, m)
  while(not nx.is_connected(graf)):
    graf = nx.barabasi_albert_graph(n, m)
  with open(plik_wyjsciowy, 'w') as plik:
    nx.write_edgelist(graf, plik_wyjsciowy, delimiter=',', data=False)
  stopnie = [graf.degree(wezel) for wezel in graf.nodes()]
  plt.hist(stopnie)
  print("sredni stopien: " + str(statistics.mean(stopnie)))
  plt.show()