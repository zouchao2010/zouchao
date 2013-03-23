# -*- coding:GBK -*-
# 创建客户端程序的结构
import idemo_demo
import iworld3d
import math3d
import math

inst = None
scn_file = "idemos/res/itownroom/scene/room.scn"
gim_file = "idemos/res/eggyolk/world3d/xiaodanhuang.gim"
fx_file = "idemos/res/eggyolk/fx/lizi.sfx"

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

def f1(i):
	print "鼠标左键点击"
	if inst:
		inst.roll_model_left(i)
		
def f2(i):
	print "鼠标右键点击"
	if inst:
		inst.roll_model_right(i)

def f3():
	print "鼠标进入"

def f4():
	print "鼠标移出"

class demo(idemo_demo.demo):
	def __init__(self):
		super(demo, self).__init__()
		pass
	
	# 创建一个3d UI
	def create_3d_ui(self, depth):
		ui = iworld3d.create_scene3d_ui(scn_file, depth = depth)
		model = iworld3d.model3d(gim_file, "", ui.get_ui_id())
		fx = iworld3d.fx3d(fx_file, 1, layer_id = ui.get_ui_id())
		model.posistion = math3d.vector(0.0, 0.0, 0.0)
		fx.position = math3d.vector(0.0, 20.0, 0.0)
		fx.restart()
		sce = ui.get_scene()
		camera = sce.get_camera()
		camera.set_placement(
			model.position + math3d.vector(0.0, 20.0, 45.0),
			math3d.vector(0, 0, -1),
			math3d.vector(0, 1, 0))
		# 设置完场景信息后，更新一下
		ui.update()
		return ui, model
	
	def init(self, browser):
		super(demo, self).init(browser)
		iworld3d.init()
		self.ui1, self.model1 = self.create_3d_ui(1)
		
		# 设置UI的位置
		self.ui1.set_pos(100, 0)
		self.ui1.set_size(1024/2,768/2)
		self.ui1.set_click_func(f1, 1)
		self.ui1.set_right_click_func(f2, 1)
		self.ui1.set_roll_over_func(f3)
		self.ui1.set_roll_out_func(f4)
		
		self.ui2, self.model2 = self.create_3d_ui(4)
		# 设置UI的位置，坐标不能为负数
		self.ui2.set_pos(400, 300)
		self.ui2.set_size(1024/2,768/2)
		self.ui2.set_click_func(f1, 2)
		self.ui2.set_right_click_func(f2, 2)
		self.ui2.set_roll_over_func(f3)
		self.ui2.set_roll_out_func(f4)
		
		self.rot1 = 0
		self.rot2 = 0
		
	# 销毁函数
	def destroy(self):
		self.model1.destroy()
		iworld3d.destroy_scene3d_ui(self.ui1.get_ui_id())
		self.model2.destroy()
		iworld3d.destroy_scene3d_ui(self.ui2.get_ui_id())
		iworld3d.destroy()
	
	# 向左旋转模型
	def roll_model_left(self, i):
		if i == 1:
			self.rot1 += math.pi / 4
			if self.rot1 > math.pi * 2:
				self.rot1 = 0.0
			self.model1.rotate_to_xyz(y = self.rot1)
		if i == 2:
			self.rot2 += math.pi / 4
			if self.rot2 > math.pi * 2:
				self.rot2 = 0.0
			self.model2.rotate_to_xyz(y = self.rot2)
	
	# 向右旋转模型
	def roll_model_right(self, i):
		if i == 1:
			self.rot1 -= math.pi / 4
			if self.rot1 < 0:
				self.rot1 = math.pi * 2
			self.model1.rotate_to_xyz(y = self.rot1)
		if i == 2:
			self.rot2 -= math.pi / 4
			if self.rot2 < 0:
				self.rot2 = math.pi * 2
			self.model2.rotate_to_xyz(y = self.rot2)
		
	# 逻辑帧
	def logic(self):
		# 刷新界面
		if self.ui1:
			self.ui1.update()
		if self.ui2:
			self.ui2.update()
	
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