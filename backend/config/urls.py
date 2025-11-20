from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from reactions.views import ReactionViewSet
from comments.views import CommentViewSet

# 注册 Reactions 和 Comments 的路由
router = DefaultRouter()
router.register(r'reactions', ReactionViewSet, basename='reactions') # basename 因为 ViewSet 没 queryset
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # App 路由
    path('api/articles/', include('articles.urls')), # 之前的 articles 路由
    path('api/', include(router.urls)),              # reactions 和 comments 挂载在 /api/ 下
    
    # CKEditor
    # path("ckeditor5/", include('ckeditor5.urls')),
    
    # Auth (预留)
    # path('api/auth/', include('users.urls')),
] 

# 静态文件服务 (开发模式)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)