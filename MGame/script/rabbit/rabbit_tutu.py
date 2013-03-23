# -*- coding:GBK -*-

import rabbit_obj
import iworld2d
import iphy2d

bomb = None

class CRabbitObj(rabbit_obj.CRabbitObj):

	def init(self):
		self.impulse = 0
		self._will_carrot_fly = False

	def init_face(self):
		self.change_look(1)

	def change_look(self, look):
		if self.face:
			self.face.change_looks("looks%s"%look)

	def update(self):
		super(CRabbitObj, self).update()
		if self._will_carrot_fly:
			self._will_carrot_fly = False
			self.carrot_fly()

	def carrot_fly(self):
		import rabbit_scene
		unit = self.face.get_unit("unit02")
		pos = unit.wpos
		obj = rabbit_scene.create_obj("obj", 7, pos[0], pos[1])
		self.phy.sensor = True

	def on_hit(self, by_obj):
		delta = 0
		if by_obj.phy.body_type == iphy2d.STATIC_BODY:
			delta = (self.phy.mass * self.phy.linear_velocity.length)
		else:
			delta = (by_obj.phy.mass * by_obj.phy.linear_velocity.length)
		lhit = int(self.impulse/8000)
		self.impulse += delta
		hit = int(self.impulse/8000)
		if  hit >= 4:
			global bomb
			bomb = iworld2d.sprite2d("idemos/res/rabbit/world2d/sprite/bomb.sp2")
			bomb.key_point = (0,0)
			bomb.pos = self.pos
			bomb.register_keyframe_event(14, destroy_bomb)
			bomb.play()
			
			self.destroy()
		elif hit == 2 and lhit == 1:
			self.change_look(3)
		elif hit == 1 and lhit == 0:
			self.change_look(2)
			self._will_carrot_fly = True

		import rabbit_scene
		rabbit_scene.add_score(int(delta))

def destroy_bomb(obj, data):
	bomb.hide()
	bomb.destroy()
