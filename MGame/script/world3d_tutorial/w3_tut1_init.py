# -*- coding:GBK -*-

# 加载模型

import idemo_demo
import idemo_glb
import iworld2d
import iworld3d

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
		self.player = None
	
	def init(self, browser):
		super(demo, self).init(browser)
		iworld2d.init()
		# 3D场景在第三层
		iworld3d.init()
		iworld3d.add_scene_to_layer2d(SCENE_LAYER)
		# 演示一个3D模型的生成
		self.player = iworld3d.model3d("idemos/res/eggyolk/world3d/xiaodanhuang.gim", "xdh", SCENE_LAYER)
		self.player.pos = (0,0,-100)

	# 销毁函数
	def destroy(self):
		self.player.destroy()
		self.player = None
		self.text = None
		iworld3d.destroy()
		iworld2d.destroy()


