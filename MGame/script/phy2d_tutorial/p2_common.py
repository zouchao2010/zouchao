# -*- coding:GBK -*-
# 教程测试框架
import random

# [-1, 1]
def randfloat():
	return random.random() * 2 - 1.0

# [lo, hi]
def randfloat_range(lo, hi):
	return random.random() * (hi - lo) + lo