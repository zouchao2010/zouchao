# -*- coding:GBK -*-
# �����ͻ��˳���Ľṹ
import idemo_demo
import avt2d_avatar
import iworld2d
import idemo_glb

inst = None

RES_MODEL = 'idemos/res/avt2d/jiangshi.2dm'
SUIT_1 = (1,2,3,4,5,6)

def init(browser):
	global inst
	if inst is None:
		iworld2d.init()
		inst = demo()
		inst.init(browser)

def destroy():
	global inst
	if inst:
		inst.destroy()
		inst = None
		iworld2d.destroy()

class demo(idemo_demo.demo):
	def __init__(self):
		super(demo, self).__init__()
		self.cur_idx = -1
		self.ac_idx = 0
	
	def init(self, browser):
		super(demo, self).init(browser)
		self.avt = avt2d_avatar.avatar2d(RES_MODEL)
		self.avt.obj.pos = 1024/2, 768/2
		self.avt.obj.play_action('move')
		# Ĭ�ϴ���һ��װ��
		self.avt.equip_items(SUIT_1)
		
		self.next_btn = idemo_glb.API.create_btn(pos=(100, 500), \
			size=(90, 20), label="��һ��")
		self.next_btn.func = self.on_next
		
		self.pre_btn = idemo_glb.API.create_btn(pos=(200, 500), \
			size=(90, 20), label="��һ��")
		self.pre_btn.func = self.on_pre
		
		self.put_btn = idemo_glb.API.create_btn(pos=(300, 500), \
			size=(90, 20), label="��")
		self.put_btn.func = self.on_put
		
		self.off_btn = idemo_glb.API.create_btn(pos=(400, 500), \
			size=(90, 20), label="��")
		self.off_btn.func = self.on_off
		
		self.df_btn = idemo_glb.API.create_btn(pos=(500, 500), \
			size=(90, 20), label="Ĭ����װ")
		self.df_btn.func = self.on_df
		
		self.ch_ac_btn = idemo_glb.API.create_btn(pos=(600, 500), \
			size=(90, 20), label="������")
		self.ch_ac_btn.func = self.ch_ac
		
		self.txt_lbl = idemo_glb.API.create_label(pos=(100, 400), size=(800, 600), text="")
		self.txt_lbl.size = 14 #�����С
		self.txt_lbl.color = 0x00ffff
		
		self.on_next()
		
	def on_next(self):
		self.cur_idx += 1
		self.set_item_txt(self.cur_idx % 10 + 1)
	
	def on_pre(self):
		self.cur_idx -= 1
		self.set_item_txt(self.cur_idx % 10 + 1)
		
	def on_put(self):
		self.avt.equip_items((self.cur_idx % 10 + 1,))
		self.set_item_txt(self.cur_idx % 10 + 1)
	
	def on_off(self):
		self.avt.unequip_items((self.cur_idx % 10 + 1,))
		self.set_item_txt(self.cur_idx % 10 + 1)
	
	def on_df(self):
		self.avt.equip_items(SUIT_1)
		self.set_item_txt(self.cur_idx % 10 + 1)
	
	def ch_ac(self):
		self.ac_idx += 1
		self.avt.obj.play_action(('move', 'attack', 'die')[self.ac_idx % 3])
	
	def set_item_txt(self, i):
		ep_info = avt2d_avatar.get_equipinfo(i)
		if ep_info:
			s = "װ����ţ�%d\nװ������:%s\n�Ƿ�װ��:%s" % (ep_info['ep_id'], ep_info['name'], self.avt.is_item_on(i))
			self.txt_lbl.text = s
	
	# ���ٺ���
	def destroy(self):
		self.next_btn.func = None
		self.pre_btn.func = None
		self.put_btn.func = None
		self.off_btn.func = None
		idemo_glb.API.simple_ui_destory()
		self.avt.destroy()
		self.next_btn = self.pre_btn = self.put_btn = self.off_btn = self.avt = None
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
		super(demo, self).on_key_msg(msg, key)

	# ��갴��
	def on_mouse_msg(self, msg, key):
		pass
	
	# ������
	def on_mouse_wheel(self, msg, delta, key_state):
		pass