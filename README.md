# Sprawozdanie z projektu - przedmiot IUM - etap 2.
Wojciech Sitek, Maciej Kasprzyk

## Wstęp
Opis realizacji etapu 1. (opis realizowanego zadania, założenia) jest dostępny w [tym notatniku](1-data-analysis/1-data-analysis.ipynb).
W ramach etapu 2.:
 - stworzyliśmy rozwiązanie oszacowujące wysokość najlepszej zniżki
 - zaimplementowaliśmy serwer umożliwiający korzystanie z rozwiązania poprzez zapytania HTTP oraz pozwalający wykonać test A/B
 - napisaliśmy klienta, który przeprowadza sztuczny test A/B
 
 ## Trenowanie
Kod trenujący model znajduję sie oraz jest opisany w [tym notatniku](4-train/train.ipynb).
Model został porównany z modelem bazowym, który zawsze zwraca najczęstsza klasę.

## Oszacowanie najlepszej zniżki
Wyjściem naszego modelu jest prawdopodobieństwo zakupu.
Przydzielona zniżka jest jednym z atrybutów.
Założyliśmy, że możliwe zniżki to `0, 5, 10, 15, 20%`.
W naszym oszacowaniu założyliśmy, że dochód ze sprzedaży każdego produktu jest stały i wynosi `40%`.
Wybieramy najlepszą zniżkę wg następującego schematu:
 - badamy `prawdopodobieństwo` jako wyjście modelu dla kolejnych zniżek
 - dla każdej zniżki liczby wartość średniego procentowego zysku wg wzoru:
  `(40% - zniżka) * prawdopodobieństwo`
 - wybieramy wysokość zniżki, dla której ta wartość jest najwyższa
 
## Serwer
Serwer napisaliśmy z użyciem `django` oraz `django rest framework`.
Posiada on 4 punkty końcowe. Zapytania wysyłane są metodami POST oraz GET, dane przekazywane są w formacie JSON.
Dane zapisywane są bazie danych `SQLite`.
1) `prediction/` - do serwowania predykcji.
 Odbiera atrybuty oraz identyfikator użytkownika.
 Odpowiada wartością przydzielonej zniżki.
 Model do predykcji jest wybierany na podstawie skrótu id użytkownika.
2) `conversion/` - do wysyłania informacji do serwera o zakupie dokonanym przez danego użytkownika.
Odbiera identyfikator użytkownika oraz zysk uzyskany z danego zakupu.
3) `resultsAB/` - Odpowiada listą zapisanych konwersji.
4) `resetAB/` - Pozwala zresetować dotychczasowe wyniki testu AB.

Aby uruchomić serwer należy:

1) Zainstalować zależności: `pip install -r requirements.txt`
2) Znajdując się w folderze `5-server` wywołać komendę `python manage.py runserver`


## TestAB
Prawdziwego testu AB nie da się przeprowadzić bez interakcji z realnymi użytkownikami.
W celu zademonstrowania przebiegu takiego testu przeprowadziliśmy go sztucznie.
Nasz model porównaliśmy z modelem, który prawdopodobieństwo zakupy losuje z rozkładu normalnego.
Rezultaty są dostępne w [tym notatniku](6-abtest-client/abtest-client.ipynb).

