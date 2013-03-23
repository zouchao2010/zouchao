# -*- coding:GBK -*-
import idemo_glb
import idemo_demo
import rabbit_scene

inst = None

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
		pass
	
	def init(self, browser):
		super(demo, self).init(browser)
		# 游戏场景初始化并且创建地图
		rabbit_scene.init()
		rabbit_scene.create_map()

	# 销毁函数
	def destroy(self):
		super(demo, self).destroy()
		rabbit_scene.destroy_scene()
		import idemo_glb
		idemo_glb.API.show_performance(False)

	# 逻辑帧
	def logic(self):
		rabbit_scene.update()
	
	# 逻辑帧后处理
	def post_logic(self):
		pass
	
	# 渲染帧
	def render(self):
		pass
	
	# 键盘消息
	def on_key_msg(self, msg, key):
		super(demo, self).on_key_msg(msg, key)
		rabbit_scene.on_key_msg(msg, key)

	# 鼠标按键
	def on_mouse_msg(self, msg, key):
		rabbit_scene.on_mouse_msg(msg, key)
	
	# 鼠标滚轮
	def on_mouse_wheel(self, msg, delta, key_state):
		pass