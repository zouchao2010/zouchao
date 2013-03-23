# -*- coding:GBK -*-

# ��ͷ����

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
		# 3D�����ڵ�����
		iworld3d.init()
		iworld3d.add_scene_to_layer2d(SCENE_LAYER)
		# ��ʾһ��3Dģ�͵�����
		self.player = iworld3d.model3d("idemos/res/eggyolk/world3d/xiaodanhuang.gim", "xdh", SCENE_LAYER)
		self.player.pos = (0,0,-100)
		self.cam_rot = 0
		# ��������ʯͷ
		self.stones = []
		for pos in ((0,0,-100),(20,30,-100),(-20,-30,-100)):
			stone =iworld3d.model3d("idemos/res/eggyolk/world3d/dalumian.gim", layer_id=SCENE_LAYER)
			stone.scale = (0.1,0.1,0.1) # ԭ��ģ��̫����Ҫ��С
			stone.pos = pos
			self.stones.append(stone)

	# ���ٺ���
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
				# ���������ʾ
				# С����46��ʾ�����x������ƽ��
				# С����28��ʾ�����y������ƽ��
				# С����13��ʾ�����z��ǰ��ƽ��
				# С����79��ʾ�����y��������ת
				# С����5��ʾ�����׼����С����
				# С����0��ʾ����ָ���ʼ״̬
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
					# ��ԭλ��
					position = math3d.vector(0,0,0)
					forward = math3d.vector(0,0,-1)
					up = math3d.vector(0,-1,0)
					# ��ԭ��ת����
					# ��ʾrotation_matrix���÷�
					cam.rotation_matrix = math3d.matrix.make_orient(forward, up)
					# ʵ���ϴ��÷���ͬ������ӿ�
					#iworld3d.set_camera_placement(SCENE_LAYER, position, forward, up)
				cam.position = position
