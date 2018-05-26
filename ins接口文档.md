ins接口文档（v1.0)
=============

-------

注：

主机地址：ktchen.cn 	注：以下url均省略主机地址 

管理员账号：instagram@mail.com

密码：instagram123

哈希密码：2ee026a318cb636861bc888df4452d25

后台url: /admin/

------------

### 接口申请

> Url : /api/Application/
>
> 注意：通过浏览器登录申请
>
> 通过后查收邮件附件（PS：写在正文中容易进垃圾桶）
>
> 附件示范：
>
> AppID: 3309_u1UMS3QpsH2j9oVi 
>
> AppKey: zL5jOnTtG9es$Lxu/dxqSlwrnhvSCafRnOvScyySMbgdZQiroYwTFNSA=



### 接口示范

> ### 接口必须参数：
>
> > timestamp
> >
> > appid
> >
> > sign
>
> ------------
>
> 例：
>
> timestamp为时间戳，假设为12345678，
>
> appid假设为3309
>
> sign = md5(timestamp + appKey)     时间戳在前，appKey在后
>
> sign假设为abcd
>
> 初始url:	/user/detail/1/
>
> 最终url: 	/user/detail/1/?timestamp=12345678&appid=3309 &sign=abcd
>
> 注：后台以及接口申请不需要如此，以下接口均需如此操作
>
> --------
>
> 错误返回信息：
>
> 1.没有timestamp参数
>
> {
>     "status": "TimeError"
> }
>
> 2、时间失效
>
> {
>     "status": "Timeout"
> }
>
> 3.没有appid参数
>
> {
>     "status": "Permission denied 403"
> }
>
> 4、sign不匹配
>
> {
>     "status": "Permission denied 405"
> }
>
> 

### 邮箱账号存在性检验接口

>   1、调用方式：post
>
> 2. 接口： /api/user/checkout/
> 3. 表单参数

| 字段名称 | 字段说明     | 类型   |
| -------- | ------------ | ------ |
| account  | 账号名或邮箱 | string |

4.正常返回参数：

1、不存在

{
    "status": "NotExist"
}

2、存在

{
    "status": "Exist"
}

5.错误返回参数

{
    "status": "UnknownError"
}



### 用户注册接口

> 描述：post发送用户注册数据，服务器发送验证码，返回信息
>
> 1.调用方式：post
>
> 2.接口：/api/user/register/
>
> 3.表单参数

| 字段名称 | 字段说明 |  类型  | 必填 |
| :------: | :------: | :----: | :--: |
| username |  账号名  | string |  Y   |
|  email   |   邮箱   | string |  Y   |
| password |   密码   | string |  Y   |
| nickname |   昵称   | string |  Y   |

4.正常返回参数

| 字段名称 | 字段说明 | 类型   |
| -------- | -------- | ------ |
| status   | 状态     | string |

例：

{
    "status": "Success",
}

5、错误返回参数

> 1、账号名重复：
>
> {
>     "status": "AccountError"
> }
>
> 2、邮箱重复：
>
> {
>     "status": "EmailError"
> }
>
> 3、密码不一致：
>
> {
>     "status": "PasswordError"
> }



### 登录接口

> 描述：用户登录
>
> 1、调用方式：post
>
> 2、接口 ：/api/user/login/
>
> 3、表单参数

|  字段名称  | 字段描述 |  类型  |          可选参数          |
| :--------: | :------: | :----: | :------------------------: |
| login_type | 登录类型 | string |      email / username      |
|   email    |   邮箱   | string |  login_type=email 时填写   |
|  username  |  账号名  | string | login_type=username 时填写 |
|  password  |   密码   | string |            必填            |

>4、正常返回参数
>
>| 字段名称        | 字段描述   | 类型   |
>| --------------- | ---------- | ------ |
>| status          | 状态       | string |
>| Authorization   | 令牌       | string |
>| id              | 用户ID     | int    |
>| username        | 账号名     | string |
>| nickname        | 昵称       | string |
>| gender          | 性别       | int    |
>| birthday        | 生日       | string |
>| following_num   | 被关注人数 | int    |
>| followed_num    | 关注人数   | int    |
>| profile_picture | 头像       | string |
>
>例：
>
>{
>    "status": "Success",
>    "Authorization": "Token e65ec79f751918b1958109ff84548d8e8407bc87",
>    "result": [
>        {
>            "id": 2,
>            "username": "管理员",
>            "nickname": "无名用户",
>            "gender": 2,
>            "birthday": "2000-01-01",
>            "following_num": 0,
>            "followed_num": 0,
>            "profile_picture": "/media/profile_picture/default.jpg"
>        }
>    ]
>}
>
>5、错误返回信息
>
>> 1、邮箱不存在
>>
>> {
>>
>> ​	"status": "EmailError"
>>
>> }
>>
>> 2、账号名不存在
>>
>> {
>>
>> ​	"status": "UsernameError"
>>
>> }
>>
>> 3、用户未激活
>>
>> {
>>
>> ​	"status": "NotActive"
>>
>> }
>>
>> 4、密码错误
>>
>> {
>>
>> ​	"status": "PasswordError"
>>
>> }
>>
>> 5、未知错误
>>
>> {
>>
>> ​	"status": "UnknownError"
>>
>> }



