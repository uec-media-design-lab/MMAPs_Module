# MMAPs Generation Module for Blender
- This is a module to reproduce Micro-Mirror Array Plates (MMAPs), which are mid-air imaging optical elements, in Blender.
- [日本語解説はこちら](https://github.com/uec-media-design-lab/MMAPs_Module/blob/master/READMEJP.md)

- See [here](https://doi.org/10.1016/j.cag.2021.02.007)  for details.
  -  Shunji Kiuchi, Naoya Koizumi. Simulating the appearance of mid-air imaging with micro-mirror array plates. *Computers & Graphics*, Vol. 96, pp. 14--23, 2021.

- mmaps/ ... The directory of MMAPs generation Module (for developer)
  - \_\_init\_\_.py       ... Initialization file
  - mmaps.py          ... Module to generate/delete MMAPs
  - myutil.py         ... Utility function module
  - mmaps_clearer.py  ... Operator class to delete MMAPs
  - mmaps_launcher.py ... Operator class to generate MMAPs
  - mmaps_manager.py  ... Panel class to manage parameters
- vcf/ ... The directory of VCF generation module (`Under development. This is very different from the optical properties of an actual VCF.`)
  - \_\_init\_\_.py       ... Initialization file
  - vcf.py            ... Module to generate/delete VCF
  - myutil.py         ... Utility function module
  - vcf_clearer.py    ... Operator class to delete VCF
  - vcf_launcher.py   ... Operator class to generate VCF
  - vcf_manager.py    ... Panel class to manage parameters
- mmaps.zip           ... For installing MMAPs generation module
- vcf.zip             ... For installing VCF generation module

# Verified version
- Blender 2.8.1


# Setup

- In Blender, go to `Edit` -> `Preferences` and select `Add-ons`.
- Select `Testing`, then go to `Install`.
  - ![](img/addon.png)
- Select `mmaps.zip` or `vcf.zip` in the Blender File View.

# Parameters settings
| Parameter        | Default |
| ---              | :-:     |
| MMAPs size       | 48.8    |
| Slit spacing     | 0.05    |
| Height scale     | 2.5     |
| Mirror detailing | 10      |
| Reflectance      | 0.87    |
| IOR              | 1.52    |

# For developer
- If you'd like to implement additional features, please modify the python files under `mmaps/` and/or `vcf/`.
- Before installing them in Blender, compress each directory into a zip file after the modification.

## Functions

> **showParam(_mirror_name = 'Mirror', glass_name = 'Glass', parent_name = 'MMAPs'_)**

Show MMAPs parameters: the length of a side, the slit spacing, the height scale, and the number of mirror partition.

**Paramters**
- `mirror_name` (string) - Mirror name _[optional]_ 
- `glass_name` (string) - Glass name _[optional]_ 
- `parent_name` (string) - Parent (empty) object name to control the MMAPs posture _[optional]_ 

---
> **getParam(_mirror_name = 'Mirror', glass_name = 'Glass', parent_name = 'MMAPs'_)**

Return MMAPs parameters.

**Paramters**
- `mirror_name` (string) - Mirror name _[optional]_ 
- `glass_name` (string) - Glass name _[optional]_ 
- `parent_name` (string) - Parent (empty) object name to control the MMAPs posture _[optional]_ 

**Returns**
- `size` (float) - Length of a side of MMAPs
- `spacing` (float) - Slit spacing
- `height_scale` (float) - Ratio of slit height to slit spacing
- `detailing` (float) - Number of the mirror partition
- `isGlass` (bool) - Presence or absence of the glass

> **clearMMAPs(_mirror_name = 'Mirror', glass_name = 'Glass', parent_name = 'MMAPs'_)**

Delete MMAPs composed of a mirror, a glass, and a parent (empty) object.

**Paramters**
- `mirror_name` (string) - Mirror name _[optional]_ 
- `glass_name` (string) - Glass name _[optional]_ 
- `parent_name` (string) - Parent (empty) object name to control the MMAPs posture _[optional]_ 

---

> **createMMAPs(_size, spacing, height_scale = 2.5, overwrite=True_)**

Create MMAPs.

**Parameters**
- `size` (float) - Length of a side of MMAPs
- `spacing` (float) - Slit spacing
- `height_scale` (float) - Ratio of slit height to slit spacing
- `overwrite` (bool) - Whether to overwrite MMAPs if it exists. If this is `True`, create new MMAPs after deleting the existing one. _[optional]_ 
- `isGlass` (bool) - Presence or absence of the glass _[optional]_ 
- `glass_center` - Whether the glass is in the middle _[optional]_ 
- `ior` - Refractive index of the glass _[optional]_ 

---

> **createDetailedMMAPs(_size, spacing, detailing = 10, height_scale = 2.5, overwrite=True, isGlass=True, glass_center=False, ior=1.52_)**

Create MMAPs that each slit mirror is divided.

**Parameters**
- `size` (float) - Length of a side of MMAPs
- `spacing` (float) - Slit mirror spacing
- `detailing` (int) - Number of parititions for each mirror. By default, each mirror is divided into 10 parts.
- `height_scale` (float) - Ratio of slit height to slit spacing
- `overwrite` (bool) - Whether to overwrite MMAPs if it exists. If this is `True`, create new MMAPs after deleting the existing one. _[optional]_ 
- `isGlass` (bool) - Presence or absence of the glass _[optional]_ 
- `glass_center` - Whether the glass is in the middle _[optional]_ 
- `ior` - Refractive index of the glass _[optional]_ 

---

> **attachMaterial(_obj, mat_name_)**

Attach a material to an object. If the object with the name specified by `mat_name` does not exist, create a new one.

**Parameters**
- `obj` (BlendDataObjects) - Object that the material will attach
- `mat_name` (string) - Material name

---

> **attachMirrorMaterial(_obj, mat_name_)**

Attach a mirror material to an object. If the object with the name specified by `mat_name` does not exist, create a new one.

**Parameters**
- `obj` (BlendDataObjects) - Object that the material will attach
- `mat_name` (string) - Material name

---

> **attachGlassMaterial(_obj, mat_name, ior=1.52_)**

Attach a glass material to an object. If the object with the name specified by `mat_name` does not exist, create a new one.

**Parameters**
- `obj` (BlendDataObjects) - Object that the material will attach
- `mat_name` (string) - Material name
- `ior` - Refractive index of the glass _[optional]_ 

---

> **addMirror(_parent, verts, faces, obj_name = 'Mirror', id = None_)**

Generate a mirror inside MMAPs. The parent object (`parent`) is required because it is assumed that the mirror is inside MMAPs.

**Parameters**
- `parent` (BlendDataObjects) - Parent object
- `verts` (array) - Vertexes coordinate data
- `faces` (array) - Vertexes index data
- `obj_name` (string) - Object name
- `id` (int) - Mirror number

---

> **addGlass(_parent, size, height, obj_name = 'Glass'_)**

Generate a glass inside MMAPs. The parent object (`parent`) is required because it is assumed that the mirror is inside MMAPs.

**Parameters**
- `parent` (BlendDataObjects) - Parent object
- `size` (float) - Length of a side of the glass
- `height` (float) - Glass thickness
- `obj_name` (string) - Object name
- `glass_center` - Whether the glass is in the middle _[optional]_ 


