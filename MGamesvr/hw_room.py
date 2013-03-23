#-*- coding:GBK -*-

import hall_object
import hall_callback
import log

class HelloWorldRoom(hall_object.HallRoom):
	def __init__(self, room_id=0, name='', mode=0, host=0, pwd='', max_num=0):

		super(HelloWorldRoom, self).__init__(room_id,
				name, mode, host, pwd, max_num)

		self.msgmgr = hall_callback.get_game_room_msgmgr()

	##  重载  ########
	def cghall_on_player_enter_room(self, player, obj):
		"""
		有玩家进入此房间时, 会回调用此函数
		"""
		self.log.info("on player enter room. uid:%s hid:%s" % (player.uid, player.hid))
	
	def cghall_on_player_leave_room(self, hid):
		"""
		有玩家离开房间时, 会回调此函数
		"""
		self.log.info("on player leave room hid:%s"%hid)

	def on_player_req_leave(self, player, msg):
		"""
		客户端请求离开
		"""
		self.log.info("on player req leave uid:%s hid:%s"\
				% (player.uid, player.hid))
		self.cghall_tell_hall_player_leave_room(player.hid)

		
