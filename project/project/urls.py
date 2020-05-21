from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from project.views import LanguageViewset

urlpatterns = [
    url(r'^translator/supported_languages', LanguageViewset.as_view({'get': 'get_languages'})),
    url(r'^translator/translate', LanguageViewset.as_view({'get': 'translate'})),
    url(r'^translator/detect_language', LanguageViewset.as_view({'get': 'detect_language'}))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
