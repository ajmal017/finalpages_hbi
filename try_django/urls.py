from django.conf.urls import url
from .test_sendemail import sending_mail

from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include # url
from blog.views import (
    blog_post_create_view,
    blog_post_list_myblogs,
)

from .views import (
    index,
    updatedocs,
    dashboard,
    list,
    profile,
    okr,
    forecast,
    proposals,
    po,
    demo,
    testcard,
    blank,
    upload,
)

from .views import LoginView, activate, RegistrationView, RequestResetLinkView, CompletePasswordChangeView, RequestActivationCode

urlpatterns = [

    path('requestactivatecode/', RequestActivationCode.as_view(), name='requestcode'),           #good
    path('', index, name='home'),                                                                #good
    path('signup/', RegistrationView.as_view(), name='signup'),
    path('members/login/', LoginView.as_view(), name='login'),
    path('request-reset/', RequestResetLinkView.as_view(), name='reset-password'),
    path('change-password/<uidb64>/<token>', CompletePasswordChangeView.as_view(), name='change-password'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
    path('dashboard/', dashboard, name='dashboard'),
    path('list/', list, name='list'),
    path('profile/', profile, name='profile'),
    path('proposals/', proposals, name='proposals'), #test upload_book.html
    path('upload/', upload, name='upload'),         #test upload_book2.html
    path('blank/', blank, name ='blank'),

    path('sendingmail/', sending_mail),                           #test sending email
    path('updatedocs/', updatedocs, name ='updatedocs'),
    path('testcard/', testcard),
    path('listings/', include('listings.urls')),       #127.0.0.1:8000/listings
    path('okr/', okr, name='okr'),
    path('forecast/', forecast, name='forecast'),
    path('po/', po, name='po'),
    path('demo/', demo, name='demo'),
    path('blog-new/', blog_post_create_view),
    path('blog/', include('blog.urls')),
    path('api/v1/', include('api.urls')),                                                                     #127.0.0.1:8000/api/v1/
    path('mycontents/', blog_post_list_myblogs),
    path('admin/', admin.site.urls),
    path('members/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






