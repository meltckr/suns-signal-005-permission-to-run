"""Issue 009 premium editorial sculpture, derived from build_signal_depth.py.

Original procedural geometry only. No real venue, trophy, chart or player likeness.
Render two art-directed stills; private PNG/.blend masters never belong in the site.
Example: blender -b --factory-startup --python scripts/blender/build_signal_premium.py
         -- --output /absolute/private/master/path --samples 96
"""
import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Euler, Vector

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
parser.add_argument('--samples', type=int, default=96)
parser.add_argument('--variant', choices=('desktop', 'mobile', 'both'), default='both')
args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
output = Path(args.output)
output.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)


def material(name, color, metal=0, rough=.4):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bs = mat.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (*color, 1)
    bs.inputs['Metallic'].default_value = metal
    bs.inputs['Roughness'].default_value = rough
    return mat


def grain(mat, scale, strength, distance, stretched=None):
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    coords = nodes.new('ShaderNodeTexCoord')
    source = coords.outputs['Object']
    if stretched:
        mapping = nodes.new('ShaderNodeVectorMath')
        mapping.operation = 'MULTIPLY'
        mapping.inputs[1].default_value = stretched
        links.new(source, mapping.inputs[0])
        source = mapping.outputs['Vector']
    noise = nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = scale
    noise.inputs['Detail'].default_value = 3
    links.new(source, noise.inputs['Vector'])
    bump = nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = strength
    bump.inputs['Distance'].default_value = distance
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], nodes.get('Principled BSDF').inputs['Normal'])


def box(name, location, dimensions, mat, bevel=.06):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    mod = obj.modifiers.new('Precision radiused edge', 'BEVEL')
    mod.width, mod.segments = bevel, 6
    obj.modifiers.new('Weighted surface normals', 'WEIGHTED_NORMAL')
    return obj


def curve(name, points, radius, mat):
    data = bpy.data.curves.new(name, 'CURVE')
    data.dimensions, data.bevel_depth, data.bevel_resolution = '3D', radius, 5
    spline = data.splines.new('POLY')
    spline.points.add(len(points) - 1)
    for point, co in zip(spline.points, points):
        point.co = (*co, 1)
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    data.materials.append(mat)
    return obj


def area(name, location, target, energy, color, size, size_y=None):
    data = bpy.data.lights.new(name, 'AREA')
    data.energy, data.color, data.size = energy, color, size
    data.shape = 'RECTANGLE' if size_y else 'DISK'
    if size_y:
        data.size_y = size_y
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()


bronze = material('Hand-brushed architectural bronze', (.33, .135, .058), .85, .34)
grain(bronze, 36, .16, .006, (1, 38, 2))
edge = material('Polished copper bevel', (.61, .27, .102), .87, .22)
grain(edge, 75, .07, .003, (1, 30, 1))
stone = material('Honed midnight basalt', (.018, .024, .036), .16, .4)
grain(stone, 83, .26, .013)
floor = material('Navy smoked glass stage', (.011, .018, .031), .26, .35)
grain(floor, 100, .1, .006)
rubber = material('Matte recessed channel rubber', (.006, .004, .003), 0, .8)
grain(rubber, 230, .18, .003)

leather = material('Warm full-grain basketball leather', (.29, .074, .018), 0, .59)
nodes, links = leather.node_tree.nodes, leather.node_tree.links
coords = nodes.new('ShaderNodeTexCoord')
pebbles = nodes.new('ShaderNodeTexVoronoi')
pebbles.inputs['Scale'].default_value = 90
pebbles.inputs['Randomness'].default_value = .84
links.new(coords.outputs['Object'], pebbles.inputs['Vector'])
height = nodes.new('ShaderNodeValToRGB')
height.color_ramp.interpolation = 'EASE'
height.color_ramp.elements[0].position = .08
height.color_ramp.elements[0].color = (.84, .84, .84, 1)
height.color_ramp.elements[1].position = .49
height.color_ramp.elements[1].color = (.04, .04, .04, 1)
links.new(pebbles.outputs['Distance'], height.inputs['Fac'])
bump = nodes.new('ShaderNodeBump')
bump.inputs['Strength'].default_value = .63
bump.inputs['Distance'].default_value = .012
links.new(height.outputs['Color'], bump.inputs['Height'])
links.new(bump.outputs['Normal'], nodes.get('Principled BSDF').inputs['Normal'])
tones = nodes.new('ShaderNodeValToRGB')
tones.color_ramp.elements[0].position = .15
tones.color_ramp.elements[0].color = (.33, .090, .021, 1)
tones.color_ramp.elements[1].position = .65
tones.color_ramp.elements[1].color = (.18, .040, .010, 1)
links.new(pebbles.outputs['Distance'], tones.inputs['Fac'])
links.new(tones.outputs['Color'], nodes.get('Principled BSDF').inputs['Base Color'])

inlay = material('Restrained amber light inlay', (.9, .31, .085), .35, .28)
bs = inlay.node_tree.nodes.get('Principled BSDF')
bs.inputs['Emission Color'].default_value = (1, .31, .09, 1)
bs.inputs['Emission Strength'].default_value = .8
box('Continuous navy stage', (0, 0, -.15), (200, 200, .25), floor)

