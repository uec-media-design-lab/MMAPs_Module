import bpy
import myutil
import math
import numpy as np
from mathutils import *

__size = 48.8
__spacing = 0.05
__height_scale = 3.0
__detailing = 10
__isInit = True
__isGlass = True
__glass_name = 'Glass'
__mirror_name = 'Mirror'
__parent_name = 'MMAPs'

# ================================================================================
def showParam(mirror_name = 'Mirror', glass_name = 'Glass', parent_name = 'MMAPs'):
    global __mirror_name, __glass_name, __parent_name

    __mirror_name, __glass_name, __parent_name = mirror_name, glass_name, parent_name
    size, spacing, height_scale, detailing, isGlass = getParam(__mirror_name, __glass_name, __parent_name)
    print('size: {}, spacing: {}, height_scale: {}, detailing: {}, Glass exists: {}'.format(size, spacing, height_scale, detailing, isGlass))

# ================================================================================
def getParam(mirror_name = 'Mirror', glass_name = 'Glass', parent_name = 'MMAPs'):
    global __size, __spacing, __height_scale, __detailing, __isInit, __isGlass, __mirror_name, __glass_name, __parent_name

    __mirror_name, __glass_name, __parent_name = mirror_name, glass_name, parent_name

    if __isInit:
        mmaps = bpy.data.objects[parent_name]
        mirrorCnt = 0
        maxMirrorSize = 0
        mirrorHeight = 0
        numVertices = 0
        for obj in bpy.data.objects:
            if obj.parent == mmaps:
                if obj.name.find(mirror_name) > -1:
                    mirrorCnt += 1
                    mirrorHeight = obj.dimensions.z

                    if obj.dimensions.x > 0 or obj.dimensions.y > 0:
                        numVertices = len(obj.data.vertices)
                    
                    if obj.dimensions.x > maxMirrorSize:
                        maxMirrorSize = obj.dimensions.x

        # Size of MMAPs
        __size = maxMirrorSize / math.sqrt(2)
        __size = round(__size, myutil.getRoundDigit(__size))

        # Slit's parameters
        __spacing = maxMirrorSize / (mirrorCnt / 2)
        __height_scale = mirrorHeight / __spacing
        __spacing = round(__spacing, myutil.getRoundDigit(__spacing))
        __height_scale = round(__height_scale, myutil.getRoundDigit(__height_scale))

        # The number of detailing of each mirror
        __detailing = int(numVertices / 4)

        # This module have already initialized.
        __isInit = False

        __isGlass = bpy.data.objects.get(__glass_name) is not None

        return __size, __spacing, __height_scale, __detailing, __isGlass
    else:
        return __size, __spacing, __height_scale, __detailing, __isGlass

# ================================================================================
def clearMMAPs(mirror_name = 'Mirror', glass_name = 'Glass', parent_name = 'MMAPs'):
    for ob in bpy.data.objects:
        # Verify whether glass or mirror have parent object named with "parent_name".
        if ob.parent == bpy.data.objects[parent_name]:
            if ob.name.find(mirror_name) > -1 or ob.name.find(glass_name) > -1:
                print("REMOVE: "+ob.name)
                bpy.data.objects.remove(ob)
        if ob.name.find(parent_name > -1):
            print("REMOVE: "+ob.name)
            bpy.data.objects.remove(ob)

