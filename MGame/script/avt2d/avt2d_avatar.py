# 2D 换装demo
import iworld2d
import avt2d_cfg


"""
	此demo目的在于给出一个2D换装的一个思路：
	
	1·	在模型编辑器中对基本部件的位置进行摆放和动作的制作,
		基本部件可以是空结点，也可以是默认装备。这里可以理
		解成为2D角色制作骨骼及其动画.
	2.	通过程序设置部件的具体表现，如层次，显示，具体表现
		(可以是图片，序列图或粒子等)
	
	demo只是利用pvz的资源进行演示，希望大家不要被demo的制作
	形式	束缚。一般avt的部件可发分上身，下身，鞋，面，头发，
	挂饰，翅膀等。你可以为身体的主要部件制作裸体，将换装的
	显示在裸体之上。你可	以根据自己项目的需要进行实际的功
	能实现。比如：
	装备数据,你可以做的更细致一些，每个装备的层次和key点都
	可配置比如有的游戏的发饰是很精细的，有的在脸的前面，有
	的在脸的后面：方法可以在模型编辑器中预留1个rlevel比脸高
	的空部件和1个比脸低的空部件。或者在程序中动态设置。
	
	总之，希望大家可以举一反三，灵活应用。
"""


# 根据编号得到装备信息
def get_equipinfo(ep_id):
	ep = 'DATA_ITEM_%d' % ep_id
	ep = getattr(avt2d_cfg, ep, None)
	return ep

# 装备类
class equipment(object):
	def __init__(self, ep_id):
		self.ep_info = get_equipinfo(ep_id)
		if self.ep_info is None:
			raise "bad equip id"
		self.ep_type = self.ep_info['ep_type']
		self.ep_id = ep_id
		self.obj = None
	
	# 创建内部对象
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
	
	# 销毁内部对象
	def destroy_obj2d(self):
		if self.obj:
			self.obj.detach_from_parent()
			self.obj.destroy()
			self.obj = None
		
# avatar形象类
class avatar2d(object):
	def __init__(self, mfile):
		self.obj = iworld2d.model2d(mfile)
		self.equips = {}
		
	# 销毁
	def destroy(self):
		for ep in self.equips.itervalues():
			ep.destroy_obj2d()
		self.equips = None
		self.obj.destroy()
		self.obj = None
	
	# 装备一个物品
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
	
	# 卸载一个物品
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
			
	# 装备一系列不同种类的物品
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
	
	# 卸载一系列物品
	def unequip_items(self, ids):
		for i in ids:
			try:
				ep = equipment(i)
				if not self.unequip_item(ep.ep_type):
					return False
			except:
				return False
		return True
	
	# 某物品是否装备
	def is_item_on(self, item_id):
		for ep in self.equips.itervalues():
			if ep.ep_id == item_id:
				return True
		return False