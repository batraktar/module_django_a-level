from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app.views import Login, Registration, Logout, ProductListView, ProductDetailView, ProductCreateView, \
    ProdUpdateView, PurchaseCreate, PurchaseView, ReturnCreateView, AdminReturnView, CancelReturn, AdminAcceptReturn

urlpatterns = [
    path('', ProductListView.as_view(), name='base'),
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Registration.as_view(), name='registration'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_item'),
    path('create_product/', ProductCreateView.as_view(), name='create'),
    path('update_product/<slug:slug>/', ProdUpdateView.as_view(), name='update'),
    path('buy/<slug:slug>/', PurchaseCreate.as_view(), name='buy_product'),
    path('purchase/', PurchaseView.as_view(), name='buy_view'),
    path('return/<int:purchase_id>/create', ReturnCreateView.as_view(), name='return'),
    path('su_returns/', AdminReturnView.as_view(), name='admin_return'),
    path('accept_return/<int:pk>', AdminAcceptReturn.as_view(), name='accept_return'),
    path('canc_ret/<int:pk>', CancelReturn.as_view(), name='cancel_return')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