### 忘记密码接口（1）

> 描述：提供忘记密码发送邮件功能
>
> 1、调用方式：get
>
> 2、接口：/api/user/password/
>
> 3、参数：email
>
> 例子：/api/user/password/?email=example@163.com
>
> 4、正常返回参数：
>
> {
>     "status": "Success",
>     "hashkey": "ed51616cad7f4588afb48137bd0731fe39a374f3"
> }
>
> 5、错误返回参数：
>
> >1、邮箱不存在：
> >
> >{
> >
> >​	"status": "NotExist"
> >
> >}
> >
> >2、未知错误：
> >
> >{
> >
> >​	"status": "UnknownError"
> >
> >}



### 忘记密码接口（2）

> ----------
>
> 描述：更新密码
>
> 1、调用方式：post
>
> 2、接口：/api/user/password/
>
> 3、表单参数
>
> | 字段名称  | 字段描述   | 类型   |
> | --------- | ---------- | ------ |
> | captcha   | 验证码     | string |
> | hashkey   | 随机哈希值 | string |
> | password  | 密码       | string |
> | password2 | 确认密码   | string |
>
> 4、正常返回参数：
>
> {
>
> ​	"status": "Success"
>
> }
>
> 5、错误返回参数：
>
> > 1、密码不一致及验证码错误
> >
> > {
> >
> > ​	"status": "Failure"
> >
> > }
> >
> > 2、未知错误
> >
> > {
> >
> > ​	"status": "UnknownError"
> >
> > }
>
> 

注：以下接口均需在请求头加入令牌：

> 例：

Authorization  :  Token 3b75b08e0ca19c5822a390d3e012d80bc122ccd6

Token与字符串有一个空格的距离,通过令牌就可以判断用户

> 错误信息：
>
> 1、无令牌
>
> {
>
>    "detail": "身份认证信息未提供。"
>
> }
>
> 2、令牌失效
>
> {
>     "detail": "认证令牌无效。"
> }



### 修改密码接口

>----
>
>描述：修改密码
>
>1、调用方式：post
>
>2、接口： /api/user/password/change/
>
>3、表单参数：
>
>| 字段名称    | 字段描述 | 类型   |
>| ----------- | -------- | ------ |
>| oldPassword | 旧密码   | string |
>| password    | 新密码   | string |
>| password2   | 确认密码 | string |
>
>4、返回参数：
>
>成功
>
>{
>    "status": "Success"
>}
>
>失败
>
>{
>    "status": "Failure"
>}
>
>未知错误
>
>{
>    "status": "UnknownError"
>}

### 发布动态接口

> ---------
>
> 描述：发布动态
>
> 1、调用方式：post
>
> 2、接口：/api/dynamic/
>
> 3、表单参数：
>
> | 字段名称     | 字段描述 | 类型   |
> | ------------ | -------- | ------ |
> | photo_num    | 照片数量 | int    |
> | photo_0      | 照片     | file   |
> | …...         | …...     | …..    |
> | Photo_8      | 照片     | file   |
> | introduction | 动态介绍 | string |
>
> 注：照片参数从photo_0开始，有几张传几张，最大为photo_8
>
> 4、正常返回参数：
>
> {
>
> ​	"status": "Success"
>
> }
>
> 5、错误返回参数：
>
> {
>
> ​	"status": "UnknownError"
>
> }

### 更新动态接口

> --------
>
> 描述：更新动态
>
> 1、调用方式：put
>
> 2、接口：/api/dynamic/
>
> 3、表单参数
>
> | 字段名称     | 字段描述 | 类型   |
> | ------------ | -------- | ------ |
> | pk           | 动态ID   | int    |
> | introduction | 动态说明 | string |
>
> 4、正常返回参数：
>
> {
>
> ​	"status": "Success"
>
> }
>
> 5、发布失败
>
> {
>
> ​	"status": "Failure"
>
> }

### 删除动态接口

