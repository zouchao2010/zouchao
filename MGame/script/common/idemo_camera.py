# -*- coding:GBK -*-
# 一个简单的相机控制，用于demo的演示
import math3d
import math
import game
import iworld3d

STYLE_FREELOOK = 0	#			自由视角
STYLE_ORBIT = 1		#			环绕
STYLE_MANUAL = 2	#			手动

# 可配置信息
INIT_DIST = 100.0	#			初始相机距离
PIXEL_TO_ANGLE = 0.006283	# 像素到弧度的比例

g_mouse_dragging = False
g_mouse_prev_pos = None

class camera_man(object):
	def __init__(self, camera):
		self._camera = camera
		self._target = None
		self._orbiting = False
		self._zooming = False
		self._topspeed = 2
		self._velocity = math3d.vector(0, 0, 0)
		self._is_forward = False
		self._is_back = False
		self._is_left = False
		self._is_right = False
		self._is_up = False
		self._is_down = False
		self._fast_move = False
		self._style = STYLE_FREELOOK
	
	def destroy(self):
		self._camera = None
	
	# 设置相机的距离
	def set_yawpitchdist(self, yaw, pitch, dist):
		if self._target:
			self._camera.position = self._target.position
			self._camera.rotation_matrix = self._target.rotation_matrix
			self._camera.yaw(yaw)
			self._camera.pitch(-pitch)
			self.move_relative(-dist)
		else:
			self._camera.set_placement(
				dist,
				math3d.vector(0, -1, -1),
				math3d.vector(0, 1, 0))
	
	# 移动相机的相对位置
	def move_relative(self, dist):
		d = self._camera.rotation_matrix.forward
		if not d.is_zero:
			d.normalize()
			self._camera.position += d * dist
		else:
			# 复位。注意，错误情况可能有递归调用。
			self.set_yawpitchdist(0, math.pi / 12.0, INIT_DIST)

	def _set_target(self, t):
		if t is self._target:
			return
		self._target = t
		if t:
			self.set_yawpitchdist(0, math.pi / 12.0, INIT_DIST)
	
	def _get_target(self):
		return self._target

	target = property(_get_target, _set_target)
	
	def _set_style(self, s):
		if self._style != STYLE_ORBIT and s == STYLE_ORBIT:
			self.manual_stop()
			self.set_yawpitchdist(0, math.pi / 12.0, INIT_DIST)
		elif self._style != STYLE_MANUAL and s == STYLE_MANUAL:
			self.manual_stop()
		self._style = s
			
	def _get_style(self):
		return self._style
	
	style = property(_get_style, _set_style)

	def manual_stop(self):
		if self._style == STYLE_FREELOOK:
			self._is_forward = False
			self._is_back = False
			self._is_left = False
			self._is_right = False
			self._is_up = False
			self._is_down = False
			self._velocity = math3d.vector(0, 0, 0)
	
	def logic(self):
		if self._style == STYLE_FREELOOK:
			accel = math3d.vector(0, 0, 0)
			if self._is_forward:
				accel += self._camera.rotation_matrix.forward
			elif self._is_back:
				accel -= self._camera.rotation_matrix.forward
			elif self._is_left:
				accel -= self._camera.rotation_matrix.right
			elif self._is_right:
				accel += self._camera.rotation_matrix.right
			elif self._is_up:
				accel += self._camera.rotation_matrix.up
			elif self._is_down:
				accel -= self._camera.rotation_matrix.up
			top_speed = self._topspeed * 20.0 if self._fast_move else self._topspeed
			if not accel.is_zero:
				accel.normalize()
				self._velocity += accel * top_speed
			else:
				self._velocity -= self._velocity * 0.1
			if self._velocity.length_sqr > top_speed * top_speed:
				self._velocity.normalize()
				self._velocity *= top_speed
			elif self._velocity.is_zero:
				self._velocity = math3d.vector(0, 0, 0)
			if self._velocity != math3d.vector(0, 0, 0):
				self._camera.position += self._velocity
		self.on_mouse_move()

	def on_key_msg (self, msg, key):
		if msg == game.MSG_KEY_DOWN:
			if key == game.VK_W:
				self._is_forward = True
			if key == game.VK_S:
				self._is_back = True
			if key == game.VK_A:
				self._is_left = True
			if key == game.VK_D:
				self._is_right = True
			if key == game.VK_PAGEUP:
				self._is_up = True
			if key == game.VK_PAGEDOWN:
				self._is_down = True
			if key == game.VK_SHIFT:
				self._fast_move = True
		elif msg == game.MSG_KEY_UP:
			if key == game.VK_W:
				self._is_forward = False
			if key == game.VK_S:
				self._is_back = False
			if key == game.VK_A:
				self._is_left = False
			if key == game.VK_D:
				self._is_right = False
			if key == game.VK_PAGEUP:
				self._is_up = False
			if key == game.VK_PAGEDOWN:
				self._is_down = False
			if key == game.VK_SHIFT:
				self._fast_move = False
			
	def on_mouse_move(self):
		if not g_mouse_dragging:
			return
		global g_mouse_prev_pos
		dx = game.mouse_x - g_mouse_prev_pos[0]
		dy = game.mouse_y - g_mouse_prev_pos[1]
		g_mouse_prev_pos = game.mouse_x, game.mouse_y
		if self._style == STYLE_ORBIT:
			if self._target:
				dist = (self._camera.position - self._target.position).length
			else:
				dist = self._camera.position.length
			if self._orbiting:
				self._camera.position = self._target.position
				self._camera.yaw(-dx * PIXEL_TO_ANGLE)
				self._camera.pitch(-dy * PIXEL_TO_ANGLE)
				self.move_relative(-dist)
			elif self._zooming:
				self.move_relative(-dy * 0.004 * dist)
		elif self._style == STYLE_FREELOOK:
			self._camera.yaw(dx * PIXEL_TO_ANGLE, iworld3d.SPACE_TYPE_WORLD)
			self._camera.pitch(dy * PIXEL_TO_ANGLE)
		
	def on_mouse_msg(self, msg, key):
		global g_mouse_dragging, g_mouse_prev_pos
		if msg == game.MSG_MOUSE_DOWN and key == game.MOUSE_BUTTON_LEFT:
			g_mouse_dragging = True
			g_mouse_prev_pos = game.mouse_x, game.mouse_y
			if self._style != STYLE_ORBIT:
				return
			if key == game.MOUSE_BUTTON_LEFT:
				self._orbiting = True
			if key == game.MOUSE_BUTTON_RIGHT:
				self._zooming = True
		if msg == game.MSG_MOUSE_UP:
			g_mouse_dragging = False
			if self._style != STYLE_ORBIT:
				return
			if key == game.MOUSE_BUTTON_LEFT:
				self._orbiting = False
			if key == game.MOUSE_BUTTON_RIGHT:
				self._zooming = False

	def on_mouse_wheel(self, msg, delta, key_state):
		if self._target:
			dist = (self._camera.position - self._target.position).length
		else:
			dist = self._camera.position.length
		self.move_relative(delta * 0.0008 * dist)
