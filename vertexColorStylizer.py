
bl_info = {
	# required
	'name': 'Vertex Color Stylizer',
	'blender': (3, 2, 0),
	'category': 'Object',
	# optional
	'version': (1, 0, 0),
	'author': 'pixelbutterfly.com',
	'description': 'Modify objects vertex color.',
	'doc_url': 'https://github.com/pixelbutterfly/vertex_color_stylizer',
}

from random import random
import bpy
import colorsys
from collections import defaultdict

# == GLOBAL VARIABLES
PROPS = [
	('randomness_intensity', bpy.props.FloatProperty(name='strength', default=.1, min=0, max=10, soft_min = 0, soft_max = 1)),
	('replaceR', bpy.props.BoolProperty(name='R', default=True)),
	('replaceG', bpy.props.BoolProperty(name='G', default=True)),
	('replaceB', bpy.props.BoolProperty(name='B', default=True)),
	('replaceA', bpy.props.BoolProperty(name='A', default=False)),
]

PROPS2 = [
	('randomness_intensity2', bpy.props.FloatProperty(name='strength', default=.1, min=0, max=10, soft_min = 0, soft_max = 1)),
	('replaceR2', bpy.props.BoolProperty(name='R', default=True)),
	('replaceG2', bpy.props.BoolProperty(name='G', default=True)),
	('replaceB2', bpy.props.BoolProperty(name='B', default=True)),
	('replaceA2', bpy.props.BoolProperty(name='A', default=False)),
]

PROPS3 = [
	('replaceR3', bpy.props.BoolProperty(name='R', default=True)),
	('replaceG3', bpy.props.BoolProperty(name='G', default=True)),
	('replaceB3', bpy.props.BoolProperty(name='B', default=True)),
	('replaceA3', bpy.props.BoolProperty(name='A', default=False)),
]		
														
