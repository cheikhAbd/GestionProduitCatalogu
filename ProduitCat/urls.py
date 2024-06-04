from django.urls import path
from ProduitCat import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # Catagorie 
    path('catagorie/', views.listAllCat, name='list_all'),
    path('catagorie/name/<str:nom>/', views.listByNameCat, name='list_by_name'),
    path('catagorie/create/', views.createCat, name='create_gatagoie'),
    path('catagorie/update/', views.modifierCat, name='update_gatagorie'),
    path('catagorie/delete/', views.deleteCat, name='delete_gatagorie'),
    
    # Product
    path('Product/', views.listAllProd, name='list_all_Prod'),
    path('Product/name/<str:nom>/', views.listByNameProd, name='list_by_name_Prod'),
    path('Product/create/', views.createProd, name='create_product'),
    path('Product/update/', views.modifierProd, name='update_product'),
    path('Product/delete/', views.deleteProd, name='delete_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)