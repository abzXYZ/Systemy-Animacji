import bpy
import math
import os

def stworzMaterial(r = 0, g = 0, b = 0, metal = 0, rough = 0, emisja = 0, nazwa = "Materiał"):
    mat = bpy.data.materials.new(name=nazwa)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (r, g, b, 1)
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

def stworzLiscie(x = 0, y = 0, wysokosc = 2, liczbaLisci = 3, promienLisci = 0.3, material = stworzMaterial()):
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

def stworzKorzenie(x = 0, y = 0, wysokosc = 2,liczbaKorzeni = 4, material = stworzMaterial()):
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

def stworzrosline(x = 0, y = 0, wysokosc = 2 ,liczbaLisci = 3 ,promienLisci = 0.3 ,liczbaKorzeni = 4 ):
    # Materiały
    matLodyga = stworzMaterial(r = 0.75,g = 0.5,b = 0.5, metal = 1, rough = 0.05, nazwa = "Materiał Łodyga")
    matLisc = stworzMaterial(r = 0,g = 0.8,b = 0.65, rough = 0.01, emisja = 0.6, nazwa = "Materiał Liść")

    # Łodyga
    stworzLodyge(x,y,wysokosc,matLodyga)

    # Los liścios (liście)
    stworzLiscie(x,y,wysokosc,liczbaLisci,promienLisci,matLisc)

    # Korzenie
    stworzKorzenie(x,y,wysokosc,liczbaKorzeni,matLodyga)



# === 1. Czyszczenie sceny (opcjonalne) ===
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

# === 2. Roślina ===
stworzrosline(x = -5, y = 0, wysokosc = 2, liczbaLisci = 3, promienLisci = 0.85, liczbaKorzeni = 3)
stworzrosline(x = 0, y = 0, wysokosc = 3, liczbaLisci = 4, promienLisci = 1, liczbaKorzeni = 3)
stworzrosline(x = 5, y = 0, wysokosc = 5, liczbaLisci = 10, promienLisci = 1, liczbaKorzeni = 5)

# === 3. Światło ===
bpy.ops.object.light_add(type='SUN', location=(3, 3, 8))
sun = bpy.context.active_object
sun.rotation_euler = (0.9, 0.2, 0.5)
sun.data.energy = 3

# === 4. Kamera ===
bpy.ops.object.camera_add(location=(15, -15, 12.5))
camera = bpy.context.active_object
camera.rotation_euler = (1.1, 0, 0.8)
bpy.context.scene.camera = camera

# === 5. Render do PNG ===
scene = bpy.context.scene
# Ścieżka: obok skryptu (katalog pliku .py) lub katalog bieżący
# Przy python skrypt.py z terminala __file__ jest dostępny
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd()
output_path = os.path.join(script_dir, "render_output.png")

scene.render.filepath = output_path
scene.render.image_settings.file_format = 'PNG'
scene.render.resolution_x = 1000
scene.render.resolution_y = 800

bpy.ops.render.render(write_still=True)

print(f"Render zapisany: {scene.render.filepath}")
