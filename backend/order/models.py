import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from product.models import Product
from users.models import User


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name=_("Foydalanuvchi"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yangilangan vaqti"))

    class Meta:
        verbose_name = _("Savatcha")
        verbose_name_plural = _("Savatchalar")

    def __str__(self):
        return f"{self.user.phone_number} ning savatchasi"

    @property
    def total_price(self):
        """Savatchadagi barcha mahsulotlarning umumiy summasi"""
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        """Savatchadagi mahsulot pozitsiyalari soni"""
        return self.items.count()


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Savatcha"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name=_("Mahsulot"),
    )
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=1,
        verbose_name=_("Miqdori"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yangilangan vaqti"))

    class Meta:
        verbose_name = _("Savatchadagi mahsulot")
        verbose_name_plural = _("Savatchadagi mahsulotlar")
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError(_("Miqdor 0 dan katta bo'lishi kerak."))
        if self.product.quantity < self.quantity:
            raise ValidationError(
                _("Omborda yetarli mahsulot yo'q. Mavjud: %(stock)s")
                % {"stock": self.product.quantity}
            )

    @property
    def total_price(self):
        """Chegirmali narx bo'lsa uni hisobga oladi"""
        price = self.product.discount_price or self.product.price
        return price * self.quantity


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", _("Yangi")
        CONFIRMED = "confirmed", _("Tasdiqlandi")
        SHIPPING = "shipping", _("Yetkazib berilmoqda")
        DELIVERED = "delivered", _("Yetkazib berildi")
        CANCELLED = "cancelled", _("Bekor qilindi")
        RETURNED = "returned", _("Qaytarildi")

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("Foydalanuvchi"),
    )
    order_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name=_("Buyurtma raqami"),
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name=_("Holati"),
    )
    total_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Umumiy summa (Snapshot)"),
    )
    address = models.CharField(
        max_length=255,
        verbose_name=_("Yetkazib berish manzili"),
    )
    contact_phone = models.CharField(
        max_length=13,
        verbose_name=_("Aloqa telefoni"),
    )
    note = models.TextField(
        blank=True,
        verbose_name=_("Izoh"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yangilangan vaqti"))

    class Meta:
        verbose_name = _("Buyurtma")
        verbose_name_plural = _("Buyurtmalar")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order_number"]),
            models.Index(fields=["user", "status"]),
            models.Index(fields=["status", "created_at"]),
        ]

    def __str__(self):
        return f"{self.order_number} - {self.user.phone_number} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_order_number():
        """ORD-YYYYMMDD-XXXX ko'rinishidagi unique raqam yaratadi"""
        date_str = timezone.now().strftime("%Y%m%d")
        random_str = str(uuid.uuid4().hex[:4]).upper()
        return f"ORD-{date_str}-{random_str}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Buyurtma"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name=_("Mahsulot"),
    )
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        verbose_name=_("Miqdori"),
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_("Sotib olingan narx (Snapshot)"),
    )
    total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Jami summa (Snapshot)"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yangilangan vaqti"))

    class Meta:
        verbose_name = _("Buyurtma mahsuloti")
        verbose_name_plural = _("Buyurtma mahsulotlari")

    def __str__(self):
        return f"{self.order.order_number} -> {self.product.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        if not self.total:
            self.total = self.price * self.quantity
        super().save(*args, **kwargs)


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="status_history",
        verbose_name=_("Buyurtma"),
    )
    from_status = models.CharField(
        max_length=20,
        choices=Order.Status.choices,
        null=True,
        blank=True,
        verbose_name=_("Eski holati"),
    )
    to_status = models.CharField(
        max_length=20,
        choices=Order.Status.choices,
        verbose_name=_("Yangi holati"),
    )
    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("O'zgartiruvchi xodim"),
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_("Izoh/Sabab"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yangilangan vaqti"))

    class Meta:
        verbose_name = _("Buyurtma statusi tarixi")
        verbose_name_plural = _("Buyurtma statuslari tarixi")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order.order_number}: {self.from_status} -> {self.to_status}"


class Return(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Kutilmoqda")
        APPROVED = "approved", _("Tasdiqlandi")
        REJECTED = "rejected", _("Rad etildi")

    order_item = models.ForeignKey(
        OrderItem,
        on_delete=models.PROTECT,
        related_name="returns",
        verbose_name=_("Buyurtma mahsuloti"),
    )
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        verbose_name=_("Qaytarilayotgan miqdor"),
    )
    reason = models.TextField(
        verbose_name=_("Qaytarish sababi"),
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("So'rov holati"),
    )
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="processed_returns",
        verbose_name=_("Ko'rib chiqqan xodim"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaratilgan vaqti"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yangilangan vaqti"))

    class Meta:
        verbose_name = _("Qaytarilgan mahsulot")
        verbose_name_plural = _("Qaytarilgan mahsulotlar")

    def __str__(self):
        return f"Return #{self.id} - {self.order_item.product.name} ({self.get_status_display()})"

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError(_("Qaytarish miqdori 0 dan katta bo'lishi kerak."))
        if self.quantity > self.order_item.quantity:
            raise ValidationError(
                _("Qaytarilayotgan miqdor sotib olingan miqdordan (%(max_qty)s) ko'p bo'lishi mumkin emas.")
                % {"max_qty": self.order_item.quantity}
            )