> -----
>
> 描述：根据提供的动态ID删除动态，非该用户返回Failure
>
> 1、调用方式：delete
>
> 2、接口：/api/dynamic/
>
> 3、请求参数:
>
> url中加入pk参数
>
> 例： /api/dynamic/?pk=1
>
> 删除动态ID为1的动态
>
> 4、返回参数：
>
> 成功："status": "Success"
>
> 失败："status": "Failure"
>
> 
>



### 首页动态列表获取 接口

> -------
>
> 描述：返回首页动态的id，按时间排序
>
> 1、调用方式：get
>
> 2、接口：/api/dynamic/
>
> 3、请求参数：
>
> 分为两类：
>
> （1）第一页：?page=1
>
>    (2)  非第一页：?page=0&post_id=23 	（假设上次请求的最后一个动态ID为23）
>
> 
>
> 4、返回参数：
>
> | 字段名称          | 字段描述         | 类型   |
> | ----------------- | ---------------- | ------ |
> | username          | 动态发布者账号名 | string |
> | introduction      | 动态介绍         | string |
> | Pub_time          | 发布时间         | string |
> | profile_picture   | 动态发布者头像   | string |
> | likes_num         | 点赞数           | int    |
> | com_num           | 评论数           | int    |
> | photo_0           | 动态第一张照片   | string |
> | is_shoucang       | 是否收藏         | bool   |
> | is_dianzan        | 是否点赞         | bool   |
> | post_id           | 动态ID           | int    |
> | user_id           | 动态发布者ID     | Int    |
> | status            | 状态码           | string |
> | photo_0_thumbnail | 动态首图缩略图   | string |
>
> 
>
> 例：
>
> {
>     "status": "Success",
>     "result": [
>         {
>             "username": "xiaochen",
>             "introduction": "",
>             "Pub_time": "2018-05-26T17:49:35.057960",
>             "profile_picture": "/media/profile_picture/default.jpg",
>             "likes_num": 1,
>             "com_num": 0,
>             "photo_0": "/media/photos/20180526174935_24.jpg",
>             "photo_0_thumbnail": "/media/CACHE/images/photos/20180526174935_24/1348303ffdee466e23a583f9e357a629.jpg",
>             "is_shoucang": true,
>             "is_dianzan": true,
>             "is_many": false,
>             "post_id": 1,
>             "user_id": 2
>         }
>     ]
> }
>
> 结果为空：
>
> {
>     "status": "null",
>
> }
>
> 
>
> 5、错误参数：
>
> {
>
> ​	"status": "UnknownError"
>
> }



### 动态详情查询接口

> ------
>
> 描述：通过动态ID查询动态信息
>
> 1、调用方式：get
>
> 2、接口: /api/post/brief/
>
> 3、请求参数：
>
> 假设动态ID = 4
>
> url: /api/post/brief/4/
>
> 4、返回参数：
>
> | 字段名称          | 字段描述         | 类型   |
> | ----------------- | ---------------- | ------ |
> | username          | 动态发布者账号名 | string |
> | introduction      | 动态简介         | string |
> | Pub_time          | 发布时间         | string |
> | profile_picture   | 动态发布者头像   | string |
> | likes_num         | 点赞数           | int    |
> | com_num           | 评论数           | int    |
> | photo_0           | 动态第一张照片   | string |
> | is_shoucang       | 是否收藏         | bool   |
> | is_dianzan        | 是否点赞         | bool   |
> | post_id           | 动态ID           | int    |
> | user_id           | 发布者ID         | int    |
> | photo_0_thumbnail | 动态首图缩略图   | string |
>
> 例：
>
> {
>     "username": "xiaochen",
>     "introduction": "",
>     "Pub_time": "2018-05-26T17:49:35.057960",
>     "profile_picture": "/media/profile_picture/default.jpg",
>     "likes_num": 1,
>     "com_num": 0,
>     "photo_0": "/media/photos/20180526174935_24.jpg",
>     "photo_0_thumbnail": "/media/CACHE/images/photos/20180526174935_24/1348303ffdee466e23a583f9e357a629.jpg",
>     "is_shoucang": true,
>     "is_dianzan": true,
>     "is_many": false,
>     "post_id": 1,
>     "user_id": 2
> }

### 动态照片查询接口

