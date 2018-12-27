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

#### data部分

| 参数  | 字段类型 | 说明               |
| :---- | :------- | :----------------- |
| error | string   | 错误信息           |
| pic   | string   | Base64编码的验证码 |
| xueyuan

### 返回error信息说明

1：'信息门户密码错误'
2：'0'（无错误）

------

## 校园卡查询密码验证

### 接口功能

更新用户昵称、头像URL、个性签名

### URL

/api/ecardLogin

### 请求格式

JSON

### HTTP请求方式

POST

### 请求参数

| 参数     | 必选  | 类型   | 说明             |
| :------- | :---- | :----- | :--------------- |
| code     | true  | string | 验证码           |
| password | false | string | 用户输入查询密码 |

### 返回字段

#### data部分

| 参数  | 字段类型 | 说明     |
| :---- | :------- | :------- |
| error | string   | 错误信息 |

### 返回error信息说明

1：'验证码错误'

2：'查询密码错误'

3：'0'（无错误）

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

需携带cookie

### 返回字段

#### data部分

| 参数    | 字段类型 | 说明                       |
| :------ | :------- | :------------------------- |
| item_1  | int      | 多少门课                   |
| item_2  | int      | 多少节课                   |
| item_3  | int      | 多少个日夜                 |
| item_4  | stirng   | 什么课陪你渡过了最长的岁月 |
| item_5  | int      | 多少次滴声                 |
| item_6  | string   | 总共花费了                 |
| item_7  | int      | 打卡多少家                 |
| item_8  | string   | 在哪家挥金如土             |
| item_9  | string   | 刷了多少元                 |
| item_10 | string   | 最常去的哪家               |
| item_11 | int      | 消费多少次                 |
| item_12 | int      | 搭乘校车多少次             |
| item_13 | int      | 挂号多少次                 |
| item_14 | int      | 逾期多少次                 |
| item_15 | int      | 坚持吃早点多少天           |
| item_16 | int      | 第几个学期                 |

### 返回error信息说明

1：'获取失败'
2：'0'（无错误）



------