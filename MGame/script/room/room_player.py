# -*- coding: gbk -*-
import iworld3d, math3d, idemo_glb
import iphy3d
import game

animation_names = [
	iworld3d.avatar3d.get_inner_anim_name("IDLE0"),#等待
	iworld3d.avatar3d.get_inner_anim_name("WALK"),#前进
	iworld3d.avatar3d.get_inner_anim_name("WALK"),#退后
	iworld3d.avatar3d.get_inner_anim_name("IDLE1"),#跳跃
	iworld3d.avatar3d.get_inner_anim_name("IDLE0"),#下落
]

init_pos = math3d.vector(0.0, 30.0, 0.0) 		# 初始位置
model_scale = 1.0								# 为适应不同场景，可调节模型比例

g_gravity = 1.0									# 下落速度，随便你设置，如果不嫌烦，可以搞个加速度下落
g_climb_height = 1.0							# 可以站住的高度
g_margin = 0.08 								# 物体间的最小距离
g_moving_speed = 1.5 							# 移动速度
g_drop_control_speed = 0.5						# 下落时，让玩家能轻微控制角色下落方向
g_jumpping_control_speed = 0.5					# 跳起的速度
g_max_jump_height = 20.0						# 跳起的最大高度
g_mouse_dragging = False
g_pixel_to_angel = 0.00314

# 控制角色运动、和场景碰撞
# 目前代码可以用于爬楼梯，下楼梯，沿碰撞边缘滑动等运动
class player(object):
	def __init__(self, scene):
		self.pre_anim_idx = 4
		self.cur_anim_idx = 4
		# 状态
		self.state = [
			self.update_moving,
			self.update_dropping,
			self.update_jumpping,
		]
		self.cur_state_idx = 1 # 初始态
		self.sce = scene
		self.avt_mgr = iworld3d.avatar_mgr()
		self.model = self.avt_mgr.create("me", idemo_glb.API.get_my_avatar())
		# 圆柱体
		size = self.model.bounding_box * model_scale
		self.col_obj = iphy3d.col_cylinder(size.x, size.y)
		self.col_obj.add_to_scene3d()
		self._pos = init_pos
		self.base_pos = math3d.vector(0, size.y, 0) #avt的基点在脚下
		self.pos = self._pos
		self.model.scale = (model_scale, model_scale, model_scale)
		self.model.anim_rate = 1.5 #速度播快一点
		self.camera = self.sce.get_camera()
		self.camera.set_placement(
			self.pos + math3d.vector(0.0, 45.0, 45.0),
			math3d.vector(0, -1, -1),
			math3d.vector(0, 1, 0))
		self.moving_dir = math3d.vector(0, 0, 0)
		self.jump_begin = math3d.vector(0, 0, 0) # 起跳位置
		self.target_pos = math3d.vector(0, 0, 0)
		self.up_ofs = None # 上提高度
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

	# 播放动画
	def play_animation(self):
		try:
			self.model.play_animation(animation_names[self.cur_anim_idx])
		except:
			pass
	
	# 碰撞检测，可参考eggyolk2中的注释
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
	
	# 更新碰撞后的位置
	def update_collide_pos(self, fraction):
		length = (self.pos - self.target_pos).length
		moved = length * fraction
		if moved < g_margin:
			return
		self._pos.intrp(self.pos, self.target_pos, (moved - g_margin) / length)
		self.pos = self._pos
	
	# 是否可站立
	def can_stand(self, pos, hit_point, normal):
		if pos.y - hit_point.y < g_climb_height:
			return False
		if normal.dot(math3d.vector(0.0, 1.0, 0.0)) < 0.5:
			return False
		return True
	
	# 每帧去检测
	def get_user_input(self, speed):
		dir = math3d.vector(0, 0, 0)
		# 前进
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
	# 各种状态下，由move, slide, step_up, step_down这些功能函数去完成各种动作
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
	
	# 移动
	def move(self):
		if self.moving_dir.is_zero:
			return
		self.model.rotation_matrix = math3d.matrix.make_orient(self.moving_dir,
			math3d.vector(0.0, 1.0, 0.0))
		self.target_pos = self.pos + self.moving_dir
		result = self.sweep_test(self.pos, self.target_pos)
		if not result.hit:
			# 可行
			self.pos = self.target_pos
		return result
	
	# 滑动
	def slide(self, result):
		# 移动到碰撞点前
		dist = (self.pos - self.target_pos).length
		moved_dis = dist * result.fraction
		if moved_dis > g_margin:
			self._pos.intrp(self.pos, self.target_pos, (moved_dis - g_margin) / dist)
		# 剩余向量
		dir_remaining = self.target_pos - self.pos
		normal = - result.normal
		if self.no_up_slide:
			normal.y = 0.0
			normal.normalize()
		# 删除法线方向上的向量
		nv = normal * dir_remaining.dot(normal)
		self.moving_dir = dir_remaining - nv
		# slide,再次碰撞检测
		self.target_pos = self.pos + self.moving_dir
		new_result = self.sweep_test(self.pos, self.target_pos)
		if not new_result.hit:
			# 可行
			self.pos = self.target_pos
		return new_result
	
	# 上楼
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
	
	# 下踏
	def step_down(self):
		# 正常来说，你让角色最大能跨的高度，取负就是它能踏下最大高度
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
	# 角色的3种状态
	#-----------------------------------------------------------------------
	def update_moving(self):
		# 跳跃
		if self.cur_state_idx == 2:
			return
		# 行走
		prev_pos = math3d.vector(self.pos)
		self.moving_dir = self.get_user_input(g_moving_speed)
		if self.moving_dir.is_zero:
			return
		cur_moving = math3d.vector(self.moving_dir)
		self.up_ofs = math3d.vector(0, 0, 0)
		result = self.move()
		# 平走失败
		if result.hit:
			# 尝试上楼
			self.step_up()
			# 按移动方向移动
			self.move_and_slide()
		result = self.step_down()
		# 踏空 或 可站立行走
		if not result.hit or self.can_stand(self.pos, result.point, result.normal):
			return
		# 上楼失败，重置信息,直行
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
			# 什么都没碰到，继续下落
			self.pos = self.target_pos
			self.pos = self.pos
			return
		# 碰撞后是否可站立
		standing_pos = math3d.vector(0, 0, 0)
		standing_pos.intrp(self.pos, self.target_pos, result.fraction)
		if self.can_stand(standing_pos, result.point, result.normal):
			self.update_collide_pos(result.fraction)
			# 进入行走态
			self.update_collide_pos(result.fraction)
			self.cur_state_idx = 0
			return
		# 进行滑动
		result = self.slide(result)
		if result.hit:
			self.update_collide_pos(result.fraction)
			if self.can_stand(self.pos, result.point, result.normal):
				# 进入行走态
				self.cur_state_idx = 0
	
	def logic(self):
		prev_pos = self.pos
		# 状态更新
		self.state[self.cur_state_idx]()
		# 镜头跟随
		self.on_mouse_move()
		ofs = self.pos - prev_pos
		self.camera.position += ofs
		# 更新显示碰撞面信息时的中心点
		self.update_debug_drawing()
		# 切换动画
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
		
		
	# 非每帧需要检测的键盘输入
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
		# 控制相机高度
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
		# 相机碰撞检测
		pos = self.pos + dir * dist
		ray_filter = iphy3d.col_filter(0, 1)
		result = iphy3d.hit_by_ray(iworld3d.NO_2D_LAYER, self.pos, pos)
		# 碰到了,相机不可到达
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
