from django.db import models
from apps.users.models import User,Zona0Manager

# Create your models here.

class TimeStampMixin(models.Model):
    
    date = models.DateField('Fecha deefectuada la transferencia', auto_now_add=True, null=True)
    time = models.TimeField('Hora de efectuada la transferencia', auto_now_add=True, null=True)
    cant_zona_point=models.DecimalField('Puntos de Zona0 transferidos', max_digits=10,  decimal_places=2, blank=False, null= False)
    email = models.EmailField('Correo Electrónico del usuario al que se le transfirió', max_length=50 , unique=False, blank = False, null= False) 
    
    """docstring for ClassName."""
    class Meta:
        abstract = True
    

class TransferOrderUsers(TimeStampMixin):
    """docstring for TransferOrderUsers."""
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=False,null=False)

    class Meta:    
        verbose_name = 'Transferencia de usuario'
        verbose_name_plural = 'Transferencias de usuarios'
        
    def __str__(self) -> str:
        return f'Transferencia del usuario {self.user} de {self.cant_zona_point} ZOP a la cuenta de {self.email}'
    
    
class TransferManagerOrderUsers(TimeStampMixin):
    """docstring for TransferManagerOrderUsers."""
    TYPE_CHOICES = [
        ('Transferencia', 'Transferencia'),
        ('Quema', 'Quema')
    ]
    user_manager = models.ForeignKey(Zona0Manager,on_delete=models.CASCADE, blank=False,null=False)
    type = models.CharField('Tipo de orden',max_length=13,default='Transferencia' ,choices=TYPE_CHOICES, blank=False, null=False)
    
    
    class Meta:    
        verbose_name = 'Recarga a usuario'
        verbose_name_plural = 'Recargas a usuarios'
        
    def __str__(self) -> str:
        return f'{self.type} del manager {self.user_manager} de {self.cant_zona_point} ZOP a la cuenta de {self.email}'
    
    
    