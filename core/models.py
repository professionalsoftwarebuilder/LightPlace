from django_extensions.db.fields import AutoSlugField
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum

from django.shortcuts import reverse
from django_countries.fields import CountryField
# from django.db.models.constraints import UniqueConstraint

from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from .fields import ImageThumbsField

from ckeditor.fields import RichTextField

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

RECIPIENT_CHANNEL = (
    ('E', 'E-Mail'),
    ('W', 'WhatsApp')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

SIZES = (
    {'code':'thumb','wxh':'100x72','resize':'crop'},
    {'code':'galry','wxh':'250x180','resize':'crop'},
    {'code':'detail','wxh':'800x576'},
)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Category(MPTTModel):
    ctg_Title = models.CharField(max_length=85, unique=True)
    ctg_Name_Long = models.TextField(blank=True, null=True)
    ctg_Slug = AutoSlugField(populate_from=('ctg_Title',))
    parent = TreeForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0)
    lft = models.PositiveIntegerField(default=0)
    rght = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=0)
    tree_id = models.PositiveIntegerField(default=0)

    class MPTTMeta:
        order_insertion_by = ['ctg_Title']

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.ctg_Title

class TextGenre(MPTTModel):
    tgn_Title = models.CharField(max_length=85, unique=True)
    tgn_Name_Long = models.TextField(blank=True, null=True)
    tgn_Slug = AutoSlugField(populate_from=('tgn_Title',))
    parent = TreeForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0)
    lft = models.PositiveIntegerField(default=0)
    rght = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=0)
    tree_id = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'textgenres'

    def __str__(self):
        return self.tgn_Title


class Tekst(models.Model):
    tks_Title = models.CharField(max_length=85, unique=True)
    tks_Name_Long = models.TextField(blank=True, null=True)
    tks_TheText = RichTextField(blank=True, null=True)
    tks_Slug = AutoSlugField(populate_from=('tks_Title',))
    tks_Genres = models.ManyToManyField(TextGenre)

    class Meta:
        verbose_name_plural = 'teksten'

    def __str__(self):
        return self.tks_Title


class ImageGenre(MPTTModel):
    ign_Title = models.CharField(max_length=85, unique=True)
    ign_Name_Long = models.TextField(blank=True, null=True)
    ign_Slug = AutoSlugField(populate_from=('ign_Title',))
    parent = TreeForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0)
    lft = models.PositiveIntegerField(default=0)
    rght = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=0)
    tree_id = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'imagegenres'

    def __str__(self):
        return self.ign_Title


class Brand(models.Model):
    brd_Name = models.CharField(max_length=85)
    brd_Name_Long = models.CharField(max_length=250, blank=True, null=True)
    brd_Ctrl = models.CharField(max_length=30, blank=True, null=True)
    brd_Is_Show = models.BooleanField(default=True)
    brd_ImagePath = models.ImageField(max_length=250, blank=True, null=True)
    brd_Descr = models.TextField(blank=True, null=True)
    brd_IndexNr = models.IntegerField(default=0)

    def __str__(self):
        return self.brd_Name


