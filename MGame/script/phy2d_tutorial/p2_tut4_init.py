# -*- coding:GBK -*-
# 创建客户端程序的结构
# friction
import idemo_demo
import iphy2d
import iworld2d
import math3d
import math

inst = None
PHY_SCALE = 15.0

def init(browser):
	global inst
	if inst is None:
		inst = demo()
		inst.init(browser)

def destroy():
	global inst
	if inst:
		inst.destroy()
		inst = None

class demo(idemo_demo.demo):
	def __init__(self):
		super(demo, self).__init__()
	
	def init(self, browser):
		super(demo, self).init(browser)
		# 初始化
		iphy2d.init()
		# debug 显示
		iworld2d.init()
		iworld2d.camera_world_pos_center(0, 0)
		iphy2d.set_debug_draw(True)
		iworld2d.camera_world_scale(PHY_SCALE)
		# 设置重力
		iphy2d.set_gravity((0, 10.0))
		# 创建一个地面
		self.ground = iphy2d.body(iphy2d.POLYGON, math3d.vector2(35.0, 1))
		self.ground.body_type = iphy2d.STATIC_BODY
		self.ground.position = math3d.vector2(0, 15)
		# 斜面1,2,3
		self.p1 = iphy2d.body(iphy2d.POLYGON, math3d.vector2(13.0, 0.25))
		self.p1.body_type = iphy2d.STATIC_BODY
		self.p1.position = math3d.vector2(-4.0, -5.0)
		self.p1.rot = 0.25
		self.p1.friction = 0.2
		self.p1.restitution = 0.0
		self.p2 = iphy2d.body(iphy2d.POLYGON, math3d.vector2(13.0, 0.25))
		self.p2.body_type = iphy2d.STATIC_BODY
		self.p2.position = math3d.vector2(4.0, 2.0)
		self.p2.rot = -0.25
		self.p2.friction = 0.2
		self.p2.restitution = 0.0
		self.p3 = iphy2d.body(iphy2d.POLYGON, math3d.vector2(13.0, 0.25))
		self.p3.body_type = iphy2d.STATIC_BODY
		self.p3.position = math3d.vector2(-4.0, 9.0)
		self.p3.rot = 0.25
		self.p3.friction = 0.2
		self.p3.restitution = 0.0
		self.bricks = []
		# 摩擦
		frictions = (0.75, 0.5, 0.35, 0.1, 0.0)
		for i in xrange(5):
			body = iphy2d.body(iphy2d.POLYGON, math3d.vector2(1, 1))
			body.body_type = iphy2d.DYNAMIC_BODY
			body.position = math3d.vector2(-10 + 4 * i, -7.0)
			body.restitution = 0.0
			body.density = 25.0
			body.friction = frictions[i]
			self.bricks.append(body)
		
	# 销毁函数
	def destroy(self):
		for b in self.bricks:
			b.destroy()
		self.bricks = None
		self.p1.destroy()
		self.p2.destroy()
		self.p3.destroy()
		self.ground.destroy()
		self.ground = self.p1 = self.p2 = self.p3 = None
		iworld2d.destroy()
		iphy2d.destroy()

	# 逻辑帧
	def logic(self):
		iphy2d.update()