PROPS4 = [
	('tint_color', bpy.props.FloatVectorProperty(name='tint color',subtype='COLOR', default=(1.0,0.0,0.0,1.0),min=0.0,max=1.0,size=4,)),
	('tint_strength', bpy.props.FloatProperty(name='tint strength', default=.1, min=0, max=1, soft_min = 0, soft_max = 1)),
	('tint_mode', bpy.props.EnumProperty(
            #(identifier, name, description, icon, number)
    items = [('MUL','Multiply','','',0), 
             ('ADD','Add','','',1),
             ('SUB','Subtract','','',2),
             ('OVRL','Overlay','','',3),
			 ('MIX','Mix','','',4),],
    name = 'tint mode',
    default = 'MIX')),
]	
# == OPERATORS
class RandomizeVertexColorsSoft(bpy.types.Operator):
	
	bl_idname = 'opr.randomize_vertex_colors_soft'
	bl_label = 'Randomize Vertex Colors Soft'
	bl_options = {'REGISTER', "UNDO"}
	
	@classmethod
	def description(cls, context, properties):
		return "Randomize vertex colors per vertex"
	
	def execute(self, context):
		for object in bpy.context.selected_objects:
			if object.type == "MESH":
				if context.mode == 'EDIT_MESH':
					bpy.ops.object.mode_set(mode='OBJECT')
					bpy.context.view_layer.objects.active = object
					mesh = object.data
					if (len(mesh.color_attributes)==0):
						mesh.color_attributes.active = mesh.color_attributes.new(name="Col", type='BYTE_COLOR', domain='CORNER')
					vertex_colors = mesh.color_attributes.active_color
					polygons = object.data.polygons
					selected_verts = []
					for vert in mesh.vertices:
						if vert.select == True:
							selected_verts.append(vert)
					
					old_colors_list = []
					for vert in vertex_colors.data:	 ## store original vert colors
						old_color = [vert.color[0],vert.color[1],vert.color[2],vert.color[3]]
						old_colors_list.append(old_color)
					
					if vertex_colors.domain == 'CORNER':
						
						vertex_map = defaultdict(list)    ## store the corners that go wtih each vert
						for poly in polygons:
							for vert_index, loop_indexes in zip(poly.vertices, poly.loop_indices):
								vertex_map[vert_index].append(loop_indexes)
					
						for vert_index, loop_indexes in vertex_map.items():
							oldR = 0
							oldG = 0
							oldB = 0
							oldA = 0
							loopTotal = 0
							for loop_index in loop_indexes:
								oldR += vertex_colors.data[loop_index].color[0]
								oldG += vertex_colors.data[loop_index].color[1]
								oldB += vertex_colors.data[loop_index].color[2]
								oldA += vertex_colors.data[loop_index].color[3]
								loopTotal += 1
								
							convertedHSVvalue = colorsys.rgb_to_hsv(oldR/loopTotal,oldG/loopTotal,oldB/loopTotal)
							oldH = convertedHSVvalue[0]
							oldS = convertedHSVvalue[1]
							oldV = convertedHSVvalue[2]
							newH = oldH + (random()-.5)*(context.scene.randomness_intensity/1.6)
							newS = oldS + (random()-.5)*(context.scene.randomness_intensity/3.0)
							newV = oldV + (random()-.5)*(context.scene.randomness_intensity/5.0)
							newA = (oldA/loopTotal) + (random()-.5)*(context.scene.randomness_intensity/5.0)
							newColor = colorsys.hsv_to_rgb(newH, newS, newV)
							newColor = newColor + (newA,)
							
							if mesh.vertices[vert_index].select:
								for loop_index in loop_indexes:
									otherOldR = vertex_colors.data[loop_index].color[0]
									otherOldG = vertex_colors.data[loop_index].color[1]
									otherOldB = vertex_colors.data[loop_index].color[2]
									otherOldA = vertex_colors.data[loop_index].color[3]
									vertex_colors.data[loop_index].color = newColor
									if (context.scene.replaceR == False):
										vertex_colors.data[loop_index].color[0] = otherOldR;
									if (context.scene.replaceG == False):
										vertex_colors.data[loop_index].color[1] = otherOldG;
									if (context.scene.replaceB == False):
										vertex_colors.data[loop_index].color[2] = otherOldB;
									if (context.scene.replaceA == False):
										vertex_colors.data[loop_index].color[3] = otherOldA;
									
								
					if vertex_colors.domain == 'POINT':	
						for poly in mesh.polygons:
							originalColor = vert.color
							oldA = originalColor[3]				
							for selected_vert in selected_verts:
								for i, index in enumerate(poly.vertices):
									if selected_vert.index == index:
										loop_index = selected_vert.index
										originalColor = mesh.color_attributes.active_color.data[loop_index].color
										oldR = originalColor[0]
										oldG = originalColor[1]
										oldB = originalColor[2]
										oldA = originalColor[3]
										convertedHSVvalue = colorsys.rgb_to_hsv(originalColor[0],originalColor[1],originalColor[2])
										oldH = convertedHSVvalue[0]
										oldS = convertedHSVvalue[1]
										oldV = convertedHSVvalue[2]
										newH = oldH + (random()-.5)*(context.scene.randomness_intensity/1.6)
										newS = oldS + (random()-.5)*(context.scene.randomness_intensity/3.0)
										newV = oldV + (random()-.5)*(context.scene.randomness_intensity/5.0)
										newA = oldA + (random()-.5)*(context.scene.randomness_intensity/5.0)
										newColor = colorsys.hsv_to_rgb(newH, newS, newV)
										newColor = newColor + (newA,)
										mesh.color_attributes.active_color.data[loop_index].color = newColor
										
										if (context.scene.replaceR == False):
											mesh.color_attributes.active_color.data[loop_index].color[0] = oldR;
										if (context.scene.replaceG == False):
											mesh.color_attributes.active_color.data[loop_index].color[1] = oldG;
										if (context.scene.replaceB == False):
											mesh.color_attributes.active_color.data[loop_index].color[2] = oldB;
										if (context.scene.replaceA == False):
											mesh.color_attributes.active_color.data[loop_index].color[3] = oldA;
					
					bpy.ops.object.mode_set(mode='EDIT')
				else:
					bpy.context.view_layer.objects.active = object
					current_mode = bpy.context.object.mode
					bpy.ops.object.mode_set(mode='OBJECT')
					mesh = object.data
					if (len(mesh.color_attributes)==0):
						mesh.color_attributes.active = mesh.color_attributes.new(name="Col", type='BYTE_COLOR', domain='CORNER')
					vertex_colors = mesh.color_attributes.active_color
					domain_current = mesh.color_attributes.active_color.domain	##get whether the original domain is CORNER ot V
					polygons = object.data.polygons
					
					old_colors_list = []
					for vert in vertex_colors.data:	 ## store original vert colors
						old_color = [vert.color[0],vert.color[1],vert.color[2],vert.color[3]]
						old_colors_list.append(old_color)
					
					if domain_current == 'CORNER':	
						vertex_map = defaultdict(list)
						for poly in polygons:
							for vert_index, loop_indexes in zip(poly.vertices, poly.loop_indices):
								vertex_map[vert_index].append(loop_indexes)
						
						for vert_index, loop_indexes in vertex_map.items():
							oldR = 0
							oldG = 0
							oldB = 0
							oldA = 0
							loopTotal = 0
							for loop_index in loop_indexes:
								oldR += vertex_colors.data[loop_index].color[0]
								oldG += vertex_colors.data[loop_index].color[1]
								oldB += vertex_colors.data[loop_index].color[2]
								oldA += vertex_colors.data[loop_index].color[3]
								loopTotal += 1
								
							convertedHSVvalue = colorsys.rgb_to_hsv(oldR/loopTotal,oldG/loopTotal,oldB/loopTotal)
							oldH = convertedHSVvalue[0]
							oldS = convertedHSVvalue[1]
							oldV = convertedHSVvalue[2]
							newH = oldH + (random()-.5)*(context.scene.randomness_intensity/1.6)
							newS = oldS + (random()-.5)*(context.scene.randomness_intensity/3.0)
							newV = oldV + (random()-.5)*(context.scene.randomness_intensity/5.0)
							newA = (oldA/loopTotal) + (random()-.5)*(context.scene.randomness_intensity/5.0)
							newColor = colorsys.hsv_to_rgb(newH, newS, newV)
							newColor = newColor + (newA,)
							
							for loop_index in loop_indexes:
								vertex_colors.data[loop_index].color = newColor
								
					if domain_current == 'POINT':			
						for vert in vertex_colors.data:
							originalColor = vert.color
							oldA = originalColor[3]
							convertedHSVvalue = colorsys.rgb_to_hsv(originalColor[0],originalColor[1],originalColor[2])
							oldH = convertedHSVvalue[0]
							oldS = convertedHSVvalue[1]
							oldV = convertedHSVvalue[2]
							newH = oldH + (random()-.5)*(context.scene.randomness_intensity/1.6)
							newS = oldS + (random()-.5)*(context.scene.randomness_intensity/3.0)
							newV = oldV + (random()-.5)*(context.scene.randomness_intensity/5.0)
							newA = oldA + (random()-.5)*(context.scene.randomness_intensity/5.0)
							newColor = colorsys.hsv_to_rgb(newH, newS, newV)
							newColor = newColor + (newA,)
							vert.color = newColor
					
					for oldColor, vert in zip(old_colors_list,vertex_colors.data):		## revert if overrides are ticked
						if (context.scene.replaceR == False):
							vert.color[0] = oldColor[0];
						if (context.scene.replaceG == False):
							vert.color[1] = oldColor[1];
						if (context.scene.replaceB == False):
							vert.color[2] = oldColor[2];
						if (context.scene.replaceA == False):
							vert.color[3] = oldColor[3];
					bpy.ops.object.mode_set ( mode = current_mode )						
		return {'FINISHED'}
		
