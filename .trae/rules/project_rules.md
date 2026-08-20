# Reliability_Row_data (DDIS) 项目规则

> 本文件基于项目实际代码和环境自动生成，是所有 AI 辅助开发的权威参考。
> 最后更新: 2026-08-20

---

## 1. 技术栈总览

| 类别         | 技术 / 版本                          | 说明                                      |
| ------------ | ------------------------------------- | ----------------------------------------- |
| 语言         | Python 3.12.9                         | 系统 Python，项目通过 requirements.txt 管理依赖 |
| Web 框架     | Django 2.1.7                          | MVT 架构，函数视图为主                     |
| REST API    | Django REST Framework 3.11.0         | 序列化器 + ViewSet/APIView                 |
| 认证         | Session + JWT (simplejwt 5.2.0)       | 同时兼容 djangorestframework-jwt 1.11.0    |
| 任务队列     | Celery 4.4.2 + Redis                   | 定时任务 (celery-beat) + 异步任务          |
| WebSocket   | Django Channels 2.2.0                 | 基于 channels-redis 2.4.2                  |
| 数据库       | MySQL (主) + MongoDB (辅)             | MySQL: PyMySQL 0.9.3 / django-mysql 3.7.0 |
|              |                                       | MongoDB: mongoengine 0.20.0 / pymongo 3.10.1 |
| 缓存/消息    | Redis 5.0.1                            | Celery broker / Channels layer / 业务缓存  |
| 后台管理     | django-simpleui 2022.4.9              | 基于 Django admin 的美化界面               |
| 前端框架     | Vue.js 2.6.10                         | **不是 Vue 3，不是 React**                |
| UI 组件库   | Element UI 2.12.0                     | Vue 2 组件库                               |
| 前端路由     | Vue Router 3.1.3                      | 仅用于部分 SPA 页面                       |
| HTTP 请求    | Axios (静态 JS 引入)                  | 非 npm 包，通过 `<script>` 引入           |
| CSS 框架    | Bootstrap 4 + 自定义 CSS              | 含 Font Awesome / Themify Icons           |
| 模板引擎     | Django Templates                      | 模板继承 (extends base.html)              |
| 构建工具     | 无                                    | 前端通过 `<script>` 标签直接引入，无 webpack/vite |
| 部署         | Windows + IIS (wfastcgi 3.0.0)       | 开发环境为 Windows                         |

---

## 2. 项目目录结构

```
Reliability_Row_data/
├── manage.py                     # Django 入口
├── requirements.txt              # Python 依赖
├── Reliability_Row_data/         # 项目主配置
│   ├── settings.py               # Django 配置 (数据库/Redis/Celery/日志/权限)
│   ├── urls.py                   # 根 URL 路由
│   └── routing.py                # Channels ASGI 路由
├── app01/                        # 核心应用 (登录/导航/权限/文件上传/WebSocket)
│   ├── views.py                 # 主视图
│   ├── models.py                # 核心模型
│   ├── serializers.py            # DRF 序列化器
│   ├── consumers.py              # Channels WebSocket 消费者
│   ├── routing.py                # WebSocket 路由
│   └── tasks.py                  # Celery 异步任务
├── CDM/                          # 各业务模块 (每个模块结构相似)
├── CQM/                          # 含 DRF 序列化器/认证/权限
├── TestPlanSW/                   # 测试计划模块
├── PersonalInfo/                # 人员信息模块
├── sales/                        # 销售模块
├── middleware/                   # 自定义中间件 (RBAC权限/IP记录)
│   ├── checkper.py              # RBAC 权限中间件
│   └── UserIP.py                # 用户IP记录中间件
├── extra_apps/                   # 第三方应用 (DjangoUeditor 等)
├── templates/                    # Django 模板 (base.html 为基础模板)
│   ├── base.html                # 基础模板 (含主题切换/ElementUI/Vue 引入)
│   ├── login.html               # 登录页
│   └── [module]/                # 各业务模块模板
├── static/                       # 静态资源
│   ├── js/                       # Vue.js / axios / jquery 等
│   ├── css/                     # 全局样式
│   ├── download_UPK/            # Vue 2.6.10 / Element UI 2.12.0 / Vue Router 3.1.3 源码
│   └── vendor/                  # 第三方 CSS/JS (fontawesome 等)
├── logs/                        # 日志文件 (按日期滚动)
├── medias/                      # 媒体文件上传目录
└── celery/                      # Celery 配置
```

