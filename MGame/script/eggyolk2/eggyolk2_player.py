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
		self.moving_dir = math3d.vector(0, 0, 0) # 移动方向
		self.target_pos = math3d.vector(0, 0, 0) # 目标位置
		self.is_dragging = False # 是否被鼠标拖动
		self.mouse_pos = (0, 0)  # 鼠标拖动位置
		self.pre_mouse_pos = (0, 0) # 上一次鼠标的位置
		
	def create_sprite(self, gim_file, name, layer_id):
		super(CGamePlayer, self).create_sprite(gim_file, name, layer_id)
		self.sprite.set_pick()   # 可被鼠标选中
		self.animations = ["npc_act_001", "npc_act_003"] # 每个状态对应的动作
		self.set_state(eggyolk2_const.PLAYER_STATE_DROPPING) # 初始状态为下落
	
	def create_bill(self, swf_file, text=""):
		if self.bill:
			self.bill.destroy()
		self.bill = iworld3d.space_movie(swf_file, True, pixel_unit=0.1, layer_id=eggyolk2_const.SCENE_LAYER)
		self.sprite.bind("cstop", self.bill)	# 绑定到cstop的挂接点上
		self.bill.billboard_type = True

		if text:
			# 获取space_movie的movie属性，再设置变量
			self.bill.movie.set_variable("name.text", text)

	def create_phy(self, layer_id):
		# 碰撞类别为npc，接受碰撞类别为npc
		self.phy = iphy3d.col_sphere(6, eggyolk2_const.COL_NPC, eggyolk2_const.COL_NPC)
		self.phy.add_to_layer(layer_id)
	
	def destroy(self):
		self.destroy_bill()
		self.sprite.destroy()

	## 更换碰撞体类型
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
			temp.rotation_matrix = self.sprite.rotation_matrix # 由于模型翻转过,此处需要翻转
			self.set_phy_key(0, 15, 0) # 设置key点
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

	# 动态碰撞检测
	def sweep_test(self, start, end):
		# 为了避免在end处碰撞而造成精度问题，此处将距离*2。
		ext_end = start + (end - start) * 2.0
		# 碰撞过滤，npc不用检测碰撞,排除碰撞类别为npc的。
		sweep_filter = iphy3d.col_filter(0, eggyolk2_const.COL_NPC, iphy3d.EXCLUDE_FILTER)
		# 开发者可用下列注释中的过滤方式对比效果
		#sweep_filter = iphy3d.col_filter(eggyolk2_const.COL_ROAD | eggyolk2_const.COL_NPC, 0, iphy3d.EXCLUDE_FILTER) # 无任何碰撞,可能会掉出屏幕
		#sweep_filter = iphy3d.col_filter(eggyolk2_const.COL_NPC , eggyolk2_const.COL_NPC, iphy3d.EQUAL_FILTER) # 只和npc碰撞，可能会掉出屏幕
		#sweep_filter = iphy3d.col_filter(eggyolk2_const.COL_NPC , eggyolk2_const.COL_ROAD, iphy3d.EQUAL_FILTER) # 只和路面碰撞
		#sweep_filter = iphy3d.col_filter(1 , 2, iphy3d.INEQUAL_FILTER) # 只和路面碰
		try:
			result = iphy3d.sweep_test(eggyolk2_const.SCENE_LAYER, self.phy, start, ext_end, sweep_filter)
		except iphy3d.iphy3d_exception, e:
			# 对模型碰撞体无用,会抛出异常，小蛋黄的模型体不是凸多边形
			print e,"切换到胶囊体"
			self.switch_phy_type(eggyolk2_const.COL_TYPE_CAPSULE, eggyolk2_const.SCENE_LAYER)
			return iphy3d.col_result()
		if result.hit:
			if result.fraction > 0.5 + eggyolk2_const.FLOAT_EPSILON:
				return iphy3d.col_result()
			else:
				result.fraction *= 2.0
				return result
		return result
	
	# 静态碰撞检测
	def anything_collision(self):
		return len(iphy3d.static_test(eggyolk2_const.SCENE_LAYER, self.phy)) != 0
	
	# 射线碰撞检测
	def is_ray_hit(self, start, end):
		return iphy3d.hit_by_ray(eggyolk2_const.SCENE_LAYER, start, end).hit
	
	# 更新碰撞后的位置
	def update_collide_pos(self, fraction):
		cur_pos = math3d.vector(*self.pos)
		length = (cur_pos - self.target_pos).length
		moved = length * fraction
		if moved < eggyolk2_const.MARGIN:
			return
		cur_pos.intrp(cur_pos, self.target_pos, (moved - eggyolk2_const.MARGIN) / length)
		self.pos = cur_pos.x, cur_pos.y, cur_pos.z
	
	# 移动
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
	
	# 更新移动
	def update_moving(self):
		# 如果在下落状态
		if self.state == eggyolk2_const.PLAYER_STATE_DROPPING:
			return
		# 行走状态
		self.moving()
	
	# 更新掉落
	def update_dropping(self):
		if self.state == eggyolk2_const.PLAYER_STATE_MOVING:
			return
		down = math3d.vector(0, eggyolk2_const.GRAVITY, 0)
		cur_pos = math3d.vector(*self.pos)
		self.target_pos = cur_pos + down
		result = self.sweep_test(cur_pos, self.target_pos)
		if not result.hit:
			# 没碰到东西，继续下落
			self.pos = self.target_pos.x, self.target_pos.y, self.target_pos.z
			self.set_state(eggyolk2_const.PLAYER_STATE_DROPPING)
			return
		# 发现碰撞，更新位置
		self.update_collide_pos(result.fraction)
		self.set_state(eggyolk2_const.PLAYER_STATE_MOVING)

	def add_round_shadow(self):
		self.sprite.add_round_shadow(False, (5,5))

	def update_plane_shadow(self):
		# 以player位置作射线，计算碰撞到哪个石头
		p0 = self.pos
		coldata = iphy3d.hit_by_ray(eggyolk2_const.SCENE_LAYER, \
			math3d.vector(p0[0], p0[1], p0[2]),\
			math3d.vector(p0[0], p0[1]+10000, p0[2]))
		if coldata.hit:
			self.sprite.set_shadow_visible(True)
			self.sprite.clear_shadows()
			# 使用场景内置的0号光照
			self.sprite.add_plane_shadow((coldata.normal, coldata.point), "light_1")
		else:
			self.sprite.set_shadow_visible(False)


	# 更新函数
	def update(self):
		self.update_dropping()
		self.update_moving()
		self.on_mouse_dragging()
		if shadow_type == 2:
			# 因为平面阴影需要计算脚底的阴影位置，所以才每帧都要运行一次
			self.update_plane_shadow()
	
	# 响应鼠标拖拽
	def on_mouse_dragging(self):
		if not self.is_dragging:
			return
		# 下落的时候也可以拖拽
		self.set_state(eggyolk2_const.PLAYER_STATE_MOVING)
		# 得到世界坐标
		p, d = iworld3d.screen_to_world(eggyolk2_const.SCENE_LAYER, 
			self.mouse_pos[0], self.mouse_pos[1])
		d.normalize()
		position = p + d * ((-100 - p.z) / d.z) # 实际应用中需保证射线足够长，且摄像机在屏幕后方
												# 此处为了保证射线在z轴方向的投影长度要大于100
												# 这里position.z近似等于-100
		pre_pos = self.pos
		pre_pos_v = math3d.vector(*pre_pos)
		# 计算长度
		d = position - pre_pos_v
		# 避免最后一次移动带来的抖动和对0向量规范化
		if d.length < 1:
			return
		d.normalize()
		p = pre_pos_v + d * 2
		# 每帧向鼠标位置移动单位向量的距离
		self.pos = p.x, p.y, p.z
		# 静态碰撞演示
		if self.anything_collision():
			self.pos = pre_pos
	
	# 瞬间移动到某个无碰撞体的屏幕点上，此函数为演示射线碰撞函数
	def flash_to_pos(self, screen_x, screen_y):
		# 得到世界坐标
		p, d = iworld3d.screen_to_world(eggyolk2_const.SCENE_LAYER, 
			screen_x, screen_y)
		d.normalize()
		position = p + d * ((-100 - p.z) / d.z) # 实际应用中需保证射线足够长，且摄像机在屏幕后方
												# 此处为了保证射线在z轴方向的投影长度要大于100
												# 这里position.z近似等于-100
		# 射线起点为摄像机的位置，终点为屏幕上物体所在层的位置
		if not self.is_ray_hit(math3d.vector(0, 0, 0), position):
			# 为了避免边缘的碰撞，再做一次static_test
			pre_pos = self.pos
			self.pos = position.x, position.y, position.z
			if self.anything_collision():
				self.pos = pre_pos
				return
			self.set_state(eggyolk2_const.PLAYER_STATE_DROPPING)
	
	## 设置玩家状态
	def set_state(self, state):
		self.state = state
		self.sprite.play_animation(self.animations[self.state])
