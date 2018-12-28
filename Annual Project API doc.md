# Annual Project API doc

## 信息门户密码验证

### 接口功能

首页登陆时学号密码检验

### URL

/api/ehallLogin

### 请求格式

JSON

### HTTP请求方式

POST

### 请求参数

| 参数     | 必选 | 类型   | 说明 |
| :------- | :--- | :----- | :--- |
| number   | true | string | 学号 |
| password | true | string | 密码 |

### 返回字段

| 参数  | 字段类型 | 说明               |
| :---- | :------- | :---------------|
| error | string   | 错误信息          |
| pic   | string   | Base64编码的验证码 |

### 返回error信息说明
0：'无错误'

其他的错误信息是明文

------

## 校园卡查询密码验证

### 接口功能

验证用户填写的验证码/传入用户自定义校园卡查询密码

### URL

/api/ecardLogin

### 请求格式

JSON

### HTTP请求方式

POST

### 鉴权

需携带cookie 且正确访问上方接口

### 请求参数

| 参数     | 必选  | 类型   | 说明             |
| :------- | :---- | :----- | :--------------- |
| code     | true  | string | 验证码           |
| password | false | string | 用户输入查询密码 |

### 返回字段

| 参数  | 字段类型 | 说明     |
| :---- | :------- | :------- |
| error | string   | 错误信息 |

### 返回error信息说明

0：'无错误'

1：'查询密码错误'

2：'验证码错误'

3：'账号错误'

4：'未执行前置步骤'

------

## 用户年度信息获取

### 接口功能

获取用户年度的全量展示信息

### URL

/api/information

### 请求格式

无

### HTTP请求方式

GET

### 鉴权

需携带cookie 且正确访问上方所有接口

### 返回字段

#### data部分

| 参数    | 字段类型 | 说明                       |
| :------ | :------- | :------------------------- |
| courseCount | int      | 课程门数              |
| classCount | int      | 课程节数                |
| classDay | int      | 换算天数                 |
| most_class | stirng   | 什么课陪你渡过了最长的岁月    |
| times  | int      | 消费次数                 |
| sum_price  | string   | 消费总额                 |
| type_count  | int      | 打卡多少家                 |
| top_price_place | string   | 最高消费商户       |
| top_price | string   | 最高消费金额               |
| most_visit_place | string   | 最常去商户             |
| most_visit_times | int      | 消费多少次                 |
| bus_times | int      | 搭乘校车多少次              |
| hosp_times | int      | 校医院次数                 |
| overdue_price | int      | 逾期总额              |
|overdue_times|int|逾期次数|
| bf_times | int      | 早点天数                   |
| trem | int      | 第几个学期                 |
|ranking|int|本学院打卡排名|

### 返回error信息说明

0：'无错误'

1：'未执行前置步骤'

2：'获取账号类型失败'

3：'获取学院信息失败'

4：'获取账单信息失败'



------