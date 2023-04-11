
bl_info = {
	# required
	'name': 'Vertex Color Stylizer',
	'blender': (3, 2, 0),
	'category': 'Object',
	# optional
	'version': (1, 0, 0),
	'author': 'pixelbutterfly',
	'description': 'Add noise to or stylize objects vertex color.',
}

from random import random
import bpy
import colorsys
from collections import defaultdict

# == GLOBAL VARIABLES
PROPS = [
	('randomness_intensity', bpy.props.FloatProperty(name='strength', default=.2, min=0, max=10, soft_min = 0, soft_max = 1)),
	('replaceR', bpy.props.BoolProperty(name='R', default=True)),
	('replaceG', bpy.props.BoolProperty(name='G', default=True)),
	('replaceB', bpy.props.BoolProperty(name='B', default=True)),
	('replaceA', bpy.props.BoolProperty(name='A', default=False)),
]

PROPS2 = [
	('randomness_intensity2', bpy.props.FloatProperty(name='Strength', default=.2, min=0, max=10, soft_min = 0, soft_max = 1)),
	('replaceR2', bpy.props.BoolProperty(name='R', default=True)),
	('replaceG2', bpy.props.BoolProperty(name='G', default=True)),
	('replaceB2', bpy.props.BoolProperty(name='B', default=True)),
	('replaceA2', bpy.props.BoolProperty(name='A', default=False)),
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
		bpy.ops.object.mode_set(mode='OBJECT')
		for object in bpy.context.selected_objects:
				mesh = object.data
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
						
		return {'FINISHED'}
		
class RandomizeVertexColorsHard(bpy.types.Operator):
	
	bl_idname = 'opr.randomize_vertex_colors_hard'
	bl_label = 'Randomize Vertex Colors Hard'
	bl_options = {'REGISTER', "UNDO"}
	
	@classmethod
	def description(cls, context, properties):
		return "Randomize colors per face corner"
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='OBJECT')
		for object in bpy.context.selected_objects:
			mesh = object.data
			bpy.context.view_layer.objects.active = bpy.data.objects[object.name]
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

			
		return {'FINISHED'}
		
class HardenVertexColors(bpy.types.Operator):
	
	bl_idname = 'opr.harden_vertex_colors'
	bl_label = 'Harden Vertex Colors'
	bl_options = {'REGISTER', "UNDO"}

	@classmethod
	def description(cls, context, properties):
		return "Average vertex colors per face"
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='OBJECT')
		for object in bpy.context.selected_objects:
				object = bpy.context.view_layer.objects.active
				mesh = object.data
				vertex_colors = mesh.color_attributes.active_color
				if len(vertex_colors.data) != len(object.data.vertices):
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
						
		return {'FINISHED'}
		
class StylizeVertexColors(bpy.types.Operator):
	
	bl_idname = 'opr.stylize_vertex_colors'
	bl_label = 'Stylize Vertex Colors'
	bl_options = {'REGISTER', "UNDO"}
	
	@classmethod
	def description(cls, context, properties):
		return "Average vertex colors AND add random color variation"
	
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='OBJECT')
		for object in bpy.context.selected_objects:
				mesh = object.data
				vertex_colors = mesh.color_attributes.active_color
				domain_current = mesh.color_attributes.active_color.domain	##get whether the original domain is CORNER ot V
				
				
				if domain_current == 'CORNER':
				
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
					

		layout.label(text='Pixelbutterfly Tools')


# == MAIN ROUTINE
CLASSES = [
	RandomizeVertexColorsSoft,
	RandomizeVertexColorsHard,
	HardenVertexColors,
	StylizeVertexColors,

	VertexColorStylizerPanel
]

def register():
	for (prop_name, prop_value) in PROPS:
		setattr(bpy.types.Scene, prop_name, prop_value)
	for (prop_name, prop_value) in PROPS2:
		setattr(bpy.types.Scene, prop_name, prop_value)
		
	for klass in CLASSES:
		bpy.utils.register_class(klass)
		

def unregister():
	for (prop_name, _) in PROPS:
		delattr(bpy.types.Scene, prop_name)

	for klass in CLASSES:
		bpy.utils.unregister_class(klass)
		

if __name__ == '__main__':
	register()
