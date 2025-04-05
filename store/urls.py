from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import AuthorViewSet, GenreViewSet, BookViewSet, ReviewViewSet, CustomerViewSet, CartViewSet, CartItemViewSet

router = DefaultRouter()

router.register('books', BookViewSet, basename='book')
router.register('authors', AuthorViewSet, basename='author')
router.register('genres', GenreViewSet, basename='genre')
router.register('Customers', CustomerViewSet, basename='Customer')
router.register('carts', CartViewSet, basename='cart')

# rating_router = NestedDefaultRouter(router, 'books', lookup='book')
# rating_router.register('rating', RatingViewSet,basename='book-rating')

review_router = NestedDefaultRouter(router, 'books', lookup='book')
review_router.register('review', ReviewViewSet ,basename='book-review')

carts_router = NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + review_router.urls + carts_router.urls