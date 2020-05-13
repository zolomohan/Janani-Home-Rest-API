from rest_framework import routers
from .api import PostViewSet

# The Default Router includes a default API root view, that returns a response containing hyperlinks to all the list views. 
# It also generates routes for optional .json style format suffixes.

router = routers.DefaultRouter()
router.register('api/posts', PostViewSet, 'posts')

urlpatterns = router.urls