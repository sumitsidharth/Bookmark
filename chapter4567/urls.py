# pyrefly: ignore [missing-import]
from django.contrib import admin
# pyrefly: ignore [missing-import]
from django.urls import include, path
# pyrefly: ignore [missing-import]
from django.shortcuts import redirect
# pyrefly: ignore [missing-import]
from django.conf import settings
# pyrefly: ignore [missing-import]
from django.conf.urls.static import static

urlpatterns = [
   
    path('', lambda request: redirect('/account/login/', permanent=False), name='home'),

    # Admin panel
    path('admin/', admin.site.urls),

    # Account app URLs
    path('account/', include('social_app.urls')),

    path('social-auth/',include('social_django.urls', namespace='social')),

    path('images/', include('images.urls', namespace='images')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )