# Lab 05 – Generator Lasu z Typami Roślin i Biomami

## Co zostało zrealizowane
Napisany został skrypt w języku Python (na podstawie skryptu z lab 04), który przy pomocy Blendera proceduralnie tworzy las złożony z drzew, krzewów i paproci, w którym występują biomy.

## Uruchomienie
Pobrać pliki i uruchomić skrypt las05.py komendą `python las05.py`

## Refleksja
Pierwotnie wszystkie rośliny znajdowały się zarazem w głównej kolekcji sceny, jak i podkolekcjach w kolekcji las (co skutkowało duplikatami na liście). Nie jestem pewien czy tak należało zrobić, ale podczas generowania roślin obiekty roślin odłączane są od głównej kolekcji, aby pozbyć się duplikatów i zachować większy porządek na liście obiektów.