class RandomizeVertexColorsHard(bpy.types.Operator):
	
	bl_idname = 'opr.randomize_vertex_colors_hard'
	bl_label = 'Randomize Vertex Colors Hard'
	bl_options = {'REGISTER', "UNDO"}
	
	@classmethod
	def description(cls, context, properties):
		return "Randomize colors per face corner"
	
	def execute(self, context):
		for object in bpy.context.selected_objects:
			if object.type == "MESH":	
				if context.mode == 'EDIT_MESH':
					bpy.ops.object.mode_set(mode='OBJECT')
					bpy.context.view_layer.objects.active = object
					mesh = object.data
					if (len(mesh.color_attributes)==0):
						mesh.color_attributes.active = mesh.color_attributes.new(name="Col", type='BYTE_COLOR', domain='CORNER')
					vertex_colors = mesh.color_attributes.active_color	## get the color attribute of the currently selected mesh
					
					selected_polys = []
					for poly in mesh.polygons:
						if poly.select == True:
							selected_polys.append(poly)

					if vertex_colors.domain == 'CORNER':	
							
						for poly in selected_polys:
							for loop_index in (poly.loop_indices):
								originalColor = mesh.color_attributes.active_color.data[loop_index].color
								oldR = originalColor[0]
								oldG = originalColor[1]
								oldB = originalColor[2]
								oldA = originalColor[3]
								convertedHSVvalue = colorsys.rgb_to_hsv(originalColor[0],originalColor[1],originalColor[2])
								oldH = convertedHSVvalue[0]
								oldS = convertedHSVvalue[1]
								oldV = convertedHSVvalue[2]
								newH = oldH + (random()-.5)*(context.scene.randomness_intensity/1.6)
								newS = oldS + (random()-.5)*(context.scene.randomness_intensity/3.0)
								newV = oldV + (random()-.5)*(context.scene.randomness_intensity/5.0)
								newA = oldA + (random()-.5)*(context.scene.randomness_intensity/5.0) 
								newColor = colorsys.hsv_to_rgb(newH, newS, newV)
								newColor = newColor + (newA,)									
								mesh.color_attributes.active_color.data[loop_index].color = newColor
								
								if (context.scene.replaceR == False):
									mesh.color_attributes.active_color.data[loop_index].color[0] = oldR;
								if (context.scene.replaceG == False):
									mesh.color_attributes.active_color.data[loop_index].color[1] = oldG;
								if (context.scene.replaceB == False):
									mesh.color_attributes.active_color.data[loop_index].color[2] = oldB;
								if (context.scene.replaceA == False):
									mesh.color_attributes.active_color.data[loop_index].color[3] = oldA;
					else:
						self.report({"ERROR"}, "One or more selected object uses per-vertex colors. Convert to face corner and try again.")
					bpy.ops.object.mode_set(mode = 'EDIT')
				else:
					bpy.context.view_layer.objects.active = object
					current_mode = bpy.context.object.mode
					bpy.ops.object.mode_set(mode='OBJECT')
					mesh = object.data
					if (len(mesh.color_attributes)==0):
						mesh.color_attributes.active = mesh.color_attributes.new(name="Col", type='BYTE_COLOR', domain='CORNER')
					vertex_colors = mesh.color_attributes.active_color	## get the color attribute of the currently selected mesh

					if vertex_colors.domain == 'CORNER':
						for vert in vertex_colors.data:
							originalColor = vert.color
							oldR = originalColor[0]
							oldG = originalColor[1]
							oldB = originalColor[2]
							oldA = originalColor[3]
							convertedHSVvalue = colorsys.rgb_to_hsv(originalColor[0],originalColor[1],originalColor[2])
							oldH = convertedHSVvalue[0]
							oldS = convertedHSVvalue[1]
							oldV = convertedHSVvalue[2]
							newH = oldH + (random()-.5)*(context.scene.randomness_intensity/1.6)
							newS = oldS + (random()-.5)*(context.scene.randomness_intensity/3.0)
							newV = oldV + (random()-.5)*(context.scene.randomness_intensity/5.0)
							newA = oldA + (random()-.5)*(context.scene.randomness_intensity/5.0) 
							newColor = colorsys.hsv_to_rgb(newH, newS, newV)
							newColor = newColor + (newA,)
							vert.color = newColor
							if (context.scene.replaceR == False):
								vert.color[0] = oldR;
							if (context.scene.replaceG == False):
								vert.color[1] = oldG;
							if (context.scene.replaceB == False):
								vert.color[2] = oldB;
							if (context.scene.replaceA == False):
								vert.color[3] = oldA;
					else:
						self.report({"ERROR"}, "One or more selected object uses per-vertex colors. Convert to face corner and try again.")
					bpy.ops.object.mode_set ( mode = current_mode )	
		return {'FINISHED'}
		
