# -*- coding: gbk -*-

import idemo_glb
import idemo_demo
import iworld3d
import itownroom_player

# ITOWN RES-------------------------------------------
scn_file = "idemos\\res\\itownroom\\scene\\room.scn"

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

class demo(idemo_demo.demo):
	def __init__(self):
		super(demo, self).__init__()
		self.scn = None
		self.player = None
	
	def init(self, browser):
		super(demo, self).init(browser)
		iworld3d.init()
		# ���س���
		self.scn = iworld3d.create_scene3d(scn_file)
		# ����г����༭���н����˹�Դ�༭���˴��������
		self.scn.create_light(iworld3d.LIGHT_TYPE_POINT)
		# ��ɫ
		self.player = itownroom_player.player(self.scn)
		
	def destroy(self):
		super(demo, self).destroy()
		self.player.destroy()
		self.scn.destroy()
		self.player = None
		self.scn = None
		iworld3d.destroy()
	
	# �߼�֡
	def logic(self):
		if self.player:
			self.player.logic()
	
	# �߼�֡����
	def post_logic(self):
		pass
	
	# ��Ⱦ֡
	def render(self):
		pass
	
	# ������Ϣ
	def on_key_msg(self, msg, key):
		super(demo, self).on_key_msg(msg, key)
		if self.player:
			self.player.on_key_msg(msg, key)

	# ��갴��
	def on_mouse_msg(self, msg, key):
		if self.player:
			self.player.on_mouse_msg(msg, key)

	# ������
	def on_mouse_wheel(self, msg, delta, key_state):
		if self.player:
			self.player.on_mouse_wheel(msg, delta, key_state)
