# -*- coding:GBK -*-

import math
import math3d
import rabbit_obj
import iworld2d
import iphy2d

testobj = None

length = 200

start_x, start_y = 300, 200

MAX_SEGMENT = 10

class CApplyForceTest(object):
	def __init__(self):
		import rabbit_scene
		# 创建一个固定物体
		self.ground = iphy2d.body(iphy2d.POLYGON, (math3d.vector2(0, 46), math3d.vector2(68, 46)))
		self.ground.body_type = iphy2d.STATIC_BODY
		self.ground.pos = (start_x/rabbit_obj.MAP_SCALE, start_y/rabbit_obj.MAP_SCALE)

		# 继续生成萝卜。。。
		self.body = []
		for i in range(MAX_SEGMENT):
			b = rabbit_scene.create_obj("obj",12, start_x, start_y+i*40)
			self.body.append(b)

	def restart(self):
		self.dj_lst = []
		pre_body = self.ground
		# 把摩擦关节连到ground和每段萝卜上
		for i in range(MAX_SEGMENT):
			self.body[i].pos = (start_x, start_y + i*40)

			gravity = 10.0
			mass = self.body[i].phy.mass
			radius = math.sqrt(2.0)
			dj = iphy2d.friction_joint(self.ground, self.body[i].phy, \
					max_force=mass*gravity, max_torque=mass*radius*gravity,  
					)
			self.dj_lst.append(dj)


	def destroy(self):
		self.ground.destroy()
		for b in self.body:
			b.destroy()
		self.body = []

def start():
	global testobj
	if testobj is None:
		testobj = CApplyForceTest()
	# 取消重力
	iphy2d.set_gravity((0, 0))
	testobj.restart()


def destroy():
	global testobj
	if testobj:
		testobj.destroy()
		testobj = None

