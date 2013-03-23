# -*- coding:GBK -*-
# 创建客户端程序的结构
# collision processing
import idemo_demo
import p2_common
import iphy2d
import iworld2d
import math3d
import math
import game

inst = None
PHY_SCALE = 15.0

def body_collide(body_a, body_b):
	# 大的吃掉小的
	if body_a.mass > body_b.mass:
		body_b.flag = True
	else:
		body_a.flag = True

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
		# 设置碰撞回调
		iphy2d.set_first_collided_callback(body_collide)
		# 创建一个地面
		self.ground = iphy2d.body(iphy2d.POLYGON, math3d.vector2(35.0, 1))
		self.ground.body_type = iphy2d.STATIC_BODY
		self.ground.position = math3d.vector2(0, 15)
		self.tr1 = self.tr2 = self.box1 = self.box2 = self.circle1 = self.circle2 = None
		
	def start_test(self):
		self.destroy_bodies()
		xlo, xhi = -5, 5
		ylo, yhi = -10, 10
		# 一个小三角形
		self.tr1 = iphy2d.body(iphy2d.POLYGON, (math3d.vector2(-1, 0),
			math3d.vector2(1.0, 0.0),
			math3d.vector2(0.0, 2.0)))
		self.tr1.body_type = iphy2d.DYNAMIC_BODY
		self.tr1.density = 1.0
		self.tr1.position = math3d.vector2(p2_common.randfloat_range(xlo, xhi),
			p2_common.randfloat_range(ylo, yhi))
		self.tr1.flag = False # 用于判断是否需要销毁
		# 一个大三角形
		self.tr2 = iphy2d.body(iphy2d.POLYGON, (math3d.vector2(-2, 0),
			math3d.vector2(2.0, 0.0),
			math3d.vector2(0.0, 4.0)))
		self.tr2.body_type = iphy2d.DYNAMIC_BODY
		self.tr2.density = 1.0
		self.tr2.position = math3d.vector2(p2_common.randfloat_range(xlo, xhi),
			p2_common.randfloat_range(ylo, yhi))
		self.tr2.flag = False # 用于判断是否需要销毁
		# 一个小矩形
		self.box1 = iphy2d.body(iphy2d.POLYGON, math3d.vector2(1.0, 0.5))
		self.box1.body_type = iphy2d.DYNAMIC_BODY
		self.box1.density = 1.0
		self.box1.position = math3d.vector2(p2_common.randfloat_range(xlo, xhi),
			p2_common.randfloat_range(ylo, yhi))
		self.box1.flag = False # 用于判断是否需要销毁
		# 一个大矩形
		self.box2 = iphy2d.body(iphy2d.POLYGON, math3d.vector2(2.0, 1.0))
		self.box2.body_type = iphy2d.DYNAMIC_BODY
		self.box2.density = 1.0
		self.box2.position = math3d.vector2(p2_common.randfloat_range(xlo, xhi),
			p2_common.randfloat_range(ylo, yhi))
		self.box2.flag = False # 用于判断是否需要销毁
		# 一个小圆形
		self.circle1 = iphy2d.body(iphy2d.SPHERE, 1.0)
		self.circle1.body_type = iphy2d.DYNAMIC_BODY
		self.circle1.density = 1.0
		self.circle1.position = math3d.vector2(p2_common.randfloat_range(xlo, xhi),
			p2_common.randfloat_range(ylo, yhi))
		self.circle1.flag = False # 用于判断是否需要销毁
		# 一个大圆形
		self.circle2 = iphy2d.body(iphy2d.SPHERE, 2.0)
		self.circle2.body_type = iphy2d.DYNAMIC_BODY
		self.circle2.density = 1.0
		self.circle2.position = math3d.vector2(p2_common.randfloat_range(xlo, xhi),
			p2_common.randfloat_range(ylo, yhi))
		self.circle2.flag = False # 用于判断是否需要销毁
	
	def destroy_bodies(self):
		if self.tr1:
			self.tr1.destroy()
		if self.tr2:
			self.tr2.destroy()
		if self.box1:
			self.box1.destroy()
		if self.box2:
			self.box2.destroy()
		if self.circle1:
			self.circle1.destroy()
		if self.circle2:
			self.circle2.destroy()
		self.tr1 = self.tr2 = self.box1 = self.box2 = self.circle1 = self.circle2 = None
	
	def handle_body(self):
		if self.tr1 and self.tr1.flag:
			self.tr1.destroy()
			self.tr1 = None
		if self.tr2 and self.tr2.flag:
			self.tr2.destroy()
			self.tr2 = None
		if self.box1 and self.box1.flag:
			self.box1.destroy()
			self.box1 = None
		if self.box2 and self.box2.flag:
			self.box2.destroy()
			self.box2 = None
		if self.circle1 and self.circle1.flag:
			self.circle1.destroy()
			self.circle1 = None
		if self.circle2 and self.circle2.flag:
			self.circle2.destroy()
			self.circle2 = None
	
	# 销毁函数
	def destroy(self):
		self.destroy_bodies()
		iworld2d.destroy()
		iphy2d.destroy()

	# 逻辑帧
	def logic(self):
		self.handle_body()
		iphy2d.update()
	
	# 键盘消息
	def on_key_msg(self, msg, key):
		super(demo, self).on_key_msg(msg, key)
		if msg == game.MSG_KEY_DOWN and key == game.VK_1:
			self.start_test()
