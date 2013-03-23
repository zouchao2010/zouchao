# -*- coding:GBK -*-
# demo的浏览器
import idemos_cfg
import idemo_glb
import game
import flashui

STATE_READY = 0		# 就绪
STATE_RUNNING = 1	# 运行

class browser(object):
	def __init__(self):
		self.cur_demo = None			# 当前的demo
		self.demo_state = STATE_READY	# 游戏的状态
		self.demo_mod = None			# 当前demo所在的模块
		self.camera_man = None			# 相机控制
		self.movie = flashui.movie("idemos/res/common/ui/idemos.swf")
		self.movie.enable_keyboard = False
		
	def init(self):
		idemo_glb.API.set_background_color(0x606060l)
		self.init_ui()
		
	def destroy(self):
		self.end_demo()
		self.cur_demo = None
		self.demo_state = STATE_READY
		self.demo_mod = None
		if self.camera_man:
			self.camera_man.destroy()
			self.camera_man = None
		del self.movie
		self.movie = None
	
	def init_ui(self):
		pos = (20, 100)
		i = 0
		keys = idemos_cfg.CFG.keys()
		keys.sort()
		titles = []
		descs = []
		cats1 = []
		cats2 = []
		pics = []
		for k in keys:
			v = idemos_cfg.CFG[k]
			titles.append(v["title"])
			descs.append(v["desc"])
			cats1.append(v["category1"])
			cats2.append(v["category2"])
			pics.append(v["thumbnail"])
		self.movie.set_variable("demo_names", keys)
		self.movie.set_variable("titles", titles)
		self.movie.set_variable("descs", descs)		
		self.movie.set_variable("categories1", cats1)
		self.movie.set_variable("categories2", cats2)
		self.movie.set_variable("pics", pics)
		self.movie.invoke("init")

	def start_demo(self, name):
		try:
			self.movie.set_variable("_visible", False)
			self.demo_mod = __import__(name + "_init")
			reload(self.demo_mod)
			self.cur_name = name
			self.demo_mod.init(self)
			self.cur_demo = self.demo_mod.inst
			self.demo_state = STATE_RUNNING
		except:
			import traceback
			print traceback.format_exc()
			idemo_glb.API.show_alert("DEMO 启动失败！")
	
	def end_demo(self):
		if self.cur_demo and self.demo_state == STATE_RUNNING:
			idemo_glb.API.set_background_color(0x606060l)
			self.movie.set_variable("_visible", True)
			self.demo_state = STATE_READY
			self.demo_mod.destroy()
			self.cur_demo = None

	def logic(self):
		if self.cur_demo and self.demo_state == STATE_RUNNING:
			self.cur_demo.logic()
		if self.camera_man:
			self.camera_man.logic()
		
	def post_logic(self):
		if self.cur_demo and self.demo_state == STATE_RUNNING:
			self.cur_demo.post_logic()
		
	def render(self):
		if self.cur_demo and self.demo_state == STATE_RUNNING:
			self.cur_demo.render()
		
	def on_key_msg(self, msg, key):
		if self.cur_demo and self.demo_state == STATE_RUNNING:
			self.cur_demo.on_key_msg(msg, key)
			if self.camera_man:
				self.camera_man.on_key_msg(msg, key)
			return
		if self.demo_state == STATE_READY:
			if msg == game.MSG_KEY_DOWN and key == game.VK_ESCAPE:
				idemo_glb.API.exit_and_join()

	def on_mouse_msg(self, msg, key):
		if self.cur_demo and self.demo_state == STATE_RUNNING:
			self.cur_demo.on_mouse_msg(msg, key)
		if self.camera_man:
			self.camera_man.on_mouse_msg(msg, key)

	def on_mouse_wheel(self, msg, delta, key_state):
		if self.cur_demo and self.demo_state == STATE_RUNNING:
			self.cur_demo.on_mouse_wheel(msg, delta, key_state)
		if self.camera_man:
			self.camera_man.on_mouse_wheel(msg, delta, key_state)