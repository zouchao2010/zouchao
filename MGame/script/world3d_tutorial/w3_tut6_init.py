# -*- coding:GBK -*-

# 镜头控制

import idemo_demo
import idemo_glb
import iworld2d
import iworld3d
import game
import math
import math3d

inst = None

SCENE_LAYER = 2
CAMERA_MOVE_STEP = 1

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
		self.player = None
	
	def init(self, browser):
		super(demo, self).init(browser)
		iworld2d.init()
		# 3D场景在第三层
		iworld3d.init()
		iworld3d.add_scene_to_layer2d(SCENE_LAYER)
		# 演示一个3D模型的生成
		self.player = iworld3d.model3d("idemos/res/eggyolk/world3d/xiaodanhuang.gim", "xdh", SCENE_LAYER)
		self.player.pos = (0,0,-100)
		self.cam_rot = 0
		# 增加三块石头
		self.stones = []
		for pos in ((0,0,-100),(20,30,-100),(-20,-30,-100)):
			stone =iworld3d.model3d("idemos/res/eggyolk/world3d/dalumian.gim", layer_id=SCENE_LAYER)
			stone.scale = (0.1,0.1,0.1) # 原来模型太大，需要缩小
			stone.pos = pos
			self.stones.append(stone)

	# 销毁函数
	def destroy(self):
		self.player.destroy()
		self.player = None
		for s in self.stones:
			s.destroy()
		self.stones = None
		self.text = None
		iworld3d.destroy()
		iworld2d.destroy()

	def on_key_msg(self, msg, key):
		super(demo, self).on_key_msg(msg, key)
		if msg == game.MSG_KEY_PRESSED:
			if key >= game.VK_NUM0 and key <= game.VK_NUM9:
				# 相机控制演示
				# 小键盘46表示相机沿x轴左右平移
				# 小键盘28表示相机沿y轴上下平移
				# 小键盘13表示相机沿z轴前后平移
				# 小键盘79表示相机沿y轴左右旋转
				# 小键盘5表示相机对准主角小蛋黄
				# 小键盘0表示相机恢复初始状态
				cam = iworld3d.get_camera(SCENE_LAYER)
				position = cam.position
				if key == game.VK_NUM4:
					position.x -= CAMERA_MOVE_STEP
				elif key == game.VK_NUM6:
					position.x += CAMERA_MOVE_STEP
				elif key == game.VK_NUM8:
					position.y -= CAMERA_MOVE_STEP
				elif key == game.VK_NUM2:
					position.y += CAMERA_MOVE_STEP
				elif key == game.VK_NUM1:
					position.z += CAMERA_MOVE_STEP
				elif key == game.VK_NUM3:
					position.z -= CAMERA_MOVE_STEP
				elif key == game.VK_NUM7:
					self.cam_rot -= 1
					cam.rotate_to_xyz(y=self.cam_rot*math.pi/200)
				elif key == game.VK_NUM9:
					self.cam_rot += 1
					cam.rotate_to_xyz(y=self.cam_rot*math.pi/200)
				elif key == game.VK_NUM5:
					cam.look_at(self.player.position)
				elif key == game.VK_NUM0:
					# 还原位置
					position = math3d.vector(0,0,0)
					forward = math3d.vector(0,0,-1)
					up = math3d.vector(0,-1,0)
					# 还原旋转矩阵
					# 演示rotation_matrix的用法
					cam.rotation_matrix = math3d.matrix.make_orient(forward, up)
					# 实际上此用法等同于这个接口
					#iworld3d.set_camera_placement(SCENE_LAYER, position, forward, up)
				cam.position = position
