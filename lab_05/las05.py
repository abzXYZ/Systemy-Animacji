import bpy
import math
import random
import os

DEBUG = False

def stworzMaterial(r = 0, g = 0, b = 0, a = 1, metal = 0, rough = 0, emisja = 0, nazwa = "Materiał"):
    mat = bpy.data.materials.new(name=nazwa)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (r, g, b, a)
    bsdf.inputs["Metallic"].default_value = metal
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Emission Color"].default_value = (r, g, b, 1)
    bsdf.inputs["Emission Strength"].default_value = emisja
    return mat

def stworzLodyge(x = 0, y = 0, wysokosc = 2, material = stworzMaterial()):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3, location=(x, y, wysokosc/2))
    lodyga = bpy.context.active_object
    lodyga.data.materials.append(material)
    lodyga.name = "Łodyga"
    lodyga.scale.z = wysokosc
    return lodyga

def stworzLiscie(x = 0, y = 0, wysokosc = 2, liczbaLisci = 3, promienLisci = 0.3, material = stworzMaterial()):
    liscie = []
    for i in range(liczbaLisci):
        angle = (2*math.pi / liczbaLisci) * i
        lx = x + math.cos(angle) * promienLisci
        ly = y + math.sin(angle) * promienLisci
        # Wysokość liścia - wzrasta co ¼ łodygi / liczbaLisci
        lz = (wysokosc*0.75) + (i * ((wysokosc*0.5)/liczbaLisci))
        bpy.ops.mesh.primitive_cube_add(size=promienLisci*2, location=(lx,ly,lz))
        lisc = bpy.context.active_object
        lisc.name = "Liść " + str(i)
        lisc.scale.y = promienLisci/2
        lisc.scale.z = promienLisci/10
        lisc.rotation_euler = (0,0.55,angle)
        lisc.data.materials.append(material)
        liscie.append(lisc)
    return liscie

def stworzKorzenie(x = 0, y = 0, wysokosc = 2,liczbaKorzeni = 4, material = stworzMaterial()):
    korzenie = []
    for i in range(liczbaKorzeni):
        angle = (2*math.pi / liczbaKorzeni) * i
        rx = math.cos(angle)
        ry = math.sin(angle)
        rz = 0-wysokosc*0.6
        bpy.ops.mesh.primitive_cube_add(size=0.25, location=(x+rx*0.6,y+ry*0.6,rz))
        korzen = bpy.context.active_object
        korzen.name = "Korzeń " + str(i)
        korzen.scale.y = 8
        korzen.rotation_euler = (1.5,-0.3,angle)
        korzen.data.materials.append(material)
        korzenie.append(korzen)
    return korzenie

def stworzrosline(x = 0, y = 0, wysokosc = 2 ,liczbaLisci = 3 ,promienLisci = 0.3 ,liczbaKorzeni = 4, matLodyga = stworzMaterial(), matLisc = stworzMaterial()):
    # Łodyga
    lodyga = stworzLodyge(x,y,wysokosc,matLodyga)

    # Los liścios (liście)
    liscie = stworzLiscie(x,y,wysokosc,liczbaLisci,promienLisci,matLisc)

    # Korzenie
    korzenie = stworzKorzenie(x,y,wysokosc,liczbaKorzeni,matLodyga)

    return [lodyga] + korzenie + liscie

def stworzroslinetyp(x,z,typ):
    # Pobieranie typu rośliny
    typ_ros = TYPY_ROSLIN[typ]
    # Losowanie wartości
    wys = random.uniform(typ_ros["wysokosc"][0], typ_ros["wysokosc"][1])
    l_lis = random.randint(typ_ros["liczba_lisci"][0],typ_ros["liczba_lisci"][1])
    p_lis = random.uniform(typ_ros["promien_lisci"][0],typ_ros["promien_lisci"][1])
    l_kor = random.randint
    (typ_ros["liczba_korzeni"][0],typ_ros["liczba_korzeni"][1])
    if DEBUG:
        print("Wygenerowana roślina:\nx: " + str(x) + "\nz: " + str(z) + "\ntyp: " + str(typ) + "\nWys.: " + str(wys) + "\nLiści: " + str(l_lis) + "\nPromień liś.: " + str(p_lis) + "\nKorzeni: " + str(l_kor))
    # Tworzenie materiałów
    kolor = typ_ros["kolor_lodygi"]
    matLodyga = stworzMaterial(kolor[0],kolor[1],kolor[2],kolor[3])
    kolor = typ_ros["kolor_lisci"]
    matLisc = stworzMaterial(kolor[0],kolor[1],kolor[2],kolor[3])
    # Tworzenie rośliny
    return stworzrosline(x = x, y = z, wysokosc = wys, liczbaLisci = l_lis, promienLisci = p_lis, liczbaKorzeni = l_kor, matLodyga=matLodyga, matLisc=matLisc)

def wybierztypbiomu(x,z,rozmiar_pola):
    if (abs(x) < 0.3 * (rozmiar_pola/2)) and (abs(z) < 0.3 * (rozmiar_pola/2)):
        return "drzewo"
    elif (abs(x) > 0.3 * (rozmiar_pola/2)) and (abs(z) > 0.3 * (rozmiar_pola/2)) and (abs(x) < 0.7 * (rozmiar_pola/2)) and (abs(z) < 0.7 * (rozmiar_pola/2)):
        if random.random() < 0.7:
            return "krzew"
        return "drzewo"
    else:
        if random.random() < 0.7:
            return "paproc"
        return "krzew"

