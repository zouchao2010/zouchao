# -*- coding:GBK -*-

import math3d
import iworld2d
import iphy2d

MAP_SCALE = 15.0

# 游戏物体的基类

class CRabbitObj(object):
	def __init__(self, ptype, param, density=0.0):
		if ptype == iphy2d.POLYGON:
			param = math3d.vector2(param[0]/MAP_SCALE, param[1]/MAP_SCALE)
		elif ptype == iphy2d.SPHERE:
			param = param/MAP_SCALE
		self.phy = iphy2d.body(ptype, param)	# 物理引擎对象
		self.phy.set_user_data(self)
		self.face = None	# 渲染对象
		self.name = ""
		self.init()

	def init(self):
		pass

	def init_face(self):
		pass

	def update(self):
		pass

	def set_name(self, name):
		self.name = name
		
	def destroy(self):
		import rabbit_scene
		del rabbit_scene.g_objs[self.id]
		if self.phy:
			self.phy.destroy()
		if self.face:
			self.face.destroy()

	def create_face(self, image_file):
		if ".2dm" in image_file:
			self.face = iworld2d.model2d(image_file)
		else:
			self.face = iworld2d.image2d(image_file)
		self.face.key_point = (0,0)
		self.init_face()


	def draw(self):
		if self.face and self.phy:
			pos = self.phy.pos
			self.face.pos = (pos[0]*MAP_SCALE, pos[1]*MAP_SCALE)
			self.face.rot = self.phy.rot
			self._pos = self.face.pos

	def on_hit(self, by_obj):
		pass

	def _get_id(self):
		return self.phy.id

	def _get_pos(self):
		return self._pos
		
	def _set_pos(self, pos):
		self._pos = pos
		self.phy.pos = (pos[0]/MAP_SCALE, pos[1]/MAP_SCALE)
		if self.face:
			self.face.pos =pos
	
	id = property(_get_id, None)
	pos = property(_get_pos, _set_pos)

