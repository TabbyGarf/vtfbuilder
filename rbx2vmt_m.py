import os
import re
import json
import sys
import subprocess
from PIL import Image, ImageChops

INPUT_COLORS = os.path.abspath("brickcolors.json")
SURFACE_DIR = os.path.abspath("surface")
MATERIAL_DIR = os.path.abspath("material")
OUTPUT = os.path.abspath("output")
TEMP = os.path.abspath("temp")
BIN_DIR = os.path.abspath("bin")

os.makedirs(OUTPUT, exist_ok=True)
os.makedirs(TEMP, exist_ok=True)

env = os.environ.copy()
env["PATH"] = BIN_DIR + os.pathsep + env["PATH"]

alpha_levels = [1.0,0.5]

def progbar(count, total, cur_file=""):

    sys.stdout.write('\r')
    os.system("cls")

    bar_len = 10
    full_blocks = ["|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\","|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\","|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\","|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\","|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\","|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\","|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\","|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\","|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\","|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\","|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\","|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\","|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\","|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\","|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\","|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\","|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\","|", "/", "—", "\\", "|", "/", "—","\\", "|", "/", "—","\\", "|", "/", "—","\\",]
    num_steps = len(full_blocks) - 1  

    total_progress = count / float(total) * bar_len
    full_chars = int(total_progress)  
    partial_progress = total_progress - full_chars
    partial_char_index = int(round(partial_progress * num_steps))

    bar = "#" * full_chars
    if full_chars < bar_len:
        bar += full_blocks[partial_char_index]
        bar += " " * (bar_len - full_chars - 1)

    percent = round(100.0 * count / float(total), 1)

    sys.stdout.write(f"|{bar}| {percent}% ({count}/{total}) {cur_file} ")
    sys.stdout.flush()

def create_vmt(vmt_path, texture_path, alpha_value):
    with open(vmt_path, 'w') as vmt_file:
        vmt_file.write(f'"LightmappedGeneric"\n{{\n')
        vmt_file.write(f'    "$basetexture" "{texture_path}"\n')
        if alpha_value < 1.0:
            vmt_file.write(f'    "$translucent" 1\n')
        vmt_file.write(f'}}\n')

colors = json.load(open(INPUT_COLORS))
material_files = [f for f in os.listdir(MATERIAL_DIR)
                  if os.path.splitext(f)[1].lower() in (".png", ".jpg", ".jpeg")]
material_basenames = {os.path.splitext(f)[0].lower(): f for f in material_files}

print("Available materials:", material_basenames.keys())
sel_mats = input("Enter materials to process (comma-separated) or 'all': ").strip()

if sel_mats.lower() != 'all':
    chosen_mats = [material_basenames[m.strip().lower()] for m in sel_mats.split(',')
        if m.strip().lower() in material_basenames]
else:
    chosen_mats = material_files
    
sys.stdout.write('\r')    
os.system("cls")

surface_files = [f for f in os.listdir(SURFACE_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
surface_basenames = {os.path.splitext(f)[0].lower(): f for f in surface_files}

print("Available surfaces:", surface_basenames.keys())
sel_surfs = input("Enter surfaces to process (comma-separated) or 'all': ").strip()

if sel_surfs.lower() != 'all':
    chosen_surfs = [surface_basenames[m.strip().lower()] for m in sel_surfs.split(',')
        if m.strip().lower() in surface_basenames]
else:
    chosen_surfs = surface_files

import concurrent.futures
import threading

lock = threading.Lock()
count = 0

def process_material(mat_file):
    local_count = 0
    mat_name = re.sub(r'\W+', '', os.path.splitext(mat_file)[0].lower())
    mat_img = Image.open(os.path.join(MATERIAL_DIR, mat_file)).convert("RGBA")
    mat_img = mat_img.resize((512, 512))

    for color in colors:
        cname = re.sub(r'\W+', '', color["name"].lower())
        cr, cg, cb, ca = color["rgba"]
        tint = Image.new("RGBA", (512, 512), (cr, cg, cb, ca))
        base_colored = ImageChops.multiply(tint, mat_img)

        for alpha in alpha_levels:
            for surf_file in chosen_surfs:
                sname = re.sub(r'\W+', '', os.path.splitext(surf_file)[0].lower())
                surf_img = Image.open(os.path.join(SURFACE_DIR, surf_file)).convert("RGBA").resize((512, 512))
                combined = Image.alpha_composite(base_colored, surf_img)

                out_dir = os.path.join(OUTPUT, "rbx", mat_name, sname)
                os.makedirs(out_dir, exist_ok=True)

                out_base = f"{mat_name}_{cname}_{sname}"
                png = os.path.join(TEMP, out_base + ".png")
                combined.save(png)

                cmd = [
                    "vtfcmd",
                    "-file", png,
                    "-output", out_dir,
                    "-rwidth", "512",
                    "-rheight", "512",
                    "-silent"
                ]
                subprocess.run(cmd, cwd=BIN_DIR, env=env, check=True, shell=True)

                vmt = os.path.join(out_dir, out_base + ".vmt")
                create_vmt(vmt, f"rbx/{mat_name}/{sname}/{out_base}", alpha)

                local_count += 1

                with lock:
                    global count
                    count += 1
                    progbar(count, total, f"rbx/{mat_name}/{sname}/" + out_base + "                              ")
    return local_count


colors = json.load(open(INPUT_COLORS))

total = len(chosen_mats) * len(colors) * len(alpha_levels) * len(chosen_surfs)

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(process_material, chosen_mats)

print("\nDone.")
