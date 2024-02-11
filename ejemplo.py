def create_order(product_ids, quantity_per_product):
    products = []
    for product_id in product_ids:
        product = Product.objects.select_for_update().get(id=product_id)
        if product.stock >= quantity_per_product:
            product.stock -= quantity_per_product
            product.save()
            products.append(product)
        else:
            raise IntegrityError("No hay suficiente stock para el producto con ID %s." % product_id)

    with transaction.atomic():
        try:
            order = Order.objects.create(products=products)
            # Aquí irían más operaciones relacionadas con la creación de la orden
        except IntegrityError:
            # Si se produce un error durante la creación de la orden, se revertirán los cambios
            pass
        
        
#Otra variante 

from django.db import transaction, IntegrityError
from rest_framework import status
from rest_framework.response import Response
from .models import Product, Order
from .serializers import OrderSerializer

def create_order(request, product_ids, quantity_per_product):
    products = []
    for product_id in product_ids:
        product = Product.objects.select_for_update().get(id=product_id)
        if product.stock >= quantity_per_product:
            product.stock -= quantity_per_product
            product.save()
            products.append(product)
        else:
            return Response({"detail": f"No hay suficiente stock para el producto con ID {product_id}."},
                            status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        try:
            order = Order.objects.create(products=products)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            # Si se produce un error durante la creación de la orden, se revertirán los cambios
            return Response({"detail": "Hubo un error al procesar su solicitud."},
                            status=status.HTTP_400_BAD_REQUEST)
            
            
#Otro ejemplo mas desarrollado 
from django.db import transaction, IntegrityError
from rest_framework import status
from rest_framework.response import Response
from .models import Producto, Compañia, User, Orden, Item
from .serializers import OrdenSerializer

def create_orden(request, items_data):
    # Suponiendo que items_data es una lista de diccionarios con información de los productos y cantidades
    try:
        with transaction.atomic():
            user = request.user  # Obtén el usuario desde el request
            company_compensation = {}  # Diccionario para llevar la compensación de puntos por compañía

            # Crear la orden pero no guardarla todavía
            orden = Orden(user=user)
            orden.save()

            for item_data in items_data:
                producto = Producto.objects.select_for_update().get(id=item_data['producto_id'])
                cantidad = item_data['cantidad']

                # Verificar stock y actualizar puntos
                if producto.stock >= cantidad:
                    producto.stock -= cantidad
                    producto.save()

                    # Calcular la compensación de puntos para cada compañía
                    company = producto.company
                    company_compensation[company] = company_compensation.get(company,  0) + cantidad * producto.value

                    # Crear el item de la orden
                    item = Item(orden=orden, producto=producto, cantidad=cantidad)
                    item.save()

                    # Restar puntos del usuario
                    user.puntos -= cantidad * producto.value
                    user.save()
                else:
                    raise IntegrityError(f"No hay suficiente stock para el producto con ID {item_data['producto_id']}.")

            # Actualizar puntos de las compañías
            for company, compensation in company_compensation.items():
                company.puntos += compensation
                company.save()

            # Guardar la orden después de todas las demás operaciones
            orden.save()

            serializer = OrdenSerializer(orden)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except IntegrityError as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # En caso de otros tipos de excepciones, también se revertirá la transacción
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
