# -*- coding:GBK -*-
import rabbit_obj
import iworld2d

class CRabbitObj(rabbit_obj.CRabbitObj):

	def init(self):
		self.flying = 0
		self.track = []

	def reset_track(self):
		for t in self.track:
			t.destroy()
		self.track = []

	def fly(self):
		self.flying = 1
		self.reset_track()

	def stop_fly(self):
		self.flying = 0
		self.reset_track()

	def update(self):
		if self.flying:
			self.flying += 1
			if self.flying >= 6:
				t = iworld2d.image2d("idemos/res/rabbit/world2d/txg/texiao.txg|020")
				t.key_point = (0,0)
				t.pos = self.face.pos
				self.track.append(t)
				self.flying = 1
		super(CRabbitObj, self).update()

	def on_hit(self, by_obj):
		if by_obj.name == 1:
			self.phy.linear_damping = 1
		self.flying = 0

	def destroy(self):
		super(CRabbitObj, self).destroy()
		self.reset_track()