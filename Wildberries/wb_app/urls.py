from django.urls import path, include
from .views import (UserProfileViewSet, CategoryListView,CategoryDetailView,
                    SubCategoryListView, SubCategoryDetailView,
                    ProductListView, ProductDetailView, ProductImageViewSet,
                    ReviewViewSet, RegisterView, CustomLoginView, LogoutView,
                    CartDetailView, CartItemViewSet, ProductCreateView)
from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'product_images', ProductImageViewSet)
router.register(r'reviews', ReviewViewSet)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_list'),
    path('login/', CustomLoginView.as_view(), name='login_list'),
    path('logout/', LogoutView.as_view(), name='logout_list'),

    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('subcategories/', SubCategoryListView.as_view(), name='subcategory_list'),
    path('subcategories/<int:pk>/', SubCategoryDetailView.as_view(), name='subcategory_detail'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('', include(router.urls)),
    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('cart_items/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('cart_items/<int:pk>/', CartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('product_create/', ProductCreateView.as_view(), name='product_create')
]