# === Słownik typów roślin ===
TYPY_ROSLIN = {
    "drzewo": {
        "wysokosc": (3.0, 5.0),   # zakres (min, max) dla random.uniform()
        "liczba_lisci": (4, 6),
        "promien_lisci": (0.4, 0.7),
        "liczba_korzeni": (4, 6),
        "kolor_lodygi": (0.15, 0.08, 0.02, 1),  # ciemny brąz
        "kolor_lisci": (0.05, 0.35, 0.1, 1),    # ciemna zieleń
    },
    "krzew": {
        "wysokosc": (0.8, 1.8),
        "liczba_lisci": (5, 8),
        "promien_lisci": (0.5, 0.9),
        "liczba_korzeni": (2, 4),
        "kolor_lodygi": (0.25, 0.15, 0.05, 1),  # jasny brąz
        "kolor_lisci": (0.1, 0.5, 0.05, 1),     # żywa zieleń
    },
    "paproc": {
        "wysokosc": (0.5, 1.2),
        "liczba_lisci": (6, 10),
        "promien_lisci": (0.6, 1.0),
        "liczba_korzeni": (2, 3),
        "kolor_lodygi": (0.2, 0.3, 0.1, 1),     # oliwkowy
        "kolor_lisci": (0.0, 0.6, 0.15, 1),     # soczysty zielony
    },
}

def generujlas(liczbaroslin = 18, rozmiar_pola = 10, seed = 42):
    random.seed(seed)
    # === 1. Czyszczenie sceny ===
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)

    # === 2. Kolekcje ===
    las = bpy.data.collections.new("Las")
    bpy.context.scene.collection.children.link(las)
    drzewa = bpy.data.collections.new("Drzewa")
    las.children.link(drzewa)
    krzewy = bpy.data.collections.new("Krzewy")
    las.children.link(krzewy)
    paprocie = bpy.data.collections.new("Paprocie")
    las.children.link(paprocie)
    podkolekcje = {"drzewo": drzewa, "krzew": krzewy, "paproc": paprocie}

    # === 3. Podłoże  ===
    bpy.ops.mesh.primitive_plane_add(size=rozmiar_pola*1.25, location=(0, 0, -0.5))
    ziemia = bpy.context.active_object
    ziemia.name = "Podloze_Lasu"

    ziemia.data.materials.append(stworzMaterial(20/255,50/255,20/255,1,0,1,0,"Trawa"))

    # Zwiększenie gęstości siatki dla modyfikatora Displace (subdivide)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=60)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Dodawanie wybojów (wyboji?) nierówności
    displace_mod = ziemia.modifiers.new(name="ForestBump", type='DISPLACE')
    noise_tex = bpy.data.textures.new("ForestNoise", type='CLOUDS')
    noise_tex.noise_scale = 2.0
    displace_mod.texture = noise_tex
    displace_mod.strength = 1.5  # Wysokość pagórków

    # === 4. Generowanie roślin ===
    for i in range(liczbaroslin):
        x = random.uniform(-rozmiar_pola/2, rozmiar_pola/2)
        z = random.uniform(-rozmiar_pola/2, rozmiar_pola/2)
        typ = wybierztypbiomu(x=x, z=z, rozmiar_pola=rozmiar_pola)
        # Adekwatna podkolekcja dla każdej rośliny
        podkol = podkolekcje[typ]
        roslina = stworzroslinetyp(x=x, z=z, typ=typ)
        for obj in roslina:
            if obj.name in bpy.context.scene.collection.objects:
                # Czyszczenie głównej kolekcji sceny (usuwanie duplikatów)
                bpy.context.scene.collection.objects.unlink(obj)
            podkol.objects.link(obj)
    
    # === 5. Światła, kamera... ===
    bpy.ops.object.light_add(type='SUN', location=(3, 3, 8))
    sun = bpy.context.active_object
    sun.rotation_euler = (0.9, 0.2, 0.5)
    sun.data.energy = 3

    # Wykalkulowana pozycja kamery dostosowująca się do rozmiaru lasu
    bpy.ops.object.camera_add(location=(rozmiar_pola * 1.25, -rozmiar_pola * 1.25, rozmiar_pola))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.8)
    bpy.context.scene.camera = camera

    # === 6. ...Akcja🎬 ===
    scene = bpy.context.scene
    # Ścieżka: obok skryptu (katalog pliku .py) lub katalog bieżący
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd()
    output_path = os.path.join(script_dir, "las_05.png")

    scene.render.filepath = output_path
    scene.render.image_settings.file_format = 'PNG'
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 800

    bpy.ops.render.render(write_still=True)
    print(f"Render zapisany: {scene.render.filepath}")

generujlas(liczbaroslin=400,rozmiar_pola=75,seed=42)

# Tak na czarną godzinę
# matLodyga = stworzMaterial(r = 0.75,g = 0.5,b = 0.5, metal = 1, rough = 0.05, nazwa = "Materiał Łodyga")
# matLisc = stworzMaterial(r = 0,g = 0.8,b = 0.65, rough = 0.01, emisja = 0.6, nazwa = "Materiał Liść")
