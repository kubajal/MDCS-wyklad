import matplotlib.pyplot as plt
import pandas as pd

pliki = ["wyjscie/barabasi_wynik.csv", "wyjscie/erdos_wynik.csv"]
for plik in pliki:
  dane = pd.read_csv(plik, delimiter=",")
  dane_zgroupowane = dane.groupby("nr_symulacji")
  dane_zgroupowane["chorzy"].value_counts()
  fig1, ax1 = plt.subplots(figsize=(8,6))
  ax1.set_title(plik + ": chorzy")
  for grupa in dane_zgroupowane.groups:
    symulacja = dane_zgroupowane.get_group(grupa)
    symulacja.plot(x="iteracje", y="chorzy", legend=False, ax=ax1, alpha=0.1, color="black")
  # df1.plot(kind="kde", ax=ax)
  ax1.set_ylabel("chorzy")
  plt.show()
  fig2, ax2 = plt.subplots(figsize=(8,6))
  ax2.set_title(plik + ": chorzy + ozdrowiali")
  for grupa in dane_zgroupowane.groups:
    symulacja = dane_zgroupowane.get_group(grupa)
    symulacja["chorzy + ozdrowiali"] = symulacja["chorzy"] + symulacja["ozdrowiali"]
    symulacja.plot(x="iteracje", y="chorzy + ozdrowiali", legend=False, ax=ax2, alpha=0.1, color="black")
  # df1.plot(kind="kde", ax=ax)
  ax2.set_ylabel("chorzy + ozdrowiali")
  plt.show()