from django.conf.urls import url
from .test_sendemail import sending_mail

from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include # url

from members.views import (
    RegistrationView,
    LoginView,
    RequestResetLinkView,
    CompletePasswordChangeView,
    RequestActivationCode,
    MySettingsView,
    activate,
    myprofile,
)

from customers.views import (
    mycustomers,
    create_customer,
    edit_customer,
    delete_customer,
)

from listings.views import (
    upload_brochure,
    upload_certificate,
    upload_eproof,
    upload_manual,
    upload_powerpoint,
    upload_proposal,
    upload_quotation,
    mydocuments,
    delete_document,
    edit_document,
    alldocuments,
    selecteddocument,
    listall,
    listselected,
    search,

    mydocumentslist,
    testdocuments,

    mydocumentsOverview,
    mydocumentstaskList,
    mydocumentstaskDetail,
    mydocumentstaskCreate,
    mydocumentstaskUpdate,
    mydocumentstaskDelete

)


from .views import (
    index,
    dashboard,
    gallery,
    forecast,
    blank,
)

from movies.views import (

get_delete_update_movie,
get_post_movies,
ListTodo,
PostList,
PostDetail

)

from api.views import (

apiOverview,
taskList,
taskDetail,
taskCreate,
taskUpdate,
taskDelete

)



from frontend.views import list

urlpatterns = [

    path('testdocuments/', testdocuments),

    path('api/', apiOverview, name="api-overview"),
    path('mydocuments-api/', mydocumentsOverview),

    path('api/frontend/', list, name="list"),
    path('mydocuments/frontend/', mydocumentslist),

	path('api/task-list/', taskList, name="task-list"),
    path('mydocuments/task-list/', mydocumentstaskList),   #json return which is used by javascript

	path('api/task-detail/<str:pk>/', taskDetail, name="task-detail"),
    path('mydocuments/task-detail/<str:pk>/', mydocumentstaskDetail),

	path('api/task-create/', taskCreate, name="task-create"),
    path('mydocuments/task-create/', mydocumentstaskCreate),

	path('api/task-update/<str:pk>/', taskUpdate, name="task-update"),
    path('mydocuments/task-update/<str:pk>/', mydocumentstaskUpdate),

	path('api/task-delete/<str:pk>/', taskDelete, name="task-delete"),
    path('mydocuments/task-delete/<str:pk>/', mydocumentstaskDelete),

    path('movies/', ListTodo.as_view()),
    path('movies/v1/', PostList.as_view()),
    path('movies/v1/<int:pk>/', PostDetail.as_view()),
    ## movies app (using REST and token to CRUD)
    path('movies/rest-auth/', include('rest_auth.urls')),
    path('movies/v1/movies/', get_post_movies.as_view(), name='get_post_movies'),
    re_path('movies/v1/movies/(?P<pk>[0-9]+)$', get_delete_update_movie.as_view(), name='get_delete_update_movie'),
    # Example: http http://127.0.0.1:8000/movies/rest-auth/login/ username="allojovi@gmail.com" password="Romans12:1"
    # Example: http http://127.0.0.1:8000/movies/v1/movies/1 "Authorization: Token 74b19be000107deb0f845c141531e00cf7132ab3"
    # Example: http http://127.0.0.1:8000/movies/v1/movies/ "Authorization: Token 74b19be000107deb0f845c141531e00cf7132ab3"
    # Example: http POST http://127.0.0.1:8000/movies/v1/movies/ "Authorization: Token 74b19be000107deb0f845c141531e00cf7132ab3" title="Ant Man and The Wasp" genre="Action" year=2018
    # Example: http PUT http://127.0.0.1:8000/movies/v1/movies/4 "Authorization: Token 74b19be000107deb0f845c141531e00cf7132ab3" title="Ant Man Only" genre="Thriller-Action" year=2001
    # Example: http DELETE http://127.0.0.1:8000/movies/v1/movies/4 "Authorization: Token 74b19be000107deb0f845c141531e00cf7132ab3"






    #function is located is at listings.views
    path('upload-brochure/', upload_brochure, name ='upload_brochure'),
    path('upload-certificate/', upload_certificate, name ='upload_certificate'),
    path('upload_eproof/', upload_eproof, name ='upload_eproof'),
    path('upload-manual/', upload_manual, name ='upload_manual'),
    path('upload-proposal/', upload_proposal, name ='upload_proposal'),
    path('upload-powerpoint/', upload_powerpoint, name ='upload_powerpoint'),
    path('upload-quotation/', upload_quotation, name ='upload_quotation'),

    path('mydocuments/', mydocuments, name ='mydocuments'),
    path('mydocuments/delete/<int:listing_id>', delete_document, name='delete_document'),
    path('mydocuments/edit/<int:listing_id>', edit_document, name='edit_document'),

    path('alldocuments/', alldocuments, name='alldocuments'),
    path('alldocuments/<int:listing_id>', selecteddocument, name='selecteddocument'),

    path('listings/search', search, name='search'),


    #function is located is at members.views
    path('myprofile/', myprofile, name='myprofile'),
    path('mysettings/', MySettingsView.as_view(), name='mysettings'),
    path('signup/', RegistrationView.as_view(), name='signup'),
    path('members/login/', LoginView.as_view(), name='login'),
    path('request-reset/', RequestResetLinkView.as_view(), name='reset-password'),
    path('change-password/<uidb64>/<token>', CompletePasswordChangeView.as_view(), name='change-password'),
    path('requestactivatecode/', RequestActivationCode.as_view(), name='requestcode'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),

    #function is located is at customers.views
    path('mycustomers/', mycustomers, name ='mycustomers'),
    path('mycustomers/create/', create_customer, name='create_customer'),
    path('mycustomers/edit/<int:customer_id>', edit_customer, name='edit_customer'),
    path('mycustomers/delete/<int:customer_id>', delete_customer, name='delete_customer'),


    path('listings/', listall, name='listings'),                         #similar to alldocuments, to be remove later
    path('listings/<int:listing_id>', listselected, name='listing'),     #similar to selecteddocument, to be remove later

## homepage (prior to successful login) ##
    path('', index, name='home'),
    path('gallery/', gallery, name='gallery'),
    path('dashboard/', dashboard, name='dashboard'),
    path('blank/', blank, name ='blank'),
    path('sendingmail/', sending_mail),                #test sending email
    #path('listings/', include('listings.urls')),       #127.0.0.1:8000/listings (btre)
    path('forecast/', forecast, name='forecast'),
    path('admin/', admin.site.urls),
    path('members/', include('django.contrib.auth.urls')),
]

#if at development phase, all static and media file are stored at local PC drive
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #find STATIC_URL as described in settings and use the path  STATIC_ROOT
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






