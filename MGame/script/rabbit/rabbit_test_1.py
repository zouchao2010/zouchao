# -*- coding:GBK -*-

import math
import math3d
import rabbit_obj
import iworld2d
import iphy2d

testobj = None

length = 200

start_x, start_y = 300, 300

class CWebTest(object):
	def __init__(self):
		import rabbit_scene
		# 创建网上的4个body
		self.body = []
		self.body.append(rabbit_scene.create_obj("obj", 7, 100, 100))
		self.body.append(rabbit_scene.create_obj("obj", 7, 300, 100))
		self.body.append(rabbit_scene.create_obj("obj", 7, 100, 300))
		self.body.append(rabbit_scene.create_obj("obj", 7, 300, 300))
		# 创建一个固定物体
		self.ground = iphy2d.body(iphy2d.POLYGON, (math3d.vector2(start_x-length, 1), math3d.vector2(start_x+length+length, 1)))
		self.ground.body_type = iphy2d.STATIC_BODY
		self.ground.pos = (0, 0)

	def restart(self):
		line_length = math3d.vector2((length/2-13)/rabbit_obj.MAP_SCALE, (length/2-15)/rabbit_obj.MAP_SCALE).length
		# 重置4个body位置
		self.body[0].pos = (start_x, start_y)
		self.body[1].pos = (start_x+length, start_y)
		self.body[2].pos = (start_x, start_y+length)
		self.body[3].pos = (start_x+length, start_y+length)

		# 四个body分别连接到ground上
		self.dj_lst = []
		p1 = math3d.vector2((start_x-length/2)/15, (start_y-length/2)/15)
		p2 = math3d.vector2(-13/rabbit_obj.MAP_SCALE, -12/rabbit_obj.MAP_SCALE)
		dj = iphy2d.distance_joint(self.ground, self.body[0].phy, \
				anchor_a=p1, anchor_b=p2, len=line_length, fre=2, damp=0.5)
		self.dj_lst.append(dj)

		p1 = math3d.vector2((start_x+length+length/2)/15, (start_y-length/2)/15)
		p2 = math3d.vector2(13/rabbit_obj.MAP_SCALE, -12/rabbit_obj.MAP_SCALE)
		dj = iphy2d.distance_joint(self.ground, self.body[1].phy, \
				anchor_a=p1, anchor_b=p2, len=line_length, fre=2, damp=0.5)
		self.dj_lst.append(dj)

		p1 = math3d.vector2((start_x-length/2)/15, (start_y+length+length/2)/15)
		p2 = math3d.vector2(-13/rabbit_obj.MAP_SCALE, 12/rabbit_obj.MAP_SCALE)
		dj = iphy2d.distance_joint(self.ground, self.body[2].phy, \
				anchor_a=p1, anchor_b=p2, len=line_length, fre=2, damp=0.5)
		self.dj_lst.append(dj)

		p1 = math3d.vector2((start_x+length+length/2)/15, (start_y+length+length/2)/15)
		p2 = math3d.vector2(13/rabbit_obj.MAP_SCALE, 12/rabbit_obj.MAP_SCALE)
		dj = iphy2d.distance_joint(self.ground, self.body[3].phy, \
				anchor_a=p1, anchor_b=p2, len=line_length, fre=2, damp=0.5)
		self.dj_lst.append(dj)

		# 用四条边连接四个body
		line_length = length/rabbit_obj.MAP_SCALE
		dj = iphy2d.distance_joint(self.body[0].phy, self.body[1].phy, \
				len=line_length, fre=2, damp=0.5)
		self.dj_lst.append(dj)
		dj = iphy2d.distance_joint(self.body[1].phy, self.body[3].phy, \
				len=line_length, fre=2, damp=0.5)
		self.dj_lst.append(dj)
		dj = iphy2d.distance_joint(self.body[3].phy, self.body[2].phy, \
				len=line_length, fre=2, damp=0.5)
		self.dj_lst.append(dj)
		dj = iphy2d.distance_joint(self.body[2].phy, self.body[0].phy, \
				len=line_length, fre=2, damp=0.5)
		self.dj_lst.append(dj)


	def destroy(self):
		self.ground.destroy()
		for b in self.body:
			b.destroy()
		self.body = []

def start():
	global testobj
	if testobj is None:
		testobj = CWebTest()
	testobj.restart()

def destroy():
	global testobj
	if testobj:
		testobj.destroy()
		testobj = None

