import math

import bpy
import numpy as np
from mathutils import *

from . import myutil

__size = 48.8
__spacing = 0.05
__height_scale = 2.5
__detailing = 10
__isInit = True
__isGlass = True
__glass_name = "Glass"
__mirror_name = "Mirror"
__parent_name = "MMAPs"


class LayerProperty:
    def __init__(self, height_scale: float, ior: float, degree: float):
        self.height_scale = height_scale
        self.ior = ior
        self.degree = degree


# ================================================================================
def clearMMAPs(mirror_name="Mirror", glass_name="Glass", parent_name="MMAPs"):
    for ob in bpy.data.objects:
        # Verify whether glass or mirror have parent object named with "parent_name".
        if ob.parent == bpy.data.objects[parent_name]:
            if ob.name.find(mirror_name) > -1 or ob.name.find(glass_name) > -1:
                print("REMOVE: " + ob.name)
                bpy.data.objects.remove(ob)

    # After mirrors and glass are deleted, parent object will be deleted.
    if bpy.data.objects.get(parent_name) is not None:
        ob = bpy.data.objects[parent_name]
        print("REMOVE: " + ob.name)
        bpy.data.objects.remove(ob)


def clearCustomMMAP():
    for ob in bpy.data.objects:
        # Verify whether glass or mirror have parent object named with "parent_name".
        if ob.parent == bpy.data.objects["CustomMMAP"]:
            if ob.name.find("Mirror_Layer") > -1 or ob.name.find("Glass_Layer") > -1:
                print("REMOVE: " + ob.name)
                bpy.data.objects.remove(ob)

    # After removing mirrors and glass, parent object will be removed.
    if bpy.data.objects.get("CustomMMAP") is not None:
        ob = bpy.data.objects["CustomMMAP"]
        print("REMOVE: " + ob.name)
        bpy.data.objects.remove(ob)


# ================================================================================
def createCustomMMAP(
    size,
    spacing,
    detailing: int,
    layer1: LayerProperty,
    layer2: LayerProperty,
    isGlass=True,
):
    """
    Instantiate customized MMAP that each layer own different properties (angle, height scale and IOR)
    """
    num_slit = int((size / spacing) * math.sqrt(2))
    # Properties of each layer
    heights = [spacing * layer1.height_scale, spacing * layer2.height_scale]
    degrees = [layer1.degree, layer2.degree]
    iors = [layer1.ior, layer2.ior]

    count = 0

    # Register empty object as parent of mirror and glass transformation
    mmaps = bpy.data.objects.new("CustomMMAP", None)
    bpy.context.collection.objects.link(mmaps)

    # Deselect all selected object to limit a target to apply transformation for only new object
    bpy.ops.object.select_all(action="DESELECT")

    for layer in range(2):
        # Place mirrors in each layer
        for i in range(num_slit):
            verts = []
            faces = []
            mirror_size = (num_slit / 2 - abs(num_slit / 2 - i)) * spacing * 2
            # Mirror offset
            offset = (i - num_slit / 2) * spacing / math.sqrt(2)
            location = (-offset, offset, 0) if layer == 0 else (offset, offset, 0)
            for j in range(int(detailing)):
                if layer == 0:
                    v1 = (
                        # (i - num_slit / 2) * spacing,
                        0,
                        -mirror_size * 0.5 + (j / detailing) * mirror_size,
                        0,
                    )
                    v2 = (
                        # (i - num_slit / 2) * spacing,
                        0,
                        -mirror_size * 0.5 + (j / detailing) * mirror_size,
                        -heights[layer],
                    )
                    v3 = (
                        # (i - num_slit / 2) * spacing,
                        0,
                        -mirror_size * 0.5 + ((j + 1) / detailing) * mirror_size,
                        -heights[layer],
                    )
                    v4 = (
                        # (i - num_slit / 2) * spacing,
                        0,
                        -mirror_size * 0.5 + ((j + 1) / detailing) * mirror_size,
                        0,
                    )
                    verts.append(v1)
                    verts.append(v2)
                    verts.append(v3)
                    verts.append(v4)
                else:
                    v1 = (
                        -mirror_size * 0.5 + (j / detailing) * mirror_size,
                        # (i - num_slit / 2) * spacing,
                        0,
                        heights[layer],
                    )
                    v2 = (
                        -mirror_size * 0.5 + (j / detailing) * mirror_size,
                        # (i - num_slit / 2) * spacing,
                        0,
                        0,
                    )
                    v3 = (
                        -mirror_size * 0.5 + ((j + 1) / detailing) * mirror_size,
                        # (i - num_slit / 2) * spacing,
                        0,
                        0,
                    )
                    v4 = (
                        -mirror_size * 0.5 + ((j + 1) / detailing) * mirror_size,
                        # (i - num_slit / 2) * spacing,
                        0,
                        heights[layer],
                    )
                    verts.append(v1)
                    verts.append(v2)
                    verts.append(v3)
                    verts.append(v4)
            faces = [tuple(np.arange(4 * detailing))]

            # Add mirror object to the current scene
            mirror = addMirror(
                parent=mmaps,
                verts=verts,
                faces=faces,
                obj_name=f"Mirror_Layer{layer}",
                id=count,
                location=location,
                x_degree=degrees[layer],
            )
            attachMirrorMaterial(mirror, mat_name="MMAPsMirror")
            count += 1

    if isGlass:
        for layer in range(2):
            # Add glass object to scene
            sign = -1 if layer == 0 else 1
            glass = addLayerGlass(
                mmaps,
                size,
                heights[layer],
                Vector((0, 0, sign * heights[layer] / 2)),
                obj_name=f"Glass_Layer{layer}",
            )
            # Attach material to glass object
            attachGlassMaterial(glass, mat_name=f"Glass_Layer{layer}", ior=iors[layer])

    # Activate parent object (MMAP)
    bpy.context.view_layer.objects.active = mmaps

    # Log message
    print("MMAPs are successfully created!")
    print(
        f"Layer1: Height scale: {layer1.height_scale}, IOR: {layer1.ior}, Degree: {layer1.degree}\n Layer2: Height sacle: {layer2.height_scale}, IOR: {layer2.ior}, Degree: {layer2.degree}"
    )
    print(f"Mirror count: {count}")

    return mmaps


