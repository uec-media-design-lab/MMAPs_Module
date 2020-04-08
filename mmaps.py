import bpy
import math
import numpy as np

# ================================================================================
def clearMMAPs(mirror_name = 'Mirror', glass_name = 'Glass', parent_name = 'MMAPs'):
    for ob in bpy.data.objects:
        if ob.name.find(mirror_name) > -1 or ob.name.find(glass_name) > -1 or ob.name.find(parent_name) > -1:
            print("REMOVE: "+ob.name)
            bpy.data.objects.remove(ob)

# ================================================================================
def createMMAPs(size, spacing, height_scale = 3, overwrite=True):
    if overwrite:
        clearMMAPs()

    # the number of slit in each layer
    numSlit = int( (size/spacing) * math.sqrt(2) )
    height = spacing * height_scale
    
    count = 0
    
    # create and register empty object as parent of mirror and glass transformation
    mmaps = bpy.data.objects.new('MMAPs', None)
    bpy.context.collection.objects.link(mmaps)
    
    for l in range(2):
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

            mirror = addMirror(parent = mmaps, verts = verts, faces = faces, obj_name = 'Mirror', id = count)
            attachMaterial(mirror, mat_name = 'MMAPsMirror')
            
            count += 1

    # log message
    print('MMAPs (no glass) are successfully created!')
    print('size: {}, slit spacing: {}, height scale: {}'.format(size, spacing, height_scale))
    print('Mirror count: {}'.format(count))

# ================================================================================
def createDetailedMMAPs(size, spacing, detailing = 10, height_scale = 3, overwrite=True):
    if overwrite:
        clearMMAPs()

    # the number of slit in each layer
    numSlit = int( (size / spacing) * math.sqrt(2))
    height = spacing * height_scale
    
    count = 0
    mmaps = bpy.data.objects.new('MMAPs', None)
    bpy.context.collection.objects.link(mmaps)
    
    for l in range(2):
        for i in range(numSlit):
            verts = []
            faces = []
            mirror_size = (numSlit/2 - abs(numSlit/2 - i)) * spacing * 2
            for j in range(detailing):
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

            # add slit mirror to scene
            mirror = addMirror(parent = mmaps, verts = verts, faces = faces, obj_name = 'Mirror', id = count)
            # attach material to mirror object
            attachMaterial(mirror, mat_name = 'MMAPsMirror')

            count += 1
    # add glass to scene
    glass = addGlass(mmaps, size, height*2, obj_name = 'Glass')
    # attach material to mirror object
    attachMaterial(glass, mat_name = 'Glass')

    # log message
    print('MMAPs are successfully created!')
    print('size: {}, slit spacing: {}, polygon detailing: {}, height scale: {}'.format(size, spacing, detailing, height_scale))
    print('Mirror count: {}'.format(count))

# ================================================================================
def attachMaterial(obj, mat_name):
    mat = bpy.data.materials.get(mat_name)
    if mat is None:
        # create materials of each planes
        mat = bpy.data.materials.new(name=mat_name)
    
    if obj.data.materials:
        # assign to 1st material slot
        obj.data.materials[0] = mat
    else:
        # no slots
        obj.data.materials.append(mat)

# ================================================================================
def addMirror(parent, verts, faces, obj_name = 'Mirror', id = None):

    # create a new mirror from vertex data
    number = str(id) if not id == None else ''
    mesh = bpy.data.meshes.new('Mirror'+number)
    mesh.from_pydata(verts, [], faces)
            
    # create object and change transformation
    mirror = bpy.data.objects.new('Mirror'+number, mesh)
    mirror.rotation_euler = (0, 0, math.pi / 4)
            
    # set parent
    mirror.parent = parent
    # register mirror to scene
    bpy.context.collection.objects.link(mirror)

    return mirror
        
# ================================================================================
def addGlass(parent, size, height, obj_name = 'Glass'):
    # create a new cube
    bpy.ops.mesh.primitive_cube_add()
    
    # newly created cube will be automatically selected
    glass = bpy.context.selected_objects[0]
    # change name
    glass.name = 'Glass'
    
    # change its dimensions
    glass.dimensions = (size, size, height)
    
    # set parent
    glass.parent = parent

    return glass