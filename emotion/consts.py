# -*- encoding: utf-8 -*-

# 符号类型集合
LOGICAL_SYMBOL = ',~^'
RELATIONAL_SYMBOL = '#%$*+&@?!'
SPECIAL_SYMBOL = '{'

# 无关义原之间的默认距离
DEFAULT_PRIMITIVE_DIS = 20

# sim(p1,p2) = alpha/(d+alpha) 距离与相似度的换算常数
ALPHA = 1.6
# 空值与非空值之间的相似度
DELTA = 0.2
# 具体次与义原的相似度
GAMMA = 0.2
# 计算实词相似读的权重，基本义原，其他义原，关系义原，关系符号义原
BETA1 = 0.5
BETA2 = 0.2
BETA3 = 0.17
BETA4 = 0.13
