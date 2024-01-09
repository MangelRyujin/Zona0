from django.db import models
from apps.users.models import User,Zona0Manager
import uuid
from gdstorage.storage import GoogleDriveStorage
gd_storage = GoogleDriveStorage()
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw 

# Create your models here.

class TimeStampMixin(models.Model):
    
    date = models.DateField('Fecha de efectuada la transferencia', auto_now_add=True, null=True)
    time = models.TimeField('Hora de efectuada la transferencia', auto_now_add=True, null=True)
    cant_zona_point=models.DecimalField('Puntos de Zona0 transferidos', max_digits=10,  decimal_places=2, blank=False, null= False)
    email = models.EmailField('Correo Electrónico del usuario al que se le transfirió', max_length=50 , unique=False, blank = False, null= False) 
    
    """docstring for ClassName."""
    class Meta:
        abstract = True
    
    
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
    
    
class TimeTransfer(models.Model):
    
    date = models.DateField('Fecha de efectuada la transferencia', auto_now_add=True, null=True)
    time = models.TimeField('Hora de efectuada la transferencia', auto_now_add=True, null=True)
    
    """docstring for ClassName."""
    class Meta:
        abstract = True
    
class ReceiveOSP(TimeTransfer):
    """docstring for ReceiveOSP."""
    STATE_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid')
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=False,null=False)
    state = models.CharField('Estado de la orden',max_length=13,default='Unpaid' ,choices=STATE_CHOICES, blank=False, null=False)
    amount = models.DecimalField('Monto a pagar',decimal_places=2, max_digits=11, default=0, null=False, blank=False)
    code = models.UUIDField(default=uuid.uuid4, editable=False, null=False, blank=False)
    image = models.ImageField(upload_to='avatar/', storage=gd_storage , null=True, blank=True)
    
    
    class Meta:    
        verbose_name = 'Recibir OSP'
        verbose_name_plural = 'Recibir OSP'
        
    def __str__(self) -> str:
        return f'Recibo generado por el usuario {self.user} con un monto de {self.amount} OSP'
    
    def save(self, *args, **kwargs):
       qr = qrcode.make(f'{self.code}')
       qr_offset = Image.new('RGB', (340, 340), 'white')
       draw_img = ImageDraw.Draw(qr_offset)
       qr_offset.paste(qr)
       file_name = f'{self.id}.png'
       stream = BytesIO()
       qr_offset.save(stream, 'PNG')
       self.image.save(file_name, File(stream), save=False)
       qr_offset.close()
       super().save(*args, **kwargs)

class TransferOSP(TimeStampMixin):
    """docstring for ReceiveOSP."""
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=False,null=False)
    receive = models.OneToOneField(ReceiveOSP,on_delete=models.CASCADE, blank=False,null=False, unique=True)
    
    class Meta:    
        verbose_name = 'Recibir OSP'
        verbose_name_plural = 'Recibir OSP'
        
    def __str__(self) -> str:
        return f'Transferencia realizada por el usuario {self.user} al recibo {self.receive}'
    