class HardenVertexColors(bpy.types.Operator):
	
	bl_idname = 'opr.harden_vertex_colors'
	bl_label = 'Harden Vertex Colors'
	bl_options = {'REGISTER', "UNDO"}

	@classmethod
	def description(cls, context, properties):
		return "Average vertex colors per face"
	
	def execute(self, context):
		for object in bpy.context.selected_objects:
			if object.type == "MESH":	
				if context.mode == 'EDIT_MESH':
						bpy.ops.object.mode_set(mode='OBJECT')
						bpy.context.view_layer.objects.active = object
						mesh = object.data
						if (len(mesh.color_attributes)==0):
							mesh.color_attributes.active = mesh.color_attributes.new(name="Col", type='BYTE_COLOR', domain='CORNER')
						vertex_colors = mesh.color_attributes.active_color
						
						selected_polys = []
						for poly in mesh.polygons:
							if poly.select == True:
								selected_polys.append(poly)
								
						if vertex_colors.domain == 'CORNER':
							for poly in selected_polys:
								oldR = 0
								oldG = 0
								oldB = 0
								oldA = 0
								vertCount = 0
								newColor = [0,0,0,0];
								for loop_index in (poly.loop_indices):
									originalColor = mesh.color_attributes.active_color.data[loop_index].color
									oldA += originalColor[3]
									oldR += originalColor[0]
									oldG += originalColor[1]
									oldB += originalColor[2]
									vertCount += 1
								newColor = [(oldR/poly.loop_total),(oldG/poly.loop_total),(oldB/poly.loop_total),(oldA/poly.loop_total)]
								for loop_index in (poly.loop_indices):
									mesh.color_attributes.active_color.data[loop_index].color = newColor
						else:
							self.report({"ERROR"}, "One or more selected object uses per-vertex colors. Convert to face corner and try again.")
						bpy.ops.object.mode_set(mode='EDIT')
				else:
					bpy.context.view_layer.objects.active = object
					current_mode = bpy.context.object.mode
					bpy.ops.object.mode_set(mode='OBJECT')
					mesh = object.data
					if (len(mesh.color_attributes)==0):
						mesh.color_attributes.active = mesh.color_attributes.new(name="Col", type='BYTE_COLOR', domain='CORNER')
					vertex_colors = mesh.color_attributes.active_color
					if vertex_colors.domain == 'CORNER':
						for poly in mesh.polygons:
							oldR = 0
							oldG = 0
							oldB = 0
							oldA = 0
							vertCount = 0
							newColor = [0,0,0,0];
							for loop_index in (poly.loop_indices):
								originalColor = vertex_colors.data[loop_index].color
								oldA += originalColor[3]
								oldR += originalColor[0]
								oldG += originalColor[1]
								oldB += originalColor[2]
								vertCount += 1
							newColor = [(oldR/poly.loop_total),(oldG/poly.loop_total),(oldB/poly.loop_total),(oldA/poly.loop_total)]
							for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
								vertex_colors.data[loop_index].color = newColor
					else:
						self.report({"ERROR"}, "One or more selected object uses per-vertex colors. Convert to face corner and try again.")
					bpy.ops.object.mode_set ( mode = current_mode )
								
		return {'FINISHED'}
		
class StylizeVertexColors(bpy.types.Operator):
	
	bl_idname = 'opr.stylize_vertex_colors'
	bl_label = 'Stylize Vertex Colors'
	bl_options = {'REGISTER', "UNDO"}
	
	@classmethod
	def description(cls, context, properties):
		return "Average vertex colors AND add random color variation"
	
	
	def execute(self, context):

		for object in bpy.context.selected_objects:
			if object.type == "MESH":	
				if context.mode == 'EDIT_MESH':
					bpy.ops.object.mode_set(mode='OBJECT')
					bpy.context.view_layer.objects.active = object
					mesh = object.data
					if (len(mesh.color_attributes)==0):
						mesh.color_attributes.active = mesh.color_attributes.new(name="Col", type='BYTE_COLOR', domain='CORNER')
					vertex_colors = mesh.color_attributes.active_color
					
					selected_polys = []
					for poly in mesh.polygons:
						if poly.select == True:
							selected_polys.append(poly)
					
					if vertex_colors.domain == 'CORNER':
					
						for poly in selected_polys:
							oldR = 0
							oldG = 0
							oldB = 0
							oldA = 0
							for loop_index in (poly.loop_indices):
								oldR += vertex_colors.data[loop_index].color[0]
								oldG += vertex_colors.data[loop_index].color[1]
								oldB += vertex_colors.data[loop_index].color[2]
								oldA += vertex_colors.data[loop_index].color[3]
							newColor = [(oldR/poly.loop_total),(oldG/poly.loop_total),(oldB/poly.loop_total),(oldA/poly.loop_total)]
							convertedHSVvalue = colorsys.rgb_to_hsv(newColor[0],newColor[1],newColor[2])
							oldH = convertedHSVvalue[0]
							oldS = convertedHSVvalue[1]
							oldV = convertedHSVvalue[2]
							newH = oldH + (random()-.5)*(context.scene.randomness_intensity2/1.6)
							newS = oldS + (random()-.5)*(context.scene.randomness_intensity2/3.0)
							newV = oldV + (random()-.5)*(context.scene.randomness_intensity2/100.0)
							newA = (oldA/poly.loop_total) + (random()-.5)*(context.scene.randomness_intensity2/5.0)
							newColor = colorsys.hsv_to_rgb(newH, newS, newV)
							newColor = [newColor[0], newColor[1], newColor[2], newA]
							for loop_index in (poly.loop_indices):
								otherOldR = vertex_colors.data[loop_index].color[0]
								otherOldG = vertex_colors.data[loop_index].color[1]
								otherOldB = vertex_colors.data[loop_index].color[2]
								otherOldA = vertex_colors.data[loop_index].color[3]
								mesh.color_attributes.active_color.data[loop_index].color = newColor
								if (context.scene.replaceR2 == False):
									mesh.color_attributes.active_color.data[loop_index].color[0] = otherOldR;
								if (context.scene.replaceG2 == False):
									mesh.color_attributes.active_color.data[loop_index].color[1] = otherOldG;
								if (context.scene.replaceB2 == False):
									mesh.color_attributes.active_color.data[loop_index].color[2] = otherOldB;
								if (context.scene.replaceA2 == False):
									mesh.color_attributes.active_color.data[loop_index].color[3] = otherOldA;
							
					else:
						self.report({"ERROR"}, "One or more selected object uses per-vertex colors. Convert to face corner and try again.")
					bpy.ops.object.mode_set(mode='EDIT')
				else:
					bpy.context.view_layer.objects.active = object
					current_mode = bpy.context.object.mode
					bpy.ops.object.mode_set(mode='OBJECT')
					mesh = object.data
					if (len(mesh.color_attributes)==0):
						mesh.color_attributes.active = mesh.color_attributes.new(name="Col", type='BYTE_COLOR', domain='CORNER')
					vertex_colors = mesh.color_attributes.active_color
							
					if vertex_colors.domain == 'CORNER':
					
						old_colors_list = []
						for vert in vertex_colors.data:	 ## store original vert colors
							old_color = [vert.color[0],vert.color[1],vert.color[2],vert.color[3]]
							old_colors_list.append(old_color)
					
						for poly in (object.data.polygons):
							oldR = 0
							oldG = 0
							oldB = 0
							oldA = 0
							vertCount = 0
							for loop_index in (poly.loop_indices):
								originalColor = vertex_colors.data[loop_index].color
								oldR += originalColor[0]
								oldG += originalColor[1]
								oldB += originalColor[2]
								oldA += originalColor[3]
								vertCount += 1
							newColor = [(oldR/poly.loop_total),(oldG/poly.loop_total),(oldB/poly.loop_total),(oldA/poly.loop_total)]
							convertedHSVvalue = colorsys.rgb_to_hsv(newColor[0],newColor[1],newColor[2])
							oldH = convertedHSVvalue[0]
							oldS = convertedHSVvalue[1]
							oldV = convertedHSVvalue[2]
							newH = oldH + (random()-.5)*(context.scene.randomness_intensity2/1.6)
							newS = oldS + (random()-.5)*(context.scene.randomness_intensity2/3.0)
							newV = oldV + (random()-.5)*(context.scene.randomness_intensity2/5.0)
							newA = (oldA/poly.loop_total) + (random()-.5)*(context.scene.randomness_intensity2/5.0)
							newColor = colorsys.hsv_to_rgb(newH, newS, newV)
							newColor = [newColor[0], newColor[1], newColor[2], newA]
							for loop_index in (poly.loop_indices):			#store old vert colors
								vertex_colors.data[loop_index].color = newColor
									
						for oldColor, vert in zip(old_colors_list,vertex_colors.data):		## revert if overrides are ticked
							if (context.scene.replaceR2 == False):
								vert.color[0] = oldColor[0];
							if (context.scene.replaceG2 == False):
								vert.color[1] = oldColor[1];
							if (context.scene.replaceB2 == False):
								vert.color[2] = oldColor[2];
							if (context.scene.replaceA2 == False):
								vert.color[3] = oldColor[3];
							
					else:
						self.report({"ERROR"}, "One or more selected object uses per-vertex colors. Convert to face corner and try again.")
					bpy.ops.object.mode_set ( mode = current_mode )
				
		return {'FINISHED'}

