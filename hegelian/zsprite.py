# A sprite class derivative that implements integer z values (larger negatives are more distant)

import pyglet
from pyglet.gl import *
from pyglet import graphics
from pyglet import image
from pyglet import sprite


"""

NOTE - DOWNLOADED FROM HERE: https://bitbucket.org/bcarpenter/anticrap-game-framework/src/907f5b84871d/zsprite.py

NB. You will need to set up z-buffering and your near and far clipping planes properly.

eg. In your window class:

    def __init__(self, etc)
        ...
        glClearDepth(1.0);
        ...

    def on_resize(self, width, height):
        # Based on the default with more useful clipping planes
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, width, 0, height, 0.5, 1000)
        gl.glMatrixMode(gl.GL_MODELVIEW)
"""


class ZSpriteGroup(sprite.SpriteGroup):
    '''Shared sprite rendering group with z-coordinate support.

    The group is automatically coallesced with other sprite groups sharing the
    same parent group, texture and blend parameters.
    '''
    def __init__(self, alpha_test_val, *args):
        super(ZSpriteGroup, self).__init__(*args)
        # this value is a bit of a hack. Ideally it would be zero, but if you
        # have any values that are close to zero, you probably want to catch them too.
        self._alpha_test_val = alpha_test_val
        
    def set_state(self):
        glEnable(self.texture.target)
        glBindTexture(self.texture.target, self.texture.id)

        glPushAttrib(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Normal alpha blending mode
        glEnable(GL_BLEND)
        glBlendFunc(self.blend_src, self.blend_dest)
        # ...plus depth testing to allow proper occlusion
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        # ...and alpha testing so that nearby objects that contain transparent areas
        # don't conceal more distant objects behind the transparency
        glEnable(GL_ALPHA_TEST)        
        glAlphaFunc(GL_GREATER, self._alpha_test_val)


class ZSprite(pyglet.sprite.Sprite):

    def __init__(self,
                 img, x=0, y=0, z=0,
                 blend_src=GL_SRC_ALPHA,
                 blend_dest=GL_ONE_MINUS_SRC_ALPHA,
                 batch=None,
                 group=None,
                 usage='dynamic',
                 alpha_test_val=0.5,
                 subpixel=False):
        '''Create a sprite with z-coordinate support.

        :Parameters:
            `img` : `AbstractImage` or `Animation`
                Image or animation to display.
            `x` : int
                X coordinate of the sprite.
            `y` : int
                Y coordinate of the sprite.
            `z` : int
                Z coordinate of the sprite.
            `blend_src` : int
                OpenGL blend source mode.  The default is suitable for
                compositing sprites drawn from back-to-front.
            `blend_dest` : int
                OpenGL blend destination mode.  The default is suitable for
                compositing sprites drawn from back-to-front.
            `batch` : `Batch`
                Optional batch to add the sprite to.
            `group` : `Group`
                Optional parent group of the sprite.
            `usage` : str
                Vertex buffer object usage hint, one of ``"none"`` (default),
                ``"stream"``, ``"dynamic"`` or ``"static"``.  Applies
                only to vertex data.
            'subpixel` : bool
                ADDED BY SAM GEEN - allows subpixel version of sprites to be used

        '''
        self._subpixel = subpixel
        if batch is not None:
            self._batch = batch

        self._x = x
        self._y = y
        self._z = z
        
        self._alpha_test_val = alpha_test_val

        if isinstance(img, image.Animation):
            self._animation = img
            self._frame_index = 0
            self._texture = img.frames[0].image.get_texture()
            self._next_dt = img.frames[0].duration
            if self._next_dt:
                clock.schedule_once(self._animate, self._next_dt)
        else:
            self._texture = img.get_texture()

        # Must use the ZSpriteGroup to be able to enable depth testing
        self._group = ZSpriteGroup(self._alpha_test_val, self._texture, blend_src, blend_dest, group)
        self._usage = usage
        self._create_vertex_list()
       

    def _set_group(self, group):
        if self._group.parent == group:
            return

        # Use ZSpriteGroup to enable depth testing
        self._group = ZSpriteGroup(self._alpha_test_val,
                                  self._texture,
                                  self._group.blend_src,
                                  self._group.blend_dest,
                                  group)

        if self._batch is not None:
           self._batch.migrate(self._vertex_list, GL_QUADS, self._group,
                               self._batch)
                               

    def _get_group(self):
        return self._group.parent

   
    # If we don't reimplement this property, it appears to defer to the
    # parent class's implementation of _get_group and _set_group, which is no good
    group = property(_get_group, _set_group,
                     doc='''Parent graphics group.

    The sprite can change its rendering group, however this can be an
    expensive operation.

    :type: `Group`
    ''')
    
    
    def _set_texture(self, texture):
        # Again, mostly copy and paste from the parent class
        if texture.id is not self._texture.id:
            self._group = ZSpriteGroup(self._alpha_test_val,
                                      texture,
                                      self._group.blend_src,
                                      self._group.blend_dest,
                                      self._group.parent)
            if self._batch is None:
                self._vertex_list.tex_coords[:] = texture.tex_coords
            else:
                self._vertex_list.delete()
                self._texture = texture
                self._create_vertex_list()
        else:
            self._vertex_list.tex_coords[:] = texture.tex_coords
        self._texture = texture
       
        
    def _create_vertex_list(self):
        # Slightly changed from the parent, in that it passes v3i instead of v2i
        # SAM GEEN HACK - SUBPIXEL FORMAT ADDED
        format = 'i'
        if self._subpixel:
            format = 'f'
        if self._batch is None:
            self._vertex_list = graphics.vertex_list(4,
                'v3'+format+'/%s' % self._usage, 
                'c4B', ('t3f', self._texture.tex_coords))
        else:
            self._vertex_list = self._batch.add(4, GL_QUADS, self._group,
                'v3'+format+'/%s' % self._usage, 
                'c4B', ('t3f', self._texture.tex_coords))
        self._update_position()
        self._update_color()

    def _update_position(self):
        # SAM GEEN HACK - Changed int cast to a float cast (i.e. nothing) if subpixel set
        # Just differs from parent in the addition of extra z vertices
        img = self._texture
        
        if self._subpixel:
            mycast = float
        else:
            mycast = int
        
        if not self._visible:
            self._vertex_list.vertices[:] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif self._rotation:
            x1 = -img.anchor_x * self._scale
            y1 = -img.anchor_y * self._scale
            x2 = x1 + img.width * self._scale
            y2 = y1 + img.height * self._scale
            x = self._x
            y = self._y
            z = self._z

            r = -math.radians(self._rotation)
            cr = math.cos(r)
            sr = math.sin(r)
            ax = mycast(x1 * cr - y1 * sr + x)
            ay = mycast(x1 * sr + y1 * cr + y)
            bx = mycast(x2 * cr - y1 * sr + x)
            by = mycast(x2 * sr + y1 * cr + y)
            cx = mycast(x2 * cr - y2 * sr + x)
            cy = mycast(x2 * sr + y2 * cr + y)
            dx = mycast(x1 * cr - y2 * sr + x)
            dy = mycast(x1 * sr + y2 * cr + y)

            self._vertex_list.vertices[:] = [ax, ay, z, bx, by, z, cx, cy, z, dx, dy, z]
        elif self._scale != 1.0:
            x1 = mycast(self._x - img.anchor_x * self._scale)
            y1 = mycast(self._y - img.anchor_y * self._scale)
            x2 = mycast(x1 + img.width * self._scale)
            y2 = mycast(y1 + img.height * self._scale)
            z = self._z
            self._vertex_list.vertices[:] = [x1, y1, z, x2, y1, z, x2, y2, z, x1, y2, z]
        else:
            x1 = mycast(self._x - img.anchor_x)
            y1 = mycast(self._y - img.anchor_y)
            x2 = x1 + img.width
            y2 = y1 + img.height
            z = self._z
            self._vertex_list.vertices[:] = [x1, y1, z, x2, y1, z, x2, y2, z, x1, y2, z]

    def _update_position_intonly(self):
        # Just differs from parent in the addition of extra z vertices
        img = self._texture
        
        if not self._visible:
            self._vertex_list.vertices[:] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif self._rotation:
            x1 = -img.anchor_x * self._scale
            y1 = -img.anchor_y * self._scale
            x2 = x1 + img.width * self._scale
            y2 = y1 + img.height * self._scale
            x = self._x
            y = self._y
            z = self._z

            r = -math.radians(self._rotation)
            cr = math.cos(r)
            sr = math.sin(r)
            ax = int(x1 * cr - y1 * sr + x)
            ay = int(x1 * sr + y1 * cr + y)
            bx = int(x2 * cr - y1 * sr + x)
            by = int(x2 * sr + y1 * cr + y)
            cx = int(x2 * cr - y2 * sr + x)
            cy = int(x2 * sr + y2 * cr + y)
            dx = int(x1 * cr - y2 * sr + x)
            dy = int(x1 * sr + y2 * cr + y)

            self._vertex_list.vertices[:] = [ax, ay, z, bx, by, z, cx, cy, z, dx, dy, z]
        elif self._scale != 1.0:
            x1 = int(self._x - img.anchor_x * self._scale)
            y1 = int(self._y - img.anchor_y * self._scale)
            x2 = int(x1 + img.width * self._scale)
            y2 = int(y1 + img.height * self._scale)
            z = self._z
            self._vertex_list.vertices[:] = [x1, y1, z, x2, y1, z, x2, y2, z, x1, y2, z]
        else:
            x1 = int(self._x - img.anchor_x)
            y1 = int(self._y - img.anchor_y)
            x2 = x1 + img.width
            y2 = y1 + img.height
            z = self._z
            self._vertex_list.vertices[:] = [x1, y1, z, x2, y1, z, x2, y2, z, x1, y2, z]

            
    def set_position(self, x, y, z):
        '''Set the X, Y, and Z coordinates of the sprite simultaneously.

        :Parameters:
            `x` : int
                X coordinate of the sprite.
            `y` : int
                Y coordinate of the sprite.
            `z` : int
                Z coordinate of the sprite.
                
        '''
        self._x = x
        self._y = y
        self._z = z
        self._update_position()

        
    position = property(lambda self: (self._x, self._y, self._z),
                        lambda self, t: self.set_position(*t),
                        doc='''The (x, y, z) coordinates of the sprite.

    :type: (int, int, int)
    ''')

        
    def _set_z(self, z):
        self._z = z
        self._update_position()

        
    z = property(lambda self: self._z, _set_z,
                 doc='''Z coordinate of the sprite.

    :type: int
    ''')
        
