from django.db import models
from apps.users.models import User
from apps.orders.models import TimeTransfer
# Create your models here. 
    
    
class Banking(TimeTransfer):
    """docstring for Institution."""
    STATE_CHOICES = (
        ('Banked', 'Banked'),
        ('Retired', 'Retired'),
        # Add other user types here
    )

    state = models.CharField('Estado de la bancarización',max_length=10, choices=STATE_CHOICES, default='Banked') 
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=False,null=False)
    amount = models.DecimalField('Monto inicial de OSP',decimal_places=2, max_digits=11, default=0, null=False, blank=False)
    
    
    class Meta:    
        verbose_name = 'Bancarización'
        verbose_name_plural = 'Bancarizaciones'
        
    REQUIRED_FIELDS = ['amount']
        
    def __str__(self) -> str:
        return f'Bancarización efectuada por {self.user.username} con un monto de {self.amount}'
    
    def retired(self,cant):
       self.state = 'Retired'
       self.active = 'False'
       self.save()
    