class InvertVertexColors(bpy.types.Operator):
	
	bl_idname = 'opr.invert_vertex_colors'
	bl_label = 'Invert Vertex Colors'
	bl_options = {'REGISTER', "UNDO"}
	
	@classmethod
	def description(cls, context, properties):
		return "Invert vertex colors"
	
	def execute(self, context):
		for object in bpy.context.selected_objects:
			if object.type == "MESH":
				if context.mode == 'EDIT_MESH':
					bpy.ops.object.mode_set(mode='OBJECT')
					bpy.context.view_layer.objects.active = object
					mesh = object.data
					if (len(mesh.color_attributes)==0):
						self.report({"ERROR"}, "One or more selected object has no vertex colors.")
					else:
						vertex_colors = mesh.color_attributes.active_color
						selected_verts = []
						for vert in mesh.vertices:
							if vert.select == True:
								selected_verts.append(vert)
						
						if vertex_colors.domain == 'CORNER':
							for polygon in mesh.polygons:
								for selected_vert in selected_verts:
									for i, index in enumerate(polygon.vertices):
										if selected_vert.index == index:
											loop_index = polygon.loop_indices[i]
											if (context.scene.replaceR3 == True):
												mesh.color_attributes.active_color.data[loop_index].color[0] = 1-mesh.color_attributes.active_color.data[loop_index].color[0]
											if (context.scene.replaceG3 == True):
												mesh.color_attributes.active_color.data[loop_index].color[1] = 1-mesh.color_attributes.active_color.data[loop_index].color[1]
											if (context.scene.replaceB3 == True):
												mesh.color_attributes.active_color.data[loop_index].color[2] = 1-mesh.color_attributes.active_color.data[loop_index].color[2]
											if (context.scene.replaceA3 == True):
												mesh.color_attributes.active_color.data[loop_index].color[3] = 1-mesh.color_attributes.active_color.data[loop_index].color[3]
						if vertex_colors.domain == 'POINT':
							for selected_vert in selected_verts:
								loop_index = selected_vert.index
								if (context.scene.replaceR3 == True):
									mesh.color_attributes.active_color.data[loop_index].color[0] = 1-mesh.color_attributes.active_color.data[loop_index].color[0]
								if (context.scene.replaceG3 == True):
									mesh.color_attributes.active_color.data[loop_index].color[1] = 1-mesh.color_attributes.active_color.data[loop_index].color[1]
								if (context.scene.replaceB3 == True):
									mesh.color_attributes.active_color.data[loop_index].color[2] = 1-mesh.color_attributes.active_color.data[loop_index].color[2]
								if (context.scene.replaceA3 == True):
									mesh.color_attributes.active_color.data[loop_index].color[3] = 1-mesh.color_attributes.active_color.data[loop_index].color[3]
					bpy.ops.object.mode_set(mode='EDIT')
				else:
					bpy.context.view_layer.objects.active = object
					current_mode = bpy.context.object.mode
					bpy.ops.object.mode_set(mode='OBJECT')
					mesh = object.data
					if (len(mesh.color_attributes)==0):
						self.report({"ERROR"}, "One or more selected object has no vertex colors.")
					else:
						vertex_colors = mesh.color_attributes.active_color
							
						for vert in vertex_colors.data:	 ## store original vert colors
							if (context.scene.replaceR3 == True):
								vert.color[0] = 1-vert.color[0]
							if (context.scene.replaceG3 == True):
								vert.color[1] = 1-vert.color[1]
							if (context.scene.replaceB3 == True):
								vert.color[2] = 1-vert.color[2]
							if (context.scene.replaceA3 == True):
								vert.color[3] = 1-vert.color[3]
					bpy.ops.object.mode_set ( mode = current_mode )
		return {'FINISHED'}
				
