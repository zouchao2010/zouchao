# -*- coding: gbk -*-
import iworld3d, math3d, idemo_glb
import iphy3d
import game

animation_names = [
	iworld3d.avatar3d.get_inner_anim_name("IDLE0"),#�ȴ�
	iworld3d.avatar3d.get_inner_anim_name("WALK"),#ǰ��
	iworld3d.avatar3d.get_inner_anim_name("WALK"),#�˺�
	iworld3d.avatar3d.get_inner_anim_name("IDLE1"),#��Ծ
	iworld3d.avatar3d.get_inner_anim_name("IDLE0"),#����
]

init_pos = math3d.vector(0.0, 30.0, 0.0) 		# ��ʼλ��
model_scale = 1.0								# Ϊ��Ӧ��ͬ�������ɵ���ģ�ͱ���

g_gravity = 1.0									# �����ٶȣ���������ã�������ӷ������Ը�����ٶ�����
g_climb_height = 1.0							# ����վס�ĸ߶�
g_margin = 0.08 								# ��������С����
g_moving_speed = 1.5 							# �ƶ��ٶ�
g_drop_control_speed = 0.5						# ����ʱ�����������΢���ƽ�ɫ���䷽��
g_jumpping_control_speed = 0.5					# ������ٶ�
g_max_jump_height = 20.0						# ��������߶�
g_mouse_dragging = False
g_pixel_to_angel = 0.00314