### 业务模块标准结构

每个业务模块 (如 CDM, CQM, MQM 等) 包含以下文件:

```
[module]/
├── __init__.py
├── admin.py          # Django Admin 注册
├── apps.py           # App 配置
├── models.py         # 数据模型
├── views.py          # 视图函数
├── urls.py           # 模块 URL 路由
├── forms.py          # Django Form (可选)
├── serializers.py    # DRF 序列化器 (仅 DRF 模块)
├── permissions.py    # 自定义权限 (可选)
└── tests.py          # 测试
```

---

## 3. 后端代码规范

### 3.1 Django 版本约束

- **Django 2.1.7** — 不可随意升级，以下 API 在此版本中有效:
  - `django.conf.urls.url` (非 `re_path`)
  - `from django.urls import path, include, re_path`
  - `path()` 支持 `<str:param>` / `<int:param>` 转换器
- **Python 3.12.9** — 注意 Django 2.1.7 与 Python 3.12 存在兼容性风险，修改核心代码时需谨慎测试

### 3.2 视图 (Views)

- **以函数视图为主** (Function-Based Views)，使用 `@csrf_exempt` 装饰器处理 POST 请求
- 登录状态检查: 每个视图函数开头检查 `request.session.get('is_login', None)`
- 未登录重定向: `return redirect('/login/')`
- 视图函数命名: 下划线风格，如 `CDM_upload`, `CDM_search`, `CDM_edit`
- 示例模式:

```python
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def CDM_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    # ... 业务逻辑
    return render(request, 'CDM/CDM_upload.html', context)
```

### 3.3 模型 (Models)

- 模型类名使用 **PascalCase**，如 `CDM`, `CQM`, `PersonalInfo`
- 字段名使用 **PascalCase / 混合命名**，如 `Customer`, `Project`, `SKU_NO`, `edit_time`
- 每个模型类定义 `Meta` 内部类，设置 `verbose_name` 和 `verbose_name_plural`
- 每个模型类定义 `toJSON(self)` 方法，用于序列化:

```python
class CDM(models.Model):
    Customer = models.CharField(max_length=20)
    Project = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'CDM'
        verbose_name_plural = verbose_name

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
        d = {}
        for attr in fields:
            d[attr] = getattr(self, attr)
        import json
        return json.dumps(d)
```

### 3.4 URL 路由

- 根 `urls.py` 中使用 `path()` 和 `re_path()` 注册路由
- 每个业务模块使用 `include()` 引入子路由，并指定 `namespace`:

```python
path('CDM/', include('CDM.urls', namespace='CDM')),
```

- 模块内 `urls.py` 使用 `path()` 定义具体路由
- 权限白名单在 `settings.SAFE_URL` 中配置 (正则匹配)

### 3.5 DRF 序列化器

- 使用 `ModelSerializer`，`fields = "__all__"` 模式:

```python
from rest_framework import serializers
from .models import *

class CQMserilizer(serializers.ModelSerializer):
    class Meta:
        model = CQM
        fields = "__all__"
```

### 3.6 认证与权限

- **Session 认证**: 默认方式，通过 `request.session` 存储用户状态
- **JWT 认证**: 使用 `djangorestframework-simplejwt 5.2.0`，配置在 `settings.SIMPLE_JWT`
- **RBAC 权限**: 通过 `middleware/checkper.py` 的 `RbacMiddleware` 实现 URL 级权限控制
- **权限白名单**: `settings.SAFE_URL` 列表中的 URL 正则匹配可跳过权限检查
- Session 配置: `SESSION_ENGINE = 'django.contrib.sessions.backends.db'`

### 3.7 中间件

- 自定义中间件位于 `middleware/` 目录
- 继承自定义 `MiddlewareMixin` 基类
- 中间件加载顺序在 `settings.MIDDLEWARE` 中严格定义

### 3.8 Celery 任务

- Celery 配置在 `settings.py` 底部
- Broker: Redis (db=1)，Result Backend: Redis (db=2)
- 定时任务通过 `CELERY_BEAT_SCHEDULE` 配置
- 异步任务定义在各模块的 `tasks.py` 中

### 3.9 日志

