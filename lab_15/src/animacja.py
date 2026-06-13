# Kod na bazie lab 12

import bpy
import random

NAZWA_MATERIALU = "Apteka"
MIN_STRENGTH = 1 # Minimalna intensywność neonu
MAX_STRENGTH = 3 # Maksymalna intensywność neonu
MIN_ODSTEP = 4 # Minimalny czas między mrugnięciami
MAX_ODSTEP = 16 # Maksymalny czas między mrugnięciami
KLATKA_START = bpy.context.scene.frame_start # Klatka początkowa animacji
KLATKA_END = bpy.context.scene.frame_end # Klatka końcowa animacji

def wyczysc_animacje_materialu(mat):
    # Czyszczenie F-Curves z węzłów
    if mat.node_tree.animation_data and mat.node_tree.animation_data.action:
        mat.node_tree.animation_data.action = None

def znajdz_node(mat, nazwa, typ_zapasowy=None):
    # Zwraca węzeł po nazwie, fallback po typie. Czytelny błąd, jeśli nie ma.
    node = mat.node_tree.nodes.get(nazwa)
    if node is None and typ_zapasowy:
        for n in mat.node_tree.nodes:
            if n.type == typ_zapasowy:
                print(f"Nie znaleziono '{nazwa}', używam '{n.name}' (typ {typ_zapasowy}).")
                return n
    if node is None:
        dostepne = [n.name for n in mat.node_tree.nodes]
        raise KeyError(f"Węzeł '{nazwa}' nie istnieje w '{mat.name}'. Dostępne: {dostepne}")
    return node

def animuj_neon(mat):
    emission = znajdz_node(mat, "Emission", typ_zapasowy='EMISSION')
    sciezka = f'nodes["{emission.name}"].inputs["Strength"].default_value'

    klatka = KLATKA_START
    
    while klatka <= KLATKA_END:
        # Losowa intensywność neonu
        sila = random.uniform(MIN_STRENGTH, MAX_STRENGTH)
        emission.inputs["Strength"].default_value = sila
        
        # Dodawanie klatki
        mat.node_tree.keyframe_insert(data_path=sciezka, frame=klatka)
        
        # Losowy odstęp między klatkami
        odstep = random.randint(MIN_ODSTEP, MAX_ODSTEP)
        klatka += odstep

mat = bpy.data.materials.get(NAZWA_MATERIALU)
if mat is None:
    print(f"Brak materialu '{NAZWA_MATERIALU}'. Dostepne: {[m.name for m in bpy.data.materials]}")
else:
    wyczysc_animacje_materialu(mat)
    animuj_neon(mat)