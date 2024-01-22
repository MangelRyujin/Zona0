from django.db import models
import uuid
from apps.orders.models import TimeTransfer
from django.core.validators import MinValueValidator,MinLengthValidator
from utils.validates.validates import validate_letters_numbers_and_spaces
import random
# Create your models here.


class MarketingApplican(TimeTransfer):
    """docstring for MarketingApplican."""
    
    place = models.CharField('A quién se vendio',validators=[MinLengthValidator(2),validate_letters_numbers_and_spaces],max_length=100, blank=False,null=False)
    prize_fund = models.DecimalField('Fondo de premio',decimal_places=2, max_digits=11,validators=[MinValueValidator(1)],default=0, null=False, blank=False)
    winners = models.PositiveIntegerField('Cantidad de premiados',validators=[MinValueValidator(1)] ,default=0,null=False, blank=False)
    cant_codes = models.PositiveIntegerField('Cantidad de codigos',validators=[MinValueValidator(1)] ,default=0,null=False, blank=False)
    
    class Meta:    
        verbose_name = 'Solicitante de marketing'
        verbose_name_plural = 'Solicitantes de marketing'
        
    def __str__(self) -> str:
        return f'{self.place} solicitó {self.prize_fund} OSP de premio, con una cantidad de {self.winners} ganadores'
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        codes = random.sample(range(self.cant_codes), self.winners)
        for i in range(self.cant_codes): 
            if i in codes:
                prize_fund_value = self.prize_fund/self.winners
            else:
                prize_fund_value = 0    
            Code.objects.create(marketingApplican=self, prize_fund=prize_fund_value)
    
        
class Code(models.Model):
    """docstring for Code."""
    marketingApplican = models.ForeignKey(MarketingApplican,related_name='marketingApplican',on_delete=models.CASCADE, blank=False,null=False)
    prize_fund = models.DecimalField('Premio',decimal_places=2, max_digits=11, default=0, null=True, blank=True)
    code = models.UUIDField(default=uuid.uuid4, editable=False, null=False, blank=False)
    redeem = models.BooleanField('Canjeado',default=False)
    
    
    class Meta:    
        verbose_name = 'Código'
        verbose_name_plural = 'Códigos'
        
    def __str__(self) -> str:
        return f'{self.marketingApplican}. Código {self.code} con valor de {self.prize_fund}'