# ���ƽ�ɫ�˶����ͳ�����ײ
# Ŀǰ�������������¥�ݣ���¥�ݣ�����ײ��Ե�������˶�
class player(object):
	def __init__(self, scene):
		self.pre_anim_idx = 4
		self.cur_anim_idx = 4
		# ״̬
		self.state = [
			self.update_moving,
			self.update_dropping,
			self.update_jumpping,
		]
		self.cur_state_idx = 1 # ��ʼ̬
		self.sce = scene
		self.avt_mgr = iworld3d.avatar_mgr()
		self.model = self.avt_mgr.create("me", idemo_glb.API.get_my_avatar())
		# Բ����
		size = self.model.bounding_box * model_scale
		self.col_obj = iphy3d.col_cylinder(size.x, size.y)
		self.col_obj.add_to_scene3d()
		self._pos = init_pos
		self.base_pos = math3d.vector(0, size.y, 0) #avt�Ļ����ڽ���
		self.pos = self._pos
		self.model.scale = (model_scale, model_scale, model_scale)
		self.model.anim_rate = 1.5 #�ٶȲ���һ��
		self.camera = self.sce.get_camera()
		self.camera.set_placement(
			self.pos + math3d.vector(0.0, 45.0, 45.0),
			math3d.vector(0, -1, -1),
			math3d.vector(0, 1, 0))
		self.moving_dir = math3d.vector(0, 0, 0)
		self.jump_begin = math3d.vector(0, 0, 0) # ����λ��
		self.target_pos = math3d.vector(0, 0, 0)
		self.up_ofs = None # ����߶�
		self.no_up_slide = False
		self.play_animation()
		self.is_debug_draw = False
	
	def destroy(self):
		global g_mouse_dragging
		g_mouse_dragging = False
		idemo_glb.API.show_sys_mouse(True)
		self.avt_mgr.destroy()
		self.col_obj.destroy()

	def _get_pos(self):
		return self._pos
	
	def _set_pos(self, _pos):
		self._pos = _pos
		self.model.position = _pos - self.base_pos
		self.col_obj.position = _pos
	
	pos = property(_get_pos, _set_pos)

	# ���Ŷ���
	def play_animation(self):
		try:
			self.model.play_animation(animation_names[self.cur_anim_idx])
		except:
			pass
	
	# ��ײ��⣬�ɲο�eggyolk2�е�ע��
	def sweep_test(self, start, end):
		ext_end = start + (end - start) * 2.0
		sweep_filter = iphy3d.col_filter(0, 1)
		try:
			result = iphy3d.sweep_test(iworld3d.NO_2D_LAYER, self.col_obj, start, ext_end, sweep_filter)
		except iphy3d.iphy3d_exception, e:
			return iphy3d.col_result()
		if result.hit:
			if result.fraction > 0.5 + 0.001:
				return iphy3d.col_result()
			else:
				result.fraction *= 2.0
				return result
		return result
	
	# ������ײ���λ��
	def update_collide_pos(self, fraction):
		length = (self.pos - self.target_pos).length
		moved = length * fraction
		if moved < g_margin:
			return
		self._pos.intrp(self.pos, self.target_pos, (moved - g_margin) / length)
		self.pos = self._pos
	
	# �Ƿ��վ��
	def can_stand(self, pos, hit_point, normal):
		if pos.y - hit_point.y < g_climb_height:
			return False
		if normal.dot(math3d.vector(0.0, 1.0, 0.0)) < 0.5:
			return False
		return True
	
	# ÿ֡ȥ���
	def get_user_input(self, speed):
		dir = math3d.vector(0, 0, 0)
		# ǰ��
		if idemo_glb.API.is_press_key(game.VK_W):
			dir.z += 1.0
			if self.cur_state_idx == 0:
				self.cur_anim_idx = 1
		if idemo_glb.API.is_press_key(game.VK_S):
			dir.z -= 1.0
			if self.cur_state_idx == 0:
				self.cur_anim_idx = 2
		if idemo_glb.API.is_press_key(game.VK_A):
			dir.x -= 1.0
			if self.cur_state_idx == 0:
				self.cur_anim_idx = 1
		if idemo_glb.API.is_press_key(game.VK_D):
			dir.x += 1.0
			if self.cur_state_idx == 0:
				self.cur_anim_idx = 1
		if dir.is_zero:
			return dir
		if dir.z < 0:
			speed *= 0.5
		dir = self.camera.rotation_matrix.mulvec3x3(dir)
		dir.y = 0
		dir.normalize()
		dir *= speed
		return dir
	
	#-----------------------------------------------------------------------
	# ����״̬�£���move, slide, step_up, step_down��Щ���ܺ���ȥ��ɸ��ֶ���
	#-----------------------------------------------------------------------
	def move_and_slide(self):
		result = self.move()
		if not result.hit:
			return
		result = self.slide(result)
		if result.hit:
			result = self.slide(result)
			if result.hit:
				self.update_collide_pos(result.fraction)
	
	# �ƶ�
	def move(self):
		if self.moving_dir.is_zero:
			return
		self.model.rotation_matrix = math3d.matrix.make_orient(self.moving_dir,
			math3d.vector(0.0, 1.0, 0.0))
		self.target_pos = self.pos + self.moving_dir
		result = self.sweep_test(self.pos, self.target_pos)
		if not result.hit:
			# ����
			self.pos = self.target_pos
		return result
	
	# ����
	def slide(self, result):
		# �ƶ�����ײ��ǰ
		dist = (self.pos - self.target_pos).length
		moved_dis = dist * result.fraction
		if moved_dis > g_margin:
			self._pos.intrp(self.pos, self.target_pos, (moved_dis - g_margin) / dist)
		# ʣ������
		dir_remaining = self.target_pos - self.pos
		normal = - result.normal
		if self.no_up_slide:
			normal.y = 0.0
			normal.normalize()
		# ɾ�����߷����ϵ�����
		nv = normal * dir_remaining.dot(normal)
		self.moving_dir = dir_remaining - nv
		# slide,�ٴ���ײ���
		self.target_pos = self.pos + self.moving_dir
		new_result = self.sweep_test(self.pos, self.target_pos)
		if not new_result.hit:
			# ����
			self.pos = self.target_pos
		return new_result
	
	# ��¥
	def step_up(self):
		self.up_ofs = math3d.vector(0, g_climb_height, 0)
		self.target_pos = self.pos + self.up_ofs
		result = self.sweep_test(self.pos, self.target_pos)
		if not result.hit:
			self.pos = self.target_pos
			return
		temp = self.pos
		self.update_collide_pos(result.fraction)
		self.up_ofs = self.pos - temp
	
	# ��̤
	def step_down(self):
		# ������˵�����ý�ɫ����ܿ�ĸ߶ȣ�ȡ����������̤�����߶�
		down = math3d.vector(0, g_climb_height, 0)
		self.target_pos = self.pos - self.up_ofs - down
		result = self.sweep_test(self.pos, self.target_pos)
		if not result.hit:
			self.pos = self.target_pos
			self.cur_state_idx = 1
			return result
		self.update_collide_pos(result.fraction)
		return result
	
	#-----------------------------------------------------------------------
	# ��ɫ��3��״̬
	#-----------------------------------------------------------------------
	def update_moving(self):
		# ��Ծ
		if self.cur_state_idx == 2:
			return
		# ����
		prev_pos = math3d.vector(self.pos)
		self.moving_dir = self.get_user_input(g_moving_speed)
		if self.moving_dir.is_zero:
			return
		cur_moving = math3d.vector(self.moving_dir)
		self.up_ofs = math3d.vector(0, 0, 0)
		result = self.move()
		# ƽ��ʧ��
		if result.hit:
			# ������¥
			self.step_up()
			# ���ƶ������ƶ�
			self.move_and_slide()
		result = self.step_down()
		# ̤�� �� ��վ������
		if not result.hit or self.can_stand(self.pos, result.point, result.normal):
			return
		# ��¥ʧ�ܣ�������Ϣ,ֱ��
		self.moving_dir = cur_moving
		self.pos = prev_pos
		self.no_up_slide = True
		self.move_and_slide()
		self.no_up_slide = False
	
	def update_jumpping(self):
		up = math3d.vector(0, 2.0 * g_gravity, 0)
		self.moving_dir = self.get_user_input(g_jumpping_control_speed)
		self.moving_dir += up
		self.target_pos = self.pos + self.moving_dir
		result = self.sweep_test(self.pos, self.target_pos)
		if not result.hit:
			self.pos = self.target_pos
			if self.pos.y - self.jump_begin.y > g_max_jump_height:
				self.pos.y = self.jump_begin.y + g_max_jump_height
				self.cur_state_idx = 1
			self.pos = self.pos
			return
		self.update_collide_pos(result.fraction)
		if self.can_stand(self.pos, result.point, result.normal):
			self.cur_state_idx = 0
		else:
			self.cur_state_idx = 1
	
	def update_dropping(self):
		down = math3d.vector(0, - g_gravity, 0)
		self.moving_dir = self.get_user_input(g_drop_control_speed)
		self.moving_dir += down
		self.target_pos = self.pos + self.moving_dir
		result = self.sweep_test(self.pos, self.target_pos)
		if not result.hit:
			# ʲô��û��������������
			self.pos = self.target_pos
			self.pos = self.pos
			return
		# ��ײ���Ƿ��վ��
		standing_pos = math3d.vector(0, 0, 0)
		standing_pos.intrp(self.pos, self.target_pos, result.fraction)
		if self.can_stand(standing_pos, result.point, result.normal):
			self.update_collide_pos(result.fraction)
			# ��������̬
			self.update_collide_pos(result.fraction)
			self.cur_state_idx = 0
			return
		# ���л���
		result = self.slide(result)
		if result.hit:
			self.update_collide_pos(result.fraction)
			if self.can_stand(self.pos, result.point, result.normal):
				# ��������̬
				self.cur_state_idx = 0
	
	def logic(self):
		prev_pos = self.pos
		# ״̬����
		self.state[self.cur_state_idx]()
		# ��ͷ����
		self.on_mouse_move()
		ofs = self.pos - prev_pos
		self.camera.position += ofs
		# ������ʾ��ײ����Ϣʱ�����ĵ�
		self.update_debug_drawing()
		# �л�����
		self.update_animation()
		if self.avt_mgr:
			self.avt_mgr.update()
	
	def update_debug_drawing(self):
		 iphy3d.set_draw_range(iworld3d.NO_2D_LAYER, self.pos.x, 
			self.pos.y, self.pos.z, 40)
	
	def update_animation(self):
		if self.pre_anim_idx != self.cur_anim_idx:
			self.play_animation()
			self.pre_anim_idx = self.cur_anim_idx
		elif self.moving_dir.is_zero and self.cur_state_idx == 0:
			self.cur_anim_idx = 0
		elif self.cur_state_idx == 2:
			self.cur_anim_idx = 3
		elif self.cur_state_idx == 1:
			self.cur_anim_idx = 4
		
		
	# ��ÿ֡��Ҫ���ļ�������
	def on_mouse_msg(self, msg, key):
		global g_mouse_dragging
		if game.MSG_MOUSE_DOWN == msg:
			if game.MOUSE_BUTTON_LEFT == key:
				g_mouse_dragging = True
				idemo_glb.API.show_sys_mouse(False)
		elif game.MSG_MOUSE_UP == msg:
			if game.MOUSE_BUTTON_LEFT == key:
				g_mouse_dragging = False
		
	
	def on_mouse_move(self):
		if not g_mouse_dragging:
			idemo_glb.API.show_sys_mouse(True)
			idemo_glb.API.lock_cursor_pos(False)
			return
		dx, dy = idemo_glb.API.lock_cursor_pos(True)
		prev_rotation = self.camera.rotation_matrix
		dis = (self.camera.position - self.pos).length
		self.camera.yaw(dx * g_pixel_to_angel, iworld3d.SPACE_TYPE_WORLD)
		self.camera.pitch(dy * g_pixel_to_angel)
		pos = self.pos - self.camera.rotation_matrix.forward * dis
		# ��������߶�
		if pos.y < 2.0 or pos.y > 60.0:
			self.camera.rotation_matrix = prev_rotation
			return
		self.camera.set_placement(pos, self.camera.rotation_matrix.forward, math3d.vector(0, 1, 0))
		
	def on_mouse_wheel(self, msg, delta, key_state):
		dir = self.camera.position - self.pos
		dist = dir.length
		dl = -delta * 0.0008 * dist
		dist = dist + dl
		if dist < 5.0:
			dist = 5.0
		elif dist > 50.0:
			dist = 50.0
		dir.normalize()
		# �����ײ���
		pos = self.pos + dir * dist
		ray_filter = iphy3d.col_filter(0, 1)
		result = iphy3d.hit_by_ray(iworld3d.NO_2D_LAYER, self.pos, pos)
		# ������,������ɵ���
		if result.hit:
			return
		self.camera.position = pos
	
	def on_key_msg(self, msg, key):
		if msg == game.MSG_KEY_DOWN:
			if key == game.VK_SPACE:
				self.jump_begin = self.pos
				self.cur_state_idx = 2
			if key == game.VK_M:
				self.is_debug_draw = not self.is_debug_draw
				iphy3d.set_debug_draw(iworld3d.NO_2D_LAYER, self.is_debug_draw)