> ------
>
> 描述：通过动态ID查询动态的所有照片，按时间排序
>
> 1、调用方式：get
>
> 2、接口：/api/photoList/
>
> 3、请求参数：在url里加入动态ID
>
> 例子：
>
> 假设动态ID=3
>
> url: /api/photoList/?postid=3
>
> 4、返回参数：
>
> | 字段名称          | 字段描述       | 类型   |
> | ----------------- | -------------- | ------ |
> | photo_num         | 照片数量       | int    |
> | result  :  id     | ID             | int    |
> | result  :  post   | 动态ID         | string |
> | result  :  photo  | 照片地址       | string |
> | photo_0_thumbnail | 动态首图缩略图 | string |
>
> 例：
>
> {
>     "photo_num": 1,
>     "result": [
>         {
>             "photo_thumbnail": "/media/CACHE/images/photos/20180526174935_53/95a42cb52daa3f22fa6c0c2b4519a875.jpg",
>             "id": 1,
>             "post": 1,
>             "photo": "/media/photos/20180526174935_53.jpg"
>         }
>     ]
> }

### 搜索接口

> --------
>
> 描述：搜索用户或动态
>
> 1、调用方式：post
>
> 2、接口 ：/api/search/
>
> 搜索用户：
>
> 请求第一页url参数：?page=1
>
> 请求非第一页url参数：?page=0&user_id=3 	(假设最后一个用户ID为3)
>
> 搜索动态：
>
> 请求第一页url参数：?page=1
>
> 请求非第一页url参数：?page=0&post_id=3 	(假设最后一个动态ID为3)
>
> > ##### 搜索用户
> >
> > ----
> >
> > 3.请求参数：
> >
> > | 字段名称   | 字段描述                  | 类型   |
> > | ---------- | ------------------------- | ------ |
> > | searchType | 搜索用户时searchType=user | string |
> > | keyword    | 搜索关键词                | string |
> >
> > 4、返回参数
> >
> > 用户信息
> >
> > | 字段名称   | 字段描述 | 类型 |
> > | ---------- | -------- | ---- |
> > | is_guanzhu | 是否关注 | Bool |
> >
> > 
> >
> > 
> >
> > 例：
> >
> > {
> >     "status": "Success",
> >     "result": [
> >         {
> >             "user_id": 4,
> >             "username": "123123",
> >             "gender": 2,
> >             "birthday": "2000-01-01",
> >             "following_num": 0,
> >             "followed_num": 0,
> >             "profile_picture": "/media/profile_picture/default.jpg",
> >             "is_guanzhu": true
> >         }
> >
> > ]
> >
> > }
> >
> > 结果为空：
> >
> > {
> >     "status": "null"
> > }
>
> 
>
> >#### 搜索动态
> >
> >------
> >
> >3、请求参数：
> >
> >| 字段名称   | 字段描述        | 类型   |
> >| ---------- | --------------- | ------ |
> >| searchType | searchType=post | string |
> >| keyword    | 搜索关键词      | string |
> >
> >4、返回参数：
> >
> >例：
> >
> >{
> >    "status": "Success",
> >    "result": [
> >        {
> >            "username": "xiaochen",
> >            "introduction": "",
> >            "Pub_time": "2018-05-26T17:49:35.057960",
> >            "profile_picture": "/media/profile_picture/default.jpg",
> >            "likes_num": 1,
> >            "com_num": 0,
> >            "photo_0": "/media/photos/20180526174935_24.jpg",
> >            "photo_0_thumbnail": "/media/CACHE/images/photos/20180526174935_24/1348303ffdee466e23a583f9e357a629.jpg",
> >            "is_shoucang": true,
> >            "is_dianzan": true,
> >            "is_many": false,
> >            "post_id": 1,
> >            "user_id": 2
> >        }
> >    ]
> >}
> >
> >结果为空：
> >
> >{
> >
> > "status": "null"
> >
> >}
>



### 被关注者动态接口

> 描述：获取关注的人发的动态，按时间排序
>
> 1、调用方式：get
>
> 2、接口：/api/user/followed/
>
> 3、请求参数：无
>
> 4、返回参数：
>
> 例：
>
> [
>     {
>         "id": 3,
>         "user": 2,
>         "introduction": "不错",
>         "Pub_time": "2018-05-15T19:42:03.672456+08:00",
>         "likes_num": 0,
>         "com_num": 0
>     },
>     {
>         "id": 2,
>         "user": 2,
>         "introduction": "不错",
>         "Pub_time": "2018-05-15T19:42:03.042706+08:00",
>         "likes_num": 0,
>         "com_num": 0
>     }
> ]



###  用户信息接口

