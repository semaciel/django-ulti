from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'), # localhost:8000/api/
    path('server_info/', views.index, name='server_info'),
    path('api_home/', views.api_home, name='api_home'), # localhost:8000/api/
    path('product_home_raw/', views.product_home_raw, name='product_home_raw'),
    # path('', views.index, name='index'),
    # path('', views.index, name='index'),



    # path('auth/', obtain_auth_token),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # # path('products/', include('products.urls'))
]
