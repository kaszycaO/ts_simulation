# NetSimulation

Prosty program sluzacy do badania niezawodności sieci.

### Wymagania

```
networkx:  pip install networkx 
pyvis:     pip instal pyvis
```

## Uruchomienie

```
python3 main.py --option [param] [MAX] [T_MAX] [p]
python3 main.py --option namefile
```


## Info
Obowiazkowe: (param)
* N -> modyfikacja macierzy natezen
* C -> modyfikacja przepustowosci
* T -> modyfikacja struktury grafu
* none/inny dowolny znak -> badanie podstawowego modelu

Dodatkowe:  
**W przypadku chęci skorzystania nalezy wybrac wszystkie!**
* MAX -> maksymalna liczba pakietow/sek
* T_MAX -> maksymalne opóźnienie
* p -> prawdopodobieństwo nieuszkodzenia łącza