> ------
>
> 描述：获取用户信息（可以获取所有人的信息）
>
> 1、调用方式：get
>
> 2、接口： /api/user/detail/
>
> 3、参数：用户ID
>
> 例子：假设用户ID为5
>
> 则请求的url为：/api/user/detail/5/
>
> 4、返回参数
>
> | 字段名称        | 字段描述       | 类型   |
> | --------------- | -------------- | ------ |
> | id              | 用户ID         | int    |
> | username        | 账号名         | string |
> | nickname        | 昵称           | string |
> | gender          | 性别           | int    |
> | birthday        | 生日           | string |
> | following_num   | 关注的人的数量 | int    |
> | followed_num    | 被关注的数量   | int    |
> | profile_picture | 图片地址       | string |
> | introduction    | 个人介绍       | string |
> | address         | 地址           | string |
> | post_num        | 动态数         | int    |
>
> 例子：
>
> {
>     "result": {
>         "id": 2,
>         "username": "管理员",
>         "nickname": "啊啊大发",
>         "gender": 1,
>         "birthday": "2010-01-05",
>         "following_num": 0,
>         "followed_num": 0,
>         "profile_picture": "/media/profile_picture/0723_2_J0Kf8zT.JPG",
>         "introduction": "啊啊大发的阿道夫",
>         "address": "黄土高坡"
>     },
>     "post_num": 25
> }



### 个人信息修改接口

> -------
>
> 描述：修改个人信息
>
> 1、调用方式：put
>
> 2、接口：/api/user/detail/
>
> 3、请求参数：
>
> | 字段名称        | 字段描述 | 类型   |
> | --------------- | -------- | ------ |
> | address         | 地址     | string |
> | nickname        | 昵称     | string |
> | gender          | 性别     | int    |
> | birthday        | 生日     | string |
> | profile_picture | 头像     | file   |
> | introduction    | 个人介绍 | string |
>
> 4、返回参数
>
> > 成功
>
> {
>
> ​	"status": "Success"
>
> }
>
> > 账号名重复
>
> {
>
> ​	"status": "AccountError"
>
> }
>
> > 未知错误
>
> {
>
> ​	"status": "UnknownError"
>
> }



### 收藏列表接口

> --------
>
> 描述：提供我收藏的动态
>
> 1、调用方法： get
>
> 2、接口：/api/post/like/
>
> 3、请求参数：无
>
> 4、返回参数：
>
> 动态列表
>
> | 字段名称          | 字段描述       | 类型   |
> | ----------------- | -------------- | ------ |
> | is_many           | 动态是否多图   | bool   |
> | photo_0_thumbnail | 动态首图缩略图 | string |
>
> 例：
>
> {
>     "status": "Success",
>     "result": [
>         {
>             "introduction": "",
>             "Pub_time": "2018-05-26T17:49:35.057960",
>             "likes_num": 1,
>             "com_num": 0,
>             "photo_0": "/media/photos/20180526174935_24.jpg",
>             "photo_0_thumbnail": "/media/CACHE/images/photos/20180526174935_24/1348303ffdee466e23a583f9e357a629.jpg",
>             "is_many": false
>         }
>     ]
> }
>
> 5、错误信息
>
> {
>
> ​	"status": "UnknownError"
>
> }



### 收藏接口

>描述：收藏动态
>
>1、调用方式：post
>
>2、接口：/api/post/like/
>
>3、请求参数：
>
>| 字段名称 | 字段描述 | 类型 |
>| -------- | -------- | ---- |
>| post_id  | 动态ID   | int  |
>
>4、返回参数
>
>成功
>
>{
>    "status": "Success"
>}
>
>失败
>
>{
>    "status": "Failure"
>}
>
>未知错误：
>
>{
>    "status": "UnknownError"
>}



### 删除收藏接口

描述：收藏动态

1、调用方式：delete

2、接口：/api/post/like/

3、请求参数：

| 字段名称 | 字段描述 | 类型 |
| -------- | -------- | ---- |
| id       | 收藏ID   | int  |

4、返回参数

成功

{
    "status": "Success"
}



未知错误：

{
    "status": "UnknownError"
}



### 关注的人接口

> ------
>
> 描述：显示关注的人
>
> 1、调用方式：get
>
> 2、接口：/api/user/friends/
>
> 3、请求参数：user_id
>
> 例： /api/user/friends/?user_id=2
>
> 4、返回参数：
>
> | 字段名称   | 字段描述             | 类型 |
> | ---------- | -------------------- | ---- |
> | is_guanzhu | 当前登录用户是否关注 | bool |
>
> 
>
> 例（结果不为空）：
>
> {
>     "status": "Success",
>     "result": [
>         {
>             "user_id": 1,
>             "username": "",
>             "gender": 2,
>             "birthday": "2000-01-01",
>             "following_num": 0,
>             "followed_num": 0,
>             "profile_picture": "/media/profile_picture/default.jpg",
>             "is_guanzhu": true
>         },
>         {
>             "user_id": 3,
>             "username": "xiaochen",
>             "gender": 2,
>             "birthday": "2000-01-01",
>             "following_num": 0,
>             "followed_num": 0,
>             "profile_picture": "/media/profile_picture/default.jpg",
>             "is_guanzhu": true
>         }
>     ]
> }
>
> （结果为空）：
>
> {
>     "status": "null"
> }

