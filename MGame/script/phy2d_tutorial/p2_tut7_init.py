# -*- coding:GBK -*-
# �����ͻ��˳���Ľṹ
# collision filter
import idemo_demo
import iphy2d
import iworld2d
import math3d
import math
import game
import p2_common

F_EDGE = 0x0001
F_FRIENDLY_CARRIER = 0x0002
F_ENEMY_CARRIER = 0x0004
F_FRIENDLY_AIRCRAFT =0x0008
F_ENEMY_AIRCRAFT = 0x0010

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
		# ��ʼ��
		iphy2d.init()
		# debug ��ʾ
		iworld2d.init()
		iworld2d.camera_world_pos_center(0, 0)
		iphy2d.set_debug_draw(True)
		iworld2d.camera_world_scale(PHY_SCALE)
		# ȡ������
		iphy2d.set_gravity((0, 0))
		# ����һ����տռ�
		self.ground1 = iphy2d.body(iphy2d.POLYGON, math3d.vector2(10, 1))
		self.ground1.position = math3d.vector2(0, -10)
		self.ground1.body_type = iphy2d.STATIC_BODY
		self.ground1.category = F_EDGE
		self.ground2 = iphy2d.body(iphy2d.POLYGON, math3d.vector2(10, 1))
		self.ground2.position = math3d.vector2(0, 10)
		self.ground2.body_type = iphy2d.STATIC_BODY
		self.ground2.category = F_EDGE
		self.ground3 = iphy2d.body(iphy2d.POLYGON, math3d.vector2(1, 10))
		self.ground3.position = math3d.vector2(-10, 0)
		self.ground3.body_type = iphy2d.STATIC_BODY
		self.ground3.category = F_EDGE
		self.ground4 = iphy2d.body(iphy2d.POLYGON, math3d.vector2(1, 10))
		self.ground4.position = math3d.vector2(10, 0)
		self.ground4.body_type = iphy2d.STATIC_BODY
		self.ground4.category = F_EDGE
		# �������
		self.objs = []
	
	# ����һ����ĸ��ս��
	# �Ѿ����ΪԲ���о�Ϊ����
	# ��ĸ��ս����
	def create_obj(self, is_friend, is_carrier):
		radius = 1
		if is_carrier:
			radius = 2
		if is_friend:
			body = iphy2d.body(iphy2d.SPHERE, radius)
		else:
			body = iphy2d.body(iphy2d.POLYGON, math3d.vector2(radius, radius))
		# ����category��mask
		if is_friend:
			if is_carrier:
				body.category = F_FRIENDLY_CARRIER
				body.collide_mask = F_EDGE | F_FRIENDLY_CARRIER | F_ENEMY_CARRIER
			else:
				body.category = F_FRIENDLY_AIRCRAFT
				body.collide_mask = F_EDGE | F_ENEMY_AIRCRAFT
		else:
			if is_carrier:
				body.category = F_ENEMY_CARRIER
				body.collide_mask = F_EDGE | F_FRIENDLY_CARRIER | F_ENEMY_CARRIER
			else:
				body.category = F_ENEMY_AIRCRAFT
				body.collide_mask = F_EDGE | F_FRIENDLY_AIRCRAFT
		return body
	
	def start_test(self):
		self.destroy_bodies()
		xlo, xhi = -9, 9
		ylo, yhi = -9, 9
		for i in xrange(3):
			obj = self.create_obj(True, True)
			obj.position = math3d.vector2(p2_common.randfloat_range(xlo, xhi),
				p2_common.randfloat_range(ylo, yhi))
			self.objs.append(obj)
			obj = self.create_obj(False, True)
			obj.position = math3d.vector2(p2_common.randfloat_range(xlo, xhi),
				p2_common.randfloat_range(ylo, yhi))
			self.objs.append(obj)
			obj = self.create_obj(True, False)
			obj.position = math3d.vector2(p2_common.randfloat_range(xlo, xhi),
				p2_common.randfloat_range(ylo, yhi))
			self.objs.append(obj)
			obj = self.create_obj(False, False)
			obj.position = math3d.vector2(p2_common.randfloat_range(xlo, xhi),
				p2_common.randfloat_range(ylo, yhi))
			self.objs.append(obj)
	
	def destroy_bodies(self):
		for obj in self.objs:
			obj.destroy()
		self.objs = []
	
	# ���ٺ���
	def destroy(self):
		self.destroy_bodies()
		iworld2d.destroy()
		iphy2d.destroy()

	# �߼�֡
	def logic(self):
		iphy2d.update()
	
	# ������Ϣ
	def on_key_msg(self, msg, key):
		super(demo, self).on_key_msg(msg, key)
		if msg == game.MSG_KEY_DOWN and key == game.VK_1:
			self.start_test()
	
	