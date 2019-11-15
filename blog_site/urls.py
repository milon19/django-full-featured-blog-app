from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as users_view
from django.contrib.auth.views import (
    LoginView, LogoutView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('register/', users_view.register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/',users_view.profile, name='profile'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)