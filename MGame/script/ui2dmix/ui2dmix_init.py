# -*- coding:GBK -*-
# 创建客户端程序的结构
import idemo_demo
import iworld2d


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

def f1():
	print "鼠标左键点击"

def f2():
	print "鼠标右键点击"

def f3():
	print "鼠标进入"

def f4():
	print "鼠标移出"

class demo(idemo_demo.demo):
	def __init__(self):
		super(demo, self).__init__()
		pass
	
	def init(self, browser):
		super(demo, self).init(browser)
		iworld2d.init()
		self.ui_id = iworld2d.canvases.create_canvas_ui(3)
		self.ui = iworld2d.canvases.get_canvas_ui(self.ui_id)
		self.image = iworld2d.image2d("idemos/res/actiondemo/demo.txg|background", layer_id = 0, ui_id = self.ui_id)
		self.model = iworld2d.model2d("idemos/res/rabbit/world2d/2dmodel/tutu.2dm", layer_id = 1, ui_id = self.ui_id)
		self.model.pos = (400, 400)
		self.sprite = iworld2d.sprite2d("idemos/res/rabbit/world2d/sprite/bomb.sp2", ui_id = self.ui_id)
		self.sprite.pos = (400, 400)
		self.sprite.play()
		self.sprite.set_loop(True)
		self.par = iworld2d.particle2d("idemos/res/rabbit/world2d/par/testmuti.par", "", 1, ui_id = self.ui_id)
		self.par.pos = (200,300)
		self.par.restart()
		self.ui.set_pos(100, 100)
		self.ui.set_size(1024/2,768/2)
		self.ui.set_view_size(1024, 768)
		self.ui.set_view_pos_center(1024 / 2, 768/2)
		self.ui.set_click_func(f1)
		self.ui.set_right_click_func(f2)
		self.ui.set_roll_over_func(f3)
		self.ui.set_roll_out_func(f4)
		
	# 销毁函数
	def destroy(self):
		self.image.destroy()
		self.model.destroy()
		self.sprite.destroy()
		self.par.destroy()
		iworld2d.canvases.destroy_canvas_ui(self.ui_id)
		iworld2d.destroy()

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