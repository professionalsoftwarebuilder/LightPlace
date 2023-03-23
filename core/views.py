from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm, CardCompileForm, ProfileForm, UserForm, OntvangerDataForm
from .models import Item, OrderItem, Order, \
    Address, Payment, Coupon, Refund, UserProfile, \
    Category, TextGenre, FotoSet, CardSession, Tekst, Ontvanger, Profile

import random
import string
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

from django.core.mail import send_mail, BadHeaderError


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def show_Categories(request):
    return render(request, "categories.html", {'categories': Category.objects.all()})


def Landing(request):
    return render(request, "landing.html", {})


def resultaat(request):
    if 'sesId' in request.session:
        sesId = request.session['sesId']
        theCardSession = CardSession.objects.filter(id=sesId).first()
        return render(request, 'card_result.html', {'theCardSession': theCardSession})

def CardAssembly(request, Id=0, ImgId=0, ontId=0):
    sesId = 0

    theCardSession = None

    if request.method == 'GET':
        if 'sesId' in request.session:
            sesId = request.session['sesId']
            print('sesionId read')
            print(sesId)

            theCardSession = CardSession.objects.filter(id=sesId).first()

            if theCardSession:
                if Id != 0:
                    selectedTekst = Tekst.objects.get(id=Id)
                    tekst_value = getattr(selectedTekst, 'tks_TheText')
                    theCardSession.csn_CardTextUser = tekst_value
                    theCardSession.save()

                if ImgId != 0:
                    selectedImg = Item.objects.get(id=ImgId)
                    theCardSession.csn_CardImage = selectedImg
                    #theCardSession.csn_CardImage_id = ImgId
                    theCardSession.save()
                    request.session['ImgId'] = ImgId
                    print('xxxxxxxxxxxxxxx')

                if ontId != 0:
                    print('In ontId')
                    selectedRecp = Ontvanger.objects.get(id=ontId)
                    theCardSession.csn_TheResipient = selectedRecp
                    # theCardSession.csn_CardImage_id = ImgId
                    theCardSession.save()
                    #request.session['ImgId'] = ImgId
                    print('recp added to card')
            else:
                theCardSession = CardSession.objects.create()
                sesId = theCardSession.id
                request.session['sesId'] = sesId
        else:
            theCardSession = CardSession.objects.create()
            sesId = theCardSession.id
            request.session['sesId'] = sesId
            print('new sesionId')
            print(sesId)

        form = CardCompileForm(instance=theCardSession)
        # if form.is_valid():
        #     form.save(commit=True)
        #     print('yyyyyyyyyyyyyyyy')
        return render(request, 'cardcompile.html', {'form': form, 'theCardSession': theCardSession})
    else:
        sesId = request.session['sesId']
        print('post: sesionId read')
        print(sesId)
        theCardSession = CardSession.objects.get(id=sesId)
        form = CardCompileForm(request.POST, instance=theCardSession)

        if form.is_valid():
            crdSes = form.save(commit=False)
            # if 'ImgId' in request.session:
            #     ImgId = request.session['ImgId']
            #     crdSes.csn_CardImage = Item.objects.get(id=ImgId)
            crdSes.save()
        return render(request, 'cardcompile.html', {'form': form, 'theCardSession': theCardSession})


def Products_Home(request):
    context = {
        'object_list': Item.objects.filter(itm_Is_Frontpage=True),
        'thecategories': Category.objects.all()
    }
    return render(request, "home.html", context)


def Products_ByCat(request, cat_id):
    lcatg = Category.objects.get(id=cat_id)
    objec_list = lcatg.item_set.all()
    
    context = {
        'object_list': objec_list,
        'thecategories': Category.objects.all()
    }
    return render(request, "home.html", context)


def Products_AllDesc(request, cat_id):
    lcatg = Category.objects.get(id=cat_id)
    
    # Category.objects.get(pk=2).get_descendants(include_self=True)
    objec_list = Item.objects.filter(itm_Categories__in=Category.objects.get(id=cat_id).get_descendants(include_self=True))
    
    context = {
        'object_list': objec_list,
        'thecategories': Category.objects.all()
    }
    return render(request, "home.html", context)

def ItemDetailView(request, slug):
    product = Item.objects.get(slug=slug)
    product.fotoset_set.select_related('itm_Fk_Item_id')

    # for fotogallery
    if product.fotoset_set.count() > 0:
      colWidth = 12 // product.fotoset_set.count()
    else:
      colWidth = 12

    context = {
        'object': product,
        'thecategories': Category.objects.all(),
        'colWidth': colWidth
    }
    return render(request, "product.html", context)


# class ItemDetailView(DetailView):
#     model = Item
#     template_name = "product.html"

#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in a QuerySet of all the books
#         theCategories = Category.objects.all()
#         context['foto_list'] = FotoSet.objects.all()

#         return context


class HomeView(ListView):
    model = Item
    context_object_name = 'object_list'
    queryset = Item.objects.all()
    paginate_by = 4
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet
        theCategories = Category.objects.all()
        context = {
            'thecategories': theCategories
        }

        return context


def startNewCard(request):
    if request.user.is_authenticated:
        form = ProfileForm(instance=request.user.profile)
        user = request.user
        context = {
            'theUser': user,
            'form': form,
        }
        return render(request, "afzendergeg.html", context)
    else:
        return render(request, 'startnewcard.html', {})

