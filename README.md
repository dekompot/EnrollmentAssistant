Jak ja to widzę:
- ``assistant/controllers`` - każdy przypadek użycia ma swój kontroler, który jest w sumie tylko z nazwy kontrolerem, ale tu będą metody odpowiadające na żądania
- ``assistant/controllers/shared`` - tu jakieś w domyśle wspólne metody 'kontrolera', np. obsługa formularza filtrującego grupy
- ``assistant/enrollment`` lub inne foldery - funkcjonalności na poziomie logiki biznesowej
- ``assistant/tests`` - "lustrzane" odbicie struktury folderów, każdy plik na jedną klasę najlepiej, np. ``enrollment.py``, a każda klasa testuje jedną metodę.
- ``assistant/templates/assistant`` - tu będą szablony html, można to potem też porozdzielać na oddzielne foldery
- ``assistant/models`` - model domenowy + funkcje użyteczne dla danego modelu
- ``assistant/urls`` - tutaj wpisujemy metody routingu dla aplikacji assistant (*projekt* może się składać z wielu *aplikacji*,
    więc jest też routing wyższego poziomu, który odsyła to co się zaczyna na *assistant* dalej do metod routingu tejże aplikacji)
- ``parsing`` - jakieś metody jeszcze z poprzedniego UniPlannera
- ``utils`` - utlisy, poza assistant aczkolwiek ten i powyższe pakiety może jeszcze zmienią swoją lokalizację, bez znaczenia teraz w sumie

TESTOWE URL:
http://127.0.0.1:8000/assistant/enrollment/search/266640/
http://127.0.0.1:8000/assistant/timetable/266640/
