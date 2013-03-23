# -*- coding:GBK -*-

import math
import math3d
import rabbit_obj
import iworld2d
import iphy2d

testobj = None

start_x, start_y = 300, 450

class CSliderCrankTest(object):
	def __init__(self):
		import rabbit_scene
		# 创建一个固定物体
		self.ground = iphy2d.body(iphy2d.POLYGON, (math3d.vector2(0, 46), math3d.vector2(68, 46)))
		self.ground.body_type = iphy2d.STATIC_BODY
		self.ground.pos = (start_x/rabbit_obj.MAP_SCALE, (start_y+200)/rabbit_obj.MAP_SCALE)

		# 最底下的杆子1
		self.crank = rabbit_scene.create_obj("obj", 13, start_x, start_y)
		# 稍长一点的杆子2
		self.follower = rabbit_scene.create_obj("obj", 14, start_x, start_y)
		# 长杆子上绑的一个矩形1
		self.piston = rabbit_scene.create_obj("obj", 15, start_x, start_y)
		# 最上面自由落体的矩形2
		self.payload = rabbit_scene.create_obj("obj", 15, start_x, start_y+200)

	def restart(self):
		pre_body = self.ground

		# 杆子1和固定物体，用旋转关节连在一起，并启用一个马达
		self.crank.pos = (start_x, start_y)
		p = math3d.vector2(start_x/rabbit_obj.MAP_SCALE, (start_y+40)/rabbit_obj.MAP_SCALE)
		a1 = pre_body.get_local_point(p)
		a2 = self.crank.phy.get_local_point(p)
		self.j1 = iphy2d.revolute_joint(pre_body, self.crank.phy, \
				anchor_a=a1, anchor_b=a2, \
				enable_motor=True, motor_speed=math.pi, max_torque = 10000)
		pre_body = self.crank.phy

		# 杆子1和杆子2，用旋转关节连在一起
		self.follower.pos = (start_x, start_y-120)
		p = math3d.vector2(start_x/rabbit_obj.MAP_SCALE, (start_y-40)/rabbit_obj.MAP_SCALE)
		a1 = pre_body.get_local_point(p)
		a2 = self.follower.phy.get_local_point(p)
		self.j2 = iphy2d.revolute_joint(pre_body, self.follower.phy, \
				anchor_a=a1, anchor_b=a2)
		pre_body = self.follower.phy

		# 杆子2和矩形1，用旋转关节连在一起
		self.piston.pos = (start_x, start_y-200)
		p = math3d.vector2(start_x/rabbit_obj.MAP_SCALE, (start_y-200)/rabbit_obj.MAP_SCALE)
		a1 = pre_body.get_local_point(p)
		a2 = self.piston.phy.get_local_point(p)
		self.j3 = iphy2d.revolute_joint(pre_body, self.piston.phy, \
				anchor_a=a1, anchor_b=a2)

		# 固定物体和矩形1，用移动关节连载一起，并启用一个马达
		p = math3d.vector2(start_x/rabbit_obj.MAP_SCALE, (start_y-200)/rabbit_obj.MAP_SCALE)
		a1 = self.ground.get_local_point(p)
		a2 = self.piston.phy.get_local_point(p)
		axis = math3d.vector2(0, 1)
		self.j4 = iphy2d.prismatic_joint(self.ground, self.piston.phy, \
				anchor_a=a1, anchor_b=a2, axis=axis, \
				enable_motor=True, max_torque=1000)

		self.payload.pos = (start_x, start_y-320)

	def destroy(self):
		self.ground.destroy()
		self.crank.destroy()
		self.follower.destroy()
		self.piston.destroy()
		self.payload.destroy()

def start():
	global testobj
	if testobj is None:
		testobj = CSliderCrankTest()
	testobj.restart()


def destroy():
	global testobj
	if testobj:
		testobj.destroy()
		testobj = None