- 日志配置在 `settings.LOGGING` 中
- 日志目录: `项目根目录/logs/`
- 日志格式: `[时间] [文件:行号] [模块:函数] [级别] - 消息`
- 按日期滚动，单文件最大 5MB，保留 5 个备份

### 3.10 文件上传

- Media 根目录: `c:/media`
- 最大内存上传: 500MB (`FILE_UPLOAD_MAX_MEMORY_SIZE`)
- 临时目录: `/media/temp`

---

## 4. 前端代码规范

### 4.1 Vue.js 版本约束

- **Vue.js 2.6.10** — **严禁使用 Vue 3 语法**
- **不使用** Composition API (`setup()`, `ref()`, `reactive()`)
- 使用 **Options API** (`data()`, `methods`, `computed`, `watch`)
- Vue 源码位于: `static/download_UPK/vue@2.6.10/dist/vue.js`

### 4.2 Element UI 版本约束

- **Element UI 2.12.0** — Vue 2 专用组件库
- **不是** Element Plus (Element Plus 是 Vue 3 版本)
- CSS 引入: `static/download_UPK/element-ui@2.12.0/lib/theme-chalk/index.css`
- 组件示例: `<el-table>`, `<el-form>`, `<el-button>`, `<el-dialog>` 等

### 4.3 前端引入方式

- **无构建工具** — 不使用 webpack/vite/rollup
- 所有 JS/CSS 通过 `<script>` 和 `<link>` 在 Django 模板中直接引入
- Axios: `static/js/axios.min.js`
- Vue: `static/download_UPK/vue@2.6.10/dist/vue.js`
- Element UI: `static/download_UPK/element-ui@2.12.0/lib/index.js`

### 4.4 模板规范

- 所有页面模板继承 `base.html`: `{% extends 'base.html' %}`
- 模板区块:
  - `{% block title %}` — 页面标题
  - `{% block css %}` — 页面样式
  - `{% block content %}` — 页面内容
  - `{% block style %}` — 额外样式
- Django 模板标签: `{% load staticfiles %}`, `{% csrf_token %}`, `{% url 'namespace:name' %}`

### 4.5 主题切换

- 支持 **深色/浅色** 主题切换 (右上角按钮)
- `body` 上动态添加 `theme-light` / `theme-dark` class
- **禁止硬编码颜色** — 使用 CSS 变量或依赖主题 class
- 禁止内联 `style="color: white;"` 等固定颜色
- 子页面背景使用 `rgba()` 半透明，不要固定背景

### 4.6 Vue 实例模式

```javascript
new Vue({
    el: '#app',
    data() {
        return {
            tableData: [],
            form: {},
            loading: false
        }
    },
    methods: {
        fetchData() {
            axios.post('/CDM/CDM_search/', {
                // ...
            }).then(res => {
                this.tableData = res.data
            })
        }
    },
    mounted() {
        this.fetchData()
    }
})
```

### 4.7 Axios 请求

- 全局使用 Axios (非 fetch API)
- POST 请求需携带 CSRF Token (通过 `Qs.stringify` 或 FormData)
- 请求 URL 使用相对路径，如 `/CDM/CDM_search/`
- 响应数据格式: 直接返回 JSON

---

## 5. 数据库规范

### 5.1 MySQL (主数据库)

- 数据库名: `reliabilityrowdata`
- 引擎: InnoDB
- 字符集: utf-8
- 连接库: PyMySQL 0.9.3 + django-mysql 3.7.0
- Django ORM 查询为主

### 5.2 MongoDB (辅助数据库)

- 连接库: mongoengine 0.20.0 + pymongo 3.10.1
- 用于非结构化数据存储 (如 mongotest 模块)
- 通过 `mongoengine.connect()` 在 `settings.py` 中初始化连接

### 5.3 Redis

- 版本: Redis 5.0.1
- 多 DB 用途分配:
  - db=1: Celery Broker
  - db=2: Celery Result Backend
  - db=3: 业务缓存 (分布式锁/幂等)
  - db=14: Channels Layer
- 密码: `DCT2019`

---

## 6. 第三方库关键清单

| 库 | 版本 | 用途 |
|---|---|---|
| Django | 2.1.7 | Web 框架 |
| djangorestframework | 3.11.0 | REST API |
| djangorestframework-simplejwt | 5.2.0 | JWT 认证 |
| djangorestframework-jwt | 1.11.0 | JWT 认证 (兼容) |
| channels | 2.2.0 | WebSocket |
| channels-redis | 2.4.2 | Channels 后端 |
| celery | 4.4.2 | 任务队列 |
| django-celery | 3.3.1 | Celery Django 集成 |
| django-cors-headers | 3.7.0 | 跨域支持 |
| django-crispy-forms | 1.7.2 | 表单渲染 |
| django-filter | 2.2.0 | 查询过滤 |
| django-import-export | 1.2.0 | 数据导入导出 |
| django-reversion | 3.0.4 | 数据版本控制 |
| django-simple-captcha | 0.5.10 | 验证码 |
| django-simpleui | 2022.4.9 | Admin 美化 |
| django-jsonfield | 1.4.1 | JSON 字段 |
| django-mongoengine | 0.4.1 | MongoDB 集成 |
| openpyxl | 3.0.0 | Excel 处理 |
| XlsxWriter | 3.0.3 | Excel 写入 |
| pandas | 1.3.5 | 数据分析 |
| Pillow | 9.2.0 | 图像处理 |
| requests | 2.21.0 | HTTP 请求 |
| openai | 1.39.0 | OpenAI API |
| exchangelib | 5.0.3 | Exchange 邮件 |
| lxml | 4.9.1 | XML/HTML 解析 |
| beautifulsoup4 | 4.7.1 | HTML 解析 |
| selenium | 3.141.0 | 浏览器自动化 |
| pycryptodome | 3.23.0 | 加密 |
| Twisted | 23.8.0 | 异步网络框架 (Channels 依赖) |

---

## 7. 启动与运行

### 7.1 开发服务器

```bash
python manage.py runserver 0.0.0.0:8000
```

### 7.2 Celery Worker

```bash
celery -A Reliability_Row_data worker -l info
```

### 7.3 Celery Beat (定时任务)

```bash
celery -A Reliability_Row_data beat -l info
```

### 7.4 Channels (WebSocket)

```bash
daphne -b 0.0.0.0 -p 8000 Reliability_Row_data.asgi:application
```

或使用项目提供的批处理文件:
- `ChannelsServer.bat` — 启动 Channels 服务
- `DDISceleryworker.bat` — 启动 Celery Worker
- `DDIScelerybeat.bat` — 启动 Celery Beat

---

## 8. AI 辅助开发关键约束

### 禁止事项

1. **禁止使用 Vue 3 语法** — 不使用 `<script setup>`, `ref()`, `reactive()`, `defineProps()`
2. **禁止使用 Element Plus** — 只能用 Element UI 2.12.0
3. **禁止使用 React** — 前端框架是 Vue 2
4. **禁止引入 npm/webpack 构建工具** — 前端无构建步骤
5. **禁止升级 Django 版本** — 项目锁定 Django 2.1.7
6. **禁止使用 Django 2.2+ 的 API** — 如 `jsonfield` 改为 `django_jsonfield`
7. **禁止在模板中硬编码颜色** — 使用主题 CSS 变量
8. **禁止使用 TypeScript** — 前端纯 JavaScript

### 必须遵守

1. **新模块必须遵循标准目录结构** (models/views/urls/admin/forms)
2. **视图函数必须检查登录状态** (`request.session.get('is_login')`)
3. **POST 请求使用 `@csrf_exempt`** 或正确处理 CSRF Token
4. **URL 路由必须注册 namespace** (如 `namespace='CDM'`)
5. **敏感信息 (密码/密钥) 已在 settings.py 中** — AI 辅助开发时不要暴露到前端
6. **模型字段命名保持 PascalCase** — 与现有代码保持一致
7. **模板必须继承 base.html** — 确保主题/导航一致
8. **日期时间处理注意时区** — `TIME_ZONE = 'Asia/Shanghai'`, `USE_TZ = False`

---

## 9. 常用 URL 路由

| URL | 说明 |
|-----|------|
| `/login/` | 登录页 |
| `/index/` | 主页 (导航菜单) |
| `/admin/` | Django Admin 后台 |
| `/docs/` | DRF API 文档 |
| `/CDM/` | CDM 模块 |
| `/CQM/` | CQM 模块 |
| `/TestPlanSW/` | SW 测试计划 |
| `/PersonalInfo/` | 人员信息 |
| `/media/` | 媒体文件 |
| `/static/` | 静态文件 |
