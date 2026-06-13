# Lab 15 - Projekt Końcowy

## Opis sceny
Animacja przedstawia perspektywę osoby wracającej do domu podczas deszczowej nocy we wschodnioeuropejskim mieście. Chciałem osiągnąć znajomy i spokojny klimat.

## Uruchomienie
Pobrać wszystkie pliki, a następnie otworzyć w Blenderze plik `assets/scena.blend`.

## Opis skryptu Python
Skrypt Python `animacja.py` wykorzystany został do animacji migotania neonu (znaku apteki). Po uruchomieniu usuwa on animacje przypisane do materiału neonu, a następnie dodaje klatki kluczowe z mrugnięciami o losowej intensywności w losowych odstępach czasu.\
Parametry do zmiany:
- **NAZWA_MATERIALU** (nazwa materiału neonu)
- **MIN_STRENGTH** (Minimalna intensywność mrugnięć neonu)
- **MAX_STRENGTH** (Maksymalna intensywność mrugnięć neonu)
- **MIN_ODSTEP** (Minimalny czas między mrugnięciami podany w klatkach)
- **MAX_ODSTEP** (Maksymalny czas między mrugnięciami podany w klatkach)
- **KLATKA_START** (Klatka początkowa animacji neonu)
- **KLATKA_END** (Klatka końcowa animacji neonu)

## Zasoby
[1995 Lada/VAZ 2107](https://sketchfab.com/3d-models/1995-ladavaz-2107-c94daeb210b244729d634975c9ed0c5b)
- Autor: [Renafox](https://sketchfab.com/kryik1023)
- Licencja: CC Attribution-NonCommercial

[Russian panel house (asset)](https://sketchfab.com/3d-models/russian-panel-house-asset-d537595db4bf4a60b955b31cde198432)
- Autor: [Yury Misiyuk](https://sketchfab.com/Tim0)
- Licencja: CC Attribution

[Night Bridge](https://polyhaven.com/a/night_bridge)
- Autor: [Sergej Majboroda](https://hdrmarket.com/)
- Licencja: CC0

[Withered Grass](https://polyhaven.com/a/withered_grass)
- Autor: [Charlotte Baglioni](https://www.artstation.com/wyrine)
- Licencja: CC0

[Brick Moss 001](https://polyhaven.com/a/brick_moss_001)
- Autorzy: [Dimitrios Savva](https://polyhaven.com/all?a=Dimitrios%20Savva), [Rico Cilliers](https://www.artstation.com/rico_b3d)
- Licencja: CC0

[Concrete Laters 02](https://polyhaven.com/a/concrete_layers_02)
- Autor: [Rob Tuytel](https://www.artstation.com/tuytel)
- Licencja: CC0

[Asphalt 02](https://polyhaven.com/a/asphalt_02)
- Autor: [Rob Tuytel](https://www.artstation.com/tuytel)
- Licencja: CC0

[Street Lamp](https://sketchfab.com/3d-models/street-lamp-152055979ddd48669529f5d4f5f3543c)
- Autor: [Yni Viar](https://sketchfab.com/yni-viar)
- Licencja: CC Attribution

[Post soviet lowpoly buildings](https://sketchfab.com/3d-models/post-soviet-lowpoly-buildings-130d02982dd84cf99b938f5a668402d0)
- Autor: [Mince](https://sketchfab.com/Mince)
- Licencja: CC Attribution

[Pharmacy](https://sketchfab.com/3d-models/pharmacy-b4b5c21b768447529d9d2d7385a68923)
- Autor: [amirsoliman](https://sketchfab.com/amirsoliman)
- Licencja: CC Attribution

## Znane bugi i ograniczenia
- Odbicia przednich świateł nadjeżdżającego samochodu na renderze trochę się "rozmywają" na mokrym asfalcie.
