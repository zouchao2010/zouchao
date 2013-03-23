# -*- coding:GBK -*-
# 创建客户端程序的结构
# Body
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
		
		# 创建body
		# dynamic body
		# 创建一个body，默认形状为矩形
		self.d_body = iphy2d.body(iphy2d.POLYGON, math3d.vector2(1.0, 1.0))
		self.d_body.body_type = iphy2d.DYNAMIC_BODY # dynamic body
		self.d_body.position = math3d.vector2(0.0, 0.0)# 起始位置
		self.d_body.rot = 0.0 # 弧度
		self.d_body.linear_velocity = math3d.vector2(-1.0, 1.0)# 线性速度
		self.d_body.angular_velocity = math.pi# 角速度
		
		# static body
		self.s_body = iphy2d.body(iphy2d.POLYGON, math3d.vector2(1.0, 1.0))
		self.s_body.body_type = iphy2d.STATIC_BODY # static body
		self.s_body.position = math3d.vector2(-10.0, 10.0)# 起始位置
		self.s_body.rot = 0.0 # 弧度
		
		# kinematic body
		self.k_body = iphy2d.body(iphy2d.POLYGON, math3d.vector2(1.0, 1.0))
		self.k_body.body_type = iphy2d.KINEMATIC_BODY # static body
		self.k_body.position = math3d.vector2(5.0, -5.0)# 起始位置
		self.k_body.rot = 0.0 # 弧度
		self.k_body.linear_velocity = math3d.vector2(-2.0, 2.0)# 线性速度
		self.k_body.angular_velocity = math.pi# 角速度
		
	# 销毁函数
	def destroy(self):
		self.d_body.destroy()
		self.s_body.destroy()
		self.k_body.destroy()
		iworld2d.destroy()
		iphy2d.destroy()

	# 逻辑帧
	def logic(self):
		iphy2d.update()