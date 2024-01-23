from django.core.exceptions import ValidationError
import re
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status

def calculate_date(value):
    bancking_date = value
    date_withdraw = datetime.now().date()
    if bancking_date > date_withdraw:
        return 'La fecha inicial no puede ser mayor a la de retiro'
    else: 
        diferencia = date_withdraw - bancking_date
        return diferencia.days
        
   
