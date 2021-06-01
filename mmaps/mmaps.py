import bpy
from . import myutil
import math
import numpy as np
from mathutils import *

__size = 48.8
__spacing = 0.05
__height_scale = 2.5
__detailing = 10
__isInit = True
__isGlass = True
__glass_name = 'Glass'
__mirror_name = 'Mirror'
__parent_name = 'MMAPs'

# ================================================================================
def clearMMAPs(mirror_name = 'Mirror', glass_name = 'Glass', parent_name = 'MMAPs'):
    for ob in bpy.data.objects:
        # Verify whether glass or mirror have parent object named with "parent_name".
        if ob.parent == bpy.data.objects[parent_name]:
            if ob.name.find(mirror_name) > -1 or ob.name.find(glass_name) > -1:
                print("REMOVE: "+ob.name)
                bpy.data.objects.remove(ob)

    # After mirrors and glass are deleted, parent object will be deleted.
    if bpy.data.objects.get(parent_name) is not None:
        ob = bpy.data.objects[parent_name]
        print("REMOVE: "+ob.name)
        bpy.data.objects.remove(ob)

# ================================================================================
def createMMAPs(size, spacing, detailing = 10, height_scale = 2.5, isGlass=True, ior=1.52):
    global __size, __spacing, __height_scale, __detailing
    __size = size
    __spacing = spacing
    __detailing = detailing
    __height_scale = height_scale
    __isInit = False
    __isGlass = isGlass

    # The number of slit in each layer
    numSlit = int( (__size / spacing) * math.sqrt(2))
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
            mirror_size = (numSlit/2 - abs(numSlit/2 - i)) * spacing * 2
            for j in range(int(detailing)):
                if l==0:
                    v1 = ((i - numSlit / 2) * spacing, -mirror_size * 0.5 + (j/detailing) * mirror_size, 0)
                    v2 = ((i - numSlit / 2) * spacing, -mirror_size * 0.5 + (j/detailing) * mirror_size, -height)
                    v3 = ((i - numSlit / 2) * spacing, -mirror_size * 0.5 + ((j+1)/detailing) * mirror_size, -height)
                    v4 = ((i - numSlit / 2) * spacing, -mirror_size * 0.5 + ((j+1)/detailing) * mirror_size, 0)
                    verts.append(v1)
                    verts.append(v2)
                    verts.append(v3)
                    verts.append(v4)
                else:
                    v1 = (-mirror_size * 0.5 + (j/detailing) * mirror_size, (i - numSlit / 2) * spacing, height)
                    v2 = (-mirror_size * 0.5 + (j/detailing) * mirror_size, (i - numSlit / 2) * spacing, 0)
                    v3 = (-mirror_size * 0.5 + ((j+1)/detailing) * mirror_size, (i - numSlit / 2) * spacing, 0)
                    v4 = (-mirror_size * 0.5 + ((j+1)/detailing) * mirror_size, (i - numSlit / 2) * spacing, height)
                    verts.append(v1)
                    verts.append(v2)
                    verts.append(v3)
                    verts.append(v4)
                    
            faces = [tuple(np.arange(4*detailing))]

            # Add slit mirror object to current scene
            mirror = addMirror(parent = mmaps, verts = verts, faces = faces, obj_name = 'Mirror', id = count)
            # Attach material to mirror object
            attachMirrorMaterial(mirror, mat_name = 'MMAPsMirror')

            count += 1

    if __isGlass:
        # Add glass object to scene
        glass = addGlass(mmaps, __size, height*2, obj_name = 'Glass')
        # Attach material to glass object
        attachGlassMaterial(glass, mat_name = 'Glass', ior=ior)

    # Activate parent object (MMAPs) 
    bpy.context.view_layer.objects.active = mmaps

    # Log message
    print('MMAPs are successfully created!')
    print('size: {}, slit spacing: {}, polygon detailing: {}, height scale: {}'.format(__size, spacing, detailing, height_scale))
    print('Mirror count: {}'.format(count))

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
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Metallic'].default_value = 0.87
    bsdf.inputs['Roughness'].default_value = 0.01
    bsdf.location = 0,0

    # Create output node
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = 400, 0

    # Link nodes
    links = mat.node_tree.links
    link = links.new(bsdf.outputs['BSDF'], node_output.inputs['Surface'])

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
    bsdf = nodes.new(type='ShaderNodeBsdfGlass')
    bsdf.inputs['Roughness'].default_value = 0.01
    bsdf.inputs['IOR'].default_value = ior
    bsdf.location = 0,0

    # Create output node
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_output.location = 400, 0

    # Link nodes
    links = mat.node_tree.links
    link = links.new(bsdf.outputs['BSDF'], node_output.inputs['Surface'])

    # Clear material of object
    obj.data.materials.clear()
    # Set material to object
    obj.data.materials.append(mat)

# ================================================================================
def addMirror(parent, verts, faces, obj_name = 'Mirror', id = None):

    # Create a new mirror from vertex data
    number = str(id) if not id == None else ''
    mesh = bpy.data.meshes.new('Mirror'+number)
    mesh.from_pydata(verts, [], faces)
            
    # Create object and change transformation
    mirror = bpy.data.objects.new('Mirror'+number, mesh)
    mirror.rotation_euler = (0, 0, math.pi / 4)
            
    # Set parent
    mirror.parent = parent
    # Register mirror to scene
    bpy.context.collection.objects.link(mirror)

    return mirror
        
# ================================================================================
def addGlass(parent, size, height, obj_name = 'Glass'):
    # Create a new cube
    bpy.ops.mesh.primitive_cube_add()
    
    # Newly created cube will be automatically selected
    glass = bpy.context.selected_objects[0]
    # Change name
    glass.name = 'Glass'
    # Set the location to origin of the scene.
    glass.location = Vector((0, 0, 0))
    
    # Change glass's dimensions
    glass.dimensions = (size, size, height)
    
    # Set parent
    glass.parent = parent

    return glass