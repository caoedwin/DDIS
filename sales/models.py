from django.db import models
from django.conf import settings
from django.utils import timezone
from app01.models import UserInfo


class Seller(models.Model):
    """卖家/商户信息"""
    PAYMENT_PROVIDER_CHOICES = [
        ('WECHAT', '微信支付'),
        ('ALIPAY', '支付宝'),
        ('BANK', '银行卡'),
    ]

    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE, related_name='seller_profile',
                                verbose_name="关联用户")
    seller_name = models.CharField(max_length=100, verbose_name="商户名称")
    seller_code = models.CharField(max_length=50, unique=True, verbose_name="商户编号")

    # 支付配置
    payment_provider = models.CharField(max_length=20, choices=PAYMENT_PROVIDER_CHOICES, default='WECHAT',
                                        verbose_name="支付服务商")

    # 微信支付配置
    wechat_appid = models.CharField(max_length=64, blank=True, verbose_name="微信AppID")
    wechat_mchid = models.CharField(max_length=64, blank=True, verbose_name="微信商户号")
    wechat_api_key = models.CharField(max_length=128, blank=True, verbose_name="微信API密钥")
    wechat_cert_path = models.CharField(max_length=500, blank=True, verbose_name="微信证书路径")
    wechat_key_path = models.CharField(max_length=500, blank=True, verbose_name="微信密钥路径")

    # 支付宝配置
    alipay_app_id = models.CharField(max_length=64, blank=True, verbose_name="支付宝AppID")
    alipay_private_key = models.TextField(blank=True, verbose_name="支付宝私钥")
    alipay_public_key = models.TextField(blank=True, verbose_name="支付宝公钥")
    alipay_gateway = models.CharField(max_length=200, blank=True, default='https://openapi.alipay.com/gateway.do',
                                      verbose_name="支付宝网关")

    # 银行卡配置（银行转账）
    bank_name = models.CharField(max_length=100, blank=True, verbose_name="银行名称")
    bank_account_name = models.CharField(max_length=100, blank=True, verbose_name="开户名")
    bank_account_number = models.CharField(max_length=50, blank=True, verbose_name="银行卡号")
    bank_branch = models.CharField(max_length=200, blank=True, verbose_name="开户行")

    # 提现配置
    withdraw_min_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="最低提现金额")
    withdraw_commission = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="提现手续费率")

    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "卖家/商户"
        verbose_name_plural = "卖家/商户列表"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.seller_code} - {self.seller_name}"


class Product(models.Model):
    """产品主表"""
    product_code = models.CharField(max_length=50, unique=True, verbose_name="产品编号")
    name = models.CharField(max_length=100, verbose_name="产品名称")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    stock = models.IntegerField(default=0, verbose_name="剩余数量")
    version = models.IntegerField(default=0, verbose_name="乐观锁版本号")
    description = models.TextField(blank=True, verbose_name="描述")

    # 关联卖家
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products', verbose_name="卖家")

    # 新增字段
    category = models.CharField(max_length=50, blank=True, verbose_name="产品分类")
    brand = models.CharField(max_length=50, blank=True, verbose_name="品牌")
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="重量(kg)")
    dimensions = models.CharField(max_length=100, blank=True, verbose_name="尺寸(长x宽x高)")
    color = models.CharField(max_length=50, blank=True, verbose_name="颜色")
    is_active = models.BooleanField(default=True, verbose_name="是否上架")
    sort_order = models.IntegerField(default=0, verbose_name="排序")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "产品"
        verbose_name_plural = "产品列表"
        ordering = ['-sort_order', '-id']

    def __str__(self):
        return f"{self.product_code} - {self.name}"


