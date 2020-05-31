from django.conf.urls import url
from .test_sendemail import sending_mail

from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include # url

from blog.views import (
    blog_post_create_view,
    blog_post_list_myblogs,
)

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
    edit_customer,
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
    alldocuments,
    selecteddocument,
    listall,
    listselected,
    search,
)


from .views import (
    index,
    dashboard,
    okr,
    forecast,
    po,
    demo,
    blank,
    upload1,
    upload2,
    upload3,
    upload4,
    upload5,
)

urlpatterns = [

    #function is located is at listings.views
    path('upload-brochure/', upload_brochure, name ='upload_brochure'),
    path('upload-certificate/', upload_certificate, name ='upload_certificate'),
    path('upload_eproof/', upload_eproof, name ='upload_eproof'),
    path('upload-manual/', upload_manual, name ='upload_manual'),
    path('upload-proposal/', upload_proposal, name ='upload_proposal'),
    path('upload-powerpoint/', upload_powerpoint, name ='upload_powerpoint'),
    path('upload-quotation/', upload_quotation, name ='upload_quotation'),

    path('mydocuments/', mydocuments, name ='mydocuments'),
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
    path('mycustomers/<int:customer_id>', edit_customer, name='customer'),

    path('listings/', listall, name='listings'),                         #similar to alldocuments, to be remove later
    path('listings/<int:listing_id>', listselected, name='listing'),     #similar to selecteddocument, to be remove later


    path('okr/', okr, name='okr'),
    path('upload1/', upload1, name='upload1'),
    path('upload2/', upload2, name='upload2'),
    path('upload3/', upload3, name='upload3'),
    path('upload4/', upload4, name='upload4'),
    path('5/', upload5, name='upload5'),

## homepage (prior to successful login) ##
    path('', index, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('blank/', blank, name ='blank'),
    path('sendingmail/', sending_mail),                #test sending email
    #path('listings/', include('listings.urls')),       #127.0.0.1:8000/listings (btre)
    path('forecast/', forecast, name='forecast'),
    path('po/', po, name='po'),
    path('demo/', demo, name='demo'),
    path('blog-new/', blog_post_create_view),
    path('blog/', include('blog.urls')),
    path('api/v1/', include('api.urls')),             #127.0.0.1:8000/api/v1/
    path('mycontents/', blog_post_list_myblogs),
    path('admin/', admin.site.urls),
    path('members/', include('django.contrib.auth.urls')),
]

#if at development phase, all static and media file are stored at local PC drive
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #find STATIC_URL as described in settings and use the path  STATIC_ROOT
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






