# -*- coding:GBK -*-
# 创建客户端程序的结构
import idemo_demo

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
		pass

	# 销毁函数
	def destroy(self):
		pass

	# 逻辑帧
	def logic(self):
		pass
	
	# 逻辑帧后处理
	def post_logic(self):
		pass
	
	# 渲染帧
	def render(self):
		pass
	
	# 键盘消息
	def on_key_msg(self, msg, key):
		super(demo, self).on_key_msg(msg, key)

	# 鼠标按键
	def on_mouse_msg(self, msg, key):
		pass
	
	# 鼠标滚轮
	def on_mouse_wheel(self, msg, delta, key_state):
		pass