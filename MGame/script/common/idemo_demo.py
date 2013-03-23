# -*- coding:GBK -*-
import game
import idemo_glb
import idemos_cfg
# demo����Ϣ
class info(object):
	def __init__(self):
		self.title = "undefined"
		self.desc = "undefined"
		self.thumbnail = "undefined"
		self.category1 = "undefined"
		self.category2 = "undefined"

# demo�Ļ���
class demo(object):
	def __init__(self):
		self.info = info()
	
	# -------------------------------------------------
	# ----------------����д����-----------------------
	# ��ʼ������
	def init(self, browser):
		self.browser = browser
		cfg = idemos_cfg.CFG[browser.cur_name]
		self.info.title = cfg["title"]
		self.info.desc = cfg["desc"]
		self.info.desc += "\nESC  �˳���demo"
		self.info.thumbnail = cfg["thumbnail"]
		self.info.category1 = cfg["category1"]
		self.info.category1 = cfg["category2"]
		
		self.text = idemo_glb.API.get_text_panel()
		self.text.set_text(self.info.desc)
		self.text.set_coord((30, 40))

	# ���ٺ���
	def destroy(self):
		self.text = None
	
	# �߼�֡
	def logic(self):
		pass
	
	# �߼�֡����
	def post_logic(self):
		pass
	
	# ��Ⱦ֡
	def render(self):
		pass
	
	# ������Ϣ
	def on_key_msg(self, msg, key):
		if msg == game.MSG_KEY_DOWN and key == game.VK_ESCAPE:
			self.browser.end_demo()

	# ��갴��
	def on_mouse_msg(self, msg, key):
		pass
	
	# ������
	def on_mouse_wheel(self, msg, delta, key_state):
		pass