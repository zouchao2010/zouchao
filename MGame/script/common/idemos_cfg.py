# -*- coding:GBK -*-

#demo browser配置文件
CFG = {
	"d2mtl_effect":\
		{
			"title" : "2D材质效果演示",
			"desc" : """
src:idemos/script/d2mtl_effect
此demo用于展示2D材质效果
iTownSDK提供了一些常用的效果，如:
泛光/灰化/暗角/HSV/漩涡/水波/马赛克等效果.
""",
			"thumbnail" : "d2mtl_effect.png",
			"category1" : "2D",
			"category2" : "进阶",
		},
	"actiondemo":\
		{
			"title" : "2D动画演示",
			"desc"	: """
src:idemos/script/action_demo
iaction2d演示demo
左右键 ----------- 前后切换demo演示
P ---------------- 暂停
S ---------------- 停止
R ---------------- 恢复
					""",
			"thumbnail" : "actiondemo.png",
			"category1" : "2D",
			"category2" : "入门",
		},
	"eggyolk2":
		{
			"title" : "3D碰撞与阴影",
			"desc"	: """
src:idemos/script/eggyolk2
3D演示demo
F2 ----------- 碰撞包围盒的演示
F3 ----------- 切换无阴影/圆影/平面阴影
F4 ----------- 把场景的0号光源，随机换一个角度(平面阴影有效)
WSAD --------- 移动小蛋黄,动态碰撞演示
鼠标左键拖动-- 拖动鼠标，小蛋黄跟随，静态碰撞演示
鼠标右键------ 瞬移小蛋黄，射线碰撞演示
数字1-4--------变换小蛋黄的碰撞体，1:胶囊体 2:圆柱体 3：球体 4：模型体(不能用于动态碰撞演示)
					""",
			"thumbnail" : "eggyolk2.png",
			"category1" : "3D",
			"category2" : "进阶",
		},
	"itownroom":
		{
			"title" : "3D角色与镜头控制",
			"desc"	: """
src:idemos/script/itownroom
3D 场景demo
welcome to iTown~
  演示如何加载场景
  演示如何进行角色控制
  演示如何进行相机控制
WASD ------------- 控制角色移动
空格 ------------- 跳跃
鼠标拖动及滚轮 --- 控制相机
M    ------------- 打开/关闭 碰撞debug显示
					""",
			"thumbnail" : "itownroom.png",
			"category1" : "3D",
			"category2" : "进阶",
		},
			"terriandemo":
	{
	"title" : "地形",
			"desc"	: """
src:idemos/script/terriandemo
3D 地形demo
  演示如何加载地形场景
  控制角色及相机请参考itownroom
WASD ------------- 控制角色移动
空格 ------------- 跳跃
鼠标拖动及滚轮 --- 控制相机
M    ------------- 打开/关闭 碰撞debug显示
					""",
			"thumbnail" : "terriandemo.png",
			"category1" : "3D",
			"category2" : "进阶",
		},
		"avatardemo":
		{
			"title" : "AVATAR演示",
			"desc"	: """
src:idemos/script/avatardemo
1) 演示如何使用动态avatar
2) 利用demo选择lookat函数的参数参考值
(调节镜头参数时请在初始时静态时进行调整，lookat是用来初始化相框的)
操作如下：
WS键 --------------- 相机高度控制
AD键 --------------- 相机距离控制
左右键 ------------- 旋转avatar
P键 ---------------- 动态/静态切换
等待类动作: -------- 1键 , 2键 , 3键, 4键
					""",
			"thumbnail" : "avatardemo.png",
			"category1" : "杂项",
			"category2" : "入门",
		},
		"rabbit":
		{
			"title" : "兔子范例",
			"desc"	: """
src:idemos/script/rabbit
物理测试demo
F1 ------ 增加20只浣熊
F2 ------ 改变重力场
F3 ------ 恢复重力场
F4 ------ 生成一段曲线和小球
F5 ------ 重新加载地图
F7 ------ 进入debug模式/还原
F11 ------ 打开/关闭性能曲线
空格------ 增加F4生成小球的向下速度
数字1 ------ 距离关节的演示
数字2 ------ 旋转关节的演示
数字3 ------ 移动关节的演示
数字4 ------ 关节组合的演示
数字5 ------ 摩擦关节的演示""",
			"thumbnail" : "rabbit.png",
			"category1" : "物理",
			"category2" : "进阶",
		},
		"ui2dmix":
		{
			"title" : "2D场景渲染到UI",
			"desc"	: """
src:idemos/script/ui2dmix
在flash上绘制2D场景
- 演示如何在UI上进行2D画布的创建
- 演示如何创建UI画布上的obj2d对象
- 演示鼠标事件响应
""",
			"thumbnail" : "ui2dmix.png",
			"category1" : "2D",
			"category2" : "入门",
		},
		"ui3dmix":
		{
			"title" : "3D场景渲染到UI",
			"desc"	: """
src:idemos/script/ui3dmix
在flash上绘制3D场景
- 演示如何在UI上进行3D画布的创建
- 演示如何创建UI画布上的obj3d对象
- 演示鼠标事件响应
	鼠标移入/移除/左键/右键
""",
			"thumbnail" : "ui3dmix.png",
			"category1" : "3D",
			"category2" : "入门",
		},
		"detourdemo":
		{
			"title" : "3D寻路",
			"desc" : """
src:idemos/script/detourdemo
3D 寻路demo
  演示如何加载静态寻路网格
  演示如何加载动态寻路网格
  演示如何使用寻路接口
操作
  按键WASD 相机镜头前后左右移动
  按键pageup/pagedown 相机镜头上下移动
  按键shift + 上述按键 相机加速移动
  鼠标滚轮 相机远近调节
  鼠标左键 相机拖拽调节
  鼠标右键 寻路到该位置
  按键B 碰撞体显示开关
  按键M 寻路显示开关
  按键P 动态重建寻路网格
  按键1 瘦人寻路演示(静态网格)
  按键2 胖人寻路演示(动态网格)
""",
			"thumbnail" : "detourdemo.png",
			"category1" : "3D",
			"category2" : "进阶",
		},
	"dynamic_scene":\
		{
			"title" : "3D分块场景的动态加载",
			"desc" : """
src:idemos/script/dynamic_scene
演示如何加载分块的场景，拼凑成一个大场景
可用于随机地图的生成

WASD ------------- 控制角色移动
""",
			"thumbnail" : "dynamic_scene.png",
			"category1" : "3D",
			"category2" : "进阶",
		},
	"HPBar":
	{
			"title" : "血条范例",
			"desc" : """
src:idemos/script/HPBar
2D/3D血条解决方案的合集（范例中会同屏跑300个不同制作方式的血条）：
按键1 2D flash版：易做多样的效果，但效率低，不推荐大量使用.
按键2 2D IMAGE版：效率高，大量使用时可用此版，注意：请使用txg组合大图以获得更好的效率！
按键3 2D SPRITE版：效率高，大量使用时可用此版，注意：请使用txg组合大图以获得更好的效率！
按键4 3D flash版：易做多样的效果，但效率低，不推荐大量使用.
按键5 3D 模型面片版:效率高，大量使用时可用此版.
总结：
* flash版可方便的做出具有动画效果且样式多变的血条，可用于主角等少量使用的地方；推荐同屏数目10个左右。
* 引擎版效率较高，适合大量使用。一般机器配置可达百级。
""",
			"thumbnail" : "HPBar.png",
			"category1" : "2D",
			"category2" : "入门",
	},
	"avt2d":
	{
		"title" : "2D换装范例",
		"desc" : """
src:idemos/script/avt2d
2D 换装demo
	此demo目的在于给出一个2D换装的一个思路。
	
	详细请参考代码注释。
""",
		"thumbnail" : "avt2d.png",
		"category1" : "2D",
		"category2" : "进阶",
	},
	"p2_tut1":
	{
		"title" : "2D物理教学1",
		"desc":"""
src:idemos/script/phy2d_tutorial/p2_tut1_init.py
Body
* 演示如何创建Body
* 演示Body的类型
""",
		"thumbnail": "p2_tut1.png",
		"category1" : "物理",
		"category2" : "入门",
	},
	"p2_tut2":
	{
		"title" : "2D物理教学2",
		"desc":"""
src:idemos/script/phy2d_tutorial/p2_tut2_init.py
Fixture
演示如何创建Fixture
按键1 进行创建
""",
		"thumbnail": "p2_tut2.png",
		"category1" : "物理",
		"category2" : "入门",
	},
	"p2_tut3":
	{
		"title" : "2D物理教学3",
		"desc":"""
src:idemos/script/phy2d_tutorial/p2_tut3_init.py
弹力
演示不同弹力系数的情况
""",
		"thumbnail": "p2_tut3.png",
		"category1" : "物理",
		"category2" : "入门",
	},
	"p2_tut4":
	{
		"title" : "2D物理教学4",
		"desc":"""
src:idemos/script/phy2d_tutorial/p2_tut4_init.py
摩擦
演示不同摩擦系数的情况
""",
		"thumbnail": "p2_tut4.png",
		"category1" : "物理",
		"category2" : "入门",
	},
	"p2_tut5":
	{
		"title" : "2D物理教学5",
		"desc":"""
src:idemos/script/phy2d_tutorial/p2_tut5_init.py
力和力矩
按键W 施加力
按键A 施加逆时针力矩
按键D 施加顺时针力矩
""",
		"thumbnail": "p2_tut5.png",
		"category1" : "物理",
		"category2" : "入门",
	},
	"p2_tut6":
	{
		"title" : "2D物理教学6",
		"desc":"""
src:idemos/script/phy2d_tutorial/p2_tut6_init.py
碰撞处理
演示如何进行碰撞处理
按键1 启动演示
""",
		"thumbnail": "p2_tut6.png",
		"category1" : "物理",
		"category2" : "入门",
	},
	"p2_tut7":
	{
		"title" : "2D物理教学7",
		"desc":"""
src:idemos/script/phy2d_tutorial/p2_tut7_init.py
碰撞过滤
演示如何进行碰撞过滤
按键1 启动演示
""",
		"thumbnail": "p2_tut7.png",
		"category1" : "物理",
		"category2" : "入门",
	},
	"w3_tut1":
	{
		"title" : "3D教学1",
		"desc":"""
src:idemos/script/world3d_tutorial/w3_tut1_init.py
演示如何加载模型""",
		"thumbnail": "w3_tut1.png",
		"category1" : "3D",
		"category2" : "入门",
	},
	"w3_tut2":
	{
		"title" : "3D教学2",
		"desc":"""
src:idemos/script/world3d_tutorial/w3_tut2_init.py
演示如何加载2D/3D混合渲染场景""",
		"thumbnail": "w3_tut2.png",
		"category1" : "3D",
		"category2" : "入门",
	},
	"w3_tut3":
	{
		"title" : "3D教学3",
		"desc":"""
src:idemos/script/world3d_tutorial/w3_tut3_init.py
演示如何播放特效
鼠标左键 播放一个特效
""",
		"thumbnail": "w3_tut3.png",
		"category1" : "3D",
		"category2" : "入门",
	},
	"w3_tut4":
	{
		"title" : "3D教学4",
		"desc":"""
src:idemos/script/world3d_tutorial/w3_tut4_init.py
演示如何对模型进行基本的操作
按键WASD 移动模型
""",
		"thumbnail": "w3_tut4.png",
		"category1" : "3D",
		"category2" : "入门",
	},
	"w3_tut5":
	{
		"title" : "3D教学5",
		"desc":"""
src:idemos/script/world3d_tutorial/w3_tut5_init.py
演示公告板""",
		"thumbnail": "w3_tut5.png",
		"category1" : "3D",
		"category2" : "入门",
	},
	"w3_tut6":
	{
		"title" : "3D教学6",
		"desc":"""
src:idemos/script/world3d_tutorial/w3_tut6_init.py
演示如何进行镜头控制
小键盘数字0-9--------- 控制相机，详细参考代码的on_key_msg
""",
		"thumbnail": "w3_tut6.png",
		"category1" : "3D",
		"category2" : "入门",
	},
	"cleandemo":
	{
		"title" : "销毁范例",
		"desc":"""
src:idemos/script/cleandemo
规范化销毁""",
		"thumbnail": "w3_tut1.png",
		"category1" : "杂项",
		"category2" : "入门",
	}
}