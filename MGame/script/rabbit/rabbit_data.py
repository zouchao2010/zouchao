# -*- coding:GBK -*-

import iphy2d

# ��Ϸ��̬�����ļ�
# ���ڴ�����弰���������ԡ���ʾ����

DATA = {

	1:{	# ����
		"phy_init":(iphy2d.POLYGON, (1000, 100)), 
		"phy_param":{
				"rot":0, 
				"friction":1, 
				"body_type":iphy2d.STATIC_BODY
				}, 
		}, 


	2:{	#Ģ��2
		"phy_init":(iphy2d.POLYGON, (60, 70)), 
		"phy_param":{
				"density":3, 
				"rot":0, 
				"friction":100, 
				"linear_damping":0
				}, 
		"face":{
			"file":"idemos/res/rabbit/world2d/txg/demo.txg|mogu2", 
			"key_point":(0,0)
			}
		}, 


	3:{	# Ģ��3
		"phy_init":(iphy2d.POLYGON, (38, 40)), 
		"phy_param":{
				"density":3, 
				"rot":0, 
				"friction":100, 
				"linear_damping":0
				}, 
		"face":{
			"file":"idemos/res/rabbit/world2d/txg/demo.txg|mogu3", 
			"key_point":(0,0)
			}
		}, 


	4:{	# ����
		"phy_init":(iphy2d.POLYGON, (35, 40)), 
		"phy_param":{
				"density":2, 
				"friction":30,
				"sensor":False, 
				"body_type":iphy2d.STATIC_BODY, 
				}, 
		"face":{
			"file":"idemos/res/rabbit/world2d/2dmodel/tutu.2dm", 
			"key_point":(0,0)
			}
		}, 


	6:{	# ǽ
		"phy_init":(iphy2d.POLYGON, (44.5, 98.5)), 
		"phy_param":{
				"density":1, 
				"friction":1, 
				"body_type":iphy2d.STATIC_BODY
				}, 
		}, 


	7:{	# ���ܲ�
		"phy_init":(iphy2d.POLYGON, (13, 12)), 
		"phy_param":{
				"density":0.5, 
				"friction":30, 
				}, 
		"face":{
			"file":"idemos/res/rabbit/world2d/txg/demo.txg|luobo", 
			"key_point":(0,0), 
			}
		}, 

	8:{	# Ģ�����1
		"phy_init":(iphy2d.POLYGON, (105, 80)), 
		"phy_param":{
				"density":3, 
				"rot":0, 
				"friction":1, 
				"linear_damping":0
				}, 
		"face":{
			"file":"idemos/res/rabbit/world2d/txg/demo.txg|mogu_h", 
			"key_point":(0,0)
			}
		}, 

	9:{	# Ģ�����2
		"phy_init":(iphy2d.POLYGON, (20, 105)), 
		"phy_param":{
				"density":3, 
				"rot":0, 
				"friction":1, 
				"linear_damping":0
				}, 
		"face":{
			"file":"idemos/res/rabbit/world2d/txg/demo.txg|mogu_b", 
			"key_point":(0,0)
			}
		}, 


	10:{	# ����
		"phy_init":(iphy2d.POLYGON, (20, 105)), 
		"phy_param":{
				"density":3, 
				"rot":0, 
				"friction":1, 
				"linear_damping":0
				}, 
		"face":{
			"file":"idemos/res/rabbit/world2d/txg/demo.txg|sinsan", 
			"key_point":(0,0)
			}
		}, 


	11:{	# С��
		"phy_init":(iphy2d.SPHERE, 10), 
		"phy_param":{
				"density":0.3, 
				"rot":0, 
				"restitution":0, 
				"friction":100000, 
				}, 
		"face":{
			"file":"idemos/res/rabbit/world2d/txg/demo.txg|huanxiong", 
			"key_point":(0,0)
			}
		}, 

	12:{	# ��С���ܲ�
		"phy_init":(iphy2d.POLYGON, (8, 5)), 
		"phy_param":{
				"density":0.2, 
				"friction":20, 
				}, 
		"face":{
			"file":"idemos/res/rabbit/world2d/txg/demo.txg|luobo", 
			"key_point":(0,0), 
			}
		}, 

	13:{	# Ģ����
		"phy_init":(iphy2d.POLYGON, (10, 40)), 
		"phy_param":{
				"density":3, 
				"rot":0, 
				"friction":1, 
				"linear_damping":0
				}, 
		"face":{
			"file":"idemos/res/rabbit/world2d/txg/demo.txg|mogu_b", 
			"key_point":(0,0),
			"size":(80, 160),
			}
		}, 

	14:{	# Ģ����
		"phy_init":(iphy2d.POLYGON, (10, 80)), 
		"phy_param":{
				"density":3, 
				"rot":0, 
				"friction":1, 
				"linear_damping":0
				}, 
		"face":{
			"file":"idemos/res/rabbit/world2d/txg/demo.txg|mogu_b", 
			"key_point":(0,0), 
			}
		}, 

	15:{	# Ģ��
		"phy_init":(iphy2d.POLYGON, (30, 30)), 
		"phy_param":{
				"density":1, 
				"rot":0, 
				}, 
		"face":{
			"file":"idemos/res/rabbit/world2d/txg/demo.txg|mogu3", 
			"key_point":(0,0)
			}
		}, 


	100:{	# ���
		"phy_init":(iphy2d.SPHERE, 35), 
		"phy_param":{
				"density":10, 
				"friction":1, 
				"restitution":0, 
				"angular_damping":0.1, 
				"linear_damping":0, 
				"body_type":iphy2d.STATIC_BODY,
				"category":1, 
				"collide_mask":1, 
				}, 
		"face":{
			"file":"idemos/res/rabbit/world2d/txg/demo.txg|huanxiong", 
			}, 
		}, 

}



def get_data(id):
	return DATA.get(id)
