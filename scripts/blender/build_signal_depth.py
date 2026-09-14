"""Original Suns Signal editorial sculpture. Blender 4.5 LTS, Cycles CPU.
No downloaded models, player likenesses, measured data or real venue depicted.
Master PNG/.blend stay outside the public site. WebP is the delivery asset.
"""
import bpy, math, argparse, sys
from pathlib import Path
from mathutils import Vector

p=argparse.ArgumentParser()
p.add_argument('--output',required=True)
p.add_argument('--samples',type=int,default=64)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)

def material(name,color,metal=0,rough=.4):
 m=bpy.data.materials.new(name);m.use_nodes=True
 n=m.node_tree.nodes;bs=n.get('Principled BSDF')
 bs.inputs['Base Color'].default_value=(*color,1)
 bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
 return m

def texture(m,scale,strength,distance):
 n=m.node_tree.nodes;l=m.node_tree.links
 noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=scale
 bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=strength;bump.inputs['Distance'].default_value=distance
 l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],n.get('Principled BSDF').inputs['Normal'])

def box(name,loc,size,mat,bevel=.07):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
 b=o.modifiers.new('Machined edge','BEVEL');b.width=bevel;b.segments=5
 o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return o

def curve(name,points,radius,mat):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=radius;c.bevel_resolution=4
 s=c.splines.new('POLY');s.points.add(len(points)-1)
 for v,co in zip(s.points,points):v.co=(*co,1)
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);c.materials.append(mat);return o

def light(name,loc,target,power,color,size):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.color=color;d.shape='DISK';d.size=size
 o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.location=loc
 o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()

bronze=material('Satin copper',(.48,.19,.065),.78,.29);texture(bronze,160,.13,.008)
stone=material('Basalt',(.018,.022,.032),.2,.38);texture(stone,95,.28,.025)
floor=material('Smoked obsidian stage',(.013,.016,.025),.35,.28);texture(floor,80,.1,.016)
leather=material('Basketball pebbled leather',(.35,.10,.027),0,.58);texture(leather,170,.65,.015)
rubber=material('Recessed black rubber',(.006,.007,.009),0,.76)
glow=material('Warm light inlay',(1,.26,.025),.25,.26)
bs=glow.node_tree.nodes.get('Principled BSDF');bs.inputs['Emission Color'].default_value=(1,.20,.015,1);bs.inputs['Emission Strength'].default_value=2.5
box('Continuous floor',(0,0,-.15),(200,200,.25),floor)
# Three physical levels: decorative metaphor for preparation, not a chart.
for i in range(3):
 x=1.4+i*1.15;y=.3+i*.68;h=.46+i*.64
 box('Basalt foundation '+str(i),(x,y,h/2),(2.35,2.55,h),stone,.09)
 box('Copper cap '+str(i),(x,y,h+.065),(2.42,2.60,.13),bronze,.045)
 box('Warm fine edge '+str(i),(x,y-1.305,h+.033),(2.21,.014,.018),glow,.004)
# Leather basketball gives the architecture scale and basketball context.
center=Vector((3.72,1.78,2.56));r=.67
bpy.ops.mesh.primitive_uv_sphere_add(segments=96,ring_count=64,radius=r,location=center)
ball=bpy.context.object;ball.name='Sculptural basketball';ball.data.materials.append(leather)
for f in ball.data.polygons:f.use_smooth=True
for rot in [(0,0,0),(math.pi/2,0,.25),(0,math.pi/2,.25)]:
 pts=[((r+.002)*math.cos(t*math.tau/180),(r+.002)*math.sin(t*math.tau/180),0) for t in range(181)]
 o=curve('Basketball channel',pts,.010,rubber);o.location=center;o.rotation_euler=rot
# A large bronze sun arc behind the steps, with actual thickness and shadows.
pts=[(3.3+3.3*math.cos(t*math.pi/180),3.8,.85+3.3*math.sin(t*math.pi/180)) for t in range(-15,196)]
curve('Copper architectural sun arc',pts,.09,bronze)
pts=[(3.3+3.18*math.cos(t*math.pi/180),3.81,.85+3.18*math.sin(t*math.pi/180)) for t in range(-15,196)]
curve('Warm inner sun arc',pts,.018,glow)
light('Large warm key',(1,-4,8),(3,1,1),1550,(1,.72,.43),7)
light('Copper rim',(7,4,6),(3,1,2),2100,(1,.34,.09),5)
light('Soft violet fill',(-3,3,5),(2,1,1),1100,(.34,.29,1),6)
light('Top softbox',(4,0,10),(3,1,0),1100,(1,.91,.78),5)
bpy.ops.object.camera_add(location=(10,-18,10))
cam=bpy.context.object;cam.name='Editorial perspective camera';target=Vector((.65,.9,1.7))
cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=13.5
bpy.context.scene.camera=cam
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=a.samples;s.cycles.use_denoising=True
s.cycles.seed=47;s.render.threads_mode='FIXED';s.render.threads=8
s.render.resolution_x=1600;s.render.resolution_y=1100;s.render.resolution_percentage=100
s.world.color=(.035,.035,.05);s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast'
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.filepath=str(out/'signal-depth-v1.png')
bpy.ops.wm.save_as_mainfile(filepath=str(out/'signal-depth-v1.blend'))
bpy.ops.render.render(write_still=True)
