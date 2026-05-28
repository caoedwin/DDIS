# PCRList/admin.py
from django.contrib import admin
from .models import PCR
from CQM.models import CQMProject
from app01.models import UserInfo

@admin.register(PCR)
class PCRAdmin(admin.ModelAdmin):
    list_display = (
        'pcr_no', 'pcr_title', 'Project', 'phase', 'category',
        'status', 'pd', 'device_fee_usd', 'whether_in_budget', 'created_by',
    )
    list_filter = ('phase', 'status', 'whether_in_budget', 'Customer')  # 修改此处
    search_fields = ('pcr_no', 'pcr_title', 'Project', 'Compalproject', 'remark')
    readonly_fields = ('pd', 'created_at', 'updated_at')
    fieldsets = (
        ('基本信息', {
            'fields': ('pcr_no', 'pcr_title', 'Customer', 'Project', 'Compalproject',
                       'phase', 'category', 'receive_date', 'status')
        }),
        ('NRE 工作量', {
            'fields': ('sample_qty', 'hc_qty', 'hc_days', 'pd', 'device_fee_usd')
        }),
        ('流程与预算', {
            'fields': ('dqa_nre_mail_to_pm', 'pm_send_nre_to_sales',
                       'execution_start', 'execution_end',
                       'whether_in_budget', 'in_budget_but_cost_add', 'remark', 'attachment')
        }),
        ('审计信息', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or getattr(request.user, 'is_SVPuser', False):
            return qs
        user = request.user
        return qs.filter(
            models.Q(created_by=user) | models.Q(Compalproject__in=user.cqmproject_set.all().values_list('Project', flat=True))
        )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'created_by':
            kwargs['queryset'] = UserInfo.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)