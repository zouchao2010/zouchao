# -*- coding:GBK -*-
# 创建客户端程序的结构
# force and torque
import idemo_demo
import iphy2d
import iworld2d
import math3d
import math
import game

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
		# 取消重力
		iphy2d.set_gravity((0, 0))
		# 创建一个封闭空间
		self.ground1 = iphy2d.body(iphy2d.POLYGON, math3d.vector2(15, 1))
		self.ground1.position = math3d.vector2(0, -15)
		self.ground1.body_type = iphy2d.STATIC_BODY
		self.ground1.resititution = 0.4
		self.ground2 = iphy2d.body(iphy2d.POLYGON, math3d.vector2(15, 1))
		self.ground2.position = math3d.vector2(0, 15)
		self.ground2.body_type = iphy2d.STATIC_BODY
		self.ground2.resititution = 0.4
		self.ground3 = iphy2d.body(iphy2d.POLYGON, math3d.vector2(1, 15))
		self.ground3.position = math3d.vector2(-15, 0)
		self.ground3.body_type = iphy2d.STATIC_BODY
		self.ground3.resititution = 0.4
		self.ground4 = iphy2d.body(iphy2d.POLYGON, math3d.vector2(1, 15))
		self.ground4.position = math3d.vector2(15, 0)
		self.ground4.body_type = iphy2d.STATIC_BODY
		self.ground4.resititution = 0.4
		
		# 创建一个飞行器
		self.body = iphy2d.body(iphy2d.POLYGON, math3d.vector2(1, 1))
		self.body.destroy_fixture(0) # 将默认的删除
		self.body.create_fixture(iphy2d.POLYGON, (math3d.vector2(2, 0),
			math3d.vector2(-1, 1), math3d.vector2(-1, -1)), 4.0)
		self.body.position = math3d.vector2(0, 2.0)
		self.body.angular_damping = 5.0
		self.body.linear_damping = 0.1
		self.body.allow_sleeping = False
		
	# 销毁函数
	def destroy(self):
		iworld2d.destroy()
		iphy2d.destroy()

	# 逻辑帧
	def logic(self):
		iphy2d.update()
	
	# 键盘消息
	def on_key_msg(self, msg, key):
		super(demo, self).on_key_msg(msg, key)
		if msg == game.MSG_KEY_PRESSED and key == game.VK_W:
			f = math3d.vector2(math.cos(self.body.rot) * 200,
				math.sin(self.body.rot) * 200)
			self.body.apply_force(f, self.body.position)
		if msg == game.MSG_KEY_PRESSED and key == game.VK_A:
			self.body.apply_torque(-50)
		if msg == game.MSG_KEY_PRESSED and key == game.VK_D:
			self.body.apply_torque(50)
	