# -*- coding:GBK -*-

import math
import math3d
import rabbit_obj
import iworld2d
import iphy2d

testobj = None

length = 200

start_x, start_y = 100, 400

MAX_SEGMENT = 30

class CBridgeTest(object):
	def __init__(self):
		import rabbit_scene
		# 创建一个固定物体
		self.ground = iphy2d.body(iphy2d.POLYGON, (math3d.vector2(-50, 1), math3d.vector2(50, 1)))
		self.ground.body_type = iphy2d.STATIC_BODY
		self.ground.pos = (20, 43)

		# 生成一段萝卜
		self.body = []
		for i in range(MAX_SEGMENT):
			b = rabbit_scene.create_obj("obj",12, start_x+i*10, start_y)
			self.body.append(b)

		# 另外模拟一个时钟的走动
		self.b1 = rabbit_scene.create_obj("bear", 100, 300, 200)
		self.b2 = rabbit_scene.create_obj("obj", 15, 300, 400)
		self.r1 = iphy2d.revolute_joint(self.b1.phy, self.b2.phy, anchor_b=self.b1.phy.get_local_point(math3d.vector2(20,26)),\
				#enable_limit=True, lower_angle=-math.pi/2, upper_angle=math.pi/2, 
				enable_motor = True, motor_speed=math.pi*0.1, max_torque=10000, 
				)

	def restart(self):
		self.dj_lst = []
		pre_body = self.ground
		# 把旋转关节都分别连到每两个萝卜上
		for i in range(MAX_SEGMENT):
			self.body[i].pos = (start_x+i*16, start_y)

			p = math3d.vector2((start_x-8+i*16)/rabbit_obj.MAP_SCALE, start_y/rabbit_obj.MAP_SCALE)
			a1 = pre_body.get_local_point(p)
			a2 = self.body[i].phy.get_local_point(p)
			dj = iphy2d.revolute_joint(pre_body, self.body[i].phy, \
					anchor_a=a1, anchor_b=a2)
			self.dj_lst.append(dj)

			pre_body = self.body[i].phy
		p = math3d.vector2((start_x-8+MAX_SEGMENT*16)/rabbit_obj.MAP_SCALE, start_y/rabbit_obj.MAP_SCALE)
		a1 = pre_body.get_local_point(p)
		a2 = self.ground.get_local_point(p)
		dj = iphy2d.revolute_joint(self.body[MAX_SEGMENT-1].phy, self.ground, \
				anchor_a=a1, anchor_b=a2)
		self.dj_lst.append(dj)


	def destroy(self):
		self.ground.destroy()
		self.b1.destroy()
		self.b2.destroy()
		for b in self.body:
			b.destroy()
		self.body = []
		self.b1 = None
		self.b2 = None

def start():
	global testobj
	if testobj is None:
		testobj = CBridgeTest()
	testobj.restart()


def destroy():
	global testobj
	if testobj:
		testobj.destroy()
		testobj = None

