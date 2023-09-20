from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.utils.html import format_html
from .models import (
    Giftpurchase,
    GiftPurchaseMessageText,
    RealGift,
    VirtualGift,
    AllGifts,
)
from .models import RealGiftPriceForRegion, VirtualGiftPriceForRegion


class GiftpurchaseAdmin(ModelAdmin):
    def get_gift(self, allgift):
        if allgift.type == "real":
            gift = RealGift.objects.get(allgift=allgift)
        else:
            gift = VirtualGift.objects.get(allgift=allgift)
        return gift

    def gift_name(self, obj):
        gift = self.get_gift(obj.gift)
        return gift.gift_name

    def image(self, obj):
        gift = self.get_gift(obj.gift)
        return format_html(
            '<img src="/media/{}" width="auto" height="45px" />'.format(gift.picture)
        )

    def amount(self, obj):
        gift = self.get_gift(obj.gift)
        return gift.cost

    def sender_location(self, obj):
        sender = obj.user
        return "%s, %s, %s" % (sender.city, sender.state, sender.country)

    def receiver_location(self, obj):
        receiver = obj.receiver
        return "%s, %s, %s" % (receiver.city, receiver.state, receiver.country)

    list_display = [
        "user",
        "purchased_on",
        "receiver",
        "gift_name",
        "image",
        "amount",
        "sender_location",
        "receiver_location",
    ]
    search_fields = [
        "user__username",
        "user__email",
        "user__fullName",
        "receiver__username",
        "receiver__email",
        "receiver__fullName",
        "gift__type",
    ]

    sender_location.short_description = "Sender's Location"
    receiver_location.short_description = "Receiver's Location"

    class Media:
        js = ("admin/js/admin_paginator.js",)

    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop("list_per_page", [25])[0])
        self.list_per_page = page_param
        return super(GiftpurchaseAdmin, self).changelist_view(request, extra_context)

class RealGiftPriceForRegionInline(admin.TabularInline):
    model = RealGiftPriceForRegion
    extra = 0
    can_delete = False

class VirtualGiftPriceForRegionInline(admin.TabularInline):
    model = VirtualGiftPriceForRegion
    extra = 0
    can_delete = False

class VirtualGiftAdmin(ModelAdmin):
    def image(self, obj):
        return format_html(
            '<img src="/media/{}" width="auto" height="45px" />'.format(obj.picture)
        )

    list_display = ["gift_name", "cost", "image", "created_at", "status"]
    search_fields = ["gift_name", "cost", "allgift__type"]
    inlines = [
        VirtualGiftPriceForRegionInline
    ]

    class Media:
        js = ("admin/js/admin_paginator.js",)

    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop("list_per_page", [25])[0])
        self.list_per_page = page_param
        return super(VirtualGiftAdmin, self).changelist_view(request, extra_context)


class AllGiftsAdmin(ModelAdmin):
    class Media:
        js = ("admin/js/admin_paginator.js",)

    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop("list_per_page", [25])[0])
        self.list_per_page = page_param
        return super(AllGiftsAdmin, self).changelist_view(request, extra_context)


class RealGiftAdmin(ModelAdmin):
    def image(self, obj):
        return format_html(
            '<img src="/media/{}" width="auto" height="45px" />'.format(obj.picture)
        )

    list_display = ["gift_name", "cost", "image", "created_at", "status"]
    search_fields = ["gift_name", "cost", "allgift__type"]
    inlines = [
        RealGiftPriceForRegionInline
    ]


    class Media:
        js = ("admin/js/admin_paginator.js",)

    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop("list_per_page", [25])[0])
        self.list_per_page = page_param
        return super(RealGiftAdmin, self).changelist_view(request, extra_context)


admin.site.register(Giftpurchase, GiftpurchaseAdmin)
admin.site.register(GiftPurchaseMessageText)
admin.site.register(AllGifts, AllGiftsAdmin)
admin.site.register(RealGift, RealGiftAdmin)
admin.site.register(VirtualGift, VirtualGiftAdmin)
