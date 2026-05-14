import bpy
import math
import os

SCIEZKA_LAB07 = r"C:/Users/Admin/Documents/SAK/lab_07/roslin.blend"
NAZWA_KOLEKCJI = "Roslina_Hero"

KLATKA_START = 1
KLATKA_KONIEC = 125
FPS = 25

def importuj_rosline(sciezka_blend, nazwa_kolekcji):
    sciezka_kolekcji = os.path.join(sciezka_blend, "Collection", nazwa_kolekcji)
    bpy.ops.wm.append(
        filepath=sciezka_kolekcji,
        directory=os.path.join(sciezka_blend, "Collection"),
        filename=nazwa_kolekcji,
    )

def wyczysc_animacje(obj):
    """Całkowicie usuwa dane animacji z obiektu."""
    if obj.animation_data:
        # To usuwa cały kontener animation_data, w tym akcje, 
        # ścieżki NLA i sterowniki (drivers)
        obj.animation_data_clear()

def animuj_lisc(obj, faza, czestosc=0.05, amplituda=0.2, klatka_start=1, klatka_koniec=125):
    """
    Korzysta z delta rotation, ktora dodaje rotacje delta do rotacji bazowej w celu zapewnienia IDEMPOTENCJI
    Krzywa sinusoidalna z indywidualną fazą.
    
    Args:
        obj: obiekt Blendera (mesh liścia)
        faza: przesunięcie fazowe sinusa (różne dla różnych liści)
        czestosc: jak szybko zmienia się kąt na klatkę (rad/klatka)
        amplituda: maksymalne wychylenie w radianach (~17° = 0.3 rad)
    """
    wyczysc_animacje(obj)
    
    # Resetujemy deltę (rotacja dodawana do bazowej rotacji) na 0 przed nową animacją
    obj.delta_rotation_euler[1] = 0.0
    
    for klatka in range(klatka_start, klatka_koniec + 1):
        # Animujemy TYLKO deltę
        kat = amplituda * math.sin(klatka * czestosc + faza)
        obj.delta_rotation_euler[1] = kat
        obj.keyframe_insert(data_path="delta_rotation_euler", frame=klatka, index=1)

def animuj_wszystkie_liscie(prefix_nazwy="Roslina_Lisc"):
    """
    Znajduje wszystkie obiekty zaczynające się od `prefix_nazwy`
    i animuje każdy z indywidualną fazą.
    """
    liscie = [obj for obj in bpy.data.objects if obj.name.startswith(prefix_nazwy)]
    for i, lisc in enumerate(liscie):
        faza_lisc = i * (2 * math.pi / max(len(liscie), 1))  # rozłożenie po pełnym okresie
        animuj_lisc(lisc, faza=faza_lisc)
    print(f"Zaanimowano {len(liscie)} liści.")

def animuj_pak(nazwa_obj="Roslina_Pak", klatka_start=30, klatka_koniec=90,
               skala_min=0.1, skala_max=0.25):
    obj = bpy.data.objects.get(nazwa_obj)
    if obj is None:
        print(f"Obiekt '{nazwa_obj}' nie istnieje. Pomijam animację pąka.")
        print(f"Dostępne obiekty: {[o.name for o in bpy.data.objects]}")
        return

    wyczysc_animacje(obj)

    obj.scale = (skala_min, skala_min, skala_min)
    obj.keyframe_insert(data_path="scale", frame=KLATKA_START)
    obj.keyframe_insert(data_path="scale", frame=klatka_start)

    obj.scale = (skala_max, skala_max, skala_max)
    obj.keyframe_insert(data_path="scale", frame=klatka_koniec)
    obj.keyframe_insert(data_path="scale", frame=KLATKA_KONIEC)

def ustaw_scene():
    bpy.context.scene.frame_start = KLATKA_START
    bpy.context.scene.frame_end = KLATKA_KONIEC
    bpy.context.scene.render.fps = FPS

if __name__ == "__main__" or True:
    ustaw_scene()
    if "Roslina_Hero" not in bpy.data.collections:
        importuj_rosline(SCIEZKA_LAB07, NAZWA_KOLEKCJI)
    animuj_wszystkie_liscie()
    animuj_pak()
    print("Skrypt zakończony.")
