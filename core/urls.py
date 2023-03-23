from django.urls import path, include
from .views import (
    CheckoutView,
    ItemDetailView,
    HomeView,
    Products_Home,
    Products_ByCat,
    Products_AllDesc,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    Landing,
    CardAssembly,
    show_Categories,
    selTekst,
    Texts_ByCat,
    login_creator,
    startNewCard,
    afzendergeg,
    ontvangergegy,
    ontvanger_lst,
    resultaat,
    sendTheMail,
    Texts_AllDesc, update_profile
)

app_name = 'core'

urlpatterns = [
    path('', Landing, name='home'),
    path('cardcompile/', CardAssembly, name='cardSession_Insert'),
    path('cardcompile/<int:Id>/', CardAssembly, name='cardSession_Update'),
    path('cardcompile/0/<int:ImgId>/', CardAssembly, name='cardSession_Card'),
    path('cardcompile/0/0/<int:ontId>/', CardAssembly, name='cardSession_Recp'),

    path('startnewcard/', startNewCard, name='startNewCard'),
    path('logincreator/', login_creator, name='login_creator'),
    path('afzendergeg/', afzendergeg, name='afzendergeg'),
    path('upd_afzendergeg/', update_profile, name='update_profile'),
    path('ontvangergeg/<int:Id>', ontvangergegy, name='ontvangergeg'),
    path('ontvangergeg/<int:Id>/<int:usrId>', ontvangergegy, name='ontvangernew'),
    #path('ontvangergeg/<int:Id>/', ontvangergegy, name='ontvangersgegx'),
    path('ontvangernew/', ontvangergegy, name='ontvangernew'),
    path('ontvangerlijst/', ontvanger_lst.as_view(), name='ontvangerlijst'),

    path('resultaat/', resultaat, name='resultaat'),

    path('products/', Products_Home, name='products'),
    path('products_bycat/<cat_id>/', Products_ByCat, name='prod_Cat'),
    path('products_alldesc/<cat_id>/', Products_AllDesc, name='prod_Desc'),

    path('product/<slug>/', ItemDetailView, name='product'),

    path('sel-tekst', selTekst, name='selTekst'),
    path('texts_bycat/<cat_id>/', Texts_ByCat, name='text_Cat'),
    path('texts_alldesc/<cat_id>/', Texts_AllDesc, name='text_Desc'),

    path('sendTheMail/<int:cdsId>', sendTheMail, name='sendTheMail'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),


]
