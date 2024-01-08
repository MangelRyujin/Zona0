from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from utils.send_email.send_email import send_email_verify,sign_value
from utils.validates.validates import validate_digits,validate_alnum,validate_letters_and_spaces,validate_letters_numbers_and_spaces
from gdstorage.storage import GoogleDriveStorage

# Create your models here.
gd_storage = GoogleDriveStorage()




# class AvatarImageUser(models.Model):
#     image = models.ImageField(upload_to='avatar/', storage=gd_storage)

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using = self.db)
        # process send email verify
        token = sign_value(user.id)
        path = f"/accounts/verify/?token={token}"
        send_email_verify(user.email,path,token)
        return user
    
    def create_user(self, username, email, password = None, **extra_fields):
        return self._create_user(username, email, password, False , False ,**extra_fields)
    
    def create_superuser(self, username, email, password = None, **extra_fields):
        return self._create_user(username, email, password, True , True ,**extra_fields)
    



class User(AbstractBaseUser, PermissionsMixin):   
        
    
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('company', 'Company'),
        # Add other user types here
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='client') 
    username = models.CharField('Nombre de Usuario',validators=[MinLengthValidator(3),validate_alnum],max_length=50, unique=True,blank = False, null= False)
    email = models.EmailField('Correo Electrónico', max_length=50 , unique=True, blank = False, null= False)
    movil =models.CharField(validators=[MinLengthValidator(8),validate_digits], max_length=8, blank = False, null= False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    verified_email = models.BooleanField('Verificar email',default=False)
    zona_point=models.DecimalField('Puntos de Zona0', max_digits=10,default=0.00,  decimal_places=2, blank=True, null= True)
    objects = UserManager()
    name = models.CharField('Nombres', max_length=50,validators=[MinLengthValidator(3),validate_letters_and_spaces],blank=False, null=False)
    last_name = models.CharField('Apellidos',validators=[MinLengthValidator(3),validate_letters_and_spaces], max_length=50, blank=False, null=False)
    ci=models.CharField('Carnet de identidad',validators=[MinLengthValidator(11),validate_digits], max_length=11, unique=True,blank = False, null= False)
    image = models.ImageField(upload_to='avatar/', storage=gd_storage , null=True, blank=True)
    
    class Meta:    
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'movil','name','last_name','ci',]
    
    def natural_key(self):
        return (self.username)
    
    def __str__(self) -> str:
        return f'{self.username}'
    
    def verify_email(self):
        """
        Marks the user as verified and assigns all the resevations that may have
        been created anonymously.
        """
        
        self.verified_email = True
        self.save()

    def is_client(self):
        return self.user_type == 'client'

    def is_company(self):
        return self.user_type == 'company'
   
    def transfer_zop(self,cant):
       self.zona_point += cant
       self.save()
       
    def burn_zop(self,cant):
        if self.zona_point - cant > 0:
            self.zona_point -= cant
            self.save()
        else: raise ValidationError("La cantidad es mayor a su monto.")
            

class Client(User):
    
    class Meta:    
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        
    def __str__(self) -> str:
        return f'{self.name} {self.last_name}'
    

class Company(User):
    TYPE_CHOICES = [
        ('Mipyme', 'Mipyme'),
        ('TCP', 'TCP'),
        ('Estatal', 'Estatal'),
    ]
    company_name = models.CharField('Nombre de Enmpresa',validators=[MinLengthValidator(2),validate_letters_numbers_and_spaces],max_length=75, unique=True,blank = False, null= False)
    company_code = models.CharField('Codigo de la empresa',validators=[validate_digits], max_length=30, blank=False, null=False)
    type = models.CharField('Tipo de empresa',max_length=7 ,choices=TYPE_CHOICES, blank=False, null=False)
    correct_company = models.BooleanField(default=False)
    
    class Meta:    
        verbose_name = 'Compañia'
        verbose_name_plural = 'Compañias'
        
    def __str__(self) -> str:
        return f'{self.company_name}'


class Zona0Manager(User):
    total_recauder = models.DecimalField('Total de puntos de Zona0 vendidos', max_digits=10,  decimal_places=2,default=0, blank=True, null= True)
    total_burn = models.DecimalField('Total de puntos de Zona0 quemados', max_digits=10,  decimal_places=2,default=0, blank=True, null= True)
    
    class Meta:    
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'
        
    def __str__(self) -> str:
        return f'{self.username}.'
    
    def recauder_zop(self,cant):
       self.total_recauder += cant
       self.save()
    
    def burn_zop(self,cant):
       self.total_burn += cant
       self.save()
       
