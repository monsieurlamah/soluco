from django.db import models
import uuid
from userauths.models import User
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_save

Account_STATUS = (
    ('actif','Actif'),
    ('en-attente','En attente'),
    ('inactif','Inactif'),
)

MARITAL_STATUS = (
    ("marier", "Marié(e)"),
    ("celibataire", "Célibataire"),
    # ("autre", "Autre"),
)

GENDER = (
    ("masculin", "Masculin"),
    ("feminin", "Feminin"),
    # ("autre", "Autre"),
)

# NATIONALITY = (
#     ("guineenne", "Guinéenne"),
#     ("senegalaise", "Sénégalaise"),
#     ("ivoirienne", "Ivoirienne")
# )

IDENTITY_TYPE = (
    ("carte_didentite_nationale", "Carte d'identité nationale"),
    ("permis_de_conduire", "Permis de conduire"),
    ("passeport_international", "Passeport international"),
)



def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s_%s" % (instance.id, ext)
    return "user_{0}/{1}".format(instance.user.id, filename)

class Account(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name = "Utilisateur")
    # account_balance = models.IntegerField(default=0000) #123 345 789 102
    account_number = ShortUUIDField(unique=True, length=10, max_length=25, prefix="127", alphabet="1234567890", verbose_name="Numéro de compte") #2175893745837
    account_id = ShortUUIDField(unique=True, length=7, max_length=25, prefix="kf", alphabet="1234567890", verbose_name="Identifiant de compte") #2175893745837
    pin_number = ShortUUIDField(unique=True, length=4, max_length=7, alphabet="1234567890", verbose_name="Code PIN") #2737
    ref_code = ShortUUIDField(unique=True, length=10, max_length=25, alphabet="abcdefgh1234567890", verbose_name="code de référence") #2737
    account_status = models.CharField(max_length=150, choices=Account_STATUS, default="inactif", verbose_name="Statut du compte")
    date = models.DateTimeField(auto_now_add=True)
    kyc_submitted = models.BooleanField(default=False)
    kyc_confirmed = models.BooleanField(default=False)
    recommended_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="recommended_by", verbose_name="Recommandé par")
    
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural="Comptes"
    
    def __str__(self):
        return f"{self.user}"
    
class ClientTerrain(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Compte")
    full_name = models.CharField(max_length=200, verbose_name="Nom complet")
    image = models.ImageField(upload_to="clientTerrain", default="default.jpg")
    marrital_status = models.CharField(max_length=100, choices=MARITAL_STATUS, verbose_name="Situation Matrimoniale")
    gender = models.CharField(max_length=100, choices=GENDER, verbose_name="Genre")
    identity_type = models.CharField(max_length=150, choices=IDENTITY_TYPE, verbose_name="Type d'identité")
    identity_image = models.ImageField(upload_to="clientTerrain", blank=True, null=True, verbose_name="Identité image")
    date_of_birth = models.DateTimeField(auto_now_add=False, verbose_name="Date de naissance")
    signature = models.ImageField(upload_to="clientTerrain")
    
    # Address
    country = models.CharField(max_length=100, verbose_name = "Pays")
    state = models.CharField(max_length=100, verbose_name="État")
    city = models.CharField(max_length=100, verbose_name="Ville")
    
    #Contact Detail
    mobile = models.CharField(max_length=100, verbose_name="Téléphone")
    fax = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}"
    

class ClientContruction(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Compte")
    full_name = models.CharField(max_length=200, verbose_name="Nom complet")
    image = models.ImageField(upload_to="clientConstruction", default="default.jpg")
    marrital_status = models.CharField(max_length=100, choices=MARITAL_STATUS, verbose_name="Situation Matrimoniale")
    gender = models.CharField(max_length=100, choices=GENDER, verbose_name="Genre")
    identity_type = models.CharField(max_length=150, choices=IDENTITY_TYPE, verbose_name="Type d'identité")
    identity_image = models.ImageField(upload_to="clientConstruction", blank=True, null=True, verbose_name="Identité image")
    date_of_birth = models.DateTimeField(auto_now_add=False, verbose_name="Date de naissance")
    signature = models.ImageField(upload_to="clientConstruction")
    documents = models.ImageField(upload_to="clientConstruction")
    
    # Address
    country = models.CharField(max_length=100, verbose_name = "Pays")
    state = models.CharField(max_length=100, verbose_name="État")
    city = models.CharField(max_length=100, verbose_name="Ville")
    
    #Contact Detail
    mobile = models.CharField(max_length=100, verbose_name="Téléphone")
    fax = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}"
    
    
    
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
        
def save_account(sender, instance, **kwargs):
    instance.account.save()
    
post_save.connect(create_account, sender=User)
post_save.connect(save_account, sender=User)