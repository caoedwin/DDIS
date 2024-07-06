from django.apps import AppConfig


class AutoresultConfig(AppConfig):
    #  不能为名称，应该是app的路径
    name = 'AutoResult'
    # 中文要显示的名称
    verbose_name = "自动化统计"
    verbose_name_plural = verbose_name