### 关注我的人 接口

> --------
>
> 描述：显示关注我的人
>
> 1、调用方式 :get 
>
> 2、接口：/api/user/lookme/
>
> 3、请求参数：user_id
>
> 例：/api/user/lookme/?user_id=2
>
> 4、返回参数：用户信息，详细信息查看上文
>
> 例：
>
> | 字段名称   | 字段描述 | 类型 |
> | ---------- | -------- | ---- |
> | is_guanzhu | 是否关注 | bool |
>
> 
>
> [
>     {
>         "user_id": 3,
>         "username": "xiaochen",
>         "gender": 2,
>         "birthday": "2000-01-01",
>         "following_num": 0,
>         "followed_num": 0,
>         "profile_picture": "/media/profile_picture/default.jpg",
>         "is_guanzhu": true
>     }
> ]

### 我关注的人的最近的消息 接口

> -----
>
> 描述：参考接口名
>
> 1、调用方式：get
>
> 2、接口：/api/user/friendmessage/
>
> 3、请求参数：无
>
> 4、返回参数：
>
> | 字段名称          | 字段描述       | 类型   |
> | ----------------- | -------------- | ------ |
> | introduction      | 动态描述       | string |
> | user_id           | 用户ID         | int    |
> | post_id           | 动态ID         | int    |
> | time              | 点赞时间       | string |
> | username          | 用户名         | string |
> | photo_0           | 首图           | string |
> | photo_0_thumbnail | 动态首图缩略图 | string |
>
> 例：
>
> {
>     "status": "Success",
>     "result": [
>         {
>             "username": "xiaochen",
>             "user_id": 2,
>             "post_id": 1,
>             "introduction": "",
>             "photo_0": "/media/photos/20180526174935_24.jpg",
>             "photo_0_thumbnail": "/media/CACHE/images/photos/20180526174935_24/1348303ffdee466e23a583f9e357a629.jpg",
>             "profile_picture": "/media/profile_picture/default.jpg",
>             "time": "2018-05-26T23:53:58.266141"
>         }
>     ]
> }

### 关注接口 

> ------
>
> 描述：通过此接口关注他人
>
> 注：重复请求可删除关注，返回信息为Failure（防止非法测试，正常删除使用删除接口）
>
> 1、调用方式：post
>
> 2、接口：/api/user/followyou/
>
> 3、请求参数：
>
> | 字段名称 | 字段描述     | 类型 |
> | -------- | ------------ | ---- |
> | pk       | 被关注人的ID | int  |
>
> 4、返回参数：
>
> >成功
> >
> >{
> >
> >​	"status": "Success"
> >
> >}
> >
> >错误：已关注
> >
> >{
> >
> >​	"status": "Failure"
> >
> >}
> >
> >未知错误
> >
> >{
> >
> >​	"status": "UnknownError"
> >
> >}



### 取消关注接口 

> ----------
>
> 描述：取消关注
>
> 1、调用方式：delete
>
> 2、接口：/api/user/followyou/
>
> 3、请求参数：
>
> | 字段名称 | 字段描述     | 类型 |
> | -------- | ------------ | ---- |
> | pk       | 被关注人的ID | int  |
>
> 4、返回参数：
>
> > 成功
> >
> > {
> >
> > ​	"status": "Success"
> >
> > }
> >
> > 未知错误
> >
> > {
> >
> > ​	"status": "UnknownError"
> >
> > }



### 检查是否关注接口

>描述：查看是否关注此用户
>
>1、调用方式：get
>
>2、接口：/api/user/checkfollow/4/	 	(假设要检查的是该用户是否关注ID为4的用户)
>
>3、请求参数：无
>
>4、返回参数：
>
>关注
>
>{
>    "status": "Yes"
>}
>
>未关注
>
>{
>    "status": "No"
>}
>
>未知错误：
>
>{
>    "status": "UnknownError"
>}
>
>

### 点赞列表 接口

