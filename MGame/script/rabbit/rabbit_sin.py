# -*- coding:GBK -*-

import math
import math3d
import rabbit_obj
import iworld2d
import iphy2d


# �������������ߵ�������ʾ


# ��ʽ: y = A * sin( w*x+phi)+k
# A = ���
# w = ���Ƶ�λ�Ƕ�������
# phi = ���࣬x=0ʱ����λ
# k = ƫ�࣬��Ӧ������ϵ�ϵ�ͼ��Ϊͼ����������ƻ�����




MAX_X = 400 # �ܳ���
MAX_SEGMENT = 80	# ������ϸ�ֵĶ���
STEP = 1.0*MAX_X/MAX_SEGMENT	# ÿ���ľ���

A = 50.0
w = math.pi/(20.0*MAX_X/MAX_SEGMENT)
phi = 0
k = 50


class CRabbitObj(rabbit_obj.CRabbitObj):
	def __init__(self, ptype, prim, density=0.0):
		x0 = 70
		y0 = 470
		x1 = -20
		y1 = A * math.cos(w * x1 + phi) + k
		self.phy_list = []
		for i in range(MAX_SEGMENT):
			x2 = x1 + STEP
			y2 = A * math.cos(w * x2 + phi) + k
			param = []
			param.append(math3d.vector2((x1+x0)/rabbit_obj.MAP_SCALE, (y1+y0)/rabbit_obj.MAP_SCALE))
			param.append(math3d.vector2((x2+x0)/rabbit_obj.MAP_SCALE, (y2+y0)/rabbit_obj.MAP_SCALE))
			phy = iphy2d.body(ptype, tuple(param))
			phy.body_type = iphy2d.STATIC_BODY
			phy.density = 1
			phy.restitution = 0
			phy.friction = 100
			phy.category = 1
			phy.collide_mask = 2	# ֻ����category=2����ײ
			self.phy_list.append(phy)	# �����������

			x1 = x2
			y1 = y2
		self.face = None	# ��Ⱦ����
		self.name = ""
		self.phy = self.phy_list[0]
		self.init()

	def _get_pos(self):
		return self._pos
		
	def _set_pos(self, pos):
		self._pos = pos
		if self.face:
			self.face.pos =pos

	def draw(self):
		pass

	def destroy(self):
		import rabbit_scene
		if self.phy_list:
			for phy in self.phy_list:
				phy.destroy()
		if self.face:
			self.face.destroy()

	pos = property(_get_pos, _set_pos)