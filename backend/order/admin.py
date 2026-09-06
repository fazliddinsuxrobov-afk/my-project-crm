from django.contrib import admin

from .models import (
    Cart,
    CartItem,
    Order,
    OrderItem,
    OrderStatusHistory,
    Return,
)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ("product", "quantity", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "total_items",
        "total_price",
        "created_at",
        "updated_at",
    )
    search_fields = ("user__phone_number",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = (
        "product",
        "quantity",
        "price",
        "total",
        "created_at",
    )
    readonly_fields = ("total", "created_at")


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    fields = (
        "from_status",
        "to_status",
        "changed_by",
        "comment",
        "created_at",
    )
    readonly_fields = ("created_at",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "user",
        "status",
        "total_price",
        "contact_phone",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "user__phone_number",
        "contact_phone",
        "address",
    )

    readonly_fields = (
        "order_number",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "order_number",
                    "user",
                    "status",
                    "total_price",
                )
            },
        ),
        (
            "Доставка",
            {
                "fields": (
                    "address",
                    "contact_phone",
                    "note",
                )
            },
        ),
        (
            "Временные данные",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    inlines = [
        OrderItemInline,
        OrderStatusHistoryInline,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product",
        "quantity",
        "price",
        "total",
        "created_at",
    )

    search_fields = (
        "order__order_number",
        "product__name",
    )

    readonly_fields = (
        "total",
        "created_at",
        "updated_at",
    )

    list_filter = ("created_at",)


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "from_status",
        "to_status",
        "changed_by",
        "created_at",
    )

    list_filter = (
        "from_status",
        "to_status",
        "created_at",
    )

    search_fields = (
        "order__order_number",
        "changed_by__phone_number",
        "comment",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_item",
        "quantity",
        "status",
        "processed_by",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "order_item__order__order_number",
        "order_item__product__name",
        "reason",
        "processed_by__phone_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
