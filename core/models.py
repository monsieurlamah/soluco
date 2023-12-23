from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


STATUS_CHOICE = (
    ('traitement', 'Traitement'),
    ('expedier', 'Expédié'),
    ('Livrer', 'Livré'),
)

STATUS = (
    ('brouillon', 'Brouillon'),
    ('desactiver', 'Désactivé'),
    ('rejeter', 'Rejeté'),
    ('en_revue', 'En revue'),
    ('publier', 'Publié'),
)

RATING = (
    (1, '★✩✩✩'),
    (2, '★★✩✩✩'),
    (3, '★★★✩✩'),
    (4, '★★★★✩'),
    (5, '★★★★★'),
)

def user_dictory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=150, verbose_name="Titre", default="Ciment")
    image = models.ImageField(upload_to="category", default="category.jpg")
    
    
    class Meta:
        verbose_name_plural = "Catégories"
    
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefgh12345")
    
    title = models.CharField(max_length=150, default="Bon founisseur", verbose_name="Titre")
    image = models.ImageField(upload_to=user_dictory_path, default="vendor.jpg")
    cover_image = models.ImageField(upload_to=user_dictory_path, default="vendor.jpg")
    # description = models.TextField(blank=True, null=True, default="Je suis un fournisseur incroyable")
    description = RichTextUploadingField(blank=True, null=True, default="Je suis un fournisseur incroyable")
    
    address = models.CharField(max_length=150, default="Conakry/Ratoma/Sonfonia",  verbose_name="Adresse")
    contact = models.CharField(max_length=150, default="+224 625 396 417")
    chat_resp_time = models.CharField(max_length=150,  default="100")
    shipping_on_time = models.CharField(max_length=150,  default="100")
    authentic_rating = models.CharField(max_length=150,  default="100")
    days_return = models.CharField(max_length=150,  default="100")
    warranty_period = models.CharField(max_length=150,  default="100")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Utilisateur")
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    
    class Meta:
        verbose_name_plural = "Fournisseurs"
    
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Tags(models.Model):
    pass

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefgh12345")
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Utilisateur")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Catégorie", related_name='category')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, verbose_name="Fournisseur", related_name="product")
    
    title = models.CharField(max_length=150, default="Cimaf", verbose_name="Titre")
    image = models.ImageField(upload_to=user_dictory_path, default="product.jpg")
    # description = models.TextField(blank=True, null=True, default="C'est le produit")
    description = RichTextUploadingField(blank=True, null=True, default="C'est le produit")
    
    price = models.IntegerField(default=0, verbose_name="Prix")
    old_price = models.IntegerField(default=0, verbose_name="Prix Promo")
    # specification = models.TextField(blank=True, null=True)
    specification = RichTextUploadingField(blank=True, null=True)
    type = models.CharField(max_length=150, null=True, blank=True, default="Construction")
    stock_account = models.CharField(max_length=100, default="8", null=True, blank=True, verbose_name="Compte de stock")
    life = models.CharField(max_length=100, default="100", null=True, blank=True, verbose_name="Vie")
    mfd = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    
    tags = TaggableManager(blank=True)
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    
    product_status = models.CharField(choices=STATUS, max_length=15, default="en_revue", verbose_name="Statut du produit")
    
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False, verbose_name="En vedette")
    digital = models.BooleanField(default=False)
    
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet="1234567890")
    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True)
    
    
    class Meta:
        verbose_name_plural = "Produits"
    
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price =  (self.price / self.old_price) * 100
        return new_price
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="p_images")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Images du produit"



#################################### Cart, Order, OrderItems And Address ##############################

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    price = models.IntegerField(default=0, verbose_name="Prix")
    paid_status = models.BooleanField(default=False, verbose_name="Statut du paiement")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de commande")
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=15, default="traitement", verbose_name="Statut du produit")
    
    class Meta:
        verbose_name_plural = "Panier de Commande"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, verbose_name="Commande")
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200, verbose_name="Article")
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0, verbose_name="Quantité")
    price = models.IntegerField(default=0, verbose_name="Prix")
    total = models.IntegerField(default=0, verbose_name="Total")
    
    class Meta:
        verbose_name_plural = "Panier de commande art"
        
    
    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' %(self.image))
    
    
#################################### Product Review, wishlist And Address #############################

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Utilisateur")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="product", verbose_name="review")
    review = models.TextField(verbose_name='Avis')
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Avis sur les produits"
        
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Utilisateur")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Produit")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Liste de voeux"
        
    def __str__(self):
        return self.product.title
    
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Utilisateur")
    mobile = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Adresse"
    
    

    

    
    
    
    