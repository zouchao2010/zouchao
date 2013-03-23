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


# ��Ϸ������ʼ������
def init():
	# ������ģ���ʼ��
	iphy2d.init(30)
	iphy2d.set_gravity((0, 10))

	global g_objs
	g_objs = {}

	# iworld2dģ���ʼ��
	iworld2d.init()
	# ���ɱ���
	global background
	background = iworld2d.image2d("idemos/res/rabbit/world2d/txg/demo.txg|background", layer_id=0)
	background.pos = (0,0)


# ����һ����Ϸ����
def create_obj(name, t, x, y):
	# t ��ʾrabbit_data��һ����̬����id���
	data = rabbit_data.get_data(t)
	phy_init = data["phy_init"]
	pparam = data["phy_param"]
	fparam = data.get("face")
	name = name.split("_")[0]

	# ͨ�����֣�������Ӧ�Ķ���
	im = __import__("rabbit_%s"%name)
	temp_obj = im.CRabbitObj(phy_init[0], phy_init[1])
	temp_obj.set_name(t)
	# ������������
	for k in pparam:
		v = pparam[k]
		setattr(temp_obj.phy, k, v)
	# ������Ⱦ����
	if fparam:
		temp_obj.create_face(fparam["file"])
		if fparam.get("size"):
			temp_obj.face.size = fparam.get("size")
		if fparam.get("key_point"):
			temp_obj.face.key_point = fparam.get("key_point")
	temp_obj.pos = (x, y)
	g_objs[temp_obj.id] = temp_obj
	return temp_obj


# ���Զ����ʽ���ļ��ж�ȡ��ͼ����
def load_map(filename):
	fr = idemo_glb.API.read_file(filename)
	# ���Ե�һ��
	buf = fr.split("\n")[1:]
	num = int(buf[0])
	buf = buf[1:]
	data = []
	for i in range(num):
		d = buf[i].split(":")
		name = d[0]
		d = d[1].split(",")
		t, x, y = int(d[0]), float(d[1]), float(d[2])	# ��ȡtype_id, x, y
		create_obj(name, t, x, y) # ����type_id, x, y������Ϸ����
		data.append((t, x, y))


# ������ͼ
def create_map():
	load_map("idemos/res/rabbit/1.map")
	
	# ������ײ��ص���һ��ֻ��Ҫ����set_collided_callback����
	# ��Ϊrabbit_tutu���õ�����������(sensor)������Ҳ��Ҫ����set_first_collided_callback/set_last_collided_callback
	iphy2d.set_collided_callback(obj_collided)
	iphy2d.set_first_collided_callback(obj_collided)
	iphy2d.set_last_collided_callback(obj_collided)


# ���ٵ�ͼ
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


# ��ײ�ص�����
def obj_collided(obj_a, obj_b):
	# ֪ͨ��ײ˫��
	obja = obj_a.get_user_data()
	objb = obj_b.get_user_data()
	if obja and objb:
		obja.on_hit(objb)
		objb.on_hit(obja)
	return True


# �����Ϣ�ص�
def on_mouse_msg(msg, key):
	global obj_on_mouse
	global down_pos
	if obj_on_mouse is None:
		# �������
		import rabbit_bear
		obj_on_mouse = create_obj("bear", 100, 0, 0)
		obj_on_mouse.face.bring_to_front()
	if msg == game.MSG_MOUSE_DOWN:
		# ��¼��갴�µ�λ��
		x = game.mouse_x
		y = game.mouse_y
		down_pos = math3d.vector2(x, y)
		obj_on_mouse.phy.linear_damping = 0
		obj_on_mouse.stop_fly()
	elif msg == game.MSG_MOUSE_UP:
		# ����ɿ�ʱ�����վ�����������Ĵ�С
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


# ������Ϣ�ص�
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
			# �������ĵ���ϵ����Ϊ0
			test = create_obj("sin", 10, 250, 560)
			ball = create_obj("obj", 11, 250, 400)
			# С�����ײ������2�������Ϊ1���򲻲�����ײ
			ball.phy.category = 2
		elif key == game.VK_F5:
			iphy2d.set_gravity((0, 10))
			destroy_map()
			create_map()
		elif key == game.VK_F7:
			if not background.is_hide():
				# ����debugģʽ
				background.hide()
				import rabbit_obj
				iworld2d.camera_world_scale(rabbit_obj.MAP_SCALE)
				iworld2d.camera_world_pos(-512+rabbit_obj.MAP_SCALE*2+4, -368+rabbit_obj.MAP_SCALE*2-20)
				iphy2d.set_debug_draw(True)
			else:
				# ��ԭ
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
			# �������ؽڵ���ʾ(�൱��box2d testbed��web)
			rabbit_test_1.start()
		elif key == game.VK_2:
			# ������ת�ؽڵ���ʾ(�൱��box2d testbed��bridge)
			rabbit_test_2.start()
		elif key == game.VK_3:
			# �����ƶ��ؽڵ���ʾ(�൱��box2d testbed��prismatic)
			rabbit_test_3.start()
		elif key == game.VK_4:
			# ������Ϲؽڵ���ʾ(�൱��box2d testbed��slider crank)
			rabbit_test_4.start()
		elif key == game.VK_5:
			# ����Ħ���ؽڵ���ʾ(�൱��box2d testbed��apply force)
			rabbit_test_5.start()
	elif msg == game.MSG_KEY_PRESSED:
		if key == game.MOUSE_BUTTON_LEFT:
			# �����ס����������������λ��
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



# ��demo��ȫ��������������ͼƬ��λ�ƺ���ת
def update():
	# �����������
	iphy2d.update()
	# ��Ϸ�߼���update
	my_update()
	# ��Ϸ��Ⱦ�����
	my_render()


# ����������Ϸ���󣬽����߼�����
def my_update():
	for id in g_objs.keys():
		o = g_objs[id]
		o.update()


# ����������Ϸ���󣬽��л���ˢ��
def my_render():
	for id in g_objs.keys():
		o = g_objs[id]
		o.draw()


def destroy_scene():
	# iphy2d��������iworld2d����
	destroy_map()
	iphy2d.destroy()
	iworld2d.destroy()

