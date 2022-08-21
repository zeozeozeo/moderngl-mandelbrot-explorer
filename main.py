import moderngl_window as mglw
MAX_ITERATIONS = 128+1
INSTANT = False

def interpolation(start, stop, step):
    if step == 1:
        return [start]
    return [start+(stop-start)/(step-1)*i for i in range(step)]

class App(mglw.WindowConfig):
    window_size = 1280, 720
    resource_dir = 'programs'
    gl_version = (4, 3)
    title = 'OpenGL'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_zoom = 0
        self.zoom = 1.2
        self.max_iter = 1
        self.camera_pos = (0, 0)
        self.wasd_down = {key: False for key in 'wasd'}
        
        self.quad_fs = mglw.geometry.quad_fs()
        self.program = self.load_program(vertex_shader='vertex.glsl', fragment_shader='fragment.glsl')
        self.program['window_size'] = self.window_size
        self.program['MAX_ITERATIONS'] = MAX_ITERATIONS
    
    def render(self, time, dt):
        self.ctx.clear()

        if self.max_iter < MAX_ITERATIONS:
            self.max_iter += 1 if not INSTANT else MAX_ITERATIONS
        # self.max_iter = MAX_ITERATIONS
        diff = abs(self.target_zoom - self.zoom)
        if not diff < 0.2:
            if self.zoom < self.target_zoom:
                self.zoom += (diff * 0.1) / 2
            else:
                self.zoom -= (diff * 0.1) / 2
                if self.zoom < 0:
                    self.zoom = 0
        
        if self.zoom < 1.2:
            self.zoom = 1.2

        # print(self.wasd_down)
        move_speed = 0.1 / (self.zoom ** 4)
        if self.wasd_down['w']:
            self.camera_pos = (self.camera_pos[0], self.camera_pos[1] - move_speed)
        if self.wasd_down['a']:
            self.camera_pos = (self.camera_pos[0] + move_speed, self.camera_pos[1])
        if self.wasd_down['s']:
            self.camera_pos = (self.camera_pos[0], self.camera_pos[1] + move_speed)
        if self.wasd_down['d']:
            self.camera_pos = (self.camera_pos[0] - move_speed, self.camera_pos[1])
        
        self.program['zoom'] = self.zoom
        self.program['max_iter'] = self.max_iter
        self.program['camera_pos'] = self.camera_pos
        # print(self.zoom)
        self.quad_fs.render(self.program)
    
    def key_event(self, key, action, modifiers):
        key_chr = chr(key)
        self.key_down = True if action == 'ACTION_PRESS' else False

        wasd_key_down = self.wasd_down.get(key_chr)
        if wasd_key_down != None:
            self.wasd_down[key_chr] = action == 'ACTION_PRESS'

        if key_chr == 't' and action == 'ACTION_PRESS':
            # self.zoom = 1.2
            # self.target_zoom = 1
            self.max_iter = 1
            # self.camera_pos = (0, 0)
        elif key_chr == 'r' and action == 'ACTION_PRESS':
            self.zoom = 1.2
            self.target_zoom = 1
            self.max_iter = 1
            self.camera_pos = (0, 0)
            
    
    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        self.target_zoom += y_offset
        if self.target_zoom < 1:
            self.target_zoom = 1

App.run()