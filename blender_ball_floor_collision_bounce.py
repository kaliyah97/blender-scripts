import bpy
import random

# Set gravity
bpy.types.Scene.gravity=(0,0,-10)

## Create a new scene if there's no active scene
#if not bpy.context.scene:
#    bpy.context.scene = bpy.data.scenes.new("Scene")

# Change the default keyframe interpolation mode for rigid body properties
bpy.context.preferences.edit.keyframe_new_interpolation_type = 'CONSTANT'

# Verify and set the default interpolation mode for rigid body properties
bpy.context.scene.tool_settings.use_keyframe_insert_auto = False  # Disable automatic keyframe interpolation
bpy.context.scene.tool_settings.keyframe_type = 'KEYFRAME'  # Set the default keyframe type to 'Keyframe'

# Save preferences
bpy.context.preferences.use_preferences_save = True
 
# Clear existing objects
bpy.ops.object.select_all(action='SELECT')

# Name of the object to deselect
object_name_to_deselect = "Cube"  # Replace "Cube" with the name of the object you want to deselect

# Iterate through selected objects and deselect the one with the specified name
for obj in bpy.context.selected_objects:
    if obj.name == object_name_to_deselect:
        obj.select_set(False)
bpy.ops.object.delete()

# Add a floor (container)
#bpy.ops.mesh.primitive_plane_add(size=30, enter_editmode=False, location=(0, 0, 0))
#floor = bpy.context.object
floor = bpy.data.objects.get("Cube")  # Change "MyFloor" to the name of your existing object


# Add collision property to the floor (container)
bpy.context.view_layer.objects.active = floor
bpy.ops.rigidbody.object_add(type='PASSIVE') 
floor.rigid_body.collision_shape = 'MESH'  # Set collision shape to mesh

ball_number = 100
ball_locations = []

for i in range(ball_number):
    randint = random.randint(-10, 10)
    ball_locations.append((randint, randint, i * 5 + 20 + randint))

balls = []

for loc in ball_locations:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=random.uniform(1, 3), enter_editmode=False, location=loc)
    ball = bpy.context.object
    ball.name = f"Ball{len(balls) + 1}"  # Adjusted ball naming
    
    balls.append(ball)
    
    initial_velocity = (random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(5, 15))
    bpy.context.view_layer.objects.active = ball
    bpy.ops.rigidbody.object_add(type='ACTIVE')
    ball.rigid_body.mass = 1
    ball.rigid_body.restitution = 4
    ball.rigid_body.friction = 0
    bpy.ops.transform.translate(value=initial_velocity)

# Set the end frame to 250 explicitly 
bpy.context.scene.frame_end = 350 

# Start the animation
bpy.ops.screen.animation_play()