def login_creator(request):
    if request.method == 'GET':
        return render(request, "logincreator.html", {})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Maak nieuwe kaartsessie aan
            nwKaarSes = CardSession.objects.create(csn_SenderNm=user.profile.prf_Naam)
            request.session['sesId'] = nwKaarSes.id
            form = ProfileForm(instance=user.profile)
            context = {
                'theUser': user,
                'form': form,
            }
            return render(request, "afzendergeg.html", context)
            ...
        else:
            # Return an 'invalid login' error message.
            ...


def afzendergeg(request):
    if request.method == 'POST':
        #form = UserDataForm(request.POST)
        if request.user.is_active:
            userId = request.user.id
            user = User.objects.get(id=userId)
            form = ProfileForm(request.POST, instance=user.profile)

            # check whether it's valid:
            if form.is_valid():
                print('is valid', userId)
                form.save(commit=True)

            context = {
                'theUser': user,
                'form': form,
            }
            return render(request, "afzendergeg.html", context)


def ontvangergegy(request, Id=0, usrId=0):
    if request.method == 'GET':
        if Id != 0:
            print('vvvvvvv')
            ontv = Ontvanger.objects.get(id=Id)
            form = OntvangerDataForm(instance=ontv)
        else:
            if usrId != 0:
                print('userId: ' + str(usrId))
                profiel = Profile.objects.get(prf_User_id=usrId)
                ontv = Ontvanger.objects.create(ont_User_id=profiel.id)
                form = OntvangerDataForm(instance=ontv)
                Id = ontv.id
                print('de id is: ', Id)
            else:
                form = OntvangerDataForm()

        context = {
            'form': form,
            'ontId': Id,
            'usrId': usrId,
        }
        print('ddddddddddd')
        return render(request, "ontvangergeg.html", context)
    else:
        if Id != 0:
            print('de id is: ', Id)
            print('vvvvvvv')
            ontv = Ontvanger.objects.get(id=Id)
            form = OntvangerDataForm(request.POST, instance=ontv)
            form.save(commit=True)
            usrId = ontv.ont_User.id
            print('committed')
        else:
            if usrId != 0:
                print('bbbbb')
                ontv = Ontvanger.objects.create(ont_User_id=usrId)
                form = OntvangerDataForm(instance=ontv)
                Id = ontv.id
                print('de id is: ', Id)
            else:
                form = OntvangerDataForm(request.POST)

        context = {
            'form': form,
            'ontId': Id,
             'usrId': usrId,
        }
        return render(request, "ontvangergeg.html", context)


class ontvanger_lst(ListView):

    template_name = 'ontvanger_lst.html'
    model = Ontvanger
    paginate_by = 8  # if pagination is desired

    def get_queryset(self):
        profile = Profile.objects.get(prf_User=self.request.user)
        #return Ontvanger.objects.filter(ont_User_id=self.kwargs['usrId'])
        return Ontvanger.objects.filter(ont_User=profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usrId'] = self.request.user.id
        print(self.request.user.id)
        return context




def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


def selTekst(request):
    tekstRecs = Tekst.objects.all()
    context = {'tekstRecs': tekstRecs,
               'tekstGenres': TextGenre.objects.all()
               }
    return render(request, "seltekst.html", context)


def Texts_AllDesc(request, cat_id):
    lcatg = TextGenre.objects.get(id=cat_id)

    # Category.objects.get(pk=2).get_descendants(include_self=True)
    objec_list = Tekst.objects.filter(
        tks_Genres__in=TextGenre.objects.get(id=cat_id).get_descendants(include_self=True))

    context = {
        'tekstRecs': objec_list,
        'tekstGenres': TextGenre.objects.all()
    }
    return render(request, "seltekst.html", context)


def Texts_ByCat(request, cat_id):
    lcatg = TextGenre.objects.get(id=cat_id)
    objec_list = lcatg.tekst_set.all()

    context = {
        'tekstRecs': objec_list,
        'tekstGenres': TextGenre.objects.all()
    }
    return render(request, "seltekst.html", context)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request-refund")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")





class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                # fetch the users card list
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({
                        'card': card_list[0]
                    })
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total() * 100)

            try:

                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        source=token
                    )

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()

                # assign the payment to the order

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                order.ref_code = create_ref_code()
                order.save()

                messages.success(self.request, "Your order was successful!")
                return redirect("/")

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed.")
                return redirect("/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")


def sendTheMail(request, cdsId=0):
    theCardSes = CardSession.objects.get(id=cdsId)
    subject = 'Een kaartje voor: ' + theCardSes.csn_TheResipient.ont_Naam
    message = theCardSes.csn_CardTextUser
    from_email = 'kaart@light-place.nl'
    #from_email = 'professionalsoftwarebuilders@gmail.com'
    to_email = theCardSes.csn_TheResipient.ont_Email
    Result = ''
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, [to_email])
        except BadHeaderError:
            Result = 'Invalid header found'
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        Result = 'Make sure all fields are entered and valid'

    context = {'theCardSes': theCardSes, 'Result': Result}
    return render(request, 'contact/sendthemail.html', context)


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('core:cardSession_Insert')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })