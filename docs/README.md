# DDIS (Reliability_Row_data) 技术维护与开发者指引

> 本文件夹为 DDIS（Device Data Information System）系统的技术维护与开发者指引文档集合。
> 适用于后续开发人员、系统维护者、系统拥有者查阅。
> 最后更新：2026-08-25

---

## 文档导航

| 文档 | 主要内容 | 适用读者 |
|------|----------|----------|
| [01-技术架构与目录结构.md](./01-技术架构与目录结构.md) | 技术栈总览、整体架构、目录结构、主程式位置 | 全部读者 |
| [02-核心运作逻辑.md](./02-核心运作逻辑.md) | 认证与权限、Celery 任务、WebSocket、中间件、日志、Redis 用途 | 开发人员、维护者 |
| [03-部署启动与运行维护.md](./03-部署启动与运行维护.md) | 启动命令、批处理文件、维护检查清单、故障排查 | 维护者、系统拥有者 |
| [04-开发规范摘要.md](./04-开发规范摘要.md) | 代码规范、新增模块步骤、禁止事项、常见坑点 | 开发人员 |

> 强烈建议新接手者按顺序阅读 01 → 02 → 03 → 04。

---

## 快速速查表

### 启动命令（Windows + 已装虚拟环境 `c:\Python372\mecheck`）

```bash
# 1) Web 服务（开发）
python manage.py runserver 0.0.0.0:8000

# 2) WebSocket / Channels（生产）
C:\Python372\mecheck\Scripts\daphne.exe -b 0.0.0.0 -p 8000 Reliability_Row_data.asgi:application
# 或双击 ChannelsServer.bat

# 3) Celery Worker
C:\Python372\mecheck\Scripts\celery.exe worker -A Reliability_Row_data -l info -P eventlet
# 或双击 DDISceleryworker.bat

# 4) Celery Beat（定时任务）
C:\Python372\mecheck\Scripts\celery.exe -A Reliability_Row_data beat -l info
# 或双击 DDIScelerybeat.bat
```

### 关键资源依赖

| 资源 | 地址 | 口令 |
|------|------|------|
| MySQL | `127.0.0.1:3306` 库名 `reliabilityrowdata` | `edwin / DCT@2019` |
| MongoDB | `127.0.0.1:27017` 库名 `admin` | `edwin / DCT@2019` |
| Redis | `localhost:6379` 密码 `DCT2019`，DB 用途见 [02-核心运作逻辑](./02-核心运作逻辑.md) | — |
| 外部 DCT API | `http://192.168.1.10/dct/api/ClientSvc/getAllProjectInfo` | NTLM 鉴权 |
| Exchange 邮件 | `webmail.compal.com`（账号配置在 `OAmail_account.json`） | — |

### 关键文件位置

| 文件 | 说明 |
|------|------|
| [manage.py](../manage.py) | Django 入口 |
| [Reliability_Row_data/settings.py](../Reliability_Row_data/settings.py) | 全局配置（数据库/Redis/Celery/日志/权限） |
| [Reliability_Row_data/urls.py](../Reliability_Row_data/urls.py) | 根 URL 路由 |
| [Reliability_Row_data/celery.py](../Reliability_Row_data/celery.py) | Celery 实例定义 |
| [Reliability_Row_data/routing.py](../Reliability_Row_data/routing.py) | Channels ASGI 路由 |
| [Reliability_Row_data/__init__.py](../Reliability_Row_data/__init__.py) | pymysql 安装为 MySQLdb + 导出 celery_app |
| [app01/views.py](../app01/views.py) | 主视图（登录/导航/Lesson 等） |
| [app01/models.py](../app01/models.py) | 核心模型（用户/角色/权限/菜单/Lesson 等） |
| [app01/tasks.py](../app01/tasks.py) | Celery 异步任务（项目同步/邮件提醒） |
| [app01/consumers.py](../app01/consumers.py) | WebSocket 消费者 |
| [middleware/checkper.py](../middleware/checkper.py) | RBAC 权限中间件 |
| [middleware/UserIP.py](../middleware/UserIP.py) | 用户访问日志中间件 |
| [service/init_permission.py](../service/init_permission.py) | 登录后权限初始化（写入 session） |
| [templates/base.html](../templates/base.html) | 全局基础模板（主题切换/ElementUI/Vue 引入） |
| [requirements.txt](../requirements.txt) | Python 依赖清单 |

> **警告**：本系统使用 **Django 2.1.7 + Python 3.12.9 + Vue 2.6.10 + Element UI 2.12.0**。
> 不可随意升级上述版本，新增前端代码严禁使用 Vue 3 / Element Plus / TypeScript / 构建工具。
> 详见 [04-开发规范摘要.md](./04-开发规范摘要.md)。
