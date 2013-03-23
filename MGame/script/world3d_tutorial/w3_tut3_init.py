# -*- coding:GBK -*-
# 特效

import idemo_demo
import idemo_glb
import iworld2d
import iworld3d
import ifxpool
import game

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
	
	def init(self, browser):
		super(demo, self).init(browser)
		iworld2d.init()
		# 3D场景在第三层
		iworld3d.init()
		iworld3d.add_scene_to_layer2d(SCENE_LAYER)

	# 销毁函数
	def destroy(self):
		self.text = None
		iworld3d.destroy()
		iworld2d.destroy()

	# 鼠标按键
	def on_mouse_msg(self, msg, key):
		if msg == game.MSG_MOUSE_DOWN:
			# 3D特效演示
			p0, dir = iworld3d.screen_to_world(SCENE_LAYER, game.mouse_x, game.mouse_y)
			dir.normalize(100)
			pos = p0 + dir	# 计算鼠标点击的屏幕位置，到实际场景中世界坐标
			sid = ifxpool.create_play_once_fx("idemos/res/eggyolk/fx/lizi.sfx")	# 生成一个特效
			sobj = ifxpool.get_fx_obj(sid)
			sobj.restart()	# 播放
			sobj.position = pos
