"""V3 procedural room extension of the approved v2 Suns Signal sculpture.

Reuses the complete v2 scene construction and its materials, without its output
loop. Adds a fictional architectural practice-room setting. No photography,
external textures, licensed venue design, signage, or real-facility claim.
Private PNG/.blend masters stay outside the public site.
"""
import ast
from pathlib import Path

base_path = Path(__file__).with_name('build_signal_premium.py')
tree = ast.parse(base_path.read_text(), filename=str(base_path))
# V2 deliberately ends with the variant assignment and render loop. Verify that
# contract rather than executing its output stage or mutating the v2 source.
assert isinstance(tree.body[-1], ast.For)
assert isinstance(tree.body[-1].target, ast.Name)
assert tree.body[-1].target.id == 'variant'
assert isinstance(tree.body[-2], ast.Assign)
assert tree.body[-2].targets[0].id == 'variants'
tree.body = tree.body[:-2]
exec(compile(tree, str(base_path), 'exec'), globals())

# Subdued hardwood grain and plank joints remain procedural shader detail.
court = material('Smoked maple practice court', (.045, .035, .025), .06, .40)
nodes, links = court.node_tree.nodes, court.node_tree.links
coord = nodes.new('ShaderNodeTexCoord')
mapping = nodes.new('ShaderNodeVectorMath')
mapping.operation = 'MULTIPLY'
mapping.inputs[1].default_value = (1, 1, 1)
links.new(coord.outputs['Object'], mapping.inputs[0])
planks = nodes.new('ShaderNodeTexBrick')
planks.offset = .55
planks.offset_frequency = 2
planks.inputs['Scale'].default_value = .5
planks.inputs['Mortar Size'].default_value = .0035
planks.inputs['Mortar Smooth'].default_value = .001
planks.inputs['Brick Width'].default_value = 1.8
planks.inputs['Row Height'].default_value = .16
planks.inputs['Color1'].default_value = (.048, .036, .024, 1)
planks.inputs['Color2'].default_value = (.023, .024, .026, 1)
planks.inputs['Mortar'].default_value = (.009, .010, .013, 1)
links.new(mapping.outputs['Vector'], planks.inputs['Vector'])
links.new(planks.outputs['Color'], nodes.get('Principled BSDF').inputs['Base Color'])
grain(court, 22, .15, .004, (.16, 8, 3))
bpy.data.objects['Continuous navy stage'].data.materials.clear()
bpy.data.objects['Continuous navy stage'].data.materials.append(court)
bpy.data.objects['Continuous navy stage'].name = 'Continuous smoked maple court'

# Court markings are an illustrative basketball cue, not measured game data.
line = material('Muted warm court markings', (.15, .145, .125), .03, .50)
curve('Illustrative practice-court arc',
      [(3.2 + 5.4 * math.cos(math.radians(t)),
        2.2 + 5.4 * math.sin(math.radians(t)), -.018)
       for t in range(-160, 161)], .022, line)
curve('Illustrative court outer line',
      [(-.2, 5.7, -.018), (8.9, 5.7, -.018), (8.9, -5.9, -.018)], .021, line)
curve('Illustrative practice lane',
      [(1.1, 5.7, -.018), (1.1, -.2, -.018),
       (5.5, -.2, -.018), (5.5, 5.7, -.018)], .016, line)
for obj in bpy.context.scene.objects:
    if obj.name.startswith('Illustrative '):
        # Flatten the cross-section into paint-level floor markings.
        obj.scale.z = .06
        obj.location.z = -.0239

# Actual wall thickness, recesses, and restrained light establish a room.
wall = material('Deep navy acoustic plaster', (.017, .025, .040), .05, .68)
grain(wall, 65, .16, .008)
recess = material('Shadowed acoustic recess', (.009, .014, .025), .03, .76)
trim = material('Blue-black architectural frame', (.022, .031, .046), .42, .35)
box('Back architectural wall', (0, 7.7, 4.8), (60, .5, 9.7), wall, .025)
for index, x in enumerate((-7, -2.6, 1.8, 6.2, 10.6)):
    box('Recessed acoustic bay %02d' % index, (x, 7.405, 4.0), (4.12, .10, 6.8), recess, .045)
    box('Vertical wall return %02d' % index, (x + 2.13, 7.31, 4.1), (.15, .31, 8.2), trim, .028)
    box('Low recessed wall reveal %02d' % index, (x, 7.29, .50), (4.1, .13, .065), bronze, .02)
box('Right room return', (10.7, 2.25, 4.8), (.5, 11.2, 9.7), wall, .03)
box('Right room shadow recess', (10.41, 1.9, 4.1), (.12, 10.1, 6.8), recess, .03)
box('Upper room shadow beam', (1.0, 6.90, 8.4), (26, 1.45, .5), trim, .05)

diffuser = material('Soft warm overhead diffuser', (.55, .58, .61), .1, .4)
bs = diffuser.node_tree.nodes.get('Principled BSDF')
bs.inputs['Emission Color'].default_value = (.77, .85, 1, 1)
bs.inputs['Emission Strength'].default_value = 1.6
for index, x in enumerate((1.5, 5.3, 9.1)):
    box('Recessed ceiling diffuser %02d' % index, (x, 6.92, 7.55), (2.65, .14, .055), diffuser, .016)

area('Broad practice room ambient', (3.8, 5.8, 7.5), (3.5, 1.5, .2),
     550, (.62, .75, 1), 5.5, 3.0)
area('Wall wash behind sculpture', (5.5, 4.6, 5.9), (4.5, 7.5, 3.4),
     380, (.58, .70, .94), 5.0)
area('Warm perimeter floor reflection', (8.8, 4.9, 3.3), (5, 1, .1),
     170, (1, .73, .49), 4.0)

variants = ('desktop', 'mobile') if args.variant == 'both' else (args.variant,)
for variant in variants:
    if variant == 'desktop':
        # Keep the full sculpture in the upper-right portion of a shallow hub.
        # Translate target and camera together to preserve the original angle.
        target, location, scale, size = (-.6, .9, -1.15), (8.4, -18, 7), 17.2, (1920, 1200)
    else:
        target, location, scale, size = (1.5, 1.1, 0), (7.5, -18, 7), 11.6, (900, 1100)
    camera.location = location
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat('-Z', 'Y').to_euler()
    camera.data.ortho_scale = scale
    scene.render.resolution_x, scene.render.resolution_y = size
    name = 'signal-room-v3-' + variant
    scene.render.filepath = str(output / (name + '.png'))
    bpy.ops.wm.save_as_mainfile(filepath=str(output / (name + '.blend')))
    bpy.ops.render.render(write_still=True)