> ------
>
> 描述：获取用户点赞的动态
>
> 1、调用方式：get
>
> 2、接口：/api/post/dianzan/        (原谅我词穷了)
>
> 3、请求参数：无
>
> 4、返回参数
>
> | 字段名称          | 字段描述       | 类型   |
> | ----------------- | -------------- | ------ |
> | is_many           | 动态是否多图   | bool   |
> | photo_0_thumbnail | 动态首图缩略图 | string |
>
> 
>
> {
>     "status": "Success",
>     "result": [
>         {
>             "username": "xiaochen",
>             "introduction": "",
>             "Pub_time": "2018-05-26T17:49:35.057960",
>             "profile_picture": "/media/profile_picture/default.jpg",
>             "likes_num": 1,
>             "com_num": 0,
>             "photo_0": "/media/photos/20180526174935_24.jpg",
>             "photo_0_thumbnail": "/media/CACHE/images/photos/20180526174935_24/1348303ffdee466e23a583f9e357a629.jpg",
>             "is_shoucang": true,
>             "is_dianzan": true,
>             "is_many": false,
>             "post_id": 1,
>             "user_id": 2
>         }
>     ]
> }



### 点赞接口

> ------
>
> 描述：通过该接口给动态点赞
>
> 注：重复调用删除该记录，返回Failure,若正常删除请使用删除接口
>
> 1、调用方式：post
>
> 2、接口：/api/post/dianzan/
>
> 3、请求参数：
>
> | 字段名称 | 字段描述 | 类型 |
> | -------- | -------- | ---- |
> | pk       | 动态ID   | int  |
>
> > 4、返回参数：
> >
> > > 成功
> > >
> > > {
> > >
> > > ​	"status": "Success"
> > >
> > > }
> > >
> > > 记录存在：
> > >
> > > {
> > >
> > > ​	"status": "Failure"
> > >
> > > }
> > >
> > > 未知错误
> > >
> > > {
> > >
> > > ​	"status": "UnknownError"
> > >
> > > }



### 取消点赞接口

> ---------
>
> > 描述：通过该接口给动态取消点赞
> >
> > 1、调用方式：delete
> >
> > 2、接口：/api/post/dianzan/
> >
> > 3、请求参数：
> >
> > | 字段名称 | 字段描述 | 类型 |
> > | -------- | -------- | ---- |
> > | pk       | 动态ID   | int  |
> >
> > > 4、返回参数：
> > >
> > > > 成功
> > > >
> > > > {
> > > >
> > > > ​	"status": "Success"
> > > >
> > > > }
> > > >
> > > > 记录不存在
> > > >
> > > > {
> > > >
> > > > ​	"status": "Failure"
> > > >
> > > > }
> > > >
> > > > 未知错误
> > > >
> > > > {
> > > >
> > > > ​	"status": "UnknownError"
> > > >
> > > > }



### 用户动态接口 

> -------
>
> 描述：获取用户的个人动态，按时间排序，因此可以通过用户ID获取所有人的个人动态，包括用户自己
>
> 1、调用方式：get
>
> 2、接口：/api/user/posts/5/	（假设用户ID为5）
>
> 3、请求参数：无
>
> 4、返回参数：
>
> | 字段名称          | 字段描述       | 类型   |
> | ----------------- | -------------- | ------ |
> | is_many           | 动态是否多图   | Bool   |
> | photo_0_thumbnail | 动态首图缩略图 | string |
>
> 表单详情参考上文:
>
> 例：
>
> {
>     "status": "Success",
>     "result": [
>         {
>             "username": "xiaochen",
>             "introduction": "",
>             "Pub_time": "2018-05-26T17:49:35.057960",
>             "profile_picture": "/media/profile_picture/default.jpg",
>             "likes_num": 1,
>             "com_num": 0,
>             "photo_0": "/media/photos/20180526174935_24.jpg",
>             "photo_0_thumbnail": "/media/CACHE/images/photos/20180526174935_24/1348303ffdee466e23a583f9e357a629.jpg",
>             "is_shoucang": true,
>             "is_dianzan": true,
>             "is_many": true,
>             "post_id": 1,
>             "user_id": 2
>         }
>     ]
> }



### 发表评论 接口

> ---------
>
> 描述：发表评论
>
> 1、调用方式：post
>
> 2、接口：/api/post/comments/
>
> 3、请求参数：
>
> | 字段名称 | 字段描述 | 类型   |
> | -------- | -------- | ------ |
> | post_id  | 动态ID   | int    |
> | content  | 评论内容 | String |
>
> 4、返回参数：
>
> 成功
>
> {
>     "status": "Success"
> }
>
> 未知错误
>
> {
>
> ​	"status": "UnknownError"
>
> }



### 删除评论接口

> -----
>
> 描述：删除评论
>
> 1、调用方式：delete
>
> 2、接口：/api/post/comments/
>
> 3、请求参数：
>
> | 字段名称   | 字段描述 | 类型 |
> | ---------- | -------- | ---- |
> | comment_id | 评论ID   | int  |
>
> 4、返回参数：
>
> 成功
>
> {
>     "status": "Success"
> }
>
> 非该用户
>
> {
>     "status": "Failure"
> }
>
> 未知错误
>
> {
>
> ​	"status": "UnknownError"
>
> }



