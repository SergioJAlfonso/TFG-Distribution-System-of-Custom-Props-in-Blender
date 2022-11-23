import bpy
import gpu
from gpu_extras.batch import batch_for_shader


#Simple class for debugging visually 
#IMPORTANT: 
# Store DrawManager variable as global is needed 
# in order to call "stop_draw", otherwise it wont work
class DrawManager:

    coords = []
    shader = None
    batch = None
    handle = None
    def __init__(self):
        self.coords = [(0, 0, 0), (0, 0, 10)]
        self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch = batch_for_shader(self.shader, 'LINES', {"pos": self.coords})
    
    def set_coords(self, new_coords):
        self.coords = new_coords
        self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch = batch_for_shader(self.shader, 'LINES', {"pos": self.coords})

    def draw(self):
        self.shader.bind()
        self.shader.uniform_float("color", (1, 0, 0, 1))
        self.batch.draw(self.shader)

    def doDraw(self):
        self.handle = bpy.types.SpaceView3D.draw_handler_add(self.draw, (), 'WINDOW', 'POST_VIEW')
        
    def stopDraw(self):
        bpy.types.SpaceView3D.draw_handler_remove(self.handle, 'WINDOW')