class Item(models.Model):
    title = models.CharField(max_length=100)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = AutoSlugField(populate_from=('title'))
    itm_Categories = models.ManyToManyField(Category)
    description = models.TextField(blank=True, default='', verbose_name='Omschrijving')
    image = ImageThumbsField(max_length=250, blank=True, null=True, sizes=SIZES)
    itm_KeyWords = models.TextField(blank=True, default='', verbose_name='Sleutelwoorden', help_text='Woorden waarmee zoekopdrachten worden vergemakkelijkt')
    itm_Name_Long = models.CharField(max_length=250, default='', blank=True)
    itm_Pitch = models.TextField(
        blank=True, default='', verbose_name='Pitch', help_text='Verkoop pitch bij dit artikel')
    itm_IndexNr = models.IntegerField(blank=True, default=0)
    itm_Ctrl = models.CharField(max_length=30, blank=True, default='')
    itm_Is_Show = models.BooleanField(blank=True, default=True)
    itm_Is_Frontpage = models.BooleanField(blank=True, default=True, verbose_name='Featured')
    itm_Is_Sale = models.BooleanField(blank=True, default=True)
    itm_Is_Newasset = models.BooleanField(blank=True, default=True)
    itm_Brand_id = models.ForeignKey(
        Brand, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Afbeelding'
        verbose_name_plural = 'Afbeeldingen'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class FotoSet(models.Model):
    fst_Title = models.CharField(
        default='', max_length=100, verbose_name='Titel')
    fst_Name_Plural = models.CharField(
        default='', max_length=100, blank=True, verbose_name='Meervoudsnaam', help_text='Om event te gebruiken in text genarator')
    itm_Fk_Item_id = models.ForeignKey(
        Item, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Bij artikel', help_text='Artikel waarbij deze foto hoort')
    fst_Slug = AutoSlugField(populate_from=(
        'fst_Title'), editable=False, verbose_name='Slug code', help_text='Speciale itemcode, dit veld niet aanpassen')
    fst_Description = models.TextField(
        blank=True, default='', verbose_name='Omschrijving')
    fst_Is_Feature = models.BooleanField(default=False, blank=True, verbose_name='Is hoofdfoto', help_text='Gebruik deze foto in de catalogus')
    fst_Is_Show = models.BooleanField(blank=True, default=True, verbose_name='Tonen', help_text='Foto al dan niet tonen in de fotoset')
    fst_Image = models.ImageField(
        max_length=250, blank=True, null=True, verbose_name='Afbeelding')
    fst_Name_Long = models.CharField(
        max_length=250, blank=True, default='', verbose_name='Naam uitgebreid')
    fst_IndexNr = models.IntegerField(
        blank=True, default=0, verbose_name='Volgnummer')
    fst_Ctrl = models.CharField(max_length=30, default='', blank=True, verbose_name='Beheercodes',
                                help_text='Dit veld alleen door de administrator te gebruiken')

    class Meta:
        verbose_name_plural = 'FotoSets'

    def __str__(self):
        return self.fst_Title


class Type(models.Model):
    ty_Nm = models.CharField(max_length=85, blank=True, null=True)
    ty_Descr = models.CharField(max_length=85, blank=True, null=True)
    ty_Ctrl = models.CharField(max_length=30, blank=True, null=True)
    ty_Is_active = models.BooleanField(default=True)


class Type_Item(models.Model):
    ti_Nm = models.CharField(max_length=85, blank=True, null=True)
    ti_TextVal = models.CharField(max_length=85, default='text value')
    ti_Ctrl = models.CharField(max_length=30, blank=True, null=True)
    ti_Is_active = models.BooleanField(default=True)
    ti_Type = models.ForeignKey(Type, on_delete=models.CASCADE)
    ti_Descr = models.CharField(max_length=85, blank=True, null=True)


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

#import chatApp.models as chAM

class Profile(models.Model):
    prf_User = models.OneToOneField(User, on_delete=models.CASCADE)
    prf_Email = models.CharField('E-mail', max_length=125, blank=True, default='')
    prf_Mobiel = models.CharField('Mobile nr', max_length=12, blank=True, default='')
    prf_Naam = models.CharField('Default Afzender naam', max_length=125, default='Jan Jansen')
    prf_bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    prf_ActiveChat = models.IntegerField( 'Active chat', blank=True, null=True)
    prf_ProfileImg = models.ImageField(
        max_length=250, blank=True, null=True, verbose_name='Profile image')

    def __str__(self):
        return self.prf_User.username


class Ontvanger(models.Model):
    ont_Naam = models.CharField('Ontvanger naam', max_length=125, default='',)
    ont_Email = models.CharField('E-mail', max_length=125, blank=True, default='')
    ont_Mobiel = models.CharField('Mobile nr', max_length=12, blank=True, default='')
    ont_User = models.ForeignKey(Profile, verbose_name='Bij Gebruiker', on_delete=models.PROTECT)

    def __str__(self):
        return self.ont_Naam


class CardSession(models.Model):
    cns_User = models.ForeignKey(Profile, on_delete=models.PROTECT, default=1, verbose_name='Gebruiker' )
    csn_Title = models.CharField(
        blank=True, default='', max_length=140, verbose_name='Title'
    )
    csn_CardImage = models.ForeignKey(
        Item, on_delete=models.CASCADE, blank=True, null=True
    )
    csn_CardTekst = models.ForeignKey(
        Tekst, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Standaard tekst',
        help_text='Kies een standaard tekst die u eventueel kunt aanvullen', related_name='cardTekst'
    )
    csn_CardTextUser = RichTextField(
        blank=True, default='', verbose_name='UserText',
        help_text='Type hier de tekst die u wilt verzenden (u kunt ook een tekst kiezen en die hier aanpassen)'
    )
    csn_TheResipient = models.ForeignKey(
        Ontvanger, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Ontvangers',
        help_text='Kies een ontvanger')
    csn_SenderNm = models.CharField(
        blank=True, default='', max_length=85, verbose_name='Afzender naam',
        help_text='Omdat die vaak vergeten wordt!'
    )
    csn_ResipientChannel = models.CharField(
        choices=RECIPIENT_CHANNEL, blank=True, null=True, max_length=1, verbose_name='Ontvanger kanaal',
        help_text = 'Via E-mail, Facebook, Sms of via WhatsApp'
    )
    csn_DatTijdVerzonden = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.pk}"


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(prf_User=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

