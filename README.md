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
* **Pillow**
  ```bash
  pip install pillow
  ```
* External tool **`vtfcmd`** (included in `bin/`)


## Usage

1. Run `vtfbuilder.py` or use `python ./vtfbuilder.py` in a terminal
1. **Select material(s)**:
   * Use `smoothplastic` if you just want the color 
   * Script lists all images in `material/`.
   * Type comma-separated names (without extension) or `all`.
   * Each selected material will be processed via `ThreadPoolExecutor`.
   * /!\ This means choosing to process one material at a time will be slower than selecting multiple at once

3. **Select surface(s)** similarly.
   * Use `smooth` if you want no overlay and just the tinted material.
4. Let the script do its work
5. Find results in `output/rbx/...`.
6. Move the `rbx/`directory to your Source game's `materials` folder.

---

## Customization

* **Add/edit colors** in `brickcolors.json`. Or extend loader to fetch from Python.
* **Add materials/surfaces** by dropping `.png/.jpg` files into respective folders.
* Define additional alpha tiers via `alpha_levels` list.
* Tweak image resolution by changing `resize((512, 512))`.
* Optionally adjust threading via `ThreadPoolExecutor(...)`.