# ================================================================================
def createMMAPs(size, spacing, height_scale = 3.0, overwrite=True, isGlass=True, glass_center=False, ior=1.52):
    global __size, __spacing, __height_scale
    __size = size
    __spacing = spacing
    __height_scale = height_scale
    __detailing = None
    __isInit = False
    __isGlass = isGlass

    # Delete exiting MMAPs
    if overwrite:
        clearMMAPs()

    # The number of slit in each layer
    numSlit = int( (__size/spacing) * math.sqrt(2) )
    height = spacing * height_scale
    
    count = 0
    
    # Create and register empty object as parent of mirror and glass transformation
    mmaps = bpy.data.objects.new('MMAPs', None)
    bpy.context.collection.objects.link(mmaps)
    
    for l in range(2):
        # Place slit mirrors in each layer
        for i in range(numSlit):
            verts = []
            glassVerts = []
            if l == 0:
                if i <= numSlit / 2:
                    verts = [((i - numSlit / 2) * spacing, -(i * spacing), 0),
                             ((i - numSlit / 2) * spacing, -(i * spacing), -height),
                             ((i - numSlit / 2) * spacing, (i * spacing), -height),
                             ((i - numSlit / 2) * spacing, (i * spacing), 0)]
                else:
                    verts = [((i - numSlit / 2) * spacing, -((numSlit - i) * spacing), 0),
                             ((i - numSlit / 2) * spacing, -((numSlit - i) * spacing), -height),
                             ((i - numSlit / 2) * spacing, ((numSlit - i) * spacing), -height),
                             ((i - numSlit / 2) * spacing, ((numSlit - i) * spacing), 0)]
            else:
                if i <= numSlit / 2:
                    verts = [( -(i * spacing), (i - numSlit / 2) * spacing, height),  
                             ( -(i * spacing), (i - numSlit / 2) * spacing, 0),  
                             ( (i * spacing), (i - numSlit / 2) * spacing, 0),  
                             ( (i * spacing), (i - numSlit / 2) * spacing, height)]  
                else:
                    verts = [( -(numSlit - i) * spacing, (i - numSlit / 2) * spacing, height),
                             ( -(numSlit - i) * spacing, (i - numSlit / 2) * spacing, 0),
                             ( (numSlit - i) * spacing, (i - numSlit / 2) * spacing, 0),
                             ( (numSlit - i) * spacing, (i - numSlit / 2) * spacing, height)]
            faces = [(0, 1, 2, 3)]

            # Add mirror object to current scene
            mirror = addMirror(parent = mmaps, verts = verts, faces = faces, obj_name = 'Mirror', id = count)
            # Attach material to mirror object
            attachMirrorMaterial(mirror, mat_name = 'MMAPsMirror')
            
            count += 1

    if __isGlass:
        # Add glass object to current scene
        glass = addGlass(mmaps, __size, height*2, obj_name = 'Glass', center=glass_center)
        # Attach material to glass object
        attachGlassMaterial(glass, mat_name = 'Glass', ior=ior)

    # Log message
    print('MMAPs (no glass) are successfully created!')
    print('size: {}, slit spacing: {}, height scale: {}'.format(__size, spacing, height_scale))
    print('Mirror count: {}'.format(count))

    return mmaps

# ================================================================================
def createDetailedMMAPs(size, spacing, detailing = 10, height_scale = 3.0, overwrite=True, isGlass=True, glass_center=False, ior=1.52):
    global __size, __spacing, __height_scale, __detailing
    __size = size
    __spacing = spacing
    __detailing = detailing
    __height_scale = height_scale
    __isInit = False
    __isGlass = isGlass

    # Delete exiting MMAPs
    if overwrite:
        clearMMAPs()

    # The number of slit in each layer
    numSlit = int( (__size / spacing) * math.sqrt(2))
    height = spacing * height_scale
    
    count = 0

    # Create and register empty object as parent of mirror and glass transformation
    mmaps = bpy.data.objects.new('MMAPs', None)
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
        glass = addGlass(mmaps, __size, height*2, obj_name = 'Glass', center=glass_center)
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
def attachMaterial(obj, mat_name):
    mat = bpy.data.materials.get(mat_name)
    if mat is None:
        # Create materials
        mat = bpy.data.materials.new(name=mat_name)
    
    if obj.data.materials:
        # Assign to 1st material slot
        obj.data.materials[0] = mat
    else:
        # There is no material in material slot of object
        obj.data.materials.append(mat)

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
def attachGlassMaterial(obj, mat_name, ior=1.45):
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
def addGlass(parent, size, height, obj_name = 'Glass', center=False):
    if center:
        # Create a new plane
        bpy.ops.mesh.primitive_plane_add()
    else:
        # Create a new cube
        bpy.ops.mesh.primitive_cube_add()
    
    # Newly created cube will be automatically selected
    glass = bpy.context.selected_objects[0]
    # Change name
    glass.name = 'Glass'
    # Set the location to origin of the scene.
    glass.location = Vector((0, 0, 0))
    
    if center:
        # Change glass's dimensions
        glass.dimensions = (size, size, 1.0)
    else:
        # Change glass's dimensions
        glass.dimensions = (size, size, height)
    
    # Set parent
    glass.parent = parent

    return glass