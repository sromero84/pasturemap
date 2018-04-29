from rest_framework import routers

from api.v1.animals.views import AnimalViewSet, HerdViewSet, WeightEntryViewSet


router = routers.SimpleRouter()
router.register(r'animals', AnimalViewSet)
router.register(r'herds', HerdViewSet)
router.register(r'weight_entries', WeightEntryViewSet)

urlpatterns = router.urls
