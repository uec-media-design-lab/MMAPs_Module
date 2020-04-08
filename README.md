# BlenderでMMAPsを作ったりするためのモジュール

# Setup
## Windows
1. C:/Program Files/Blender Foundation/Blender [version]/[version]/scripts/startup/
以下にmmaps.pyを配置する
2. Blenderを起動
3. pythonで`import mmaps`を実行する

## Mac
1. `/Applications/Blender.app/Contents/Resources/2.80/scripts/startup/` 以下にmmaps.pyを配置する
```
mv MMAPs_Module/mmaps.py /Applications/Blender.app/Contents/Resources/2.80/scripts/startup/
```
2. Blenderを起動
3. pythonで`import mmaps`を実行する

# Example

```python:example.py
import mmaps

mmaps.createMMAPs(size=48.8, spacing=0.05, height_scale = 3.0)
```

# Functions

> **clearMMAPs(_mirror_name = 'Mirror', glass_name = 'Glass', parent_name = 'MMAPs'_)**

MMAPs(ミラー、ガラス、空オブジェクトで構成される)を削除する
    
**Paramters**
- `mirror_name` (string) - ミラーの名前
- `glass_name` (string) - ガラスの名前
- `parent_name` (string) - MMAPsの姿勢を制御するための親(空)オブジェクトの名前

---

> **createMMAPs(_size, spacing, height_scale = 3, overwrite=True_)**

MMAPsを生成する

**Parameters**
- `size` (float) - MMAPsの一辺の大きさ
- `spacing` (float) - スリットミラー間の間隔
- `height_scale` (float) - スリット間隔を基準としてスリットの高さを決めるための倍率
- `overwrite` (bool) - MMAPsが存在した場合に上書きするかどうか。`True`の場合、既存のMMAPsを削除してから新規生成する

---

> **createDetailedMMAPs(_size, spacing, detailing = 10, height_scale = 3.0, overwrite=True_)**

各スリットミラーを分割したMMAPsを生成する

**Parameters**
- `size` (float) - MMAPsの一辺の大きさ
- `spacing` (float) - スリットミラー間の間隔
- `detailing` (int) - 各ミラーの分割数。デフォルトでは各ミラーを10分割する。
- `height_scale` (float) - スリット間隔を基準としてスリットの高さを決めるための倍率
- `overwrite` (bool) - MMAPsが存在した場合に上書きするかどうか。`True`の場合、既存のMMAPsを削除してから新規生成する

---

> **attachMaterial(_obj, mat_name_)**

オブジェクトにマテリアルを設定する。`mat_name`で指定される名前のオブジェクトが存在しない場合は新規に作成する。

**Parameters**
- `obj` (BlendDataObjects) - マテリアルを設定する対象のオブジェクト
- `mat_name` (string) - マテリアルの名前

---

> **addMirror(_parent, verts, faces, obj_name = 'Mirror', id = None_)**

ミラーを生成する。MMAPs内部のミラーを想定しているので、親オブジェクト(`parent`)は必須。

**Parameters**
- `parent` (BlendDataObjects) - 親オブジェクト
- `verts` (array) - 頂点情報
- `faces` (array) - 頂点番号情報(インデックス)
- `obj_name` (string) - オブジェクトの名前
- `id` (int) - ミラーの番号

---

> **addGlass(_parent, size, height, obj_name = 'Glass'_)**

ガラスを生成する。MMAPs内部のガラスを想定しているので、親オブジェクト(`parent`)は必須。

**Parameters**
- `parent` (BlendDataObjects) - 親オブジェクト
- `size` (float) - ガラスの一辺の大きさ
- `height` (float) - ガラスの高さ
- `obj_name` (string) - オブジェクトの名前


