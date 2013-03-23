# -*- coding:GBK -*-
# 创建客户端程序的结构
import idemo_demo
import random
import flashui
import iworld2d
import iworld3d
import math3d
import game

inst = None

FLA_RES = 'idemos/res/HPBar/hp.swf'
BACK_IMG = 'idemos/res/HPBar/hp.txg|white'
FRONT_IMG = 'idemos/res/HPBar/hp.txg|red'
MODEL_RES = 'idemos/res/HPBar/xuetiao.gim'
TEXT_RES = 'idemos/res/HPBar/xuetiao/xuetiao_%02d.dds'
SPR2D_RES = 'idemos/res/HPBar/xuetiao/xuetiao.sp2'

def init(browser):
	global inst
	if inst is None:
		iworld2d.init()
		iworld3d.init()
		iworld3d.add_scene_to_layer2d(1)
		inst = demo()
		inst.init(browser)

def destroy():
	global inst
	if inst:
		inst.destroy()
		iworld3d.destroy()
		iworld2d.destroy()
		inst = None

# 2dflash版血条
class flaHP(object):
	def __init__(self):
		self.obj = flashui.movie(FLA_RES)
		self.obj.enable_keyboard = False
		self.obj.enbale_mouse = False
		self.obj.align = flashui.Align_TopLeft
		self.x = -1
		self.hp = 1
	
	def rand_init(self):
		x, y = random.randint(0, 1024), random.randint(0, 768)
		self.x = x
		self.obj.set_variable('_x', x)
		self.obj.set_variable('_y', y)
	
	def destroy(self):
		del self.obj
	
	def set_pos(self, x):
		self.obj.set_variable('_x', x)
		self.x = x
	
	def set_hp(self, hp):
		self.obj.set_variable('hp._width', int(100 * hp))
		self.hp = hp
	
	def logic(self):
		if self.x > 1024:
			self.set_pos(0)
		else:
			self.set_pos(self.x + 2)
		if self.hp <= 0:
			self.hp = 1
		else:
			self.set_hp(self.hp - 0.01)

# image2d版本血条
class img2dHP(object):
	def __init__(self):
		self.obj = iworld2d.empty2d()
		self.b = iworld2d.image2d(BACK_IMG)
		self.f = iworld2d.image2d(FRONT_IMG)
		self.f.rlevel = 1
		self.b.attach_to_parent(self.obj)
		self.f.attach_to_parent(self.obj)
		self.x = -1
		self.hp = -1
	
	def rand_init(self):
		x, y = random.randint(0, 1024), random.randint(0, 768)
		self.x = x
		self.obj.pos = x, y
	
	def destroy(self):
		self.b.destroy()
		self.f.destroy()
		self.obj.destroy()
		self.b = self.f = self.obj = None
	
	def set_pos(self, x):
		self.obj.pos = x, self.obj.pos[1]
		self.x = x
		
	def set_hp(self, hp):
		self.f.scale = (hp, 1)
		self.hp = hp
	
	def logic(self):
		if self.x > 1024:
			self.set_pos(0)
		else:
			self.set_pos(self.x + 2)
		if self.hp <= 0:
			self.hp = 1
		else:
			self.set_hp(self.hp - 0.01)

# spr2d版
class spr2dHP(img2dHP):
	def __init__(self):
		self.obj = iworld2d.sprite2d(SPR2D_RES)
		self.hp = -1
	
	def destroy(self):
		self.obj.destroy()
		self.obj = None
	
	def set_hp(self, hp):
		self.obj.set_frame(int(hp * 21))
		self.hp = hp
	
		
# 3Dflash版本
class fla3dHP(object):
	def __init__(self):
		self.obj = iworld3d.space_movie(FLA_RES)
		self.obj.billboard_type = True
		self.hp = -1
		
	def rand_init(self):
		x = random.random() * 50 * random.choice([-1, 1])
		y = random.random() * 40 * random.choice([-1, 1])
		z = (random.random() + 0.2) * -200
		self.obj.position = math3d.vector(x, y, z)
	
	def destroy(self):
		self.obj.destroy()
		self.obj = None
	
	def set_pos(self, x):
		pass
	
	def set_hp(self, hp):
		self.obj.movie.set_variable('hp._width', int(100 * hp))
		self.hp = hp
	
	def logic(self):
		if self.obj.position.x > 50:
			self.obj.position = math3d.vector(-50, self.obj.position.y, self.obj.position.z)
		else:
			self.obj.position = math3d.vector(self.obj.position.x + 1, self.obj.position.y, self.obj.position.z)
			
		if self.hp <= 0:
			self.hp = 1
		else:
			self.set_hp(self.hp - 0.01)

# 3D面片血条
class modelHP(fla3dHP):
	def __init__(self):
		self.obj = iworld3d.model3d(MODEL_RES)
		self.hp = -1
		self.obj.set_submesh_texture(0, TEXT_RES % 20)
	
	def set_hp(self, hp):
		self.obj.set_submesh_texture(0, TEXT_RES % int(hp * 21))
		self.hp = hp
	
class demo(idemo_demo.demo):
	def __init__(self):
		super(demo, self).__init__()
		self.objs = []
		
	def init(self, browser):
		super(demo, self).init(browser)
		
	def create_fla(self, n):
		for i in xrange(n):
			f = flaHP()
			f.rand_init()
			self.objs.append(f)
	
	def create_img2d(self, n):
		for i in xrange(n):
			o = img2dHP()
			o.rand_init()
			self.objs.append(o)
	
	def create_spr2d(self, n):
		for i in xrange(n):
			o = spr2dHP()
			o.rand_init()
			self.objs.append(o)
	
	def create_fla3d(self, n):
		for i in xrange(n):
			o = fla3dHP()
			o.rand_init()
			self.objs.append(o)
	
	def create_model3d(self, n):
		for i in xrange(n):
			o = modelHP()
			o.rand_init()
			self.objs.append(o)
	
	# 销毁函数
	def destroy(self):
		for o in self.objs:
			o.destroy()
		self.objs = []

	# 逻辑帧
	def logic(self):
		for o in self.objs:
			o.logic()
	
	# 逻辑帧后处理
	def post_logic(self):
		pass
	
	# 渲染帧
	def render(self):
		pass
	
	# 键盘消息
	def on_key_msg(self, msg, key):
		super(demo, self).on_key_msg(msg, key)
		if msg == game.MSG_KEY_DOWN and key == game.VK_1:
			self.destroy()
			self.create_fla(300)
		if msg == game.MSG_KEY_DOWN and key == game.VK_2:
			self.destroy()
			self.create_img2d(300)
		if msg == game.MSG_KEY_DOWN and key == game.VK_3:
			self.destroy()
			self.create_spr2d(300)
		if msg == game.MSG_KEY_DOWN and key == game.VK_4:
			self.destroy()
			self.create_fla3d(300)
		if msg == game.MSG_KEY_DOWN and key == game.VK_5:
			self.destroy()
			self.create_model3d(300)
		

	# 鼠标按键
	def on_mouse_msg(self, msg, key):
		pass
	
	# 鼠标滚轮
	def on_mouse_wheel(self, msg, delta, key_state):
		pass