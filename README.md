# **ADApi_fastapi**
>广告api：为广告部提供api接口服务。其中接口服务,分为文件和数据库api服务。文件主要包含五表+月数据,数据库是team_station等。
## **项目具体内容**
>广告api是部署在Windows(172.16.128.240)中,采用用Python3.7+fastapi0.63搭建。其中启动文件为main.py,项目日志在logs文件夹下。通过http://172.16.128.240:8000/docs可以查看项目的url以及参数。

### **模块介绍**
>项目模块主要分为:项目启动配置项(main),文件处理app(process_dir),数据库处理app(sql_app),公共函数(public_function),日志文件(logs)等构成.

### **模块重要性**
模块名称|使用频率|重要性|重要性分级
:---:|:---:|:---:|:---:|
extensions|少|一般|1
logs|少|一般|1
process_dir|最高|最|4
public_function|最高|最|4
sql_app|最高|最|4



### **模块详情**
ADApi_fastapi
├─extensions
│  ├─loggers #  项目日志配置项:格式以及保存输出逻辑
├─logs # 项目日志
├─process_dir # 文件处理模块:主要是将windows服务器文件与广告后台Linux(172.16.128.145)产生桥梁,将windows服务器文件信息给Linux后台中的Django应用调用,通过也提供文件传输通道。
│  └─routes.py # 文件具体的路由和视图函数:文件夹/文件的相关函数(具体查看路由的注释)
├─public_function # 公共函数
│  ├─accessManager.py # 权限设置项,暂时没有完善
│  ├─process_file.py # 文件相关处理函数
│  ├─public_function.py # 一些常用的公共函数
│  ├─query_frequently_table_info.py # 常用的数据库快捷查询(redis缓存+MySQL)
│  ├─response_message.py # 返回消息提示
│  ├─sql_write_read.py # 数据库处理方法与函数:MySQL+Redis
├─sql_app # 数据库处理模块
│  ├─crud.py # 增删改查(前期测试用,后期没有用)
│  ├─database.py # 连接的数据库(session)信息
│  ├─main.py # 数据库连接的主函数:全部路由
│  ├─models.py # 数据库表对象模型以及自定义模型
│  ├─query_table.py # 查询数据库表的自定义函数
│  ├─routes.py # 没有用
│  └─schema.py # 数据库模型，用于快速构建数据库表的增删改查
├─.gitignore # 管理git中忽略的文件或是文件夹
├─.create_model.py # 脚本可以生成数据库表对于的api模型
├─Dockerfile # Docker配置项
├─gunicorn_config.py # 使用gunicorn启动项目配置项,暂时没有用到.
├─main.py # **项目启动项**,项目的配置项等
├─request_test.py # 请求测试脚本
├─requirements.txt # 项目依赖包
├─routers.py # 早期编写路由和视图
├─schema.py # 早期编写模型
├─static.py # 静态参数
├─test.py # 测试脚本



### **主要维护项**
>项目主要是维护与开发主要包含**文件处理app(process_dir)**与**数据库app(sql_app)**,同时将自己的类或是函数放使用public_function管理。


### **注意事项**
>1.api框架挂掉了,那么广告后台Django则无法正常运行.
>2.windows服务器磁盘满了也会导致fastapi框架挂掉.