class ProductImage(models.Model):
    """产品图片（多张）"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="产品")
    image = models.ImageField(upload_to='product_images/%Y/%m/%d/', verbose_name="图片")
    is_cover = models.BooleanField(default=False, verbose_name="是否封面")
    sort_order = models.IntegerField(default=0, verbose_name="排序")
    description = models.CharField(max_length=200, blank=True, verbose_name="图片描述")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "产品图片"
        verbose_name_plural = "产品图片"
        ordering = ['-is_cover', 'sort_order']

    def __str__(self):
        return f"{self.product.name} - 图片{self.id}"


class Warehouse(models.Model):
    """仓库信息"""
    warehouse_code = models.CharField(max_length=20, unique=True, verbose_name="仓库编号")
    name = models.CharField(max_length=100, verbose_name="仓库名称")
    address = models.TextField(verbose_name="仓库地址")
    contact_person = models.CharField(max_length=50, verbose_name="联系人")
    contact_phone = models.CharField(max_length=20, verbose_name="联系电话")
    region = models.CharField(max_length=50, verbose_name="地区")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "仓库"
        verbose_name_plural = "仓库列表"
        ordering = ['region', 'name']

    def __str__(self):
        return f"{self.warehouse_code} - {self.name}"


class ProductWarehouse(models.Model):
    """产品仓库关联（库存明细）"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='warehouses', verbose_name="产品")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='products', verbose_name="仓库")
    stock = models.IntegerField(default=0, verbose_name="仓库库存")
    reserved_stock = models.IntegerField(default=0, verbose_name="预留库存")
    min_stock = models.IntegerField(default=0, verbose_name="最低库存预警")
    max_stock = models.IntegerField(default=0, verbose_name="最高库存预警")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "产品仓库库存"
        verbose_name_plural = "产品仓库库存"
        unique_together = ['product', 'warehouse']

    def __str__(self):
        return f"{self.product.name} - {self.warehouse.name}"


class Order(models.Model):
    """订单主表"""
    STATUS_CHOICES = [
        ('PENDING', '待支付'),
        ('PAYING', '支付中'),
        ('PAID', '已支付'),
        ('SHIPPED', '已发货'),
        ('DELIVERED', '已送达'),
        ('COMPLETED', '已完成'),
        ('CANCELLED', '已取消'),
        ('REFUNDING', '退款中'),
        ('REFUNDED', '已退款'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('WECHAT', '微信支付'),
        ('ALIPAY', '支付宝'),
        ('BANK', '银行卡支付'),
    ]

    order_no = models.CharField(max_length=64, unique=True, verbose_name="订单号")
    user = models.ForeignKey('app01.UserInfo', on_delete=models.SET_NULL, null=True, verbose_name="用户")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="商品")
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, verbose_name="卖家")
    quantity = models.IntegerField(default=1, verbose_name="数量")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="总金额")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="支付方式")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="状态")

    # 支付平台返回的交易号
    transaction_id = models.CharField(max_length=64, blank=True, unique=True, null=True, verbose_name="支付平台交易号")

    # 收货信息
    receiver_name = models.CharField(max_length=50, blank=True, verbose_name="收货人")
    receiver_phone = models.CharField(max_length=20, blank=True, verbose_name="收货电话")
    receiver_address = models.TextField(blank=True, verbose_name="收货地址")
    receiver_region = models.CharField(max_length=50, blank=True, verbose_name="收货地区")

    # 物流信息
    logistics_company = models.CharField(max_length=50, blank=True, verbose_name="物流公司")
    logistics_no = models.CharField(max_length=50, blank=True, verbose_name="物流单号")
    logistics_status = models.CharField(max_length=20, blank=True, verbose_name="物流状态")
    logistics_info = models.TextField(blank=True, verbose_name="物流信息")
    shipped_at = models.DateTimeField(null=True, blank=True, verbose_name="发货时间")
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name="送达时间")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")
    cancelled_at = models.DateTimeField(null=True, blank=True, verbose_name="取消时间")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单列表"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_no} - {self.product.name}"