class BlendVertexColors(bpy.types.Operator):
	
	bl_idname = 'opr.blend_vertex_colors'
	bl_label = 'Blend Vertex Colors'
	bl_options = {'REGISTER', "UNDO"}
	
	@classmethod
	def description(cls, context, properties):
		return "Blend vertex colors"
	
	
	def execute(self, context):
		for object in bpy.context.selected_objects:
			if object.type == "MESH":
				if context.mode == 'EDIT_MESH':
					bpy.ops.object.mode_set(mode='OBJECT')
					bpy.context.view_layer.objects.active = object
					mesh = object.data
					if (len(mesh.color_attributes)==0):
						mesh.color_attributes.active = mesh.color_attributes.new(name="Col", type='BYTE_COLOR', domain='CORNER')
					vertex_colors = mesh.color_attributes.active_color
					
					selected_polys = []
					for poly in mesh.polygons:
						if poly.select == True:
							selected_polys.append(poly)
					
					selected_verts = []
					for vert in mesh.vertices:
						if vert.select == True:
							selected_verts.append(vert)
					
					if vertex_colors.domain == 'CORNER':	
						for poly in selected_polys:
							for loop_index in (poly.loop_indices):
								if (context.scene.tint_mode == 'MUL'):
									vertex_colors.data[loop_index].color[0] = ((vertex_colors.data[loop_index].color[0]*context.scene.tint_color[0])*context.scene.tint_color[3])+(vertex_colors.data[loop_index].color[0]*(1-context.scene.tint_color[3]))
									vertex_colors.data[loop_index].color[1] = ((vertex_colors.data[loop_index].color[1]*context.scene.tint_color[1])*context.scene.tint_color[3])+(vertex_colors.data[loop_index].color[1]*(1-context.scene.tint_color[3]))
									vertex_colors.data[loop_index].color[2] = ((vertex_colors.data[loop_index].color[2]*context.scene.tint_color[2])*context.scene.tint_color[3])+(vertex_colors.data[loop_index].color[2]*(1-context.scene.tint_color[3]))
								elif (context.scene.tint_mode == 'ADD'):
									vertex_colors.data[loop_index].color[0] = vertex_colors.data[loop_index].color[0]+(context.scene.tint_color[0]*context.scene.tint_color[3])
									vertex_colors.data[loop_index].color[1] = vertex_colors.data[loop_index].color[1]+(context.scene.tint_color[1]*context.scene.tint_color[3])
									vertex_colors.data[loop_index].color[2] = vertex_colors.data[loop_index].color[2]+(context.scene.tint_color[2]*context.scene.tint_color[3])
								elif (context.scene.tint_mode == 'SUB'):
									vertex_colors.data[loop_index].color[0] = vertex_colors.data[loop_index].color[0]-(context.scene.tint_color[0]*context.scene.tint_color[3])
									vertex_colors.data[loop_index].color[1] = vertex_colors.data[loop_index].color[1]-(context.scene.tint_color[1]*context.scene.tint_color[3])
									vertex_colors.data[loop_index].color[2] = vertex_colors.data[loop_index].color[2]-(context.scene.tint_color[2]*context.scene.tint_color[3])
								elif (context.scene.tint_mode == 'OVRL'):
									if (vertex_colors.data[loop_index].color[0]<.5):
										vertex_colors.data[loop_index].color[0] = (2*vertex_colors.data[loop_index].color[0]*(context.scene.tint_color[0])*context.scene.tint_color[3])+((1-context.scene.tint_color[3])*vertex_colors.data[loop_index].color[0])
									else:
										vertex_colors.data[loop_index].color[0] = (1-(2*(1-vertex_colors.data[loop_index].color[0])*(1-(context.scene.tint_color[0]))*context.scene.tint_color[3]))+(1-(context.scene.tint_color[3])*vertex_colors.data[loop_index].color[0])
									if (vertex_colors.data[loop_index].color[1]<.5):
										vertex_colors.data[loop_index].color[1] = (2*vertex_colors.data[loop_index].color[1]*(context.scene.tint_color[1])*context.scene.tint_color[3])+((1-context.scene.tint_color[3])*vertex_colors.data[loop_index].color[1])
									else:
										vertex_colors.data[loop_index].color[1] = (1-(2*(1-vertex_colors.data[loop_index].color[1])*(1-(context.scene.tint_color[1]))*context.scene.tint_color[3]))+((1-context.scene.tint_color[3])*vertex_colors.data[loop_index].color[1])
									if (vertex_colors.data[loop_index].color[2]<.5):
										vertex_colors.data[loop_index].color[2] = (2*vertex_colors.data[loop_index].color[2]*(context.scene.tint_color[2])*context.scene.tint_color[3])+((1-context.scene.tint_color[3])*vertex_colors.data[loop_index].color[2])
									else:
										vertex_colors.data[loop_index].color[2] = (1-(2*(1-vertex_colors.data[loop_index].color[2])*(1-(context.scene.tint_color[2]))*context.scene.tint_color[3]))+((1-context.scene.tint_color[3])*vertex_colors.data[loop_index].color[2])
								elif (context.scene.tint_mode == 'MIX'):
									vertex_colors.data[loop_index].color[0] = (vertex_colors.data[loop_index].color[0]*(1-context.scene.tint_color[3])+context.scene.tint_color[0]*context.scene.tint_color[3])
									vertex_colors.data[loop_index].color[1] = (vertex_colors.data[loop_index].color[1]*(1-context.scene.tint_color[3])+context.scene.tint_color[1]*context.scene.tint_color[3])
									vertex_colors.data[loop_index].color[2] = (vertex_colors.data[loop_index].color[2]*(1-context.scene.tint_color[3])+context.scene.tint_color[2]*context.scene.tint_color[3])
									
					if vertex_colors.domain == 'POINT':
						for selected_vert in selected_verts:
							loop_index = selected_vert.index
							if (context.scene.tint_mode == 'MUL'):
								vertex_colors.data[loop_index].color[0] = ((vertex_colors.data[loop_index].color[0]*context.scene.tint_color[0])*context.scene.tint_color[3])+(vertex_colors.data[loop_index].color[0]*(1-context.scene.tint_color[3]))
								vertex_colors.data[loop_index].color[1] = ((vertex_colors.data[loop_index].color[1]*context.scene.tint_color[1])*context.scene.tint_color[3])+(vertex_colors.data[loop_index].color[1]*(1-context.scene.tint_color[3]))
								vertex_colors.data[loop_index].color[2] = ((vertex_colors.data[loop_index].color[2]*context.scene.tint_color[2])*context.scene.tint_color[3])+(vertex_colors.data[loop_index].color[2]*(1-context.scene.tint_color[3]))
							elif (context.scene.tint_mode == 'ADD'):
								vertex_colors.data[loop_index].color[0] = vertex_colors.data[loop_index].color[0]+(context.scene.tint_color[0]*context.scene.tint_color[3])
								vertex_colors.data[loop_index].color[1] = vertex_colors.data[loop_index].color[1]+(context.scene.tint_color[1]*context.scene.tint_color[3])
								vertex_colors.data[loop_index].color[2] = vertex_colors.data[loop_index].color[2]+(context.scene.tint_color[2]*context.scene.tint_color[3])
							elif (context.scene.tint_mode == 'SUB'):
								vertex_colors.data[loop_index].color[0] = vertex_colors.data[loop_index].color[0]-(context.scene.tint_color[0]*context.scene.tint_color[3])
								vertex_colors.data[loop_index].color[1] = vertex_colors.data[loop_index].color[1]-(context.scene.tint_color[1]*context.scene.tint_color[3])
								vertex_colors.data[loop_index].color[2] = vertex_colors.data[loop_index].color[2]-(context.scene.tint_color[2]*context.scene.tint_color[3])
							elif (context.scene.tint_mode == 'OVRL'):
								if (vertex_colors.data[loop_index].color[0]<.5):
									vertex_colors.data[loop_index].color[0] = (2*vertex_colors.data[loop_index].color[0]*(context.scene.tint_color[0])*context.scene.tint_color[3])+((1-context.scene.tint_color[3])*vertex_colors.data[loop_index].color[0])
								else:
									vertex_colors.data[loop_index].color[0] = (1-(2*(1-vertex_colors.data[loop_index].color[0])*(1-(context.scene.tint_color[0]))*context.scene.tint_color[3]))+(1-(context.scene.tint_color[3])*vertex_colors.data[loop_index].color[0])
								if (vertex_colors.data[loop_index].color[1]<.5):
									vertex_colors.data[loop_index].color[1] = (2*vertex_colors.data[loop_index].color[1]*(context.scene.tint_color[1])*context.scene.tint_color[3])+((1-context.scene.tint_color[3])*vertex_colors.data[loop_index].color[1])
								else:
									vertex_colors.data[loop_index].color[1] = (1-(2*(1-vertex_colors.data[loop_index].color[1])*(1-(context.scene.tint_color[1]))*context.scene.tint_color[3]))+((1-context.scene.tint_color[3])*vertex_colors.data[loop_index].color[1])
								if (vertex_colors.data[loop_index].color[2]<.5):
									vertex_colors.data[loop_index].color[2] = (2*vertex_colors.data[loop_index].color[2]*(context.scene.tint_color[2])*context.scene.tint_color[3])+((1-context.scene.tint_color[3])*vertex_colors.data[loop_index].color[2])
								else:
									vertex_colors.data[loop_index].color[2] = (1-(2*(1-vertex_colors.data[loop_index].color[2])*(1-(context.scene.tint_color[2]))*context.scene.tint_color[3]))+((1-context.scene.tint_color[3])*vertex_colors.data[loop_index].color[2])
							elif (context.scene.tint_mode == 'MIX'):
								vertex_colors.data[loop_index].color[0] = (vertex_colors.data[loop_index].color[0]*(1-context.scene.tint_color[3])+context.scene.tint_color[0]*context.scene.tint_color[3])
								vertex_colors.data[loop_index].color[1] = (vertex_colors.data[loop_index].color[1]*(1-context.scene.tint_color[3])+context.scene.tint_color[1]*context.scene.tint_color[3])
								vertex_colors.data[loop_index].color[2] = (vertex_colors.data[loop_index].color[2]*(1-context.scene.tint_color[3])+context.scene.tint_color[2]*context.scene.tint_color[3])

					bpy.ops.object.mode_set(mode='EDIT')
				else:
					bpy.context.view_layer.objects.active = object
					current_mode = bpy.context.object.mode
					bpy.ops.object.mode_set(mode='OBJECT')
					mesh = object.data
					if (len(mesh.color_attributes)==0):
						self.report({"ERROR"}, "One or more selected object has no vertex colors.")
					else:
						vertex_colors = mesh.color_attributes.active_color
							
						for vert in vertex_colors.data:	 ## store original vert colors
							if (context.scene.tint_mode == 'MUL'):
								vert.color[0] = ((vert.color[0]*context.scene.tint_color[0])*context.scene.tint_color[3])+(vert.color[0]*(1-context.scene.tint_color[3]))
								vert.color[1] = ((vert.color[1]*context.scene.tint_color[1])*context.scene.tint_color[3])+(vert.color[1]*(1-context.scene.tint_color[3]))
								vert.color[2] = ((vert.color[2]*context.scene.tint_color[2])*context.scene.tint_color[3])+(vert.color[2]*(1-context.scene.tint_color[3]))
							elif (context.scene.tint_mode == 'ADD'):
								vert.color[0] = vert.color[0]+(context.scene.tint_color[0]*context.scene.tint_color[3])
								vert.color[1] = vert.color[1]+(context.scene.tint_color[1]*context.scene.tint_color[3])
								vert.color[2] = vert.color[2]+(context.scene.tint_color[2]*context.scene.tint_color[3])
							elif (context.scene.tint_mode == 'SUB'):
								vert.color[0] = vert.color[0]-(context.scene.tint_color[0]*context.scene.tint_color[3])
								vert.color[1] = vert.color[1]-(context.scene.tint_color[1]*context.scene.tint_color[3])
								vert.color[2] = vert.color[2]-(context.scene.tint_color[2]*context.scene.tint_color[3])
							elif (context.scene.tint_mode == 'OVRL'):
								if (vert.color[0]<.5):
									vert.color[0] = (2*vert.color[0]*(context.scene.tint_color[0])*context.scene.tint_color[3])+((1-context.scene.tint_color[3])*vert.color[0])
								else:
									vert.color[0] = (1-(2*(1-vert.color[0])*(1-(context.scene.tint_color[0]))*context.scene.tint_color[3]))+(1-(context.scene.tint_color[3])*vert.color[0])
								if (vert.color[1]<.5):
									vert.color[1] = (2*vert.color[1]*(context.scene.tint_color[1])*context.scene.tint_color[3])+((1-context.scene.tint_color[3])*vert.color[1])
								else:
									vert.color[1] = (1-(2*(1-vert.color[1])*(1-(context.scene.tint_color[1]))*context.scene.tint_color[3]))+((1-context.scene.tint_color[3])*vert.color[1])
								if (vert.color[2]<.5):
									vert.color[2] = (2*vert.color[2]*(context.scene.tint_color[2])*context.scene.tint_color[3])+((1-context.scene.tint_color[3])*vert.color[2])
								else:
									vert.color[2] = (1-(2*(1-vert.color[2])*(1-(context.scene.tint_color[2]))*context.scene.tint_color[3]))+((1-context.scene.tint_color[3])*vert.color[2])
							elif (context.scene.tint_mode == 'MIX'):
								vert.color[0] = (vert.color[0]*(1-context.scene.tint_color[3])+context.scene.tint_color[0]*context.scene.tint_color[3])
								vert.color[1] = (vert.color[1]*(1-context.scene.tint_color[3])+context.scene.tint_color[1]*context.scene.tint_color[3])
								vert.color[2] = (vert.color[2]*(1-context.scene.tint_color[3])+context.scene.tint_color[2]*context.scene.tint_color[3])

					bpy.ops.object.mode_set ( mode = current_mode )
					
		return {'FINISHED'}		
