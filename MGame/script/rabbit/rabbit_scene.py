# -*- coding:GBK -*-

import iphy2d
import iworld2d
import math3d

import rabbit_data
import idemo_glb

import random
import game

import rabbit_test_1
import rabbit_test_2
import rabbit_test_3
import rabbit_test_4
import rabbit_test_5

obj_on_mouse = None

g_objs = {}
down_pos = None
g_score = 0

ball = None
background = None

pflag = False


# 游戏场景初始化函数
def init():
	# 对物理模块初始化
	iphy2d.init(30)
	iphy2d.set_gravity((0, 10))

	global g_objs
	g_objs = {}

	# iworld2d模块初始化
	iworld2d.init()
	# 生成背景
	global background
	background = iworld2d.image2d("idemos/res/rabbit/world2d/txg/demo.txg|background", layer_id=0)
	background.pos = (0,0)


# 创建一个游戏对象
def create_obj(name, t, x, y):
	# t 表示rabbit_data的一个静态数据id编号
	data = rabbit_data.get_data(t)
	phy_init = data["phy_init"]
	pparam = data["phy_param"]
	fparam = data.get("face")
	name = name.split("_")[0]

	# 通过名字，生成相应的对象
	im = __import__("rabbit_%s"%name)
	temp_obj = im.CRabbitObj(phy_init[0], phy_init[1])
	temp_obj.set_name(t)
	# 设置物理数据
	for k in pparam:
		v = pparam[k]
		setattr(temp_obj.phy, k, v)
	# 设置渲染数据
	if fparam:
		temp_obj.create_face(fparam["file"])
		if fparam.get("size"):
			temp_obj.face.size = fparam.get("size")
		if fparam.get("key_point"):
			temp_obj.face.key_point = fparam.get("key_point")
	temp_obj.pos = (x, y)
	g_objs[temp_obj.id] = temp_obj
	return temp_obj


# 从自定义格式的文件中读取地图数据
def load_map(filename):
	fr = idemo_glb.API.read_file(filename)
	# 忽略第一行
	buf = fr.split("\n")[1:]
	num = int(buf[0])
	buf = buf[1:]
	data = []
	for i in range(num):
		d = buf[i].split(":")
		name = d[0]
		d = d[1].split(",")
		t, x, y = int(d[0]), float(d[1]), float(d[2])	# 获取type_id, x, y
		create_obj(name, t, x, y) # 根据type_id, x, y创建游戏对象
		data.append((t, x, y))


# 创建地图
def create_map():
	load_map("idemos/res/rabbit/1.map")
	
	# 设置碰撞后回调，一般只需要设置set_collided_callback即可
	# 因为rabbit_tutu中用到传感器属性(sensor)，所以也需要设置set_first_collided_callback/set_last_collided_callback
	iphy2d.set_collided_callback(obj_collided)
	iphy2d.set_first_collided_callback(obj_collided)
	iphy2d.set_last_collided_callback(obj_collided)


# 销毁地图
def destroy_map():
	rabbit_test_1.destroy()
	rabbit_test_2.destroy()
	rabbit_test_3.destroy()
	rabbit_test_4.destroy()
	rabbit_test_5.destroy()

	global g_objs
	for id in g_objs.keys():
		o = g_objs[id]
		o.destroy()
	g_objs = {}
	global obj_on_mouse, ball
	obj_on_mouse = None
	ball = None


# 碰撞回调函数
def obj_collided(obj_a, obj_b):
	# 通知碰撞双方
	obja = obj_a.get_user_data()
	objb = obj_b.get_user_data()
	if obja and objb:
		obja.on_hit(objb)
		objb.on_hit(obja)
	return True


# 鼠标消息回调
def on_mouse_msg(msg, key):
	global obj_on_mouse
	global down_pos
	if obj_on_mouse is None:
		# 生成浣熊
		import rabbit_bear
		obj_on_mouse = create_obj("bear", 100, 0, 0)
		obj_on_mouse.face.bring_to_front()
	if msg == game.MSG_MOUSE_DOWN:
		# 记录鼠标按下的位置
		x = game.mouse_x
		y = game.mouse_y
		down_pos = math3d.vector2(x, y)
		obj_on_mouse.phy.linear_damping = 0
		obj_on_mouse.stop_fly()
	elif msg == game.MSG_MOUSE_UP:
		# 鼠标松开时，按照距离计算推力的大小
		newpos = math3d.vector2(game.mouse_x, game.mouse_y)
		if down_pos is None:
			return
		nn = (down_pos-newpos)
		if nn:
			nn.x *= 40
			nn.y *= 40
		print "bear linear impulse", nn.length
		obj_on_mouse.phy.body_type = iphy2d.DYNAMIC_BODY
		obj_on_mouse.phy.apply_linear_impulse(nn, obj_on_mouse.phy.position)
		obj_on_mouse.fly()

		down_pos = None


