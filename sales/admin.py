from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import (
    Product, ProductImage, Warehouse, ProductWarehouse,
    Order, OrderLogistics, PaymentRecord, IdempotentKey,
    ProductReview, ReviewImage, UserFeedback, Seller
)

User = get_user_model()


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_cover', 'sort_order', 'description')
    readonly_fields = ('created_at',)


class ProductWarehouseInline(admin.TabularInline):
    model = ProductWarehouse
    extra = 1
    fields = ('warehouse', 'stock', 'reserved_stock', 'min_stock', 'max_stock')
    readonly_fields = ('updated_at',)


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('seller_code', 'seller_name', 'user', 'payment_provider', 'is_active', 'created_at')
    list_display_links = ('seller_code', 'seller_name')  # 点击可编辑
    search_fields = ('seller_code', 'seller_name', 'user__username')
    list_filter = ('payment_provider', 'is_active')
    list_editable = ('payment_provider', 'is_active')  # 可直接在列表页编辑
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('基本信息', {'fields': ('user', 'seller_name', 'seller_code', 'is_active')}),
        ('支付配置', {'fields': ('payment_provider',)}),
        ('微信支付', {'fields': ('wechat_appid', 'wechat_mchid', 'wechat_api_key', 'wechat_cert_path', 'wechat_key_path')}),
        ('支付宝', {'fields': ('alipay_app_id', 'alipay_private_key', 'alipay_public_key', 'alipay_gateway')}),
        ('银行转账', {'fields': ('bank_name', 'bank_account_name', 'bank_account_number', 'bank_branch')}),
        ('提现配置', {'fields': ('withdraw_min_amount', 'withdraw_commission')}),
        ('时间信息', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_code', 'name', 'seller', 'price', 'stock', 'category', 'brand', 'is_active', 'created_at')
    list_display_links = ('product_code', 'name')  # 点击可编辑
    search_fields = ('product_code', 'name', 'brand', 'category')
    list_filter = ('category', 'brand', 'is_active', 'seller', 'created_at')
    list_editable = ('price', 'stock', 'is_active', 'category', 'brand')  # 列表页直接编辑
    readonly_fields = ('created_at', 'updated_at', 'version')
    inlines = [ProductImageInline, ProductWarehouseInline]
    fieldsets = (
        ('基本信息', {'fields': ('product_code', 'name', 'seller', 'category', 'brand', 'description')}),
        ('价格与库存', {'fields': ('price', 'stock', 'version')}),
        ('规格属性', {'fields': ('weight', 'dimensions', 'color')}),
        ('状态与排序', {'fields': ('is_active', 'sort_order')}),
        ('时间信息', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('warehouse_code', 'name', 'region', 'address', 'contact_person', 'contact_phone', 'is_active')
    list_display_links = ('warehouse_code', 'name')  # 点击可编辑
    search_fields = ('warehouse_code', 'name', 'address', 'region')
    list_filter = ('region', 'is_active')
    list_editable = ('region', 'contact_person', 'contact_phone', 'is_active')  # 列表页直接编辑
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('基本信息', {'fields': ('warehouse_code', 'name', 'region', 'address', 'is_active')}),
        ('联系信息', {'fields': ('contact_person', 'contact_phone')}),
        ('时间信息', {'fields': ('created_at', 'updated_at')}),
    )


class OrderLogisticsInline(admin.TabularInline):
    model = OrderLogistics
    extra = 0
    fields = ('logistics_company', 'logistics_no', 'status', 'content', 'location', 'track_time')
    readonly_fields = ('created_at',)


class PaymentRecordInline(admin.TabularInline):
    model = PaymentRecord
    extra = 0
    fields = ('payment_no', 'payment_method', 'amount', 'status', 'created_at')
    readonly_fields = ('payment_no', 'payment_method', 'amount', 'created_at')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_no', 'user', 'seller', 'product', 'quantity', 'total_amount', 'payment_method', 'status', 'created_at')
    list_display_links = ('order_no',)  # 点击可编辑
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_no', 'user__username', 'product__name', 'receiver_name', 'receiver_phone')
    inlines = [PaymentRecordInline, OrderLogisticsInline]
    list_editable = ('status', 'payment_method')  # 列表页直接编辑状态
    readonly_fields = ('created_at', 'updated_at', 'paid_at')
    fieldsets = (
        ('基本信息', {'fields': ('order_no', 'user', 'seller', 'product', 'quantity', 'total_amount', 'payment_method', 'status', 'transaction_id')}),
        ('收货信息', {'fields': ('receiver_name', 'receiver_phone', 'receiver_address', 'receiver_region')}),
        ('物流信息', {'fields': ('logistics_company', 'logistics_no', 'logistics_status', 'logistics_info', 'shipped_at', 'delivered_at')}),
        ('时间信息', {'fields': ('created_at', 'updated_at', 'paid_at', 'cancelled_at')}),
    )


@admin.register(OrderLogistics)
class OrderLogisticsAdmin(admin.ModelAdmin):
    list_display = ('order', 'logistics_company', 'logistics_no', 'status', 'track_time')
    list_display_links = ('order',)
    list_filter = ('status', 'logistics_company')
    search_fields = ('order__order_no', 'logistics_no')
    list_editable = ('status', 'logistics_company')  # 列表页直接编辑
    readonly_fields = ('created_at',)
    fieldsets = (
        ('订单信息', {'fields': ('order',)}),
        ('物流信息', {'fields': ('logistics_company', 'logistics_no', 'status', 'content', 'location', 'operator')}),
        ('时间信息', {'fields': ('track_time', 'created_at')}),
    )


@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ('payment_no', 'order', 'seller', 'payment_method', 'amount', 'status', 'created_at')
    list_display_links = ('payment_no',)
    list_filter = ('status', 'payment_method')
    search_fields = ('payment_no', 'order__order_no')
    list_editable = ('status',)  # 列表页直接编辑状态
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('基本信息', {'fields': ('payment_no', 'order', 'seller', 'payment_method', 'amount', 'status')}),
        ('回调数据', {'fields': ('callback_data',)}),
        ('时间信息', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(IdempotentKey)
class IdempotentKeyAdmin(admin.ModelAdmin):
    list_display = ('idempotent_key', 'order', 'status', 'created_at')
    list_display_links = ('idempotent_key',)
    list_filter = ('status',)
    search_fields = ('idempotent_key', 'order__order_no')
    list_editable = ('status',)  # 列表页直接编辑状态
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('基本信息', {'fields': ('idempotent_key', 'order', 'status')}),
        ('时间信息', {'fields': ('created_at', 'updated_at')}),
    )


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1
    fields = ('image', 'sort_order')
    readonly_fields = ('created_at',)


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating', 'title', 'is_approved', 'is_recommend', 'created_at')
    list_display_links = ('id', 'title')
    list_filter = ('rating', 'is_approved', 'is_recommend', 'created_at')
    search_fields = ('product__name', 'user__username', 'content', 'title')
    inlines = [ReviewImageInline]
    list_editable = ('is_approved', 'is_recommend', 'rating')  # 列表页直接编辑
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('评价信息', {'fields': ('order', 'product', 'user', 'rating', 'title', 'content', 'advantages', 'disadvantages')}),
        ('状态设置', {'fields': ('is_anonymous', 'is_approved', 'is_recommend')}),
        ('时间信息', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'feedback_type', 'title', 'status', 'created_at')
    list_display_links = ('id', 'title')
    list_filter = ('feedback_type', 'status', 'created_at')
    search_fields = ('user__username', 'title', 'content')
    list_editable = ('status', 'feedback_type')  # 列表页直接编辑
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('基本信息', {'fields': ('user', 'order', 'product', 'feedback_type', 'title', 'content', 'status')}),
        ('处理信息', {'fields': ('handler', 'handle_content', 'handled_at')}),
        ('附件', {'fields': ('images',)}),
        ('时间信息', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'image', 'sort_order', 'created_at')
    list_display_links = ('id',)
    list_editable = ('sort_order',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('评价图片', {'fields': ('review', 'image', 'sort_order')}),
        ('时间信息', {'fields': ('created_at',)}),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'is_cover', 'sort_order', 'description', 'created_at')
    list_display_links = ('id',)
    list_filter = ('is_cover', 'product')
    search_fields = ('product__name', 'description')
    list_editable = ('is_cover', 'sort_order', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('图片信息', {'fields': ('product', 'image', 'is_cover', 'sort_order', 'description')}),
        ('时间信息', {'fields': ('created_at',)}),
    )


@admin.register(ProductWarehouse)
class ProductWarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'warehouse', 'stock', 'reserved_stock', 'min_stock', 'max_stock', 'updated_at')
    list_display_links = ('id',)
    list_filter = ('warehouse',)
    search_fields = ('product__name', 'warehouse__name')
    list_editable = ('stock', 'reserved_stock', 'min_stock', 'max_stock')
    readonly_fields = ('updated_at',)
    fieldsets = (
        ('库存信息', {'fields': ('product', 'warehouse', 'stock', 'reserved_stock', 'min_stock', 'max_stock')}),
        ('时间信息', {'fields': ('updated_at',)}),
    )