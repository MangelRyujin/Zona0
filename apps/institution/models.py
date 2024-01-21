from django.db import models
from apps.users.models import User
from apps.orders.models import TimeTransfer
import uuid
from django.core.validators import MinLengthValidator
from gdstorage.storage import GoogleDriveStorage
from utils.validates.validates import validate_letters_numbers_and_spaces

gd_storage = GoogleDriveStorage()

# Create your models here. 
    
    
class Institution(models.Model):
    """docstring for Institution."""
    
    institution_name = models.CharField('Nombre de Enmpresa',validators=[MinLengthValidator(2),validate_letters_numbers_and_spaces],max_length=75, unique=True,blank = False, null= False)
    institution_osp = models.DecimalField('Donaciones en OSP',decimal_places=2, max_digits=11, default=0, null=False, blank=False)
    description = models.CharField('Descripción de la institución', validators=[validate_letters_numbers_and_spaces], max_length=500)
    image = models.ImageField(upload_to='avatar/', storage=gd_storage , null=True, blank=True)
    active = models.BooleanField(default=True)
    
    
    class Meta:    
        verbose_name = 'Institucion'
        verbose_name_plural = 'Instituciones'
        
    def __str__(self) -> str:
        return f'Institucion {self.institution_name}'
    
    def donation_osp(self,cant):
       self.institution_osp += cant
       self.save()
    
class Donation(TimeTransfer):
    """docstring for Donation."""
    
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=False,null=False)
    amount = models.DecimalField('Monto a donar',decimal_places=2, max_digits=11, default=0, null=False, blank=False)
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE, blank=False,null=False)
    
    
    class Meta:    
        verbose_name = 'Donacion'
        verbose_name_plural = 'Donaciones'
        
    def __str__(self) -> str:
        return f'Donacion realizada por el usuario {self.user} con un monto de {self.amount}  a la institucion {self.institution}'


class Gallery(models.Model):
    """docstring for Gallery."""
    
    institution = models.ForeignKey(Institution,related_name='galleryInstitution' ,on_delete=models.CASCADE, blank=False,null=False)
    image = models.ImageField(upload_to='avatar/', storage=gd_storage , null=True, blank=True)
    description = models.CharField('Descripción de la imagen', validators=[validate_letters_numbers_and_spaces], max_length=100)
    
    class Meta:    
        verbose_name = 'Galeria de institucion'
        verbose_name_plural = 'Galeria de instituciones'
        
    def __str__(self) -> str:
        return f'Imagen {self.id} de la institución {self.institution.institution_name}'
    