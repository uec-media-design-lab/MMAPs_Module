# BlenderでMMAPsを作ったりするためのモジュール

# Setup
versionはそれぞれのBlenderのバージョンに合わせてください。
これは**Blender2.80**を想定して書いています。

## Windows
1. C:/Program Files/Blender Foundation/Blender 2.80/2.80/scripts/startup/
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

## 最新版
```python:example.py
import mmaps

# 鏡の反射率は0.87に設定されています
mmaps.createDetailedMMAPs(size=48.8, spacing=0.05, height_scale=2.5, detailing=10, ior=1.52)
```

# Memo
- `mmaps.py` にガベージコレクションについての記述を追加しました。
  - 現状ではメモリ管理の観点からうまく動いているかはわかりません。
  - 星さんによると、変わらずルーバーを作るときに落ちるそう...

# Functions

> **showParam(_mirror_name = 'Mirror', glass_name = 'Glass', parent_name = 'MMAPs'_)**

MMAPsのパラメータ(一辺の長さ、スリット間隔、高さ比率、分割数)を表示

**Paramters**
- `mirror_name` (string) - ミラーの名前 _[optional]_ 
- `glass_name` (string) - ガラスの名前 _[optional]_ 
- `parent_name` (string) - MMAPsの姿勢を制御するための親(空)オブジェクトの名前 _[optional]_ 

---
> **getParam(_mirror_name = 'Mirror', glass_name = 'Glass', parent_name = 'MMAPs'_)**

MMAPsのパラメータ(一辺の長さ、スリット間隔、高さ比率、分割数)を返す

**Paramters**
- `mirror_name` (string) - ミラーの名前 _[optional]_ 
- `glass_name` (string) - ガラスの名前 _[optional]_ 
- `parent_name` (string) - MMAPsの姿勢を制御するための親(空)オブジェクトの名前 _[optional]_ 

**Returns**
- `size` (float) - 一辺の長さ
- `spacing` (float) - スリット間隔
- `height_scale` (float) - 高さ比率
- `detailing` (float) - 分割数
- `isGlass` (bool) - ガラスの有無

> **clearMMAPs(_mirror_name = 'Mirror', glass_name = 'Glass', parent_name = 'MMAPs'_)**

MMAPs(ミラー、ガラス、空オブジェクトで構成される)を削除する
    
**Paramters**
- `mirror_name` (string) - ミラーの名前 _[optional]_ 
- `glass_name` (string) - ガラスの名前 _[optional]_ 
- `parent_name` (string) - MMAPsの姿勢を制御するための親(空)オブジェクトの名前 _[optional]_ 

---

> **createMMAPs(_size, spacing, height_scale = 3, overwrite=True_)**

MMAPsを生成する

**Parameters**
- `size` (float) - MMAPsの一辺の大きさ
- `spacing` (float) - スリットミラー間の間隔
- `height_scale` (float) - スリット間隔を基準としてスリットの高さを決めるための倍率
- `overwrite` (bool) - MMAPsが存在した場合に上書きするかどうか。`True`の場合、既存のMMAPsを削除してから新規生成する _[optional]_ 
- `isGlass` (bool) - ガラスの有無 _[optional]_ 
- `glass_center` - ガラスが真ん中かどうか _[optional]_ 
- `ior` - ガラスの屈折率 _[optional]_ 

---

> **createDetailedMMAPs(_size, spacing, detailing = 10, height_scale = 3.0, overwrite=True, isGlass=True, glass_center=False, ior=1.45_)**

各スリットミラーを分割したMMAPsを生成する

**Parameters**
- `size` (float) - MMAPsの一辺の大きさ
- `spacing` (float) - スリットミラー間の間隔
- `detailing` (int) - 各ミラーの分割数。デフォルトでは各ミラーを10分割する。
- `height_scale` (float) - スリット間隔を基準としてスリットの高さを決めるための倍率
- `overwrite` (bool) - MMAPsが存在した場合に上書きするかどうか。`True`の場合、既存のMMAPsを削除してから新規生成する _[optional]_ 
- `isGlass` (bool) - ガラスの有無 _[optional]_ 
- `glass_center` - ガラスが真ん中かどうか _[optional]_ 
- `ior` - ガラスの屈折率 _[optional]_ 

---

> **attachMaterial(_obj, mat_name_)**

オブジェクトにマテリアルを設定する。`mat_name`で指定される名前のオブジェクトが存在しない場合は新規に作成する。

**Parameters**
- `obj` (BlendDataObjects) - マテリアルを設定する対象のオブジェクト
- `mat_name` (string) - マテリアルの名前

---

> **attachMirrorMaterial(_obj, mat_name_)**

オブジェクトに鏡のマテリアルを設定する。`mat_name`で指定される名前のオブジェクトが存在しない場合は新規に作成する。

**Parameters**
- `obj` (BlendDataObjects) - マテリアルを設定する対象のオブジェクト
- `mat_name` (string) - マテリアルの名前

---

> **attachGlassMaterial(_obj, mat_name, ior=1.45_)**

オブジェクトにガラスのマテリアルを設定する。`mat_name`で指定される名前のオブジェクトが存在しない場合は新規に作成する。

**Parameters**
- `obj` (BlendDataObjects) - マテリアルを設定する対象のオブジェクト
- `mat_name` (string) - マテリアルの名前
- `ior` - ガラスの屈折率 _[optional]_ 

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
- `glass_center` - ガラスが真ん中かどうか _[optional]_ 


