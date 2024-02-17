from django.db import models
from apps.users.models import User
from apps.orders.models import TimeTransfer
from django.core.validators import MinLengthValidator
import uuid
import random
import string
# Create your models here. 
    
    
class Card(models.Model):
    """docstring for Card."""
    
    user = models.OneToOneField(User,on_delete=models.CASCADE, blank=False,null=False, unique=True)
    pin = models.UUIDField(default=uuid.uuid4, editable=False, null=False, blank=False)
    min_withdraw = models.DecimalField('Minimo diario a extraer',decimal_places=2, max_digits=11, default=0, null=False, blank=False)
    active = models.BooleanField('Tarjeta activa',default=True)
    on_hold = models.BooleanField('En espera',default=False)
    discount_code = models.CharField('Código de descuento', default='0A1A2A',validators=[MinLengthValidator(6)],max_length=6,blank = False, null= False)
    
    class Meta:    
        verbose_name = 'Tarjeta OS'
        verbose_name_plural = 'Tarjetas OS'
    
    def save(self, *args, **kwargs):
        caracters = string.ascii_letters + string.digits
        length = random.randint(6, 6)   # Generate random length of string
        chain = ''.join(random.choice(caracters) for _ in range(length)) #   Generate the random string
        self.discount_code = chain
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f'Tarjeta asignada al usuario {self.user.username} pin: {self.pin}'
    
    def desactive(self):
       self.active = 'False'
       self.save()
       
    def modified_min_withdraw(self,cant):
        if cant >= 0:
            self.min_withdraw = cant
            self.save()
        else:
            pass
        
       
class DiscountCard(TimeTransfer):
    """docstring for DiscountCard."""
    card = models.ForeignKey(Card,on_delete=models.CASCADE, blank=False,null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=False,null=False)
    amount = models.DecimalField('Descuento de OSP',decimal_places=2, max_digits=11, default=0, null=False, blank=False)
    
    
    class Meta:    
        verbose_name = 'Descuento Tarjeta OS'
        verbose_name_plural = 'Descuentos Tarjetas OS'
        
        
    def __str__(self) -> str:
        return f'Descuento de {self.user.username} a la tarjeta del usuario {self.card.user.username} de {self.amount} OSP'
    
    def retired(self):
       self.state = 'Retired'
       self.active = 'False'
       self.save()
    