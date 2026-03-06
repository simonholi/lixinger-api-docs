# K线数据API购买

**路径**: K线数据  
**端点**: `https://open.lixinger.com/api/cn/company/candlestick`  
**方法**: POST

## 描述

©2016-2024 理杏仁 | 北京乾谦慧科技有限公司 | 违法和不良信息举报中心 互联网违法和不良信息投诉：010-86460785

## 请求参数

| 参数名 | 类型 | 必填 | 描述 | 默认值 |
|--------|------|------|------|--------|
| token | Yes | 否 | 我的Token页有用户专属且唯一的Token。 |  |
| stockCode | Yes | 否 | 请参考股票信息API获取合法的stockCode。stockCode仅在请求数据为date range的情况下生效。 |  |
| type | No | 否 | 除复权类型， 例如， “lxr_fc_rights”。
当前支持:
不复权: ex_rights
理杏仁前复权: lxr_fc_rights
前复权: fc_rights
后复权: bc_rights |  |
| date | No | 否 | 信息日期。用于获取指定日期数据。 |  |
| startDate | No | 否 | 信息起始时间。用于获取一定时间范围内的数据。开始和结束的时间间隔不超过10年 |  |
| endDate | No | 否 | 信息结束时间。用于获取一定时间范围内的数据。默认值是上周一。 |  |
| adjustForwardDate | No | 否 | 前复权指定起始时间点。
需要注意的是，请与endDate一起使用且大于或等于endDate。 获取复权类型数据时要传入，不传时默认值是endDate。 |  |
| adjustBackwardDate | No | 否 | 后复权指定起始时间点。
需要注意的是，请与startDate一起使用且小于或等于startDate。 获取复权类型数据时要传入，不传时默认值是startDate。 |  |
| limit | No | 否 | 返回最近数据的数量。 |  |
| date | Date | 否 |  |  |
| stockCode | String | 否 |  |  |
| open | Number | 否 |  |  |
| close | Number | 否 |  |  |
| high | Number | 否 |  |  |
| low | Number | 否 |  |  |
| volume | Number | 否 |  |  |
| amount | Number | 否 |  |  |
| change | Number | 否 |  |  |
| to_r | Number | 否 |  |  |
| complexFactor | Number | 否 |  |  |

## 响应字段

见示例响应
