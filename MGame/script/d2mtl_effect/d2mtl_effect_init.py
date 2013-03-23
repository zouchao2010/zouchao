# -*- coding:GBK -*-
# 创建客户端程序的结构
import idemo_demo
import flashui
import d2mtl_effect_cfg
import iworld2d

inst = None
param_key = -1

def init(browser):
	global inst
	if inst is None:
		inst = demo()
		inst.init(browser)

def destroy():
	if inst:
		inst.destroy()

class demo(idemo_demo.demo):
	def __init__(self):
		super(demo, self).__init__()
		self.movie = None
		self.image = None
		self.back = None
		self.effect_id = -1 # 效果id
	
	def init(self, browser):
		super(demo, self).init(browser)
		iworld2d.init()
		self.movie = flashui.movie("idemos/res/d2mtl_effect/ui/ui.swf", True, True, flashui.SM_NoScale)
		self.movie.enable_keyboard = False
		self.image = iworld2d.image2d("idemos/res/d2mtl_effect/background.jpg")
		self.back = iworld2d.image2d("idemos/res/eggyolk/bg/bg_far.png")
		self.image.rlevel = 1
		self.image.scale = (0.5, 0.5)
		self.image.pos = (1024 / 2, 768 / 2)
		self.image.key_point = (0, 0)
		txts = ["原图", ]
		ids = [0, ]
		for k, v in d2mtl_effect_cfg.config.iteritems():
			ids.append(k)
			txts.append(v["name"])
		self.movie.set_array("effect_ids", ids)
		self.movie.set_array("effect_menu.dataProvider", txts)
		self.set_effect(0)

	# 销毁函数
	def destroy(self):
		del self.movie
		self.movie = None
		self.image.destroy()
		self.image = None
		self.back.destroy()
		self.back = None
		iworld2d.destroy()
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
		super(demo, self).on_key_msg(msg, key)

	# 鼠标按键
	def on_mouse_msg(self, msg, key):
		pass
	
	# 鼠标滚轮
	def on_mouse_wheel(self, msg, delta, key_state):
		pass
	
		# 初始化设置界面
	def set_effect_fla(self, i):
		cfg = d2mtl_effect_cfg.config.get(i, None)
		self.movie.invoke("init", len(cfg) - 1)
		if cfg is None:
			return
		for k, v in cfg.iteritems():
			if k == "name":
				continue
			self.movie.set_variable("index", k)
			self.movie.set_variable("txt", v["txt"])
			self.movie.set_variable("min", v["min"])
			self.movie.set_variable("max", v["max"])
			self.movie.set_variable("pos", v["default"])
			self.movie.invoke("set_control_arg")
	
	# 设置效果
	def set_effect(self, i):
		if not i:
			self.image.cancel_common_effect()
			self.movie.invoke("init", 0)
			return
		self.effect_id = i
		self.image.set_common_effect(i)
		self.set_effect_fla(i)

def set_effect_param_key(key):
	global param_key
	param_key = key

def set_effect_param_value(value):
	if inst and inst.effect_id != -1:
		# 改变配置的值
		cfg = d2mtl_effect_cfg.config[inst.effect_id]
		cfg[param_key]["value"] = value * 1.0 / cfg[param_key]["scale"]
		# hsv调节
		if inst.effect_id == 4:
			h = cfg[0]["value"]
			s = cfg[1]["value"]
			v = cfg[2]["value"]
			inst.image.set_com_effect_params(hue_delta = h, saturation = s, lightness = v)
			return
		# 水波调节
		if inst.effect_id == 5:
			t = cfg[0]["value"]
			w = cfg[1]["value"]
			a = cfg[2]["value"]
			inst.image.set_com_effect_params(wave_time = t, wave_size = w, amplitude = a, is_h = True, is_v = True)
			return
		# 漩涡调节
		if inst.effect_id == 6:
			x = cfg[0]["value"]
			y = cfg[1]["value"]
			s = cfg[2]["value"]
			inst.image.set_com_effect_params(center = (x, y), strength = s)
			return
		# 波纹调节
		if inst.effect_id == 7:
			x = cfg[0]["value"]
			y = cfg[1]["value"]
			a = cfg[2]["value"]
			f = cfg[3]["value"]
			inst.image.set_com_effect_params(center = (x, y), amplitude = a, frequency = f)
			return
		# 马赛克
		if inst.effect_id == 8:
			x = cfg[0]["value"]
			y = cfg[1]["value"]
			inst.image.set_com_effect_params(pixel_count = (x, y))
			return


def set_effect(i):
	if inst:
		inst.effect_id = i
		inst.set_effect(i)

