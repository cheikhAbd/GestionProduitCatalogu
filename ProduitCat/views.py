from bson import Regex
from rest_framework import status
from rest_framework.decorators import api_view , parser_classes
from rest_framework.response import Response
from .models import Product ,Category
from .serializers import ProductSerializer,CategorySerializer
from django.shortcuts import render
from rest_framework.parsers import JSONParser ,MultiPartParser, FormParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage


# ----- Category --------------------

@csrf_exempt
@api_view(['GET'])
def listAllCat(request):
    Categorys = Category.objects.all()
    serializerProd = CategorySerializer(Categorys, many=True)
    return JsonResponse(serializerProd.data,safe=False)

@csrf_exempt
@api_view(['GET'])
def listByNameCat(request, nom):
    nom = nom.replace('"', '')
    # Log the value of 'nom' to check if it's being passed correctly
    print(f"Received search term: {nom}")
    
    category = Category.objects.filter(name__icontains=nom)
    # Log the query results to see what is being returned from the database
    print(f"Query results: {category}")

    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def createCat(request):
    Cat_data = JSONParser().parse(request)
    serializerCat = CategorySerializer(data=Cat_data)
    if serializerCat.is_valid():
        serializerCat.save()
        return JsonResponse("Added Successfully",safe=False)
    return JsonResponse("Failed To Add",safe=False)

@csrf_exempt
@api_view(['PUT'])
def modifierCat(request):
    try:
        cat_data = JSONParser().parse(request)
        cat_id = cat_data.get('CatId')  # Utilisez get() pour éviter KeyError
        if cat_id is None:
            return JsonResponse('CatId field is missing in the request data', status=status.HTTP_400_BAD_REQUEST)

        category_instance = Category.objects.get(pk=cat_id)
    except Category.DoesNotExist:
        return JsonResponse('Category not found!', status=status.HTTP_404_NOT_FOUND)
    
    serializer = CategorySerializer(category_instance, data=cat_data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['DELETE'])
def deleteCat(request):
    try:
        cat_data = JSONParser().parse(request)
        category_instance = Category.objects.get(pk=cat_data['CatId'])
    except Category.DoesNotExist:
        return JsonResponse('Category not found!', status=status.HTTP_404_NOT_FOUND)
    
    category_instance.delete()
    return JsonResponse("Deleted Successfully!", safe=False)


# ---- Product --------------------

@csrf_exempt
@api_view(['GET'])
def listAllProd(request):
    Products = Product.objects.all()
    serializerProd = ProductSerializer(Products, many=True)
    return JsonResponse(serializerProd.data,safe=False)


@csrf_exempt
@api_view(['GET'])
def listByNameProd(request, nom):
    nom = nom.replace('"', '')
    prod = Product.objects.filter(name__icontains=nom)
    serializer = ProductSerializer(prod, many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def createProd(request):
    print("Requête reçue :", request)
    print("Fichiers reçus :", request.FILES)  # Debug
    print("Données reçues :", request.data)  # Debug

    Pro_data = request.data.copy()  # Faites une copie des données pour les modifier si nécessaire
    file = request.FILES.get('imageProd')

    if file:
        print("Fichier détecté :", file)
        Pro_data['imageProd'] = file

    serializerProd = ProductSerializer(data=Pro_data)
    if serializerProd.is_valid():
        print("Données valides")
        product_instance = serializerProd.save()
        if file:
            # Enregistrez le fichier en utilisant le stockage par défaut
            file_name = default_storage.save(file.name, file)
            product_instance.imageProd = file_name  # Sauvegardez le chemin du fichier dans l'instance du produit
            product_instance.save()  # Sauvegardez les modifications de l'instance
        return JsonResponse({"message": "Added Successfully"}, safe=False)
    else:
        print("Erreurs du sérialiseur :", serializerProd.errors)  # Debug
        return JsonResponse(serializerProd.errors, safe=False)

@csrf_exempt
@api_view(['PUT'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def modifierProd(request):
    
    try:
        Pro_data = request.data.copy()
        prod_id = Pro_data.get('ProdId')  # Utilisez get() pour éviter KeyError
        if prod_id is None:
            return JsonResponse('ProdId field is missing in the request data', status=status.HTTP_400_BAD_REQUEST)

        Product_instance = Product.objects.get(pk=prod_id)
    except Product.DoesNotExist:
        return JsonResponse('Product not found!', status=status.HTTP_404_NOT_FOUND)
    
    file = request.FILES.get('imageProd')

    if file:
        print("Fichier détecté :", file)
        Pro_data['imageProd'] = file
    
    serializer = ProductSerializer(Product_instance, data=Pro_data)
    if serializer.is_valid():
        print("Données valides")
        product_instance = serializer.save()
        if file:
            # Enregistrez le fichier en utilisant le stockage par défaut
            file_name = default_storage.save(file.name, file)
            product_instance.imageProd = file_name  # Sauvegardez le chemin du fichier dans l'instance du produit
            product_instance.save()  # Sauvegardez les modifications de l'instance
        return JsonResponse({"message": "Update Successfully"}, safe=False)
    else:
        print("Erreurs du sérialiseur :", serializer.errors)  # Debug
        return JsonResponse(serializer.errors, safe=False)


@csrf_exempt
@api_view(['DELETE'])
def deleteProd(request):
    try:
        Pro_data = JSONParser().parse(request)
        Product_instance = Product.objects.get(pk=Pro_data['CatId'])
    except Product.DoesNotExist:
        return JsonResponse('Product not found!', status=status.HTTP_404_NOT_FOUND)
    
    Product_instance.delete()
    return JsonResponse("Deleted Successfully!", safe=False)