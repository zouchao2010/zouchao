# -*- coding:GBK -*-
config = {
	1 : {
		"name" : "泛光",
	},
	2 : {
		"name" : "灰化",
	},
	3 : {
		"name" : "暗角"
	},
	4 : {
		"name" : "HSV",
		0 : {
			"txt" : "hue",	# 参数名
			"min" : -180,	# 界面显示最小值
			"max" : 180,	# 界面显示最大值
			"default" : 0,	# 界面显示初始值
			"value" : 0,	# 实际值
			"scale" : 1,	# 界面显示值的比例
		},
		1 : {
			"txt" : "saturation",
			"min" : 0,
			"max" : 200,
			"default" : 100,
			"value" : 1,
			"scale" : 100,
		},
		2 : {
			"txt" : "lightness",
			"min" : -100,
			"max" : 100,
			"default" : 0,
			"value" : 0,
			"scale" : 100,
		}
	},

	5 : {
		"name" : "水波",
		0 : {
			"txt" : "time",
			"min" : 0,
			"max" : 800,
			"default" : 0,
			"value" : 0.0,
			"scale" : 100,
		},
		1 : {
			"txt" : "wave_size",
			"min" : 0,
			"max" : 100,
			"default" : 40,
			"value" : 0.4,
			"scale" : 100,
		},
		2 : {
			"txt" : "amplitude",
			"min" : 0,
			"max" : 100,
			"default" : 20,
			"value" : 0.2,
			"scale" : 100,
		},
	},
	6 : {
		"name" : "漩涡",
		0 : {
			"txt" : "center_x",
			"min" : 0,
			"max" : 100,
			"default" : 50,
			"value" : 0.5,
			"scale" : 100,
		},
		1 : {
			"txt" : "center_y",
			"min" : 0,
			"max" : 100,
			"default" : 50,
			"value" : 0.5,
			"scale" : 100,
		},
		2 : {
			"txt" : "strength",
			"min" : 0,
			"max" : 200,
			"default" : 0,
			"value" : 20,
			"scale" : 10,
		},
	},
	7 : {
		"name" : "波纹",
		0 : {
			"txt" : "center_x",
			"min" : 0,
			"max" : 100,
			"default" : 50,
			"value" : 0.5,
			"scale" : 100,
		},
		1 : {
			"txt" : "center_y",
			"min" : 0,
			"max" : 100,
			"default" : 50,
			"value" : 0.5,
			"scale" : 100,
		},
		2 : {
			"txt" : "amplitude",
			"min" : 0,
			"max" : 100,
			"default" : 10,
			"value" : 0.1,
			"scale" : 100,
		},
		3 : {
			"txt" : "frequency",
			"min" : 0,
			"max" : 100,
			"default" : 70,
			"value" : 70.0,
			"scale" : 1,
		},
	},
	8 : {
		"name" : "马赛克",
		0 : {
			"txt" : "x轴数目",
			"min" : 20,
			"max" : 100,
			"default" : 60,
			"value" : 60.0,
			"scale" : 1,
		},
		1 : {
			"txt" : "y轴数目",
			"min" : 20,
			"max" : 100,
			"default" : 60,
			"value" : 60.0,
			"scale" : 1,
		},
	}
}