### 评论列表

> ------
>
> 描述：通过动态的ID查询评论
>
> 1、调用方式：get
>
> 2、接口：/api/post/comments/
>
> 3、参数：post_id
>
> 例子：/api/post/comments/?post_id=4
>
> 4、返回参数：
>
> | 字段名称 | 字段描述   | 类型   |
> | -------- | ---------- | ------ |
> | id       | 评论ID     | int    |
> | user     | 评论者的ID | int    |
> | post     | 动态ID     | int    |
> | content  | 评论内容   | string |
> | Pub_time | 发布时间   | string |
>
> 
>
> [
>     {
>         "id": 11,
>         "user": 2,
>         "post": 4,
>         "content": "111",
>         "Pub_time": "2018-05-18T00:36:53.676498+08:00"
>     },
>     {
>         "id": 10,
>         "user": 2,
>         "post": 4,
>         "content": "111",
>         "Pub_time": "2018-05-18T00:36:53.426185+08:00"
>     }
>
> ]

### 消息列表接口

>----
>
>描述：获取最近的消息
>
>1、调用方式：get
>
>2、接口：/api/user/messages/
>
>3、请求参数：无
>
>4、返回参数：
>
>>### 关注
>>
>>消息类型:messageType=1
>>
>>| 字段名称        | 字段描述         | 类型   |
>>| --------------- | ---------------- | ------ |
>>| user_id         | 关注人ID         | int    |
>>| username        | 关注人用户名     | string |
>>| profile_picture | 关注人头像       | string |
>>| messageType     | 消息类型         | int    |
>>| time            | 时间             | string |
>>| is_guanzhu      | 当前用户是否关注 | bool   |
>
>> ### 点赞
>>
>> 消息类型:messageType=2
>>
>> | 字段名称          | 字段描述       | 类型   |
>> | ----------------- | -------------- | ------ |
>> | user_id           | 同上           | 同上   |
>> | username          | 同上           | 同上   |
>> | profile_picture   | 同上           | 同上   |
>> | messageType       | 同上           | 同上   |
>> | time              | 同上           | 同上   |
>> | post_id           | 动态ID         | int    |
>> | photo_0           | 动态首图       | string |
>> | photo_0_thumbnail | 动态首图缩略图 | string |
>
>> ### 评论
>>
>> 消息类型:messageType=3
>>
>> | 字段名称          | 字段描述       | 类型   |
>> | ----------------- | -------------- | ------ |
>> | user_id           | 同上           | 同上   |
>> | username          | 同上           | 同上   |
>> | profile_picture   | 同上           | 同上   |
>> | messageType       | 同上           | 同上   |
>> | time              | 同上           | 同上   |
>> | post_id           | 同上           | 同上   |
>> | photo_0           | 同上           | 同上   |
>> | content           | 评论内容       | string |
>> | photo_0_thumbnail | 动态首图缩略图 | string |
>
>例：
>
>{
>    "status": "Success",
>    "result": [
>        {
>            "user_id": 2,
>            "username": "管理员",
>            "profile_picture": "/media/profile_picture/0723_2_J0Kf8zT.JPG",
>            "messageType": 3,
>            "time": "2018-05-25T00:36:53.426185+08:00",
>            "post_id": 4,
>            "photo_0": "/media/photos/20180517195857_68.jpg",
>            "content": "112",
>
>​            "photo_0_thumbnail": "/media/CACHE/images/photos/20180526174935_24/1348303ffdee466e23a583f9e357a629.jpg"           },
>
>​         {       
>
>​		 "user_id": 2,       
>
>​		 "username": "xiaochen",       
>
>​		 "profile_picture": "/media/profile_picture/default.jpg",       
>
>​		 "messageType": 2,       
>
>​		 "time": "2018-05-26T23:53:58.266141",       
>
>​		 "post_id": 1,        
>
>​		 "photo_0": "/media/photos/20180526174935_24.jpg",       
>
>​		 "photo_0_thumbnail": "/media/CACHE/images/photos/20180526174935_24/1348303ffdee466e23a583f9e357a629.jpg"   
>
>​	 },
>        {
>            "user_id": 3,
>            "username": "xiaochen",
>            "profile_picture": "/media/profile_picture/default.jpg",
>            "messageType": 1,
>            "time": "2018-05-15T11:54:52.280891+08:00",
>            "is_guanzhu": true
>        }
>    ]
>}