# ================================================================================
def createMMAPs(size, spacing, detailing=10, height_scale=2.5, isGlass=True, ior=1.52):
    global __size, __spacing, __height_scale, __detailing
    __size = size
    __spacing = spacing
    __detailing = detailing
    __height_scale = height_scale
    __isInit = False
    __isGlass = isGlass

    # The number of slit in each layer
    numSlit = int((__size / spacing) * math.sqrt(2))
    height = spacing * height_scale

    count = 0

    # Create and register empty object as parent of mirror and glass transformation
    mmaps = bpy.data.objects.new(__parent_name, None)
    bpy.context.collection.objects.link(mmaps)

    for l in range(2):
        # Place slit mirrors in each layer
        for i in range(numSlit):
            verts = []
            faces = []
            mirror_size = (numSlit / 2 - abs(numSlit / 2 - i)) * spacing * 2
            for j in range(int(detailing)):
                if l == 0:
                    v1 = (
                        (i - numSlit / 2) * spacing,
                        -mirror_size * 0.5 + (j / detailing) * mirror_size,
                        0,
                    )
                    v2 = (
                        (i - numSlit / 2) * spacing,
                        -mirror_size * 0.5 + (j / detailing) * mirror_size,
                        -height,
                    )
                    v3 = (
                        (i - numSlit / 2) * spacing,
                        -mirror_size * 0.5 + ((j + 1) / detailing) * mirror_size,
                        -height,
                    )
                    v4 = (
                        (i - numSlit / 2) * spacing,
                        -mirror_size * 0.5 + ((j + 1) / detailing) * mirror_size,
                        0,
                    )
                    verts.append(v1)
                    verts.append(v2)
                    verts.append(v3)
                    verts.append(v4)
                else:
                    v1 = (
                        -mirror_size * 0.5 + (j / detailing) * mirror_size,
                        (i - numSlit / 2) * spacing,
                        height,
                    )
                    v2 = (
                        -mirror_size * 0.5 + (j / detailing) * mirror_size,
                        (i - numSlit / 2) * spacing,
                        0,
                    )
                    v3 = (
                        -mirror_size * 0.5 + ((j + 1) / detailing) * mirror_size,
                        (i - numSlit / 2) * spacing,
                        0,
                    )
                    v4 = (
                        -mirror_size * 0.5 + ((j + 1) / detailing) * mirror_size,
                        (i - numSlit / 2) * spacing,
                        height,
                    )
                    verts.append(v1)
                    verts.append(v2)
                    verts.append(v3)
                    verts.append(v4)

            faces = [tuple(np.arange(4 * detailing))]

            # Add slit mirror object to current scene
            mirror = addMirror(
                parent=mmaps, verts=verts, faces=faces, obj_name="Mirror", id=count
            )
            # Attach material to mirror object
            attachMirrorMaterial(mirror, mat_name="MMAPsMirror")

            count += 1

    if __isGlass:
        # Add glass object to scene
        glass = addGlass(mmaps, __size, height * 2, obj_name="Glass")
        # Attach material to glass object
        attachGlassMaterial(glass, mat_name="Glass", ior=ior)

    # Activate parent object (MMAPs)
    bpy.context.view_layer.objects.active = mmaps

    # Log message
    print("MMAPs are successfully created!")
    print(
        "size: {}, slit spacing: {}, polygon detailing: {}, height scale: {}".format(
            __size, spacing, detailing, height_scale
        )
    )
    print("Mirror count: {}".format(count))

    return mmaps


