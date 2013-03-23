# -*- coding:GBK -*-

import hall_callback

import hw_room
import hw_msg

event_callback = {
		'hw_cs_leave_room': hw_room.HelloWorldRoom.on_player_req_leave,
}

def init():
	global event_callback
	### 设置游戏房间的 消息定义 和 消息回调函数
	hall_callback.register_game_room_msgdefine_and_callback(\
		hw_msg.msg, event_callback)

	### 设置房间类的定义
	hall_callback.set_class_define(
			{ ### 游戏模式: (最小人数, 最大人数, 类, 模式名称) 
				1: (1, 1, hw_room.HelloWorldRoom, "单人模式"),
			} 
	)


## 使用公共大厅
hall_callback.use_hall()
### 设置初始化函数
hall_callback.init = init

