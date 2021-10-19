from django.contrib import admin
# from django.contrib.admin import AdminSite

from .models import \
    Item, \
    OrderItem, \
    Order,     \
    Payment,   \
    Coupon,    \
    Refund, \
    Address,    \
    UserProfile, \
    Profile,  \
    Category, \
    Brand, \
    FotoSet, \
    Tekst, \
    ImageGenre, \
    TextGenre, \
    Ontvanger, \
    CardSession


# class TheAdminSite(AdminSite):
#     site_header = 'Dress your dreams administratie'


# admin_site = TheAdminSite(name='admin')


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'refund_requested',
                    'refund_granted',
                    'shipping_address',
                    'billing_address',
                    'payment',
                    'coupon'
                    ]
    list_display_links = [
        'user',
        'shipping_address',
        'billing_address',
        'payment',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'user__username',
        'ref_code'
    ]
    actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


class FotoSetInline(admin.TabularInline):
    model = FotoSet


class ItemAdmin(admin.ModelAdmin):
    inlines = [
        FotoSetInline,
    ]


admin.site.register(Item, ItemAdmin)
#admin.site.register(OrderItem)
#admin.site.register(Order, OrderAdmin)
#admin.site.register(Payment)
#admin.site.register(Coupon)
#admin.site.register(Refund)
#admin.site.register(Address, AddressAdmin)
#admin.site.register(UserProfile)
admin.site.register(Profile)
admin.site.register(Category)
#admin.site.register(FotoSet)
#admin.site.register(Brand)
admin.site.register(Tekst)
admin.site.register(TextGenre)
admin.site.register(ImageGenre)
admin.site.register(Ontvanger)
admin.site.register(CardSession)
