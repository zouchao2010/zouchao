# -*- coding:GBK -*-
import iworld3d
import math3d
import math
import flashui
import iphy3d

import eggyolk2_const
import eggyolk2_obj

shadow_type = 0

class CGamePlayer(eggyolk2_obj.CGameObj):
	def init(self):
		self.bill = None
		self.moving_dir = math3d.vector(0, 0, 0) # �ƶ�����
		self.target_pos = math3d.vector(0, 0, 0) # Ŀ��λ��
		self.is_dragging = False # �Ƿ�����϶�
		self.mouse_pos = (0, 0)  # ����϶�λ��
		self.pre_mouse_pos = (0, 0) # ��һ������λ��
		
	def create_sprite(self, gim_file, name, layer_id):
		super(CGamePlayer, self).create_sprite(gim_file, name, layer_id)
		self.sprite.set_pick()   # �ɱ����ѡ��
		self.animations = ["npc_act_001", "npc_act_003"] # ÿ��״̬��Ӧ�Ķ���
		self.set_state(eggyolk2_const.PLAYER_STATE_DROPPING) # ��ʼ״̬Ϊ����
	
	def create_bill(self, swf_file, text=""):
		if self.bill:
			self.bill.destroy()
		self.bill = iworld3d.space_movie(swf_file, True, pixel_unit=0.1, layer_id=eggyolk2_const.SCENE_LAYER)
		self.sprite.bind("cstop", self.bill)	# �󶨵�cstop�Ĺҽӵ���
		self.bill.billboard_type = True

		if text:
			# ��ȡspace_movie��movie���ԣ������ñ���
			self.bill.movie.set_variable("name.text", text)

	def create_phy(self, layer_id):
		# ��ײ���Ϊnpc��������ײ���Ϊnpc
		self.phy = iphy3d.col_sphere(6, eggyolk2_const.COL_NPC, eggyolk2_const.COL_NPC)
		self.phy.add_to_layer(layer_id)
	
	def destroy(self):
		self.destroy_bill()
		self.sprite.destroy()

	## ������ײ������
	def switch_phy_type(self, col_type, layer_id):
		if self.phy is	None:
			return
		self.set_phy_key(0, 0, 0)
		if col_type == eggyolk2_const.COL_TYPE_CAPSULE:
			temp = iphy3d.col_capsule(4, 4, eggyolk2_const.COL_NPC, eggyolk2_const.COL_NPC)
		elif col_type == eggyolk2_const.COL_TYPE_CYLINDER:
			temp = iphy3d.col_cylinder(4, 6, eggyolk2_const.COL_NPC, eggyolk2_const.COL_NPC)
		elif col_type == eggyolk2_const.COL_TYPE_MODEL:
			temp = iphy3d.col_model(self.sprite, eggyolk2_const.COL_NPC, eggyolk2_const.COL_NPC)
			temp.rotation_matrix = self.sprite.rotation_matrix # ����ģ�ͷ�ת��,�˴���Ҫ��ת
			self.set_phy_key(0, 15, 0) # ����key��
		elif col_type == eggyolk2_const.COL_TYPE_SPHERE:
			temp = iphy3d.col_sphere(6, eggyolk2_const.COL_NPC, eggyolk2_const.COL_NPC)
		else:
			return
		self.phy.remove_from_layer()
		self.phy = temp
		self.pos = self.pos
		self.phy.add_to_layer(layer_id)
		iphy3d.update(layer_id)

	def destroy_bill(self):
		if self.bill:
			self.bill.destroy()
			self.bill = None

	# ��̬��ײ���
	def sweep_test(self, start, end):
		# Ϊ�˱�����end����ײ����ɾ������⣬�˴�������*2��
		ext_end = start + (end - start) * 2.0
		# ��ײ���ˣ�npc���ü����ײ,�ų���ײ���Ϊnpc�ġ�
		sweep_filter = iphy3d.col_filter(0, eggyolk2_const.COL_NPC, iphy3d.EXCLUDE_FILTER)
		# �����߿�������ע���еĹ��˷�ʽ�Ա�Ч��
		#sweep_filter = iphy3d.col_filter(eggyolk2_const.COL_ROAD | eggyolk2_const.COL_NPC, 0, iphy3d.EXCLUDE_FILTER) # ���κ���ײ,���ܻ������Ļ
		#sweep_filter = iphy3d.col_filter(eggyolk2_const.COL_NPC , eggyolk2_const.COL_NPC, iphy3d.EQUAL_FILTER) # ֻ��npc��ײ�����ܻ������Ļ
		#sweep_filter = iphy3d.col_filter(eggyolk2_const.COL_NPC , eggyolk2_const.COL_ROAD, iphy3d.EQUAL_FILTER) # ֻ��·����ײ
		#sweep_filter = iphy3d.col_filter(1 , 2, iphy3d.INEQUAL_FILTER) # ֻ��·����
		try:
			result = iphy3d.sweep_test(eggyolk2_const.SCENE_LAYER, self.phy, start, ext_end, sweep_filter)
		except iphy3d.iphy3d_exception, e:
			# ��ģ����ײ������,���׳��쳣��С���Ƶ�ģ���岻��͹�����
			print e,"�л���������"
			self.switch_phy_type(eggyolk2_const.COL_TYPE_CAPSULE, eggyolk2_const.SCENE_LAYER)
			return iphy3d.col_result()
		if result.hit:
			if result.fraction > 0.5 + eggyolk2_const.FLOAT_EPSILON:
				return iphy3d.col_result()
			else:
				result.fraction *= 2.0
				return result
		return result
	
	# ��̬��ײ���
	def anything_collision(self):
		return len(iphy3d.static_test(eggyolk2_const.SCENE_LAYER, self.phy)) != 0
	
	# ������ײ���
	def is_ray_hit(self, start, end):
		return iphy3d.hit_by_ray(eggyolk2_const.SCENE_LAYER, start, end).hit
	
	# ������ײ���λ��
	def update_collide_pos(self, fraction):
		cur_pos = math3d.vector(*self.pos)
		length = (cur_pos - self.target_pos).length
		moved = length * fraction
		if moved < eggyolk2_const.MARGIN:
			return
		cur_pos.intrp(cur_pos, self.target_pos, (moved - eggyolk2_const.MARGIN) / length)
		self.pos = cur_pos.x, cur_pos.y, cur_pos.z
	
	# �ƶ�
	def moving(self):
		if self.moving_dir.is_zero:
			return
		cur_pos = math3d.vector(*self.pos)
		self.target_pos = cur_pos + self.moving_dir
		result = self.sweep_test(cur_pos, self.target_pos)
		if not result.hit:
			self.pos = self.target_pos.x, self.target_pos.y, self.target_pos.z
			return
		self.update_collide_pos(result.fraction)
	
	# �����ƶ�
	def update_moving(self):
		# ���������״̬
		if self.state == eggyolk2_const.PLAYER_STATE_DROPPING:
			return
		# ����״̬
		self.moving()
	
	# ���µ���
	def update_dropping(self):
		if self.state == eggyolk2_const.PLAYER_STATE_MOVING:
			return
		down = math3d.vector(0, eggyolk2_const.GRAVITY, 0)
		cur_pos = math3d.vector(*self.pos)
		self.target_pos = cur_pos + down
		result = self.sweep_test(cur_pos, self.target_pos)
		if not result.hit:
			# û������������������
			self.pos = self.target_pos.x, self.target_pos.y, self.target_pos.z
			self.set_state(eggyolk2_const.PLAYER_STATE_DROPPING)
			return
		# ������ײ������λ��
		self.update_collide_pos(result.fraction)
		self.set_state(eggyolk2_const.PLAYER_STATE_MOVING)

	def add_round_shadow(self):
		self.sprite.add_round_shadow(False, (5,5))

	def update_plane_shadow(self):
		# ��playerλ�������ߣ�������ײ���ĸ�ʯͷ
		p0 = self.pos
		coldata = iphy3d.hit_by_ray(eggyolk2_const.SCENE_LAYER, \
			math3d.vector(p0[0], p0[1], p0[2]),\
			math3d.vector(p0[0], p0[1]+10000, p0[2]))
		if coldata.hit:
			self.sprite.set_shadow_visible(True)
			self.sprite.clear_shadows()
			# ʹ�ó������õ�0�Ź���
			self.sprite.add_plane_shadow((coldata.normal, coldata.point), "light_1")
		else:
			self.sprite.set_shadow_visible(False)


	# ���º���
	def update(self):
		self.update_dropping()
		self.update_moving()
		self.on_mouse_dragging()
		if shadow_type == 2:
			# ��Ϊƽ����Ӱ��Ҫ����ŵ׵���Ӱλ�ã����Բ�ÿ֡��Ҫ����һ��
			self.update_plane_shadow()
	
	# ��Ӧ�����ק
	def on_mouse_dragging(self):
		if not self.is_dragging:
			return
		# �����ʱ��Ҳ������ק
		self.set_state(eggyolk2_const.PLAYER_STATE_MOVING)
		# �õ���������
		p, d = iworld3d.screen_to_world(eggyolk2_const.SCENE_LAYER, 
			self.mouse_pos[0], self.mouse_pos[1])
		d.normalize()
		position = p + d * ((-100 - p.z) / d.z) # ʵ��Ӧ�����豣֤�����㹻���������������Ļ��
												# �˴�Ϊ�˱�֤������z�᷽���ͶӰ����Ҫ����100
												# ����position.z���Ƶ���-100
		pre_pos = self.pos
		pre_pos_v = math3d.vector(*pre_pos)
		# ���㳤��
		d = position - pre_pos_v
		# �������һ���ƶ������Ķ����Ͷ�0�����淶��
		if d.length < 1:
			return
		d.normalize()
		p = pre_pos_v + d * 2
		# ÿ֡�����λ���ƶ���λ�����ľ���
		self.pos = p.x, p.y, p.z
		# ��̬��ײ��ʾ
		if self.anything_collision():
			self.pos = pre_pos
	
	# ˲���ƶ���ĳ������ײ�����Ļ���ϣ��˺���Ϊ��ʾ������ײ����
	def flash_to_pos(self, screen_x, screen_y):
		# �õ���������
		p, d = iworld3d.screen_to_world(eggyolk2_const.SCENE_LAYER, 
			screen_x, screen_y)
		d.normalize()
		position = p + d * ((-100 - p.z) / d.z) # ʵ��Ӧ�����豣֤�����㹻���������������Ļ��
												# �˴�Ϊ�˱�֤������z�᷽���ͶӰ����Ҫ����100
												# ����position.z���Ƶ���-100
		# �������Ϊ�������λ�ã��յ�Ϊ��Ļ���������ڲ��λ��
		if not self.is_ray_hit(math3d.vector(0, 0, 0), position):
			# Ϊ�˱����Ե����ײ������һ��static_test
			pre_pos = self.pos
			self.pos = position.x, position.y, position.z
			if self.anything_collision():
				self.pos = pre_pos
				return
			self.set_state(eggyolk2_const.PLAYER_STATE_DROPPING)
	
	## �������״̬
	def set_state(self, state):
		self.state = state
		self.sprite.play_animation(self.animations[self.state])
