# 🛠️ `VTFBuilder` — Three Layered Material (TLM) to VMT Batch Converter

Converts Three Layered Materials (TLMs) into Valve VMT/VTF textures for use in Source Engine mapping.
Included: 
* Roblox materials, with variants (mossy, rusty, ...)
* Roblox surfaces (studs, inlets, universal, glue) (RETRO)
* Dev surfaces (Wall, Grid)
* JSON with the 208 RBX BrickColors and 10 additionnal Dev Colors 

## How does it work, what do you mean by TLM (Three Layered Material)?
It's because it has 3 "layers" to make one texture, a color tint, a material and an overlay/surface.

Here is exactly how the code builds the texture:
* Load material image
* Generate tint color from JSON
* Tint material via pixel-wise multiply
* Overlay surface texture on the tinted material

<img width="700" height="250" alt="workflow" src="https://github.com/user-attachments/assets/8eeefcdc-bd57-4986-8252-4dc486fc3003" />

## Prerequisites

* **Python 3**
* **Pillow** (`pip install pillow`)
* External tool **`vtfcmd`** (included in `bin/`)


## Usage

1. Download entire repo and have it in a folder
2. Run `vtfbuilder.py` or use `python ./vtfbuilder.py` in a terminal,   
   * add `--output-path "path/to/materials"` to extract directly to your materials folder
   * add `--keep-png (true/yes/1)` to keep the temporary pngs
   * Example `vtfbuilder.py --keep-png 1 --output-path "D:\Steam\steamapps\common\GarrysMod\garrysmod\materials"`
4. **Select material(s)**:
   * Use `smoothplastic` if you just want the color, `neon` will make the texture "glow" ($selfillum 1, no light emission.) 
   * Script lists all images in `material/`.
   * Type comma-separated names (without extension) or `all`.
   * Each selected material will be processed via `ThreadPoolExecutor`.
   * /!\ This means choosing to process one material at a time will be slower than selecting multiple at once

5. **Select surface(s)** similarly.
   * Use `smooth` if you want no overlay and just the tinted material.
6. Let the script do its work
7. Find results in `output/rbx/...`.
8. Move the `rbx/`directory to your Source game's `materials` folder.

## Size Estimation

**Full: (All possible textures)**

![formula](https://quicklatex.com/cache3/a9/ql_27b6b017f91c4216432ea58a89b28da9_l3.png)










