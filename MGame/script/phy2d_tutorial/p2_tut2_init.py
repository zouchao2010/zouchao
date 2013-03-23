# -*- coding:GBK -*-
# 创建客户端程序的结构
# Fxitures
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
		self.b1 = None
		self.b2 = None
		self.b3 = None
		
	def create_fixs(self):
		if self.b1:
			self.b1.destroy()
		if self.b2:
			self.b2.destroy()
		if self.b3:
			self.b3.destroy()
		# 创建一个圆形
		self.b1 = iphy2d.body(iphy2d.SPHERE, 1.0)
		self.b1.body_type = iphy2d.DYNAMIC_BODY # dynamic body
		self.b1.position = math3d.vector2(-10, 0)# 起始位置
		# 创建一个矩形
		self.b2 = iphy2d.body(iphy2d.POLYGON, math3d.vector2(1.0, 1.0))
		self.b2.body_type = iphy2d.DYNAMIC_BODY # dynamic body
		self.b2.position = math3d.vector2(0, 0)# 起始位置
		# 创建一个多边形
		self.b3 = iphy2d.body(iphy2d.POLYGON, (math3d.vector2(-1.0, 2.0),
			math3d.vector2(-1, 0), math3d.vector2(0, -3),
			math3d.vector2(1, 0), math3d.vector2(1, 1),
			))
		self.b3.body_type = iphy2d.DYNAMIC_BODY # dynamic body
		self.b3.position = math3d.vector2(10, 0)# 起始位置
		
	def create_fixs_one_body(self):
		if self.b1:
			self.b1.destroy()
		if self.b2:
			self.b2.destroy()
		if self.b3:
			self.b3.destroy()
		self.b1 = iphy2d.body(iphy2d.SPHERE, 1.0)
		self.b1.body_type = iphy2d.DYNAMIC_BODY # dynamic body
		self.b1.position = math3d.vector2(0, 0)# 起始位置
		# 中心处增加一个矩形
		self.b1.create_fixture(iphy2d.POLYGON, math3d.vector2(1.0, 1.0), 1)
		# 中心处增加一个多边形
		self.b1.create_fixture(iphy2d.POLYGON, (math3d.vector2(-1.0, 2.0),
			math3d.vector2(-1, 0), math3d.vector2(0, -3),
			math3d.vector2(1, 0), math3d.vector2(1, 1),
			), 1)
		self.b2 = None
		self.b3 = None
		
	# 销毁函数
	def destroy(self):
		if self.b1:
			self.b1.destroy()
		if self.b2:
			self.b2.destroy()
		if self.b3:
			self.b3.destroy()
		self.b1 = self.b2 = self.b3 = None
		iworld2d.destroy()
		iphy2d.destroy()

	# 逻辑帧
	def logic(self):
		iphy2d.update()
	
	# 键盘消息
	def on_key_msg(self, msg, key):
		super(demo, self).on_key_msg(msg, key)
		if msg == game.MSG_KEY_DOWN and key == game.VK_1:
			self.create_fixs()
		if msg == game.MSG_KEY_DOWN and key == game.VK_2:
			self.create_fixs_one_body()
	
	