# -*- coding:GBK -*-
import game
import idemo_glb
import idemos_cfg
# demo的信息
class info(object):
	def __init__(self):
		self.title = "undefined"
		self.desc = "undefined"
		self.thumbnail = "undefined"
		self.category1 = "undefined"
		self.category2 = "undefined"

# demo的基类
class demo(object):
	def __init__(self):
		self.info = info()
	
	# -------------------------------------------------
	# ----------------可重写函数-----------------------
	# 初始化函数
	def init(self, browser):
		self.browser = browser
		cfg = idemos_cfg.CFG[browser.cur_name]
		self.info.title = cfg["title"]
		self.info.desc = cfg["desc"]
		self.info.desc += "\nESC  退出该demo"
		self.info.thumbnail = cfg["thumbnail"]
		self.info.category1 = cfg["category1"]
		self.info.category1 = cfg["category2"]
		
		self.text = idemo_glb.API.get_text_panel()
		self.text.set_text(self.info.desc)
		self.text.set_coord((30, 40))

	# 销毁函数
	def destroy(self):
		self.text = None
	
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
		if msg == game.MSG_KEY_DOWN and key == game.VK_ESCAPE:
			self.browser.end_demo()

	# 鼠标按键
	def on_mouse_msg(self, msg, key):
		pass
	
	# 鼠标滚轮
	def on_mouse_wheel(self, msg, delta, key_state):
		pass