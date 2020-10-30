import bpy
import math
import numpy as np
import gc

size_ = 48.8
spacing_ = 0.05
height_scale_ = 3.0
height_ = 0.01
length_ = 0.01
louver_angle_ = 0
view_angle_ = 0
clearance_ = 0
detailing_ = 10

# ================================================================================
def showParam():
	global size_, spacing_, height_, louver_angle_
	print('size: {}, spacing: {}, height: {}, louver_angle: {}'.format(size_, spacing_, height_, louver_angle_))

# ================================================================================
def getParam():
	global size_, spacing_, height_, detailing_
	return size_, spacing_, height_, detailing_

# ================================================================================
def clearVCF(louver_name = 'Louver', glass_name = 'Glass', parent_name = 'VCF'):
	for ob in bpy.data.objects:
		if ob.name.find(louver_name) > -1 or ob.name.find(glass_name) > -1 or ob.name.find(parent_name) > -1:
			print("REMOVE: "+ob.name)
			bpy.data.objects.remove(ob)

# ================================================================================
def createVCF(size, spacing, view_angle = 0, max_beam_transmission_angle = 0, height = 0.01, clearance = 0, overwrite=True):
	global size_, spacing_, height_, height_scale_, length_, louver_angle_, view_angle_
	size_ = size
	spacing_ = spacing#ルーバーの間隔
	height_ = height#ルーバーの高さ
	clearance_ = clearance
	louver_angle_ = math.radians(90-max_beam_transmission_angle)#平面に対するルーバーの角度
	view_angle_ = math.radians(view_angle)#視野角
	detailing_ = None

	top_offset=0#上辺のルーバー傾斜方向へのズレ

	if overwrite:
		clearVCF()

	# the number of slit in each layer
	numSlit = int( (size_/spacing))

	if(view_angle > 0):
		l=(1/2)*spacing_*(math.sin(louver_angle_)/math.tan(view_angle_)) * (1 + math.sqrt( math.tan(view_angle_) ** 2 / math.sin(louver_angle_)**2 + 1) )
		length_=l*2
		height_=length_*math.sin(louver_angle_)
		top_offset=length_*math.cos(louver_angle_)
		print ('l:{}'.format(l))

	showParam()

	count = 0

	# create and register empty object as parent of mirror and glass transformation
	vcf = bpy.data.objects.new('VCF', None)
	bpy.context.collection.objects.link(vcf)
	for i in range(numSlit):
		verts = []

		verts = [( -size_/2+(i * spacing_)+top_offset, -size_/2, height_ + clearance_),
				( -size_/2+(i * spacing_), -size_/2, 0 + clearance_),
				( -size_/2+(i * spacing_), size_/2, 0 + clearance_),
				( -size_/2+(i * spacing_)+top_offset, size_/2, height_ + clearance_)]
		faces = [(0, 1, 2, 3)]
		louver = addLouver(parent = vcf, verts = verts, faces = faces, obj_name = 'Louver', id = count)
		attachLouverMaterial(louver, mat_name = 'VCF_Louver')
		del verts
		del faces
		gc.collect()
		count += 1

	# log message
	print('VCF is successfully created!')
	print('size: {}, slit spacing: {}, height: {}'.format(size_, spacing, height_))
	print('Louver count: {}'.format(count))

	return vcf

# ================================================================================
def attachMaterial(obj, mat_name):
	mat = bpy.data.materials.get(mat_name)
	if mat is None:
		# create materials
		mat = bpy.data.materials.new(name=mat_name)

	if obj.data.materials:
		# assign to 1st material slot
		obj.data.materials[0] = mat
	else:
		# no slots
		obj.data.materials.append(mat)



def attachLouverMaterial(obj, mat_name):
	mat = bpy.data.materials.get(mat_name)
	if mat is None:
		# create materials
		mat = bpy.data.materials.new(name=mat_name)

	# enable to use node
	mat.use_nodes = True
	# clear nodes of material
	nodes = mat.node_tree.nodes
	nodes.clear()

	# create princpled bsdf node
	bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
	bsdf.inputs['Base Color'].default_value = (0,0,0,1)
	bsdf.inputs['Metallic'].default_value = 0
	bsdf.inputs['Specular'].default_value = 0
	bsdf.inputs['Roughness'].default_value = 0
	bsdf.location = 0,0

	# create output node
	node_output = nodes.new(type='ShaderNodeOutputMaterial')
	node_output.location = 400, 0

	# link nodes
	links = mat.node_tree.links
	link = links.new(bsdf.outputs['BSDF'], node_output.inputs['Surface'])

	# clear material of object
	obj.data.materials.clear()
	# set material to object
	obj.data.materials.append(mat)

def addLouver(parent, verts, faces, obj_name = 'Louver', id = None):

	# create a new mirror from vertex data
	number = str(id) if not id == None else ''
	mesh = bpy.data.meshes.new('Louver'+number)
	mesh.from_pydata(verts, [], faces)

	# create object and change transformation
	louver = bpy.data.objects.new('Louver'+number, mesh)
	#louver.rotation_euler = (0, 0, math.pi / 4)

	# set parent
	louver.parent = parent
	# register mirror to scene
	bpy.context.collection.objects.link(louver)

	return louver
