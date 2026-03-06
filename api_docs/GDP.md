# Gdp API购买

**路径**: GDP  
**端点**: `https://open.lixinger.com/api/macro/gdp`  
**方法**: POST

## 描述

©2016-2024 理杏仁 | 北京乾谦慧科技有限公司 | 违法和不良信息举报中心 互联网违法和不良信息投诉：010-86460785

## 请求参数

| 参数名 | 类型 | 必填 | 描述 | 默认值 |
|--------|------|------|------|--------|
| token | Yes | 否 | 我的Token页有用户专属且唯一的Token。 |  |
| startDate | Yes | 否 | 信息起始时间。开始和结束的时间间隔不超过10年 |  |
| endDate | Yes | 否 | 信息结束时间。 |  |
| limit | No | 否 | 返回最近数据的数量。limit仅在请求数据为date range的情况下生效。 |  |
| areaCode | Yes | 否 | 区域编码，如{areaCode}。
当前支持:
大陆: cn
美国: us |  |
| metricsList | Yes | 否 | 指标数组，指标格式为[granularity].[metricsName].[expressionCalculateType]。如['q.gdp.t']
指标参数示例:
指标名 :metricsName
granularity(时间粒度):
expressionCalculateType(数据统计方式):
大陆支持:
GDP :gdp
q(季度):
t(累积)
t_y2y(累积同比)
c(当期)
c_c2c(当期环比)
不变价GDP :gdp_cp
q(季度):
t(累积)
c(当期)
人均GDP :per_gdp
q(季度):
t(累积)
t_y2y(累积同比)
第一产业GDP :pi_gdp
q(季度):
t(累积)
t_y2y(累积同比)
c(当期)
c_c2c(当期环比)
第二产业GDP :si_gdp
q(季度):
t(累积)
t_y2y(累积同比)
c(当期)
c_c2c(当期环比)
第三产业GDP :ti_gdp
q(季度):
t(累积)
t_y2y(累积同比)
c(当期)
c_c2c(当期环比)
第一产业对GDP贡献率 :pi_gdp_c_r
q(季度):
t(累积)
c(当期)
第二产业对GDP贡献率 :si_gdp_c_r
q(季度):
t(累积)
c(当期)
第三产业对GDP贡献率 :ti_gdp_c_r
q(季度):
t(累积)
q(季度):
t(累积)
c(当期)
GNI :gni
q(季度):
t(累积)
t_y2y(累积同比)
美国支持:
GDP :gdp
q(季度):
t(累积)
t_c2c(累积环比)
t_y2y(累积同比) |  |

## 响应字段

见示例响应