class OrderLogistics(models.Model):
    """物流追踪信息"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='logistics_tracks', verbose_name="订单")
    logistics_company = models.CharField(max_length=50, verbose_name="物流公司")
    logistics_no = models.CharField(max_length=50, verbose_name="物流单号")
    status = models.CharField(max_length=50, verbose_name="状态")
    content = models.TextField(verbose_name="物流信息内容")
    location = models.CharField(max_length=200, blank=True, verbose_name="位置")
    operator = models.CharField(max_length=50, blank=True, verbose_name="操作人")
    track_time = models.DateTimeField(verbose_name="追踪时间")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "物流追踪"
        verbose_name_plural = "物流追踪"
        ordering = ['-track_time']

    def __str__(self):
        return f"{self.order.order_no} - {self.track_time}"

class PaymentRecord(models.Model):
    """支付记录"""
    PAYMENT_STATUS = [
        ('PENDING', '待支付'),
        ('PROCESSING', '处理中'),
        ('SUCCESS', '成功'),
        ('FAILED', '失败'),
    ]
    payment_no = models.CharField(max_length=64, unique=True, verbose_name="支付平台流水号")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments', verbose_name="订单")
    seller = models.ForeignKey('sales.Seller',
        on_delete=models.PROTECT,
        null=True,  # 允许为空
        blank=True,
        verbose_name="卖家")
    payment_method = models.CharField(max_length=20, choices=Order.PAYMENT_METHOD_CHOICES, verbose_name="支付方式")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="支付金额")
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING', verbose_name="支付状态")
    callback_data = models.TextField(default='{}', blank=True, verbose_name="回调原始数据")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "支付记录"
        verbose_name_plural = "支付记录"

    def __str__(self):
        return f"{self.payment_no} - {self.order.order_no}"


class IdempotentKey(models.Model):
    """幂等键表"""
    STATUS_CHOICES = [
        ('PROCESSING', '处理中'),
        ('SUCCESS', '成功'),
        ('FAILED', '失败'),
    ]
    idempotent_key = models.CharField(max_length=128, unique=True, verbose_name="幂等键")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="订单")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PROCESSING', verbose_name="处理状态")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "幂等键"
        verbose_name_plural = "幂等键"
        indexes = [
            models.Index(fields=['idempotent_key']),
        ]

    def __str__(self):
        return self.idempotent_key


class ProductReview(models.Model):
    """用户评价"""
    RATING_CHOICES = [
        (1, '1星-非常差'),
        (2, '2星-差'),
        (3, '3星-一般'),
        (4, '4星-好'),
        (5, '5星-非常好'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reviews', verbose_name="订单")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="产品")
    user = models.ForeignKey('app01.UserInfo', on_delete=models.SET_NULL, null=True, verbose_name="用户")

    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="评分")
    title = models.CharField(max_length=200, blank=True, verbose_name="评价标题")
    content = models.TextField(verbose_name="评价内容")

    advantages = models.TextField(blank=True, verbose_name="优点")
    disadvantages = models.TextField(blank=True, verbose_name="缺点")
    is_anonymous = models.BooleanField(default=False, verbose_name="是否匿名")
    is_approved = models.BooleanField(default=False, verbose_name="是否审核通过")
    is_recommend = models.BooleanField(default=False, verbose_name="是否推荐")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "用户评价"
        verbose_name_plural = "用户评价"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.user.username if self.user else '匿名'} - {self.rating}星"


class ReviewImage(models.Model):
    """评价图片"""
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, related_name='images', verbose_name="评价")
    image = models.ImageField(upload_to='review_images/%Y/%m/%d/', verbose_name="图片")
    sort_order = models.IntegerField(default=0, verbose_name="排序")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "评价图片"
        verbose_name_plural = "评价图片"
        ordering = ['sort_order']

    def __str__(self):
        return f"评价{self.review.id} - 图片{self.id}"


class UserFeedback(models.Model):
    """用户反馈"""
    FEEDBACK_TYPE_CHOICES = [
        ('COMPLAINT', '投诉'),
        ('SUGGESTION', '建议'),
        ('QUESTION', '咨询'),
        ('AFTER_SALES', '售后'),
        ('OTHER', '其他'),
    ]
    STATUS_CHOICES = [
        ('PENDING', '待处理'),
        ('PROCESSING', '处理中'),
        ('RESOLVED', '已解决'),
        ('CLOSED', '已关闭'),
    ]

    user = models.ForeignKey('app01.UserInfo', on_delete=models.CASCADE, related_name='feedbacks', verbose_name="用户")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='feedbacks',
                              verbose_name="关联订单")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='feedbacks',
                                verbose_name="关联产品")

    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES, verbose_name="反馈类型")
    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="状态")

    images = models.TextField(blank=True, verbose_name="附件图片(JSON数组)")

    handler = models.ForeignKey('app01.UserInfo', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='handled_feedbacks', verbose_name="处理人")
    handle_content = models.TextField(blank=True, verbose_name="处理内容")
    handled_at = models.DateTimeField(null=True, blank=True, verbose_name="处理时间")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "用户反馈"
        verbose_name_plural = "用户反馈"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_feedback_type_display()} - {self.title}"