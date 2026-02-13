from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UEInspectionItem, UEBatch, UEScoreRecord


# ---------- 检查项目管理 ----------
@admin.register(UEInspectionItem)
class UEInspectionItemAdmin(admin.ModelAdmin):
    """UE检查项目后台配置"""
    list_display = ('Item', 'Function', 'Category', 'characteristic', 'detailed_description', 'inspect_method')
    list_filter = ('Function', 'Category')
    search_fields = ('Item', 'Category', 'characteristic', 'detailed_description')
    ordering = ('Item',)
    # 若字段过多，可折叠详细字段
    fieldsets = (
        (None, {
            'fields': ('Item', 'Function', 'Category', 'characteristic')
        }),
        ('详细说明', {
            'fields': ('detailed_description', 'inspect_method'),
            'classes': ('wide', 'collapse'),
        }),
    )


# ---------- 评分记录内联（用于批次详情页）----------
class UEScoreRecordInline(admin.TabularInline):
    """将评分记录以表格形式嵌入批次编辑页"""
    model = UEScoreRecord
    extra = 0  # 不显示额外空白行
    fields = ('inspection_item', 'OneStar', 'TwoStar', 'ThreeStar', 'NotSup', 'remark', 'scorer', 'scored_date')
    readonly_fields = ('scored_date',)  # 评分时间自动生成，只读
    raw_id_fields = ('inspection_item', 'scorer')  # 外键使用搜索框，避免下拉列表过长
    verbose_name = '评分记录'
    verbose_name_plural = '评分记录'


# ---------- 批次管理 ----------
@admin.register(UEBatch)
class UEBatchAdmin(admin.ModelAdmin):
    """UE检查批次后台配置"""
    list_display = ('batch_id', 'project', 'batch_name', 'test_date', 'created_by', 'created_date')
    list_filter = ('project', 'test_date')
    search_fields = ('batch_name', 'project__Project')  # 跨关联表搜索
    date_hierarchy = 'test_date'  # 日期层级筛选
    raw_id_fields = ('project', 'created_by')  # 外键使用搜索框
    inlines = [UEScoreRecordInline]  # 内嵌该批次的所有评分记录
    ordering = ('-test_date',)


# ---------- 评分记录独立管理（可选）----------
@admin.register(UEScoreRecord)
class UEScoreRecordAdmin(admin.ModelAdmin):
    """UE评分记录后台配置（独立查看所有评分）"""
    list_display = ('record_id', 'batch', 'inspection_item', 'scorer',
                    'OneStar', 'TwoStar', 'ThreeStar', 'NotSup', 'scored_date')
    list_filter = ('batch', 'scorer', 'inspection_item__Function')
    search_fields = ('batch__batch_name', 'inspection_item__Item', 'remark')
    raw_id_fields = ('batch', 'inspection_item', 'scorer')
    readonly_fields = ('scored_date',)
    ordering = ('-scored_date',)