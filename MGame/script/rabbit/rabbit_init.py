# -*- coding:GBK -*-
import idemo_glb
import idemo_demo
import rabbit_scene

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
		pass
	
	def init(self, browser):
		super(demo, self).init(browser)
		# ��Ϸ������ʼ�����Ҵ�����ͼ
		rabbit_scene.init()
		rabbit_scene.create_map()

	# ���ٺ���
	def destroy(self):
		super(demo, self).destroy()
		rabbit_scene.destroy_scene()
		import idemo_glb
		idemo_glb.API.show_performance(False)

	# �߼�֡
	def logic(self):
		rabbit_scene.update()
	
	# �߼�֡����
	def post_logic(self):
		pass
	
	# ��Ⱦ֡
	def render(self):
		pass
	
	# ������Ϣ
	def on_key_msg(self, msg, key):
		super(demo, self).on_key_msg(msg, key)
		rabbit_scene.on_key_msg(msg, key)

	# ��갴��
	def on_mouse_msg(self, msg, key):
		rabbit_scene.on_mouse_msg(msg, key)
	
	# ������
	def on_mouse_wheel(self, msg, delta, key_state):
		pass