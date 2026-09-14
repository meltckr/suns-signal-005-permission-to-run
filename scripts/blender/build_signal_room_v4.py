"""V4 spatial-depth extension of the approved Suns Signal room scene.

Reuses the complete v3 construction, including the steps, ball, ring, court,
materials, and architectural walls, without executing its render loop. Adds
perspective, ceiling scale, distant glass depth, converging court cues, and
restrained atmosphere. Reference photography is never loaded or composited.
Private PNG/.blend masters stay outside the public site.
"""
import ast
import math
from pathlib import Path

import bpy
from mathutils import Vector


base_path = Path(__file__).with_name('build_signal_room.py')
tree = ast.parse(base_path.read_text(), filename=str(base_path))
assert isinstance(tree.body[-1], ast.For)
assert isinstance(tree.body[-1].target, ast.Name)
assert tree.body[-1].target.id == 'variant'
assert isinstance(tree.body[-2], ast.Assign)
assert tree.body[-2].targets[0].id == 'variants'
tree.body = tree.body[:-2]
exec(compile(tree, str(base_path), 'exec'), globals())


# Bring the smoked maple forward as a floor material while keeping it dark
# enough to support the live title treatment on the left side of the frame.
court_bs = court.node_tree.nodes.get('Principled BSDF')
court_bs.inputs['Roughness'].default_value = .31
if court_bs.inputs.get('Coat Weight'):
    court_bs.inputs['Coat Weight'].default_value = .18
if court_bs.inputs.get('Coat Roughness'):
    court_bs.inputs['Coat Roughness'].default_value = .26
for brick in (node for node in court.node_tree.nodes if node.bl_idname == 'ShaderNodeTexBrick'):
    brick.inputs['Scale'].default_value = .68
    brick.inputs['Brick Width'].default_value = 2.4
    brick.inputs['Row Height'].default_value = .12
    brick.inputs['Color1'].default_value = (.066, .041, .023, 1)
    brick.inputs['Color2'].default_value = (.028, .023, .021, 1)

# Long floor cues converge naturally under the perspective lens. They remain
# illustrative and deliberately incomplete rather than becoming a court plan.
for name, points, radius in (
    ('V4 long left court seam', [(-5.8, -18, -.018), (-5.8, 7.1, -.018)], .017),
    ('V4 long center court seam', [(7.9, -18, -.018), (7.9, 7.1, -.018)], .017),
    ('V4 far baseline', [(-5.8, 6.1, -.018), (9.8, 6.1, -.018)], .015),
):
    obj = curve(name, points, radius, line)
    obj.scale.z = .055
    obj.location.z = -.024


# The ceiling and soffits make the viewer feel contained inside a tall volume.
ceiling = material('V4 charcoal ceiling plane', (.010, .014, .022), .05, .76)
box('V4 high ceiling plane', (1.4, 1.9, 9.55), (30, 23, .36), ceiling, .03)
for index, y in enumerate((-1.8, 2.1, 5.8)):
    box('V4 ceiling beam %02d' % index, (1.4, y, 9.12), (27, .34, .62), trim, .035)

cove = material('V4 warm ceiling cove', (.44, .24, .12), .18, .32)
cove_bs = cove.node_tree.nodes.get('Principled BSDF')
cove_bs.inputs['Emission Color'].default_value = (1.0, .48, .19, 1)
cove_bs.inputs['Emission Strength'].default_value = 2.1
for index, y in enumerate((.25, 4.0)):
    box('V4 ceiling cove %02d' % index, (4.1, y, 8.77), (10.8, .055, .055), cove, .01)


# A dark glazed office band sits beyond the court. Interior light is deliberately
# soft and secondary; it supplies a far plane rather than another focal object.
glass = material('V4 smoked office glass', (.015, .035, .055), .12, .19)
glass_bs = glass.node_tree.nodes.get('Principled BSDF')
if glass_bs.inputs.get('Transmission Weight'):
    glass_bs.inputs['Transmission Weight'].default_value = .58
