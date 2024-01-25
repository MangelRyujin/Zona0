from django.db import models
from apps.users.models import User
from apps.orders.models import TimeTransfer
# Create your models here. 
    
    
class Card(models.Model):
    """docstring for Card."""
    
    user = models.OneToOneField(User,on_delete=models.CASCADE, blank=False,null=False, unique=True)
    min_withdraw = models.DecimalField('Minimo diario a extraer',decimal_places=2, max_digits=11, default=0, null=False, blank=False)
    active = models.BooleanField('Tarjeta activa',default=True)
    
    
    class Meta:    
        verbose_name = 'Tarjeta OS'
        verbose_name_plural = 'Tarjetas OS'
        
        
    def __str__(self) -> str:
        return f'Tarjeta asignada al usuario {self.user.username}'
    
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
        verbose_name = 'Tarjeta OS'
        verbose_name_plural = 'Tarjetas OS'
        
        
    def __str__(self) -> str:
        return f'Tarjeta asignada al usuario {self.user.username}'
    
    def retired(self):
       self.state = 'Retired'
       self.active = 'False'
       self.save()
    