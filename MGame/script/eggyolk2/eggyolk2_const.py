# -*- coding:GBK -*-
SCENE_LAYER = 2

GRAVITY = 1								# 下落速度
MARGIN = 0.1							# 物体间的最小距离
MOVING_SPEED = 1						# 移动速度

PLAYER_STATE_MOVING		= 0				# 玩家移动状态
PLAYER_STATE_DROPPING	= 1				# 玩家下落状态
FLOAT_EPSILON = 0.001					# 浮点数精度

# 碰撞检测的类别
COL_NPC = 0x0001						# 与npc碰撞
COL_ROAD = 0x0002						# 与路面碰撞

# 碰撞体的种类
COL_TYPE_SPHERE = 0						# 球体
COL_TYPE_CAPSULE = 1						# 胶囊体
COL_TYPE_CYLINDER= 2						# 圆柱体
COL_TYPE_MODEL	 = 3						# 模型