# ================================================================================
def attachMirrorMaterial(obj, mat_name):
    mat = bpy.data.materials.get(mat_name)
    if mat is None:
        # Create materials
        mat = bpy.data.materials.new(name=mat_name)

    # Enable to use node
    mat.use_nodes = True
    # Clear nodes of material
    nodes = mat.node_tree.nodes
    nodes.clear()

    # Create princpled bsdf node
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.inputs["Metallic"].default_value = 0.87
    bsdf.inputs["Roughness"].default_value = 0.01
    bsdf.location = 0, 0

    # Create output node
    node_output = nodes.new(type="ShaderNodeOutputMaterial")
    node_output.location = 400, 0

    # Link nodes
    links = mat.node_tree.links
    link = links.new(bsdf.outputs["BSDF"], node_output.inputs["Surface"])

    # Clear material of object
    obj.data.materials.clear()
    # Set material to object
    obj.data.materials.append(mat)


# ================================================================================
def attachGlassMaterial(obj, mat_name, ior=1.52):
    mat = bpy.data.materials.get(mat_name)
    if mat is None:
        # Create materials
        mat = bpy.data.materials.new(name=mat_name)

    # Enable to use node
    mat.use_nodes = True
    # Clear nodes of material
    nodes = mat.node_tree.nodes
    nodes.clear()

    # Create princpled bsdf node
    bsdf = nodes.new(type="ShaderNodeBsdfGlass")
    bsdf.inputs["Roughness"].default_value = 0.01
    bsdf.inputs["IOR"].default_value = ior
    bsdf.location = 0, 0

    # Create output node
    node_output = nodes.new(type="ShaderNodeOutputMaterial")
    node_output.location = 400, 0

    # Link nodes
    links = mat.node_tree.links
    link = links.new(bsdf.outputs["BSDF"], node_output.inputs["Surface"])

    # Clear material of object
    obj.data.materials.clear()
    # Set material to object
    obj.data.materials.append(mat)


# ================================================================================
def addMirror(
    parent,
    verts,
    faces,
    obj_name="Mirror",
    id=None,
    location=(0, 0, 0),
    x_degree: float = None,
):
    # Create a new mirror from vertex data
    number = str(id) if not id == None else ""
    mesh = bpy.data.meshes.new("Mirror" + number)
    mesh.from_pydata(verts, [], faces)

    # Create object and change transformation
    mirror = bpy.data.objects.new(f"{obj_name}_{number}", mesh)

    # Register mirror to scene
    bpy.context.collection.objects.link(mirror)
    mirror.select_set(True)

    # If degree is specified, the mirror will be rotated on x-axis at the first
    bpy.ops.transform.rotate(value=math.radians(x_degree), orient_axis="X")
    bpy.ops.transform.translate(value=location)
    bpy.ops.transform.rotate(value=math.pi / 4, orient_axis="Z")

    # Set parent
    mirror.parent = parent

    # Deselect object so that prevent global transformation operation
    mirror.select_set(False)

    return mirror


# ================================================================================
def addLayerGlass(parent, size, height, center, obj_name="Glass"):
    # Create a new cube
    bpy.ops.mesh.primitive_cube_add()

    # Newly created cube will be automatically selected
    glass = bpy.context.selected_objects[0]
    # Change name
    glass.name = obj_name
    # Set the location to origin of the scene.
    glass.location = center

    # Change glass's dimensions
    glass.dimensions = (size, size, height)

    # Set parent
    glass.parent = parent

    return glass


# ================================================================================
def addGlass(parent, size, height, obj_name="Glass"):
    # Create a new cube
    bpy.ops.mesh.primitive_cube_add()

    # Newly created cube will be automatically selected
    glass = bpy.context.selected_objects[0]
    # Change name
    glass.name = "Glass"
    # Set the location to origin of the scene.
    glass.location = Vector((0, 0, 0))

    # Change glass's dimensions
    glass.dimensions = (size, size, height)

    # Set parent
    glass.parent = parent

    return glass
