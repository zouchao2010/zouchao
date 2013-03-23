# -*- coding:GBK -*-

# ���demo��ʾ��򵥵�2D/3D�����Ⱦ����
# ʹ����3D��ģ�ͺ���Ч
import idemo_glb
import iworld2d
import iworld3d
import ifxpool
import game
import math
import random
import flashui
import iphy3d
import idemo_demo
import math3d
import eggyolk2_obj
import eggyolk2_player
import eggyolk2_const

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

CAMERA_MOVE_STEP = 1

class demo(idemo_demo.demo):
	def __init__(self):
		super(demo, self).__init__()
		self.stones = []
		self.cam_rot = 0
		self.bgs = None
		self.perform_flag = False
		self.player = None
		self.npc = None
		self.collision_draw = False
		self.down_keys = [False, False, False, False]

	def init(self, browser):
		super(demo, self).init(browser)
		# ����4��ͼ�㣬0/1/3��Ϊ2Dͼ��
		# ͼ��2���ǹҽ�һ��3D����������3Dģ�͵���ʾ
		iworld2d.init(4)
		self.bgs = []
		self.bgs.append(iworld2d.image2d("idemos/res/eggyolk/bg/bg_far.png", layer_id=0))
		self.bgs.append(iworld2d.image2d("idemos/res/eggyolk/bg/bg_mid.png", layer_id=1))
		self.bgs.append(iworld2d.image2d("idemos/res/eggyolk/bg/bg_near.png", layer_id=3))
		self.bgs[1].pos = (0, 260)
		self.bgs[2].pos = (0, 580)
		
		# 3D�����ڵ�����
		iworld3d.init()
		iworld3d.add_scene_to_layer2d(eggyolk2_const.SCENE_LAYER)
		self.create_objs()
	
	def destroy(self):
		super(demo, self).destroy()
		self.player.destroy()
		self.npc.destroy()
		for b in self.bgs:
			b.destroy()
		self.bgs = []
		self.player = None
		self.npc = None
		iworld3d.destroy()

	def create_player(self):
		p = eggyolk2_player.CGamePlayer()
		p.create_sprite("idemos/res/eggyolk/world3d/xiaodanhuang.gim", "xdh", eggyolk2_const.SCENE_LAYER)
		p.create_phy(eggyolk2_const.SCENE_LAYER)
		# ��Ϊԭģ������صģ������Ҫ���������ʾ������ƫ��
		p.set_sprite_key(0, 15, 0)
		p.sprite.rotate_to_xyz(y=math.pi) 
		return p

	def create_objs(self):
		self.player = self.create_player()
		self.player.pos = (17, -15, -100)
		self.npc = self.create_player()
		self.npc.pos = (30, 17, -100)
		self.npc.create_bill('idemos/res/eggyolk/gfx/bill.swf', "npc��ײ������Ŷ")
		
		# ��������ʯͷ
		for pos in ((0,0,-100),(20,30,-100),(-20,-30,-100)):
			stone = eggyolk2_obj.CGameObj()
			stone.create_sprite("idemos/res/eggyolk/world3d/dalumian.gim", "s1", eggyolk2_const.SCENE_LAYER)
			stone.create_phy(eggyolk2_const.SCENE_LAYER)
			stone.sprite.scale = (0.1,0.1,0.1) # ԭ��ģ��̫����Ҫ��С
			stone.sprite.accept_shadow(True)
			stone.pos = pos
			self.stones.append(stone)
		iphy3d.update(eggyolk2_const.SCENE_LAYER)

	def logic(self):
		if self.collision_draw:
			iphy3d.set_draw_range(eggyolk2_const.SCENE_LAYER, self.player.pos[0], self.player.pos[1], self.player.pos[2], 20)
		self.player.update()
		iphy3d.update(eggyolk2_const.SCENE_LAYER)

	def on_key_msg(self, msg, key):
		super(demo, self).on_key_msg(msg, key)
		if msg == game.MSG_KEY_PRESSED:
			if key == game.VK_A:
				self.player.moving_dir.x = -1
				self.player.moving_dir.y = 0
				self.player.moving_dir *= eggyolk2_const.MOVING_SPEED
				self.down_keys[0] = True
			elif key == game.VK_D:
				self.player.moving_dir.x = 1
				self.player.moving_dir.y = 0
				self.player.moving_dir *= eggyolk2_const.MOVING_SPEED
				self.down_keys[1] = True
			elif key == game.VK_W:
				self.player.moving_dir.x = 0
				self.player.moving_dir.y = -1
				self.player.moving_dir *= eggyolk2_const.MOVING_SPEED
				self.down_keys[2] = True
			elif key == game.VK_S:
				self.player.moving_dir.x = 0
				self.player.moving_dir.y = 1
				self.player.moving_dir *= eggyolk2_const.MOVING_SPEED
				self.down_keys[3] = True
			elif key == game.MOUSE_BUTTON_LEFT:
				self.player.mouse_pos = game.mouse_x, game.mouse_y
		elif msg == game.MSG_KEY_UP:
			is_adws_up = False
			if key == game.VK_F2:
				# F2 ����3D��ײ�е���ʾ(��ײ�е���ʾһ��Ϊ�߿���ʽ������debugʹ�ã������������ײ����ʾΪ�ȱ߰����壬
				# Բ�������ײ��Ϊ�������ߵ�)
				self.collision_draw = not self.collision_draw
				iphy3d.set_debug_draw(eggyolk2_const.SCENE_LAYER, self.collision_draw)
			elif key == game.VK_F3:
				# 0 -- ����Ӱ
				# 1 -- ԲӰ
				# 2 -- ƽ����Ӱ
				self.player.sprite.clear_shadows()
				eggyolk2_player.shadow_type = (eggyolk2_player.shadow_type + 1) % 3
				if eggyolk2_player.shadow_type == 1:
					self.player.add_round_shadow()
			elif key == game.VK_F4:
				# ��0�ŵƹ������һ������
				l = iworld3d.get_light(eggyolk2_const.SCENE_LAYER, "light_1")
				l.direction = math3d.vector(random.random()*2-1, -1, random.random()*2-1)	# �̶�y�᷽����ģ�����ֻ��self.npcͷ����ת
			elif key == game.VK_F7:
				self.perform_flag = not self.perform_flag
				idemo_glb.API.show_performance(self.perform_flag)
			elif key == game.VK_1:
				self.player.switch_phy_type(eggyolk2_const.COL_TYPE_CAPSULE, eggyolk2_const.SCENE_LAYER)
			elif key == game.VK_2:
				self.player.switch_phy_type(eggyolk2_const.COL_TYPE_CYLINDER, eggyolk2_const.SCENE_LAYER)
			elif key == game.VK_3:
				self.player.switch_phy_type(eggyolk2_const.COL_TYPE_SPHERE, eggyolk2_const.SCENE_LAYER)
			elif key == game.VK_4:
				self.player.switch_phy_type(eggyolk2_const.COL_TYPE_MODEL, eggyolk2_const.SCENE_LAYER)
			elif key == game.VK_A:
				self.down_keys[0] = False
				is_adws_up = True
			elif key == game.VK_D:
				self.down_keys[1] = False
				is_adws_up = True
			elif key == game.VK_W:
				self.down_keys[2] = False
				is_adws_up = True
			elif key == game.VK_S:
				self.down_keys[3] = False
				is_adws_up = True
			if not (True in self.down_keys) and is_adws_up:
				self.player.moving_dir = math3d.vector(0, 0, 0)
				self.player.set_state(eggyolk2_const.PLAYER_STATE_DROPPING)
			
	def on_mouse_msg(self, msg, key):
		if msg == game.MSG_MOUSE_DOWN:
			if key == game.MOUSE_BUTTON_LEFT:
				x, y = game.mouse_x, game.mouse_y
				if iworld3d.pick(eggyolk2_const.SCENE_LAYER, x, y) == self.player.sprite:
					self.player.is_dragging = True
					self.player.mouse_pos = x, y
			if key == game.MOUSE_BUTTON_RIGHT:
				self.player.flash_to_pos(game.mouse_x, game.mouse_y)
		if msg == game.MSG_MOUSE_UP:
			if key == game.MOUSE_BUTTON_LEFT:
				if self.player.is_dragging:
					self.player.is_dragging = False
					self.player.set_state(eggyolk2_const.PLAYER_STATE_DROPPING)


