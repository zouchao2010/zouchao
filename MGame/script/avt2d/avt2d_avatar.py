# 2D ��װdemo
import iworld2d
import avt2d_cfg


"""
	��demoĿ�����ڸ���һ��2D��װ��һ��˼·��
	
	1��	��ģ�ͱ༭���жԻ���������λ�ý��аڷźͶ���������,
		�������������ǿս�㣬Ҳ������Ĭ��װ�������������
		���Ϊ2D��ɫ�����������䶯��.
	2.	ͨ���������ò����ľ�����֣����Σ���ʾ���������
		(������ͼƬ������ͼ�����ӵ�)
	
	demoֻ������pvz����Դ������ʾ��ϣ����Ҳ�Ҫ��demo������
	��ʽ	������һ��avt�Ĳ����ɷ�����������Ь���棬ͷ����
	���Σ����ȡ������Ϊ�������Ҫ�����������壬����װ��
	��ʾ������֮�ϡ����	�Ը����Լ���Ŀ����Ҫ����ʵ�ʵĹ�
	��ʵ�֡����磺
	װ������,��������ĸ�ϸ��һЩ��ÿ��װ���Ĳ�κ�key�㶼
	�����ñ����е���Ϸ�ķ����Ǻܾ�ϸ�ģ��е�������ǰ�棬��
	�������ĺ��棺����������ģ�ͱ༭����Ԥ��1��rlevel������
	�Ŀղ�����1�������͵Ŀղ����������ڳ����ж�̬���á�
	
	��֮��ϣ����ҿ��Ծ�һ���������Ӧ�á�
"""


# ���ݱ�ŵõ�װ����Ϣ
def get_equipinfo(ep_id):
	ep = 'DATA_ITEM_%d' % ep_id
	ep = getattr(avt2d_cfg, ep, None)
	return ep

# װ����
class equipment(object):
	def __init__(self, ep_id):
		self.ep_info = get_equipinfo(ep_id)
		if self.ep_info is None:
			raise "bad equip id"
		self.ep_type = self.ep_info['ep_type']
		self.ep_id = ep_id
		self.obj = None
	
	# �����ڲ�����
	def create_obj2d(self):
		res_type = self.ep_info['res_type']
		res_path = self.ep_info['res_path']
		if res_type == avt2d_cfg.RES_IMG:
			self.obj = iworld2d.image2d(res_path)
			return True
		if res_type == avt2d_cfg.RES_SPR:
			self.obj = iworld2d.sprite2d(res_path)
			return True
		return False
	
	# �����ڲ�����
	def destroy_obj2d(self):
		if self.obj:
			self.obj.detach_from_parent()
			self.obj.destroy()
			self.obj = None
		
# avatar������
class avatar2d(object):
	def __init__(self, mfile):
		self.obj = iworld2d.model2d(mfile)
		self.equips = {}
		
	# ����
	def destroy(self):
		for ep in self.equips.itervalues():
			ep.destroy_obj2d()
		self.equips = None
		self.obj.destroy()
		self.obj = None
	
	# װ��һ����Ʒ
	def equip_item(self, ep):
		if ep.ep_type in self.equips:
			old_ep = self.equips.get(ep.ep_type)
			old_ep.destroy_obj2d()
		if not ep.create_obj2d():
			return False
		unit = self.obj.get_unit(ep.ep_type)
		if unit:
			ep.obj.attach_to_parent(unit)
			ep.obj.key_point = unit.key_point
			self.equips[ep.ep_type] = ep
			return True
		return False
	
	# ж��һ����Ʒ
	def unequip_item(self, ep_type):
		try:
			if ep_type in self.equips:
				ep = self.equips.get(ep_type, None)
				if ep is None:
					return False
				ep.destroy_obj2d()
				del self.equips[ep_type]
				return True
		except:
			return False
			
	# װ��һϵ�в�ͬ�������Ʒ
	def equip_items(self, ids):
		for i in ids:
			try:
				ep = equipment(i)
				ret = self.equip_item(ep)
				if not ret:
					return False
			except:
				return False
		return True
	
	# ж��һϵ����Ʒ
	def unequip_items(self, ids):
		for i in ids:
			try:
				ep = equipment(i)
				if not self.unequip_item(ep.ep_type):
					return False
			except:
				return False
		return True
	
	# ĳ��Ʒ�Ƿ�װ��
	def is_item_on(self, item_id):
		for ep in self.equips.itervalues():
			if ep.ep_id == item_id:
				return True
		return False