# The three rising levels preserve the approved v1 visual metaphor.
for index in range(3):
    x, y, h = 1.4 + index * 1.15, .3 + index * .68, .46 + index * .64
    box('Basalt foundation %02d' % index, (x, y, h / 2), (2.35, 2.55, h), stone, .08)
    box('Polished copper lower lip %02d' % index, (x, y, h + .033), (2.41, 2.61, .075), edge, .034)
    box('Brushed bronze upper plate %02d' % index, (x, y, h + .092), (2.39, 2.59, .07), bronze, .026)
    box('Inset amber edge %02d' % index, (x, y - 1.306, h + .025), (2.19, .012, .009), inlay, .003)
    # Two narrow, machined horizontal score lines catch the light on the front fascia.
    for offset in (.11, .145):
        box('Copper engraved fascia %02d %.2f' % (index, offset),
            (x, y - 1.277, h - offset), (2.18, .005, .006), bronze, .002)

radius = .84
center = Vector((3.72, 1.71, 1.74 + .128 + radius))
bpy.ops.mesh.primitive_uv_sphere_add(segments=144, ring_count=96, radius=radius, location=center)
ball = bpy.context.object
ball.name = 'Pebbled leather basketball'
ball.data.materials.append(leather)
for polygon in ball.data.polygons:
    polygon.use_smooth = True

# Four slightly recessed channels define an eight-panel basketball.
# No logo or claimed official equipment is introduced.
rotation = Euler((.19, -.28, -.31), 'XYZ').to_matrix()
channel_radius = radius - .012
for index, tilt in enumerate((0, math.pi / 2)):
    channel_points = []
    axis = Euler((tilt, 0, 0), 'XYZ').to_matrix()
    for step in range(361):
        theta = math.tau * step / 360
        point = rotation @ axis @ Vector((channel_radius * math.cos(theta), channel_radius * math.sin(theta), 0))
        channel_points.append(center + point)
    curve('Recessed great-circle channel %d' % index, channel_points, .021, rubber)
for sign in (-1, 1):
    channel_points = []
    for step in range(361):
        theta = math.tau * step / 360
        px = sign * .56 * math.sin(theta)
        py = math.cos(theta)
        pz = math.sqrt(1 - .56 ** 2) * math.sin(theta)
        point = rotation @ Vector((px, py, pz)) * channel_radius
        channel_points.append(center + point)
    curve('Sweeping panel channel %d' % sign, channel_points, .020, rubber)

# Double-sided, physically thick sun arc. The warm inner rim is intentionally subtle.
for name, rr, depth, mat in (
    ('Brushed bronze solar arc', 3.3, .080, bronze),
    ('Polished front solar rim', 3.3, .023, edge),
    ('Warm inner solar rim', 3.19, .012, inlay),
):
    y = 3.75 if name == 'Polished front solar rim' else 3.81
    points = [(3.3 + rr * math.cos(math.radians(t)), y,
               .85 + rr * math.sin(math.radians(t))) for t in range(-15, 196)]
    curve(name, points, depth, mat)

area('Warm broad key', (1, -4, 8), (3, 1, 1.5), 1550, (1, .77, .54), 5.5)
area('Copper edge light', (7, 4, 6), (3, 1, 2), 1650, (1, .44, .18), 4.5)
area('Cool navy separation', (-3, 3, 5), (2, 1, 1), 900, (.25, .40, .80), 5.5)
area('Leather detail softbox', (4, -1, 9), (3.7, 1.7, 2.8), 850, (1, .91, .77), 3.3)
area('Tall camera-side reflection', (7, -4, 4), (3, 1, 1), 400, (1, .88, .72), 1.5, 5)

bpy.ops.object.camera_add(location=(10, -18, 10))
camera = bpy.context.object
camera.name = 'Art-directed editorial camera'
camera.data.type = 'ORTHO'
scene = bpy.context.scene
scene.camera = camera
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = args.samples
scene.cycles.use_denoising = True
scene.cycles.seed = 47
scene.render.threads_mode = 'FIXED'
scene.render.threads = 8
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (.038, .055, .085, 1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .18
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'AgX - Medium High Contrast'
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'
scene.render.resolution_percentage = 100

variants = ('desktop', 'mobile') if args.variant == 'both' else (args.variant,)
for variant in variants:
    if variant == 'desktop':
        target, location, scale, size = (1.0, .9, 1.85), (10, -18, 10), 13.2, (1920, 1200)
    else:
        target, location, scale, size = (3.0, 1.1, 1.95), (9, -18, 9), 7.8, (900, 1100)
    camera.location = location
    camera.rotation_euler = (Vector(target) - camera.location).to_track_quat('-Z', 'Y').to_euler()
    camera.data.ortho_scale = scale
    scene.render.resolution_x, scene.render.resolution_y = size
    name = 'signal-premium-v2-' + variant
    scene.render.filepath = str(output / (name + '.png'))
    bpy.ops.wm.save_as_mainfile(filepath=str(output / (name + '.blend')))
    bpy.ops.render.render(write_still=True)
