from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'articles'

router = DefaultRouter()
router.register(r'news', views.NewsViewSet)
router.register(r'books', views.BookInfoViewSet)
router.register(r'reviews/categories', views.BookReviewCategoryViewSet)
router.register(r'reviews', views.BookReviewViewSet)
router.register(r'opinions', views.OpinionViewSet)
router.register(r'literature', views.LiteratureViewSet)
router.register(r'qa', views.QAViewSet)
router.register(r'translations', views.TranslationViewSet)
router.register(r'history', views.HistoryViewSet)
router.register(r'papers', views.PaperViewSet)
router.register(r'classics', views.ClassicBookViewSet)
router.register(r'library', views.LibraryViewSet)
router.register(r'scriptures', views.ScriptureViewSet)
router.register(r'scripture-chapters', views.ScriptureChapterViewSet)
router.register(r'contact', views.ContactViewSet)

urlpatterns = [
    path('search/', views.GlobalSearchView.as_view(), name='global-search'),
    path('', include(router.urls)),
]