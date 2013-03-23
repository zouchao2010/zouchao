# -*- coding:GBK -*-

import game
import iapi
import idemo_glb
import idemo_browser

game_id = 0
browser = None

def init (**args):
	global game_id, browser
	game_id = int(args['gameid'])
	API = iapi.API()
	# 注册回调
	API.register_callback( game_id,
		my_logic, my_render, my_post_logic,
		on_key_msg = on_key_msg, on_mouse_msg = on_mouse_msg, on_mouse_wheel =  on_mouse_wheel)
	# 关闭聊天窗口
	API.chat_hide(True)
	idemo_glb.API = API
	# 启动browser
	browser = idemo_browser.browser()
	browser.init()

def force_destroy():
	global browser
	browser.destroy()
	browser = None
	idemo_glb.API = None

def my_logic():
	if browser:
		browser.logic()
	
def my_post_logic():
	if browser:
		browser.post_logic()
	
def my_render():
	if browser:
		browser.render()
	
def on_key_msg(msg, key):
	if browser:
		browser.on_key_msg(msg, key)

def on_mouse_msg(msg, key):
	if browser:
		browser.on_mouse_msg(msg, key)

def on_mouse_wheel(msg, delta, key_state):
	if browser:
		browser.on_mouse_wheel(msg, delta, key_state)

def start_demo(demo):
	if browser:
		browser.start_demo(demo)
