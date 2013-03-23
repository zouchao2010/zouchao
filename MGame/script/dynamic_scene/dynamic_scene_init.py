import idemo_glb
import idemo_demo
import iworld3d
import math3d
import game
import math


inst = None
SCN_FILE = "idemos/res/dynamic_scene/scene/s%d.scn"


# 相机相对主角的偏移
CAMERA_DISTANCE = math3d.vector(0,-50,100)

def init(browser):
	global inst
	if inst is None:
		inst = demo()
		inst.init(browser)

def destroy():
	global inst
	if inst:
		inst.destroy()
		inst = None
		
# 场景为
class demo(idemo_demo.demo):
	def __init__(self):
		super(demo, self).__init__()
		iworld3d.init()
		self.scn = iworld3d.create_scene3d(SCN_FILE%1)
		
		self.player = iworld3d.model3d("idemos/res/eggyolk/world3d/xiaodanhuang.gim")
		self.player.pos = (0,0,0)
		
		self.camera = iworld3d.get_camera(iworld3d.NO_2D_LAYER)

		# 预先生成如下分块的场景，其中1为刚生成的self.scn
		# 323
		# 212
		# 323
		for offset in ((-1,0), (1,0), (0,-1), (0,1)):
			self.scn.auto_load_scene(SCN_FILE%2, math3d.vector(offset[0]*400, 0, offset[1]*400))
		for offset in ((1,1), (-1,1), (1,-1), (-1,-1)):
			self.scn.auto_load_scene(SCN_FILE%3, math3d.vector(offset[0]*400, 0, offset[1]*400))
		
		self.scn.set_view_range(100)
		# 如果设置1000，则一开始就能看到所有场景
		# self.scn.set_view_range(1000)

		self.scene_pos = {}	# 记录动态加载的场景位置


	def init(self, browser):
		super(demo, self).init(browser)


	# 销毁函数
	def destroy(self):
		pass


	# 逻辑帧
	def logic(self):
		if self.player:
			self.camera.position = self.player.position-CAMERA_DISTANCE
			self.camera.look_at(self.player.position)
			
			# 主角位置设为场景自动加载的中心点
			self.scn.set_view_position(self.player.position)
			
			# 动态添加外围的场景
			x = int(self.player.position.x+200)/400
			y = int(self.player.position.z+200)/400
			if (abs(x)>=2 or abs(y)>=2) and (x, y) not in self.scene_pos:
				self.scene_pos[(x, y)] = 1
				self.scn.auto_load_scene(SCN_FILE%4, math3d.vector(x*400, 0, y*400))
				


	# 键盘消息
	def on_key_msg(self, msg, key):
		super(demo, self).on_key_msg(msg, key)
		if key == game.VK_W and msg==game.MSG_KEY_PRESSED:
			self.player.position += math3d.vector(0,0,5)
		elif key == game.VK_S and msg==game.MSG_KEY_PRESSED:
			self.player.position += math3d.vector(0,0,-5)
		elif key == game.VK_A and msg==game.MSG_KEY_PRESSED:
			self.player.position += math3d.vector(-5,0,0)
		elif key == game.VK_D and msg==game.MSG_KEY_PRESSED:
			self.player.position += math3d.vector(5,0,0)