glass_bs.inputs['IOR'].default_value = 1.46
office_glow = material('V4 distant office glow', (.17, .10, .055), .02, .62)
office_bs = office_glow.node_tree.nodes.get('Principled BSDF')
office_bs.inputs['Emission Color'].default_value = (.78, .34, .12, 1)
office_bs.inputs['Emission Strength'].default_value = .42
box('V4 distant office glow plane', (8.0, 7.28, 5.25), (7.5, .035, 3.55), office_glow, .02)
for index, x in enumerate((5.0, 7.0, 9.0, 11.0)):
    box('V4 glazed office bay %02d' % index, (x, 7.04, 5.25), (1.82, .08, 3.45), glass, .025)
    box('V4 office mullion %02d' % index, (x + .96, 6.98, 5.25), (.075, .16, 3.62), trim, .012)
box('V4 office head', (8.0, 6.97, 7.02), (7.95, .18, .12), trim, .018)
box('V4 office sill', (8.0, 6.97, 3.48), (7.95, .18, .12), trim, .018)


# Restrained atmosphere catches the warm/cool split around the sculpture. The
# camera stays outside the volume so the title side does not become milky.
volume_mat = bpy.data.materials.new('V4 restrained room atmosphere')
volume_mat.use_nodes = True
volume_nodes = volume_mat.node_tree.nodes
volume_links = volume_mat.node_tree.links
for node in list(volume_nodes):
    volume_nodes.remove(node)
volume_output = volume_nodes.new('ShaderNodeOutputMaterial')
volume_scatter = volume_nodes.new('ShaderNodeVolumePrincipled')
volume_scatter.inputs['Density'].default_value = .0065
volume_scatter.inputs['Anisotropy'].default_value = .18
volume_scatter.inputs['Color'].default_value = (.35, .43, .56, 1)
volume_links.new(volume_scatter.outputs['Volume'], volume_output.inputs['Volume'])
bpy.ops.mesh.primitive_cube_add(size=1, location=(3.0, 3.0, 4.65))
atmosphere = bpy.context.object
atmosphere.name = 'V4 bounded atmospheric volume'
atmosphere.dimensions = (18, 13.5, 9.0)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
atmosphere.data.materials.append(volume_mat)


# Turn the broad wash into reflected room light and sharpen the warm/cool
# architecture. Existing sculpture lights remain in place.
bpy.data.lights['Warm perimeter floor reflection'].energy = 90
bpy.data.lights['Broad practice room ambient'].energy = 430
bpy.data.lights['Wall wash behind sculpture'].energy = 270
area('V4 warm high side key', (11.0, -2.0, 8.3), (3.2, 1.3, 2.1),
     1120, (1.0, .69, .42), 5.4, 2.7)
area('V4 cool window fill', (-6.0, -.5, 6.2), (2.0, 1.2, 2.0),
     760, (.31, .50, .88), 6.4, 4.0)
area('V4 office ambient', (8.0, 6.3, 7.7), (7.8, 4.3, 4.5),
     210, (1.0, .56, .31), 4.2, 1.2)


# Focus remains on the ball and upper platform. Perspective and shallow, gentle
# focus falloff make the far architecture establish scale without competing.
bpy.ops.object.empty_add(type='PLAIN_AXES', location=center)
focus = bpy.context.object
focus.name = 'V4 ball focus target'
camera.data.type = 'PERSP'
camera.data.lens = 38
camera.data.sensor_width = 36
camera.data.clip_start = .1
camera.data.clip_end = 250
camera.data.dof.use_dof = True
camera.data.dof.focus_object = focus
camera.data.dof.aperture_fstop = 5.6
camera.data.dof.aperture_blades = 8

scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .10
scene.cycles.samples = args.samples
scene.cycles.use_denoising = True
scene.cycles.seed = 47

variants = ('desktop', 'mobile') if args.variant == 'both' else (args.variant,)
for variant in variants:
    if variant == 'desktop':
        target = (-.65, 1.15, .45)
        location = (8.7, -19.0, 3.35)
        lens = 40
        shift_x = 0.0
        size = (1920, 1200)
    else:
        target = (1.55, 1.25, -.20)
        location = (8.0, -18.0, 3.85)
        lens = 46
        shift_x = 0.0
        size = (900, 1100)
    camera.location = location
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat('-Z', 'Y').to_euler()
    camera.data.lens = lens
    camera.data.shift_x = shift_x
    scene.render.resolution_x, scene.render.resolution_y = size
    name = 'signal-room-v4-' + variant
    scene.render.filepath = str(output / (name + '.png'))
    bpy.ops.wm.save_as_mainfile(filepath=str(output / (name + '.blend')))
    bpy.ops.render.render(write_still=True)
