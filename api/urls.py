# api/urls.py
from django.urls import path, include

from blog.views import PostList, PostDetail

urlpatterns = [

    path('<int:pk>/', PostDetail.as_view()),            # 127.0.0.1:8000/api/v1/1 (show details of api-1
    path('', PostList.as_view()),                       #127.0.0.1:8000/api/v1/   (show all the api list)


# development purposes
    path('api-auth/', include('rest_framework.urls')),  #for development purpose only - allow to choose users to login/logout (arrow) using Django Restframework tool (http://127.0.0.1:8000/api/v1/)
                                                        # does not allow 127.0.0.1:8000/api/v1/api-auth
    #path('rest-auth/', include('rest_auth.urls')),      # allows login http://127.0.0.1:8000/api/v1/api-auth/login/
    #path('rest-auth/registration', include('rest_auth.registration.urls')), # allows registration at http://127.0.0.1:8000/api/v1/api-auth/registration/

]
