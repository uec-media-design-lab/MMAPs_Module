# BlenderでMMAPsを生成するモジュール
- これは、Micro-Mirror Array Platesをblender内で再現するためのモジュールです。
- 使用方法は[こちら](https://www.media.lab.uec.ac.jp/?p=2569)を参照下さい。

- MMAPsの再現性に関しては[論文](https://doi.org/10.1016/j.cag.2021.02.007)をご確認下さい。
  -  Shunji Kiuchi, Naoya Koizumi. Simulating the appearance of mid-air imaging with micro-mirror array plates. *Computers & Graphics*,2021.
-  vcf(Louver film)は再現できていません。簡易的なものになっています。

- mmaps/ ... MMAPs作成用アドオンフォルダ(開発用)
  - __init__.py       ... 初期化ファイル
  - mmaps.py          ... MMAPs生成/削除用モジュール
  - myutil.py         ... Utility関数モジュール
  - mmaps_clearer.py  ... MMAPs削除用オペレータクラス
  - mmaps_launcher.py ... MMAPs生成用オペレータクラス
  - mmaps_manager.py  ... パラメータ管理用パネルクラス
- vcf/
  - __init__.py       ... 初期化ファイル
  - vcf.py            ... VCF生成/削除用モジュール
  - myutil.py         ... Utility関数モジュール
  - vcf_clearer.py    ... VCF削除用オペレータクラス
  - vcf_launcher.py   ... VCF生成用オペレータクラス
  - vcf_manager.py    ... パラメータ管理用パネルクラス
- mmaps.zip           ... インストール用(MMAPs)
- vcf.zip             ... インストール用(VCF)

# 検証version
- Blender 2.8.1


# Setup

- Edit -> Preferences を立ち上げ、Add-ons を選択
- Testing を選択後、Install を押す。
  - ![](img/addon.png)
- ファイルエクスプローラーが出るので、`mmaps.zip` or `vcf.zip` を選択。

# パラメータの設定
- MMAPsサイズ  : 48.8
- スリット間隔 : 0.05
- 高さ比率     : 2.5
- ミラー分割数 : 10
- 反射率       : 0.87
- 屈折率       : 1.52

# 開発用メモ
- 開発時は、`mmaps/` or `vcf/` 以下のpythonファイルを修正し、修正終了後は 各ディレクトリを zip 形式に圧縮してください。

# Functions

## MMAPs Launcher

> **clearMMAPs(_mirror_name = 'Mirror', glass_name = 'Glass', parent_name = 'MMAPs'_)**

MMAPs(ミラー、ガラス、空オブジェクトで構成される)を削除する
    
**Paramters**
- `mirror_name` (string) - ミラーの名前 _[optional]_ 
- `glass_name` (string) - ガラスの名前 _[optional]_ 
- `parent_name` (string) - MMAPsの姿勢を制御するための親(空)オブジェクトの名前 _[optional]_ 

---

> **createMMAPs(_size, spacing, detailing = 10, height_scale = 2.5, isGlass=True, ior=1.52_)**

各スリットミラーを分割したMMAPsを生成する

**Parameters**
- `size` (float) - MMAPsの一辺の大きさ
- `spacing` (float) - スリットミラー間の間隔
- `detailing` (int) - 各ミラーの分割数。デフォルトでは各ミラーを10分割する。
- `height_scale` (float) - スリット間隔に対するスリットの高さの比率
- `isGlass` (bool) - ガラスの有無 _[optional]_ 
- `ior` - ガラスの屈折率 _[optional]_ 

---

> **attachMirrorMaterial(_obj, mat_name_)**

オブジェクトに鏡のマテリアルを設定する。`mat_name`で指定される名前のオブジェクトが存在しない場合は新規に作成する。

**Parameters**
- `obj` (BlendDataObjects) - マテリアルを設定する対象のオブジェクト
- `mat_name` (string) - マテリアルの名前

---

> **attachGlassMaterial(_obj, mat_name, ior=1.52_)**

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



## VCF Launcher

> **clearVCF(louver_name = 'Louver', glass_name = 'Glass', parent_name = 'VCF')**

VCF(ルーバー、空オブジェクトで構成される)を削除する
    
**Paramters**
- `louver_name` (string) - ルーバーの名前 _[optional]_ 
- `glass_name` (string) - ガラスの名前 _[optional]_ 
- `parent_name` (string) - VCFの姿勢を制御するための親(空)オブジェクトの名前 _[optional]_ 

---

> **createVCF(name,size, spacing, view_angle = 0, max_beam_transmission_angle = 0, height = 0.01, clearance = 0)**

ルーバーを並べたVCFを生成する

**Parameters**
- `size` (float) - MMAPsの一辺の大きさ
- `spacing` (float) - ルーバーの間隔
- `view_angle` (float) - VCFの視野角
- `max_beam_transmission_angle` (float) - 平面に垂直な面からのルーバーの角度
- `height` (float) - VCFの高さ
- `clearance` (float) - ルーバーの開始位置余白

---

> **attachLouverMaterial(_obj, mat_name_)**

オブジェクトに吸光材のマテリアルを設定する。`mat_name`で指定される名前のオブジェクトが存在しない場合は新規に作成する。

**Parameters**
- `obj` (BlendDataObjects) - マテリアルを設定する対象のオブジェクト
- `mat_name` (string) - マテリアルの名前

---

> **addMLouver(_parent, verts, faces, obj_name = 'Louver', id = None_)**

ルーバーを生成する。フィルム内のルーバーを想定しているので、親オブジェクト(`parent`)は必須。

**Parameters**
- `parent` (BlendDataObjects) - 親オブジェクト
- `verts` (array) - 頂点情報
- `faces` (array) - 頂点番号情報(インデックス)
- `obj_name` (string) - オブジェクトの名前
- `id` (int) - ルーバーの番号