# 键盘消息回调
def on_key_msg(msg, key):
	global ball
	if msg == game.MSG_KEY_DOWN:
		if key is game.VK_F1:
			for i in range(20):
				test = create_obj("bear", 100, random.randint(50, 1000), random.randint(0, 100))
				test.phy.body_type = iphy2d.DYNAMIC_BODY
		elif key is  game.VK_F2:
			iphy2d.set_gravity((10, 1))
		elif key is game.VK_F3:
			iphy2d.set_gravity((0, 10))
		elif key is game.VK_F4:
			# 球和曲面的弹性系数均为0
			test = create_obj("sin", 10, 250, 560)
			ball = create_obj("obj", 11, 250, 400)
			# 小球的碰撞参数是2，如果设为1，则不产生碰撞
			ball.phy.category = 2
		elif key == game.VK_F5:
			iphy2d.set_gravity((0, 10))
			destroy_map()
			create_map()
		elif key == game.VK_F7:
			if not background.is_hide():
				# 进入debug模式
				background.hide()
				import rabbit_obj
				iworld2d.camera_world_scale(rabbit_obj.MAP_SCALE)
				iworld2d.camera_world_pos(-512+rabbit_obj.MAP_SCALE*2+4, -368+rabbit_obj.MAP_SCALE*2-20)
				iphy2d.set_debug_draw(True)
			else:
				# 还原
				iphy2d.set_debug_draw(False)
				background.show()
				iworld2d.camera_world_scale(1)
				iworld2d.camera_world_pos(0, 0)
		elif key == game.VK_F11:
			global pflag
			pflag = not pflag
			idemo_glb.API.show_performance(pflag)
		elif key == game.VK_SPACE:
			if ball:
				ball.phy.apply_linear_impulse(math3d.vector2(0,100), ball.phy.position)
				ball.phy.density = 100
				ball.phy.restitution = 0
		elif key == game.VK_1:
			# 进入距离关节的演示(相当于box2d testbed的web)
			rabbit_test_1.start()
		elif key == game.VK_2:
			# 进入旋转关节的演示(相当于box2d testbed的bridge)
			rabbit_test_2.start()
		elif key == game.VK_3:
			# 进入移动关节的演示(相当于box2d testbed的prismatic)
			rabbit_test_3.start()
		elif key == game.VK_4:
			# 进入组合关节的演示(相当于box2d testbed的slider crank)
			rabbit_test_4.start()
		elif key == game.VK_5:
			# 进入摩擦关节的演示(相当于box2d testbed的apply force)
			rabbit_test_5.start()
	elif msg == game.MSG_KEY_PRESSED:
		if key == game.MOUSE_BUTTON_LEFT:
			# 如果按住鼠标左键，则更新浣熊位置
			x = game.mouse_x
			y = game.mouse_y
			if obj_on_mouse:
				obj_on_mouse.pos = (x, y)
				obj_on_mouse.phy.body_type = iphy2d.STATIC_BODY
	elif msg == game.MSG_KEY_UP:
		if key == game.VK_SPACE:
			if ball:
				ball.phy.density = 0.3



def add_score(s):
	global g_score
	g_score += s
	#print ("score : %s"%(g_score/800))



# 此demo完全由物理引擎驱动图片的位移和旋转
def update():
	# 物理引擎更新
	iphy2d.update()
	# 游戏逻辑层update
	my_update()
	# 游戏渲染层更新
	my_render()


# 遍历所有游戏对象，进行逻辑更新
def my_update():
	for id in g_objs.keys():
		o = g_objs[id]
		o.update()


# 遍历所有游戏对象，进行绘制刷新
def my_render():
	for id in g_objs.keys():
		o = g_objs[id]
		o.draw()


def destroy_scene():
	# iphy2d必须先于iworld2d销毁
	destroy_map()
	iphy2d.destroy()
	iworld2d.destroy()

