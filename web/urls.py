from django.urls import path
from . import views

urlpatterns = [
    # ex: /dbeer/beers/
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('blog/blogpost/<name>', views.blogpost, name='blogpost')
    # ex: /dbbeer/beers/beer/26908705-cb50-4a94-b046-d838de429500/
    # path('beer/<uuid:beerId>/', views.beerDetail, name='beer-detail')
]
