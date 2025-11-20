from django.shortcuts import render
from django.db.models import F, Q
from django.core.cache import cache
from rest_framework import viewsets, filters, status, permissions,serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

# 引入之前定义的模型和序列化器
from .models import (
    News, BookInfo, BookReview, BookReviewCategory, Opinion, Literature,
    QA, Translation, History, Paper, ClassicBook, Library,
    Scripture, ScriptureChapter, Contact
)
from .serializers import (
    NewsSerializer, BookInfoSerializer, BookReviewSerializer,
    BookReviewCategorySerializer, OpinionSerializer, LiteratureSerializer,
    QASerializer, TranslationSerializer, HistorySerializer,
    PaperSerializer, ClassicBookSerializer, LibrarySerializer,
    ScriptureSerializer, ScriptureChapterSerializer
)

# ==================== 基础配置 ====================

class StandardResultsSetPagination(PageNumberPagination):
    """标准分页配置"""
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class SmartViewCountMixin:
    """
    智能阅读量统计 Mixin
    策略：使用 Cache 记录 'IP + 文章ID'，30分钟内不重复计数
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # 获取客户端 IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            
        # 构建缓存键: view_count:model:id:ip
        model_name = instance._meta.model_name
        cache_key = f'view_count:{model_name}:{instance.id}:{ip}'
        
        # 检查缓存，如果不存在则增加阅读量
        if not cache.get(cache_key):
            # 使用 F 表达式原子更新，避免并发问题
            instance.total_views = F('total_views') + 1
            instance.today_views = F('today_views') + 1
            instance.save(update_fields=['total_views', 'today_views', 'last_view_date'])
            
            # 设置缓存，有效期 30 分钟 (1800秒)
            cache.set(cache_key, 1, 1800)
            
            # 重新刷新实例以获取最新数值
            instance.refresh_from_db()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class BaseArticleViewSet(SmartViewCountMixin, viewsets.ModelViewSet):
    """
    文章视图基类
    集成：权限控制、过滤、搜索、分页、智能阅读量
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # 未登录只读，登录可编辑
    ordering_fields = ['created_at', 'updated_at', 'total_views']
    ordering = ['-updated_at'] # 默认按更新时间倒序

    def get_queryset(self):
        """
        重写查询集：
        - 管理员(Superuser/Staff): 可以看到所有文章
        - 普通用户/游客: 只能看到 is_published=True 的文章
        """
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        
        # 如果模型有 is_published 字段，则过滤
        if hasattr(self.queryset.model, 'is_published'):
            return queryset.filter(is_published=True)
        return queryset

# ==================== 具体视图集 ====================

class NewsViewSet(BaseArticleViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    search_fields = ['title', 'content', 'author']

class BookInfoViewSet(BaseArticleViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
    search_fields = ['title', 'author', 'isbn', 'publisher']

class BookReviewCategoryViewSet(viewsets.ModelViewSet):
    """书评分类 (通常只需读取，管理员编辑)"""
    queryset = BookReviewCategory.objects.all()
    serializer_class = BookReviewCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookReviewViewSet(BaseArticleViewSet):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    search_fields = ['title', 'content']
    filterset_fields = ['category'] # 允许通过 ?category=ID 过滤

class OpinionViewSet(BaseArticleViewSet):
    queryset = Opinion.objects.all()
    serializer_class = OpinionSerializer
    search_fields = ['title', 'content', 'author']

class LiteratureViewSet(BaseArticleViewSet):
    queryset = Literature.objects.all()
    serializer_class = LiteratureSerializer
    search_fields = ['title', 'content']

class QAViewSet(BaseArticleViewSet):
    queryset = QA.objects.all()
    serializer_class = QASerializer
    search_fields = ['title', 'content']
    
    def get_queryset(self):
        # QA 的特殊逻辑：普通用户只能看 is_approved=True
        queryset = QA.objects.all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(is_published=True, is_approved=True)

class TranslationViewSet(BaseArticleViewSet):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    search_fields = ['title', 'content', 'original_title', 'original_author']

class HistoryViewSet(BaseArticleViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    search_fields = ['title', 'content']

class PaperViewSet(BaseArticleViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    search_fields = ['title']

class ClassicBookViewSet(BaseArticleViewSet):
    queryset = ClassicBook.objects.all()
    serializer_class = ClassicBookSerializer
    search_fields = ['title']

class LibraryViewSet(BaseArticleViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    search_fields = ['title', 'author_intro', 'content_intro', 'isbn']

# ==================== 经训视图 ====================

class ScriptureViewSet(BaseArticleViewSet):
    queryset = Scripture.objects.all()
    serializer_class = ScriptureSerializer
    search_fields = ['title']

class ScriptureChapterViewSet(BaseArticleViewSet):
    queryset = ScriptureChapter.objects.all()
    serializer_class = ScriptureChapterSerializer
    search_fields = ['title', 'content']
    filterset_fields = ['scripture'] # 允许 ?scripture=ID 获取某部经训的所有章节

# ==================== 联系我们 ====================

class ContactViewSet(viewsets.GenericViewSet, 
                     viewsets.mixins.CreateModelMixin, 
                     viewsets.mixins.ListModelMixin):
    """
    联系我们
    - 允许任何人创建 (POST)
    - 只有管理员可以查看列表 (GET)
    """
    queryset = Contact.objects.all()
    serializer_class = serializers.ModelSerializer # 简单的内部序列化器即可
    
    # 定义一个简单的内部序列化器，避免循环导入
    class ContactSerializer(serializers.ModelSerializer):
        class Meta:
            model = Contact
            fields = '__all__'
            read_only_fields = ['is_handled', 'created_at']

    serializer_class = ContactSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()] # 允许任何人提交
        return [permissions.IsAdminUser()] # 只有管理员能看列表


# ==================== 全局搜索 (聚合接口) ====================

from rest_framework.views import APIView

class GlobalSearchView(APIView):
    """
    全局搜索接口
    GET /api/articles/search/?q=关键字
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"results": []})

        # 定义需要搜索的模型列表
        # 可以根据需要调整，为了性能不建议一次搜太多，或者使用 Elasticsearch (进阶)
        # 这里使用简单的数据库 LIKE 查询聚合
        
        results = []
        
        # 辅助函数：搜索并追加结果
        def search_model(Model, Serializer, type_name, search_fields=['title']):
            # 构造 Q 对象
            q_obj = Q()
            for field in search_fields:
                q_obj |= Q(**{f"{field}__icontains": query})
            
            # 过滤发布状态
            qs = Model.objects.filter(q_obj)
            if hasattr(Model, 'is_published'):
                qs = qs.filter(is_published=True)
            
            # 取前3条以保证性能
            data = Serializer(qs[:3], many=True, context={'request': request}).data
            for item in data:
                item['type'] = type_name # 标记类型
                results.append(item)

        # 执行搜索 (示例：搜索几个主要模型)
        search_model(News, NewsSerializer, 'news', ['title', 'content'])
        search_model(BookReview, BookReviewSerializer, 'book_review', ['title', 'content'])
        search_model(Paper, PaperSerializer, 'paper', ['title'])
        search_model(Opinion, OpinionSerializer, 'opinion', ['title', 'content'])
        
        # 按时间排序混合结果
        results.sort(key=lambda x: x.get('updated_at', ''), reverse=True)

        return Response({"count": len(results), "results": results})