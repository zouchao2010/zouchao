# -*- coding:GBK -*-

import math
import math3d
import rabbit_obj
import iworld2d
import iphy2d

testobj = None

length = 200

start_x, start_y = 100, 500

MAX_SEGMENT = 2

class CPrismaticTest(object):
	def __init__(self):
		import rabbit_scene
		# 创建一个固定物体
		self.ground = iphy2d.body(iphy2d.POLYGON, (math3d.vector2(0, 46), math3d.vector2(68, 46)))
		self.ground.body_type = iphy2d.STATIC_BODY
		self.ground.pos = (10, 15)

		self.body = rabbit_scene.create_obj("obj",3, start_x, start_y)

	def restart(self):
		self.body.pos = (start_x, start_y)
		# 示范移动关节
		axis = math3d.vector2(2, 1)
		axis.normalize()
		dj = iphy2d.prismatic_joint(self.ground, self.body.phy, \
				axis = axis, enable_motor=True, motor_speed=10, max_torque = 1000, \
				enable_limit=True, min_translation=0, max_translation=20)
		self.dj = dj


	def destroy(self):
		self.ground.destroy()
		self.body.destroy()

def start():
	global testobj
	if testobj is None:
		testobj = CPrismaticTest()
	testobj.restart()


def destroy():
	global testobj
	if testobj:
		testobj.destroy()
		testobj = None

