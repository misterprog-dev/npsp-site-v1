from django.db import models
import uuid
import random
import string 
import bcrypt

def password():
    return ''.join([random.choice(string.digits + string.ascii_letters) for i in range(0, 10)])

def get_hashed_password(pwd):
    return bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())

# Models Gestionnaire here.
class Gestionnaire(models.Model):
    nom = models.CharField(max_length=50, blank=True, help_text='Nom : ')
    prenom = models.CharField(max_length=50, blank=True, help_text='Prenom(s) : ')
    email = models.EmailField(max_length=50, help_text='Email : ', blank=False)
    contact = models.CharField(max_length=50, blank=True, help_text='Contact : ')
    mdp = password()
    password = models.CharField(max_length=50, default= mdp, help_text='Mot de passe definit')
    commune = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['email']
    
    def save(self, *args, **kwargs):
        if self.password:
            self.password = get_hashed_password(self.password)
        super(Gestionnaire, self).save(*args, **kwargs)

# Model type client
class TypeClient(models.Model):
    libelle = models.CharField(max_length=200, help_text='Type client : ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['libelle']
    
    def __str__(self):
        return self.libelle

#Adresse du client
# class Adresse(models.Model):
#     ville = models.CharField(max_length=255)
#     location = PlainLocationField(based_fields=['city'], zoom=19)

# Models Client here.
class Client(models.Model):
    nom = models.CharField(max_length=50, blank=True)
    prenom = models.CharField(max_length=50)
    type_client = models.ForeignKey('TypeClient',verbose_name=("libelle"), on_delete=models.CASCADE,)
    email = models.EmailField(unique=True)
    mdp = password()
    password = models.CharField(max_length=255, default=mdp, help_text='Mot de passe par defaut : '+mdp)
    contact = models.CharField(max_length=50, blank=True) 
    service_time = models.DecimalField(max_digits=4, decimal_places=2, default = 8.0)   
    ville = models.CharField(max_length=255, default = None)
    x = models.DecimalField(max_digits=40, decimal_places=33, default = None)
    y = models.DecimalField(max_digits=40, decimal_places=33, default = None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['email']
    
    def __str__(self):
        return str(self.id) + ' ' + self.nom + ' ' + self.prenom + ' ' + str(self.type_client) + ' ' + self.email + ' ' + self.contact + ' ' + self.ville + ' ' + str(self.y) + ' ' + str(self.x)
