# -*- coding:GBK -*-

import hall_callback

import hw_room
import hw_msg

event_callback = {
		'hw_cs_leave_room': hw_room.HelloWorldRoom.on_player_req_leave,
}

def init():
	global event_callback
	### ������Ϸ����� ��Ϣ���� �� ��Ϣ�ص�����
	hall_callback.register_game_room_msgdefine_and_callback(\
		hw_msg.msg, event_callback)

	### ���÷�����Ķ���
	hall_callback.set_class_define(
			{ ### ��Ϸģʽ: (��С����, �������, ��, ģʽ����) 
				1: (1, 1, hw_room.HelloWorldRoom, "����ģʽ"),
			} 
	)


## ʹ�ù�������
hall_callback.use_hall()
### ���ó�ʼ������
hall_callback.init = init