# == PANELS
class VertexColorStylizerPanel(bpy.types.Panel):
	
	bl_idname = 'VIEW3D_PT_vertex_color_stylizer'
	bl_label = 'Vertex Color Stylizer'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = "Vert Color Stylizer"

	def draw(self, context):
		layout = self.layout
		scene = context.scene	   
		row = layout.row()
		col = layout.column(align=True)
		
		vis_box = layout.box()
		vis_box2 = layout.box()
		vis_box3 = layout.box()
		vis_box4 = layout.box()
		vis_box5 = layout.box()
		
		vis_box_row = vis_box.row()
		vis_box3_row = vis_box3.row()
		
		
		vis_box.operator('opr.randomize_vertex_colors_soft', text='Randomize Vertex Colors (soft)')
		vis_box.operator('opr.randomize_vertex_colors_hard', text='Randomize Vertex Colors (hard)')
		## dislay the user input properties
		
		row = vis_box.row()
		row.prop(context.scene, 'replaceR')
		row.prop(context.scene, 'replaceG')
		row.prop(context.scene, 'replaceB')
		row.prop(context.scene, 'replaceA')
		row = vis_box.row()
		row.prop(context.scene, 'randomness_intensity')
		
		vis_box.label(text='adds noise to vert color')
		
		vis_box2.operator('opr.harden_vertex_colors', text='Harden Vertex Colors')
		vis_box2.label(text='averages vert colors per face')
		
		vis_box3.operator('opr.stylize_vertex_colors', text='Stylize Vertex Colors')
		row = vis_box3.row()
		row.prop(context.scene, 'replaceR2')
		row.prop(context.scene, 'replaceG2')
		row.prop(context.scene, 'replaceB2')
		row.prop(context.scene, 'replaceA2')
		row = vis_box3.row()
		row.prop(context.scene, 'randomness_intensity2')
		vis_box3.label(text='averages vert colors AND adds noise')
		
		vis_box4.operator('opr.invert_vertex_colors', text='Invert Vertex Colors')
		row = vis_box4.row()
		row.prop(context.scene, 'replaceR3')
		row.prop(context.scene, 'replaceG3')
		row.prop(context.scene, 'replaceB3')
		row.prop(context.scene, 'replaceA3')
		row = vis_box4.row()
		
		vis_box5.operator('opr.blend_vertex_colors', text='Blend Vertex Colors')
		row = vis_box5.row()
		row.prop(context.scene, 'tint_color')
		row.prop(context.scene, 'tint_mode')
		row = vis_box5.row()			

		layout.label(text='Pixelbutterfly Tools')

class PanelPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__

	# Addon Preferences https://docs.blender.org/api/blender_python_api_2_67_release/bpy.types.AddonPreferences.html

	def draw(self, context):
		layout = self.layout

		box = layout.box()

		box.label(text="Additional Links")
		col = box.column(align=True)
		col.operator("wm.url_open", text="Developer Website", icon='WORDWRAP_ON').url = "https://www.pixelbutterfly.com"
		

# == MAIN ROUTINE
CLASSES = [
	RandomizeVertexColorsSoft,
	RandomizeVertexColorsHard,
	HardenVertexColors,
	StylizeVertexColors,
	InvertVertexColors,
	BlendVertexColors,
	VertexColorStylizerPanel,
	PanelPreferences
]

def register():
	for (prop_name, prop_value) in PROPS:
		setattr(bpy.types.Scene, prop_name, prop_value)
	for (prop_name, prop_value) in PROPS2:
		setattr(bpy.types.Scene, prop_name, prop_value)
	for (prop_name, prop_value) in PROPS3:
		setattr(bpy.types.Scene, prop_name, prop_value)
	for (prop_name, prop_value) in PROPS4:
		setattr(bpy.types.Scene, prop_name, prop_value)
	for klass in CLASSES:
		bpy.utils.register_class(klass)
		

def unregister():
	for (prop_name, _) in PROPS:
		delattr(bpy.types.Scene, prop_name)
	for (prop_name, _) in PROPS2:
		delattr(bpy.types.Scene, prop_name)
	for (prop_name, _) in PROPS3:
		delattr(bpy.types.Scene, prop_name)
	for (prop_name, _) in PROPS4:
		delattr(bpy.types.Scene, prop_name)

	for klass in CLASSES:
		bpy.utils.unregister_class(klass)
		

if __name__ == '__main__':
	register()
