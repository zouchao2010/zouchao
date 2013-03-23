# -*- coding:GBK -*-
# 创建客户端程序的结构
# restitution
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
		self.ground.position = math3d.vector2(0, 25)
		self.ground.resititution = 0.0
		self.balls = []
		# 弹力
		restitutions = (0.0, 0.1, 0.3, 0.5, 0.75, 0.9, 1.0)
		for i in xrange(7):
			body = iphy2d.body(iphy2d.SPHERE, 1.0)
			body.body_type = iphy2d.DYNAMIC_BODY
			body.position = math3d.vector2(-10 + 3 * i, 20.0)
			body.restitution = restitutions[i]
			body.density = 1.0
			self.balls.append(body)
		
	# 销毁函数
	def destroy(self):
		for b in self.balls:
			b.destroy()
		self.balls = None
		self.ground.destroy()
		self.ground = None
		iworld2d.destroy()
		iphy2d.destroy()

	# 逻辑帧
	def logic(self):
		iphy2d.update()