
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from test_task import views 
from django.conf.urls import include
#list all urls 

urlpatterns =[ 
    path('',views.dashboard, name='dashboard'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('Add-Product/',views.addproduct, name='addproduct'),
    path('View-Product/',views.viewproduct, name='viewproduct'),
    path('add_product_api',views.add_product_api, name='add_product_api'),
    path('get_product_api',views.get_product_api, name='get_product_api'),
    path('search_product_api',views.search_product_api, name='search_product_api'),

    path('admin/', admin.site.urls),
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
