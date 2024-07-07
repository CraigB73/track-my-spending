from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='home', permanent=True)),
    path('about/', include('about.urls'), name='about_urls'),
    path("accounts/", include("allauth.urls")),
    path('budget/', include('budget.urls'), name='budget_urls'),
    path('home/', include('home.urls'), name='home_urls'),
    path('transaction/', include('transaction.urls'), name='transaction_urls'),
    path('admin/', admin.site.urls),
 
    
]
