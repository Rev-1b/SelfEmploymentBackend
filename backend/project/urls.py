from django.contrib import admin
from django.urls import include, path

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/customers/', include('customers.urls')),
    path('api/v1/documents/', include('documents.urls')),
    # path("__debug__/", include("debug_toolbar.urls")),
]
