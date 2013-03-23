# -*- coding:GBK -*-

import math
import math3d
import rabbit_obj
import iworld2d
import iphy2d


# 物理引擎中曲线的制作演示


# 公式: y = A * sin( w*x+phi)+k
# A = 振幅
# w = 控制单位角度内周期
# phi = 初相，x=0时的相位
# k = 偏距，反应在坐标系上的图像为图像的整体上移或下移




MAX_X = 400 # 总长度
MAX_SEGMENT = 80	# 此曲线细分的段数
STEP = 1.0*MAX_X/MAX_SEGMENT	# 每步的距离

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
			phy.collide_mask = 2	# 只接受category=2的碰撞
			self.phy_list.append(phy)	# 物理引擎对象

			x1 = x2
			y1 = y2
		self.face = None	# 渲染对象
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