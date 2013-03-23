# -*- coding:GBK -*-

# 对模型进行操作

# -*- coding:GBK -*-
# 创建客户端程序的结构
import idemo_demo
import idemo_glb
import iworld2d
import iworld3d
import ifxpool
import game
import math
import random

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
		self.bgs = []
		self.player = None
		self.rot = 4
		self.perform_flag = False
	
	def init(self, browser):
		super(demo, self).init(browser)
		
		# 设置4个图层，0/1/3作为2D图层
		# 2则是挂接一个3D场景，用于3D模型的演示
		iworld2d.init(4)
		self.bgs.append(iworld2d.image2d("idemos/res/eggyolk/bg/bg_far.png", layer_id=0))
		self.bgs.append(iworld2d.image2d("idemos/res/eggyolk/bg/bg_mid.png", layer_id=1))
		self.bgs.append(iworld2d.image2d("idemos/res/eggyolk/bg/bg_near.png", layer_id=3))
		self.bgs[1].pos = (0, 260)
		self.bgs[2].pos = (0, 580)
		
		# 3D场景在第三层
		iworld3d.init()
		iworld3d.add_scene_to_layer2d(SCENE_LAYER)

		self.create_player()

	def create_player(self):
		# 演示一个3D模型的生成
		self.player = iworld3d.model3d("idemos/res/eggyolk/world3d/xiaodanhuang.gim", "xdh", SCENE_LAYER)
		self.player.pos = (-8,48,-100)	# 此位置刚好被前景层挡着
		self.player.rotate_to_xyz(y=math.pi)

	# 销毁函数
	def destroy(self):
		for b in self.bgs:
			b.destroy()
		self.bgs = []
		self.player.destroy()
		self.player = None
		self.text = None
		iworld3d.destroy()
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
		if msg == game.MSG_KEY_PRESSED:
			if key == game.VK_A:
				pos = self.player.pos
				self.player.pos = (pos[0]-1, pos[1], pos[2])
			elif key == game.VK_D:
				pos = self.player.pos
				self.player.pos = (pos[0]+1, pos[1], pos[2])
			elif key == game.VK_W:
				pos = self.player.pos
				self.player.pos = (pos[0], pos[1]-1, pos[2])
				
			elif key == game.VK_S:
				pos = self.player.pos
				self.player.pos = (pos[0], pos[1]+1, pos[2])
				
			elif key == game.VK_Z:
				pos = self.player.pos
				self.player.pos = (pos[0], pos[1], pos[2]+1)
			elif key == game.VK_X:
				pos = self.player.pos
				self.player.pos = (pos[0], pos[1], pos[2]-1)
		elif msg == game.MSG_KEY_UP:
			if key == game.VK_F1:
				if self.player:
					# 随机播放一个动作
					aname = random.choice(("npc_act_001", "npc_act_003", "npc_act_004", "npc_act_005", ))
					print "change animation", aname, self.player.pos
					self.player.play_animation(aname)
			elif key == game.VK_F7:
				self.perform_flag = not self.perform_flag
				idemo_glb.API.show_performance(self.perform_flag)
			elif key == game.VK_1:
				# 模型旋转演示，每次旋转45度
				self.rot = (self.rot+1)%8
				self.player.rotate_to_xyz(y=math.pi/4*self.rot)