from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'sales'

urlpatterns = [
    # ========== 前台页面 ==========
    path('', views.product_list, name='product_list'),
    path('product_list/', views.product_list, name='product_list_alt'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # ========== 管理员后台页面 ==========
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/products/', views.admin_products, name='admin_products'),
    path('admin/warehouses/', views.admin_warehouses, name='admin_warehouses'),
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/reviews/', views.admin_reviews, name='admin_reviews'),
    path('admin/feedbacks/', views.admin_feedbacks, name='admin_feedbacks'),

    # ========== 商户配置 ==========
    path('seller_config/', views.seller_config, name='seller_config'),
    path('api/seller_config/save/', views.api_seller_config_save, name='api_seller_config_save'),
    path('api/seller_config/get/', views.api_seller_config_get, name='api_seller_config_get'),

    # ========== 商品管理 API ==========
    path('api/products/', views.api_products, name='api_products'),
    path('api/products/purchase/', views.api_products_for_purchase, name='api_products_for_purchase'),
    path('api/product/<int:product_id>/', views.api_product_detail, name='api_product_detail'),
    path('api/product/create/', views.api_product_create, name='api_product_create'),
    path('api/product/update/<int:product_id>/', views.api_product_update, name='api_product_update'),
    path('api/product/delete/<int:product_id>/', views.api_product_delete, name='api_product_delete'),
    path('api/sync_stock/', views.api_sync_stock_to_redis, name='api_sync_stock'),

    # ========== 产品图片 API ==========
    path('api/product/<int:product_id>/images/', views.api_product_images, name='api_product_images'),
    path('api/product/image/delete/<int:image_id>/', views.api_product_image_delete, name='api_product_image_delete'),
    path('api/product/image/upload/', views.api_product_image_upload, name='api_product_image_upload'),
    # ⬇️ 添加这一行 ⬇️
    path('api/product/image/set_cover/<int:image_id>/', views.api_product_image_set_cover, name='api_product_image_set_cover'),

    # ========== 仓库 API ==========
    path('api/warehouses/', views.api_warehouses, name='api_warehouses'),
    path('api/warehouse/create/', views.api_warehouse_create, name='api_warehouse_create'),
    path('api/warehouse/update/<int:warehouse_id>/', views.api_warehouse_update, name='api_warehouse_update'),
    path('api/warehouse/delete/<int:warehouse_id>/', views.api_warehouse_delete, name='api_warehouse_delete'),
    path('api/warehouse/<int:warehouse_id>/products/', views.api_warehouse_products, name='api_warehouse_products'),
    path('api/warehouse/product/update/', views.api_warehouse_product_update, name='api_warehouse_product_update'),

    # ========== 订单 API ==========
    path('api/create_order/', views.api_create_order, name='api_create_order'),
    path('api/pay/', views.api_pay, name='api_pay'),
    path('api/callback/', views.api_callback, name='api_callback'),
    path('api/order_status/<str:order_no>/', views.api_order_status, name='api_order_status'),
    path('api/order/<str:order_no>/logistics/', views.api_order_logistics, name='api_order_logistics'),
    path('api/order/<str:order_no>/update_logistics/', views.api_update_logistics, name='api_update_logistics'),
    path('api/orders/', views.api_orders_list, name='api_orders_list'),
    path('api/order/update_status/<str:order_no>/', views.api_order_update_status, name='api_order_update_status'),

    # ========== 评价 API ==========
    path('api/product/<int:product_id>/reviews/', views.api_product_reviews, name='api_product_reviews'),
    path('api/review/create/', views.api_review_create, name='api_review_create'),
    path('api/review/<int:review_id>/like/', views.api_review_like, name='api_review_like'),
    path('api/review/<int:review_id>/images/', views.api_review_images, name='api_review_images'),
    path('api/review/<int:review_id>/approve/', views.api_review_approve, name='api_review_approve'),
    path('api/review/<int:review_id>/delete/', views.api_review_delete, name='api_review_delete'),

    # ========== 反馈 API ==========
    path('api/feedback/create/', views.api_feedback_create, name='api_feedback_create'),
    path('api/feedback/list/', views.api_feedback_list, name='api_feedback_list'),
    path('api/feedback/<int:feedback_id>/', views.api_feedback_detail, name='api_feedback_detail'),
    path('api/feedback/<int:feedback_id>/handle/', views.api_feedback_handle, name='api_feedback_handle'),

    # ========== 支付相关 ==========
    path('api/create_payment/', views.api_create_payment, name='api_create_payment'),
    path('api/payment_callback/', views.api_payment_callback, name='api_payment_callback'),
    path('api/payment_result/', views.api_payment_result, name='api_payment_result'),
    path('api/payment_status/<str:order_no>/', views.api_query_payment_status, name='api_query_payment_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)