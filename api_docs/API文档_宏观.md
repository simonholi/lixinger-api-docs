# 场内基金认购净流入API购买

**路径**: API文档/宏观  
**端点**: `https://open.lixinger.com/api/cn/index/hot/ifet_sni`  
**方法**: POST

## 描述

©2016-2024 理杏仁 | 北京乾谦慧科技有限公司 | 违法和不良信息举报中心 互联网违法和不良信息投诉：010-86460785

## 请求参数

| 参数名 | 类型 | 必填 | 描述 | 默认值 |
|--------|------|------|------|--------|
| token | Yes | 否 | 我的Token页有用户专属且唯一的Token。 |  |
| stockCodes | Yes | 否 | 指数代码数组。stockCodes长度>=1且<=100，格式如下：["000016"]。
请参考指数信息API获取合法的stockCode。 |  |
| stockCode | String | 否 |  |  |
| last_data_date | Date | 否 |  |  |
| cpc | Number | 否 |  |  |
| ifet_as | Number | 否 |  |  |
| ifet_sni_ytd | Number | 否 |  |  |
| ifet_sni_w1 | Number | 否 |  |  |
| ifet_sni_w2 | Number | 否 |  |  |
| ifet_ssni_m1 | Number | 否 |  |  |
| ifet_sni_m3 | Number | 否 |  |  |
| ifet_sni_m6 | Number | 否 |  |  |
| ifet_sni_y1 | Number | 否 |  |  |
| ifet_sni_y2 | Number | 否 |  |  |
| ifet_sni_fys | Number | 否 |  |  |

## 响应字段

见示例响应
