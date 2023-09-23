from django.contrib import admin
from django.urls import path, include
from scraping.views import (
    home_view, list_view, v_detail, VDetail, VList, VCreate, VUpdate, VDelete
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/', list_view, name='list'),
    # path('list/', VList.as_view(), name='list'),
    path('accounts/', include(('accounts.urls', 'accounts'))),
    path('detail/<int:pk>/', VDetail.as_view(), name='detail'),
    path('create/', VCreate.as_view(), name='create'),
    path('update/<int:pk>/', VUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', VDelete.as_view(), name='delete'),
    path('', home_view, name='home'),
]