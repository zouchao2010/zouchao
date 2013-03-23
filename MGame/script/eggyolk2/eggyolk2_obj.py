# -*- coding:GBK -*-
import iworld3d
import iphy3d
import eggyolk2_const

class CGameObj(object):
	def __init__(self):
		self.sprite = None	# 3D模型
		self.phy = None	# 3D碰撞系统
		self._pos = (0,0,0)	# 逻辑坐标
		self._sprite_key = (0, 0, 0)
		self._phy_key = (0, 0, 0)
		self.init()

	def init(self):
		pass

	def destroy(self):
		if self.phy:
			self.phy.destroy()
			self.phy = None
		if self.sprite:
			self.sprite.destroy()
			self.sprite = None

	def create_sprite(self, gim_file, name, layer_id):
		self.sprite = iworld3d.model3d(gim_file, name, layer_id)

	def create_phy(self, layer_id):
		# 碰撞类别为road，接受碰撞类别为npc
		self.phy = iphy3d.col_box(20, 6.5, 10, eggyolk2_const.COL_NPC, eggyolk2_const.COL_ROAD)
		self.phy.add_to_layer(layer_id)

	def _get_pos(self):
		return self._pos
		
	def _set_pos(self, pos):
		self._pos = pos
		if self.sprite:
			self.sprite.pos =(pos[0]+self._sprite_key[0], pos[1]+self._sprite_key[1], pos[2]+self._sprite_key[2])
		if self.phy:
			self.phy.pos =(pos[0]+self._phy_key[0], pos[1]+self._phy_key[1], pos[2]+self._phy_key[2])

	def set_sprite_key(self, key_x, key_y, key_z):
		self._sprite_key = (key_x, key_y, key_z)
	def set_phy_key(self, key_x, key_y, key_z):
		self._phy_key = (key_x, key_y, key_z)

	pos = property(_get_pos, _set_pos)

