# -*- coding:GBK -*-

# 2D/3D�����Ⱦ

import idemo_demo
import idemo_glb
import iworld2d
import iworld3d
import math

inst = None

SCENE_LAYER = 2

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
		self.bgs = []
		self.player = None
	
	def init(self, browser):
		super(demo, self).init(browser)
		
		# ����4��ͼ�㣬0/1/3��Ϊ2Dͼ��
		# 2���ǹҽ�һ��3D����������3Dģ�͵���ʾ
		iworld2d.init(4)
		self.bgs.append(iworld2d.image2d("idemos/res/eggyolk/bg/bg_far.png", layer_id=0))
		self.bgs.append(iworld2d.image2d("idemos/res/eggyolk/bg/bg_mid.png", layer_id=1))
		self.bgs.append(iworld2d.image2d("idemos/res/eggyolk/bg/bg_near.png", layer_id=3))
		self.bgs[1].pos = (0, 260)
		self.bgs[2].pos = (0, 580)
		
		# 3D�����ڵ�����
		iworld3d.init()
		iworld3d.add_scene_to_layer2d(SCENE_LAYER)
		
		# ��ʾһ��3Dģ�͵�����
		self.player = iworld3d.model3d("idemos/res/eggyolk/world3d/xiaodanhuang.gim", "xdh", SCENE_LAYER)
		self.player.pos = (-8,48,-100)	# ��λ�øպñ�ǰ���㵲��
		self.player.rotate_to_xyz(y=math.pi)

	# ���ٺ���
	def destroy(self):
		for b in self.bgs:
			b.destroy()
		self.bgs = []
		self.player.destroy()
		self.player = None
		self.text = None
		iworld3d.destroy()
		iworld2d.destroy()